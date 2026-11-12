/**
 * investorRoom: everything behind taliferro.tech/investor-room.
 *
 * The public page (public/investor-room.html) holds only the sign-in form. All
 * room content comes from here, and only after a valid session:
 *
 *   POST /api/investor-room/signin    {code, agree}  -> sets the __session cookie (7 days)
 *   POST /api/investor-room/signout
 *   GET  /api/investor-room/room                     -> the room as JSON (content/investor-room.json + this investor)
 *   GET  /api/investor-room/doc?id=                  -> a document: PDFs stamped with the investor's name
 *   POST /api/investor-room/event     {type, ref, value}
 *   POST /api/investor-room/question  {body}         -> saved, emailed to the contact owner
 *   POST /api/investor-room/interest  {amount}       -> saved, emailed to the contact owner
 *
 * Data lives in the separate Firestore database "investor-room" (the project's
 * default database belongs to the Blair Capital site). Files live in the private
 * bucket gs://taliferro-investor-room. Firebase Hosting only forwards a cookie
 * named __session, hence the name.
 *
 * Investors, codes, questions and the view log are managed with admin.js.
 * Deploy: firebase deploy --only functions:investor-room --project taliferro-de66f
 */
const crypto = require('crypto')
const fs = require('fs')
const path = require('path')
const { onRequest } = require('firebase-functions/v2/https')
const { defineSecret } = require('firebase-functions/params')
const { initializeApp } = require('firebase-admin/app')
const { getStorage } = require('firebase-admin/storage')
const { getFirestore, Timestamp } = require('firebase-admin/firestore')
const { PDFDocument, StandardFonts, rgb } = require('pdf-lib')
const codes = require('./lib/codes')

initializeApp()
const db = getFirestore('investor-room')
const SENDGRID_API_KEY = defineSecret('SENDGRID_API_KEY')
const CONTENT = JSON.parse(fs.readFileSync(path.join(__dirname, 'content', 'investor-room.json'), 'utf8'))

const BUCKET = 'taliferro-investor-room'
const COOKIE = '__session'
const SESSION_MS = 7 * 24 * 60 * 60 * 1000
const VIDEO_LINK_MS = 2 * 60 * 60 * 1000
const FILE_LINK_MS = 5 * 60 * 1000
const MAX_TRIES = 5
const TRY_WINDOW_MS = 15 * 60 * 1000
const EVENT_TYPES = new Set(['section', 'video_play', 'video_progress', 'slide'])

const sha = s => crypto.createHash('sha256').update(String(s)).digest('hex')
const now = () => Timestamp.now()

/* ---------------------------------------------------------------- helpers */

function clientIp(req) {
  return (req.get('x-forwarded-for') || req.ip || '').split(',')[0].trim()
}

function readCookie(req, name) {
  const raw = req.get('cookie') || ''
  for (const part of raw.split(';')) {
    const i = part.indexOf('=')
    if (i > -1 && part.slice(0, i).trim() === name) return decodeURIComponent(part.slice(i + 1).trim())
  }
  return ''
}

function setSessionCookie(res, token, maxAgeSec) {
  res.set('Set-Cookie', `${COOKIE}=${token}; Max-Age=${maxAgeSec}; Path=/; HttpOnly; Secure; SameSite=Lax`)
}

function contactFor(inv) {
  return CONTENT.contacts[inv.contactOwnerId] || CONTENT.contacts[CONTENT.defaultContact]
}

function firstName(name) {
  return String(name || '').trim().split(/\s+/)[0] || 'there'
}

function initials(name) {
  return String(name || '').trim().split(/\s+/).map(w => w[0]).slice(0, 2).join('').toUpperCase()
}

function visibleDocs(inv) {
  const hidden = new Set(inv.hiddenDocs || [])
  return CONTENT.documents.filter(d => !hidden.has(d.id) && (!d.onlyFor || d.onlyFor.includes(inv.id)))
}

async function logEvent(investorId, type, ref, value) {
  const e = { investorId, type, ref: ref == null ? null : String(ref).slice(0, 200), at: now() }
  if (value != null) e.value = typeof value === 'number' ? value : String(value).slice(0, 200)
  await db.collection('events').add(e)
}

async function sendMail(to, subject, text) {
  try {
    const r = await fetch('https://api.sendgrid.com/v3/mail/send', {
      method: 'POST',
      headers: { Authorization: `Bearer ${SENDGRID_API_KEY.value()}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        personalizations: [{ to: [{ email: to }] }],
        from: { email: CONTENT.mailFrom, name: 'Taliferro Tech investor room' },
        subject,
        content: [{ type: 'text/plain', value: text }],
      }),
    })
    if (!r.ok) console.error('sendgrid', r.status, await r.text())
  } catch (err) {
    console.error('sendgrid', err)
  }
}

/* ---------------------------------------------------------------- throttle */

async function throttled(keys) {
  const snaps = await db.getAll(...keys.map(k => db.collection('throttle').doc(k)))
  return snaps.some(s => s.exists && Date.now() - s.get('first') < TRY_WINDOW_MS && s.get('count') >= MAX_TRIES)
}

async function recordMiss(keys) {
  await Promise.all(keys.map(k => db.runTransaction(async t => {
    const ref = db.collection('throttle').doc(k)
    const s = await t.get(ref)
    if (!s.exists || Date.now() - s.get('first') > TRY_WINDOW_MS) t.set(ref, { first: Date.now(), count: 1 })
    else t.update(ref, { count: s.get('count') + 1 })
  })))
}

async function clearMisses(keys) {
  await Promise.all(keys.map(k => db.collection('throttle').doc(k).delete()))
}

/* ---------------------------------------------------------------- session */

function isExpired(inv) {
  return inv.status === 'expired' || (inv.expiresAt && inv.expiresAt.toMillis() < Date.now())
}

async function currentInvestor(req) {
  const token = readCookie(req, COOKIE)
  if (!token) return null
  const s = await db.collection('sessions').doc(sha(token)).get()
  if (!s.exists || s.get('expiresAt').toMillis() < Date.now()) return null
  const inv = await db.collection('investors').doc(s.get('investorId')).get()
  if (!inv.exists) return null
  const data = { id: inv.id, ...inv.data() }
  if (data.status !== 'active' || isExpired(data)) return null
  return data
}

/* ---------------------------------------------------------------- routes */

async function signin(req, res) {
  const { code, agree } = req.body || {}
  if (agree !== true) return res.status(400).json({ error: 'agree' })
  const ip = clientIp(req)
  const c = codes.normalize(code)
  const keys = ['ip_' + sha(ip).slice(0, 40), 'code_' + codes.codeId(c)]
  if (await throttled(keys)) return res.status(429).json({ error: 'wait' })

  let match = null
  if (c.length === codes.LENGTH) {
    const snap = await db.collection('investors').where('codeId', '==', codes.codeId(c)).limit(10).get()
    match = snap.docs.find(d => codes.checkCode(c, d.get('codeSalt'), d.get('codeHash'))) || null
  }
  if (!match || match.get('status') === 'revoked') {
    await recordMiss(keys)
    return res.status(401).json({ error: 'code' })
  }

  const inv = { id: match.id, ...match.data() }
  const contact = contactFor(inv)
  if (isExpired(inv)) {
    const last = inv.expiredNoticeAt ? inv.expiredNoticeAt.toMillis() : 0
    if (Date.now() - last > 24 * 60 * 60 * 1000) {
      await match.ref.update({ expiredNoticeAt: now() })
      await sendMail(contact.email, `Investor room: ${inv.name}'s code has expired`,
        `${inv.name} (${inv.email}${inv.firm ? ', ' + inv.firm : ''}) tried to open the investor room with an expired code.\n\n` +
        `Extend it with: node admin.js extend ${inv.email} --days 30`)
    }
    return res.status(410).json({ error: 'expired', contact: contact.name })
  }

  await clearMisses(keys)
  const token = crypto.randomBytes(32).toString('base64url')
  await db.collection('sessions').doc(sha(token)).set({
    investorId: inv.id, ip, createdAt: now(), expiresAt: Timestamp.fromMillis(Date.now() + SESSION_MS),
  })
  await match.ref.update({ ndaAcceptedAt: now(), ndaIp: ip, ndaVersion: CONTENT.ndaVersion, lastSignInAt: now() })
  await logEvent(inv.id, 'signin', null)
  setSessionCookie(res, token, SESSION_MS / 1000)
  res.json({ ok: true })
}

async function signout(req, res) {
  const token = readCookie(req, COOKIE)
  if (token) await db.collection('sessions').doc(sha(token)).delete()
  setSessionCookie(res, '', 0)
  res.json({ ok: true })
}

async function questionsFor(inv) {
  const snap = await db.collection('questions').where('investorId', '==', inv.id).get()
  return snap.docs
    .map(d => ({ id: d.id, body: d.get('body'), at: d.get('createdAt').toMillis(), answer: d.get('answer') || null }))
    .sort((a, b) => b.at - a.at)
}

async function room(req, res, inv) {
  const contact = contactFor(inv)
  const bucket = getStorage().bucket(BUCKET)
  const expires = Date.now() + VIDEO_LINK_MS
  // A video that can't be signed is left out rather than failing the whole room.
  const videos = (await Promise.all(CONTENT.videos.map(async v => {
    try {
      const [url] = await bucket.file(v.file).getSignedUrl({ version: 'v4', action: 'read', expires })
      return { id: v.id, title: v.title, length: v.length, presenter: v.presenter, url }
    } catch (err) {
      console.error('sign video', v.file, err.message)
      return null
    }
  }))).filter(Boolean)
  let deck = null
  if (CONTENT.deck && CONTENT.deck.slides && CONTENT.deck.slides.length) {
    try {
      const slides = await Promise.all(CONTENT.deck.slides.map(async s => {
        const [url] = await bucket.file(s.img).getSignedUrl({ version: 'v4', action: 'read', expires })
        return { title: s.title, url }
      }))
      deck = { pdf: CONTENT.deck.pdf, slides }
    } catch (err) {
      console.error('sign deck', err.message)
    }
  }
  const interest = await db.collection('interest').doc(inv.id).get()
  res.json({
    investor: { name: inv.name, firstName: firstName(inv.name) },
    contact: { name: contact.name, title: contact.title, initials: initials(contact.name), bookingUrl: contact.bookingUrl || '', email: contact.email },
    updatedAt: CONTENT.updatedAt,
    terms: CONTENT.terms,
    videos,
    videoPoster: CONTENT.videoPoster,
    deck,
    numbers: CONTENT.numbers,
    portfolio: CONTENT.portfolio,
    acquisition: CONTENT.acquisition,
    risks: CONTENT.risks,
    documents: visibleDocs(inv).map(({ id, title, detail, action, icon, video }) => ({ id, title, detail, action, icon, video })),
    questions: await questionsFor(inv),
    interest: interest.exists ? interest.get('amount') : null,
  })
}

async function stampPdf(buf, inv) {
  const pdf = await PDFDocument.load(buf)
  const font = await pdf.embedFont(StandardFonts.Helvetica)
  const date = new Date().toISOString().slice(0, 10)
  const text = `Confidential · ${inv.name} · ${inv.email} · ${date}`.replace(/[^\x20-\x7E·]/g, '')
  for (const page of pdf.getPages()) {
    const { width } = page.getSize()
    const size = 7
    const w = font.widthOfTextAtSize(text, size)
    page.drawText(text, { x: (width - w) / 2, y: 14, size, font, color: rgb(0.45, 0.47, 0.52) })
  }
  pdf.setTitle(`${pdf.getTitle() || 'Taliferro Tech'} (confidential, ${inv.name})`)
  return Buffer.from(await pdf.save())
}

async function doc(req, res, inv) {
  const d = visibleDocs(inv).find(x => x.id === req.query.id)
  if (!d || !d.file) return res.status(404).json({ error: 'doc' })
  const file = getStorage().bucket(BUCKET).file(d.file)
  await logEvent(inv.id, 'download', d.id)
  if (d.stamp) {
    const [buf] = await file.download()
    const out = await stampPdf(buf, inv)
    res.set('Content-Type', 'application/pdf')
    res.set('Content-Disposition', `attachment; filename="${path.basename(d.file)}"`)
    return res.send(out)
  }
  const [url] = await file.getSignedUrl({ version: 'v4', action: 'read', expires: Date.now() + FILE_LINK_MS })
  res.redirect(302, url)
}

async function event(req, res, inv) {
  const { type, ref, value } = req.body || {}
  if (!EVENT_TYPES.has(type)) return res.status(400).json({ error: 'type' })
  await logEvent(inv.id, type, ref, typeof value === 'number' ? value : null)
  res.json({ ok: true })
}

async function question(req, res, inv) {
  const body = String((req.body && req.body.body) || '').trim()
  if (!body || body.length > 4000) return res.status(400).json({ error: 'body' })
  const contact = contactFor(inv)
  await db.collection('questions').add({ investorId: inv.id, name: inv.name, email: inv.email, body, createdAt: now() })
  await logEvent(inv.id, 'question', null)
  await sendMail(contact.email, `Investor room question from ${inv.name}`,
    `${inv.name} (${inv.email}${inv.firm ? ', ' + inv.firm : ''}) asked:\n\n${body}\n\n` +
    `Answer it so it shows in their room: node admin.js questions, then node admin.js answer <id> "..."`)
  res.json({ questions: await questionsFor(inv) })
}

async function interest(req, res, inv) {
  const amount = Math.round(Number(req.body && req.body.amount))
  if (!Number.isFinite(amount) || amount <= 0 || amount > 100000000) return res.status(400).json({ error: 'amount' })
  const ref = db.collection('interest').doc(inv.id)
  const prev = await ref.get()
  await ref.set({ investorId: inv.id, name: inv.name, email: inv.email, amount, updatedAt: now(),
    createdAt: prev.exists ? prev.get('createdAt') : now() })
  await logEvent(inv.id, 'interest', null, amount)
  const contact = contactFor(inv)
  await sendMail(contact.email, `Investor room: ${inv.name} indicated $${amount.toLocaleString('en-US')}`,
    `${inv.name} (${inv.email}${inv.firm ? ', ' + inv.firm : ''}) indicated interest of $${amount.toLocaleString('en-US')}` +
    (prev.exists ? ` (was $${prev.get('amount').toLocaleString('en-US')}).` : '.') + '\n\nIt is not a commitment.')
  res.json({ amount, contact: contact.name })
}

const PUBLIC_ROUTES = { 'POST signin': signin, 'POST signout': signout }
const ROOM_ROUTES = {
  'GET room': room, 'GET doc': doc, 'POST event': event, 'POST question': question, 'POST interest': interest,
}

exports.investorRoom = onRequest(
  { region: 'us-central1', secrets: [SENDGRID_API_KEY], maxInstances: 4, memory: '512MiB' },
  async (req, res) => {
    res.set('Cache-Control', 'private, no-store')
    res.set('X-Robots-Tag', 'noindex, nofollow')
    const action = req.path.replace(/^\/api\/investor-room\/?/, '').replace(/\/$/, '')
    const key = `${req.method} ${action}`
    // JSON-only POSTs: a cross-site form can't send application/json without a preflight.
    if (req.method === 'POST' && !req.is('application/json')) return res.status(415).json({ error: 'json' })
    try {
      if (PUBLIC_ROUTES[key]) return await PUBLIC_ROUTES[key](req, res)
      if (!ROOM_ROUTES[key]) return res.status(404).json({ error: 'route' })
      const inv = await currentInvestor(req)
      if (!inv) return res.status(401).json({ error: 'session' })
      return await ROOM_ROUTES[key](req, res, inv)
    } catch (err) {
      console.error(key, err)
      res.status(500).json({ error: 'server' })
    }
  }
)
