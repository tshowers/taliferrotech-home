#!/usr/bin/env node
/**
 * Investor room admin. Runs on your machine with your gcloud login
 * (gcloud auth application-default login) against the "investor-room"
 * Firestore database in taliferro-de66f.
 *
 *   node admin.js add --name "Jordan Lee" --email jordan@fund.com [--firm "Fund"] [--days 60] [--contact tyrone]
 *   node admin.js list
 *   node admin.js newcode <email>             issue a fresh code (the old one stops working)
 *   node admin.js extend <email> --days 30    push the expiry out and reactivate
 *   node admin.js revoke <email>              shut the door now (also ends open sessions)
 *   node admin.js log [<email>] [--limit 50]  sign-ins, sections, video progress, downloads...
 *   node admin.js questions                   open questions first
 *   node admin.js answer <questionId> "..."   shows in that investor's room
 *   node admin.js interest                    amounts investors have indicated
 *
 * The code is printed once, at add/newcode. Only its hash is stored.
 */
const { initializeApp, applicationDefault } = require('firebase-admin/app')
const { getFirestore, Timestamp } = require('firebase-admin/firestore')
const codes = require('./lib/codes')

initializeApp({ credential: applicationDefault(), projectId: 'taliferro-de66f' })
const db = getFirestore('investor-room')
const DAY = 24 * 60 * 60 * 1000

function flags(argv) {
  const out = { _: [] }
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) out[argv[i].slice(2)] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true
    else out._.push(argv[i])
  }
  return out
}

const day = ts => (ts ? ts.toDate().toISOString().slice(0, 10) : '-')
const when = ts => (ts ? ts.toDate().toISOString().replace('T', ' ').slice(0, 16) : '-')

async function findInvestor(key) {
  if (!key) throw new Error('Give an email or investor id.')
  const byId = await db.collection('investors').doc(key).get()
  if (byId.exists) return byId
  const snap = await db.collection('investors').where('email', '==', key.toLowerCase()).limit(1).get()
  if (snap.empty) throw new Error(`No investor ${key}`)
  return snap.docs[0]
}

async function uniqueCode() {
  for (;;) {
    const code = codes.newCode()
    const clash = await db.collection('investors').where('codeId', '==', codes.codeId(code)).limit(1).get()
    if (clash.empty) return code
  }
}

function printCode(name, code, expiresAt) {
  console.log(`\nAccess code for ${name}:  ${codes.format(code)}`)
  console.log(`Expires ${day(expiresAt)}. Send it in the invitation email with the link https://taliferro.tech/investor-room`)
  console.log('This is the only time the code is shown.\n')
}

async function endSessions(investorId) {
  const snap = await db.collection('sessions').where('investorId', '==', investorId).get()
  await Promise.all(snap.docs.map(d => d.ref.delete()))
  return snap.size
}

const commands = {
  async add(f) {
    if (!f.name || !f.email) throw new Error('add needs --name and --email')
    const email = String(f.email).toLowerCase()
    const dup = await db.collection('investors').where('email', '==', email).limit(1).get()
    if (!dup.empty) throw new Error(`${email} already has a record. Use newcode or extend.`)
    const code = await uniqueCode()
    const expiresAt = Timestamp.fromMillis(Date.now() + Number(f.days || 60) * DAY)
    const ref = await db.collection('investors').add({
      name: String(f.name), email, firm: f.firm ? String(f.firm) : null,
      contactOwnerId: f.contact ? String(f.contact) : 'tyrone',
      status: 'active', expiresAt, createdAt: Timestamp.now(), ...codes.makeCredential(code),
    })
    console.log(`Added ${f.name} (${ref.id}).`)
    printCode(f.name, code, expiresAt)
  },

  async list() {
    const snap = await db.collection('investors').orderBy('createdAt', 'desc').get()
    if (snap.empty) return console.log('No investors yet. Add one with: node admin.js add --name ... --email ...')
    for (const d of snap.docs) {
      const v = d.data()
      const expired = v.expiresAt && v.expiresAt.toMillis() < Date.now()
      console.log(`${v.name.padEnd(24)} ${v.email.padEnd(32)} ${(expired && v.status === 'active' ? 'expired' : v.status).padEnd(8)} ` +
        `expires ${day(v.expiresAt)}  last in ${when(v.lastSignInAt)}  ${d.id}`)
    }
  },

  async newcode(f) {
    const d = await findInvestor(f._[0])
    const code = await uniqueCode()
    await d.ref.update({ ...codes.makeCredential(code), status: 'active' })
    printCode(d.get('name'), code, d.get('expiresAt'))
  },

  async extend(f) {
    const d = await findInvestor(f._[0])
    const base = Math.max(Date.now(), d.get('expiresAt') ? d.get('expiresAt').toMillis() : 0)
    const expiresAt = Timestamp.fromMillis(base + Number(f.days || 30) * DAY)
    await d.ref.update({ expiresAt, status: 'active' })
    console.log(`${d.get('name')} now expires ${day(expiresAt)}.`)
  },

  async revoke(f) {
    const d = await findInvestor(f._[0])
    await d.ref.update({ status: 'revoked', revokedAt: Timestamp.now() })
    const n = await endSessions(d.id)
    console.log(`Revoked ${d.get('name')} and ended ${n} open session(s).`)
  },

  async log(f) {
    let q = db.collection('events').orderBy('at', 'desc').limit(Number(f.limit || 50))
    const names = {}
    if (f._[0]) {
      const d = await findInvestor(f._[0])
      q = db.collection('events').where('investorId', '==', d.id)
      names[d.id] = d.get('name')
    }
    const snap = await q.get()
    const rows = snap.docs.map(d => d.data()).sort((a, b) => b.at.toMillis() - a.at.toMillis()).slice(0, Number(f.limit || 50))
    for (const id of new Set(rows.map(r => r.investorId))) {
      if (!names[id]) { const d = await db.collection('investors').doc(id).get(); names[id] = d.exists ? d.get('name') : id }
    }
    if (!rows.length) return console.log('Nothing logged yet.')
    for (const r of rows) {
      console.log(`${when(r.at)}  ${String(names[r.investorId]).padEnd(22)} ${r.type.padEnd(15)} ${r.ref || ''}${r.value != null ? ' ' + r.value : ''}`)
    }
  },

  async questions() {
    const snap = await db.collection('questions').orderBy('createdAt', 'desc').get()
    if (snap.empty) return console.log('No questions yet.')
    const docs = snap.docs.sort((a, b) => Number(!!a.get('answer')) - Number(!!b.get('answer')))
    for (const d of docs) {
      const v = d.data()
      console.log(`\n[${v.answer ? 'answered' : 'OPEN'}] ${d.id}  ${when(v.createdAt)}  ${v.name} <${v.email}>`)
      console.log(`  Q: ${v.body}`)
      if (v.answer) console.log(`  A: ${v.answer}`)
    }
  },

  async answer(f) {
    const [id, ...rest] = f._
    const text = rest.join(' ').trim()
    if (!id || !text) throw new Error('answer needs a question id and the answer text')
    const ref = db.collection('questions').doc(id)
    if (!(await ref.get()).exists) throw new Error(`No question ${id}`)
    await ref.update({ answer: text, answeredAt: Timestamp.now(), answeredBy: f.by || 'Tyrone Showers' })
    console.log('Answer saved. It shows in their room the next time they open it.')
  },

  async interest() {
    const snap = await db.collection('interest').orderBy('amount', 'desc').get()
    if (snap.empty) return console.log('No interest indicated yet.')
    let total = 0
    for (const d of snap.docs) {
      const v = d.data()
      total += v.amount
      console.log(`$${v.amount.toLocaleString('en-US').padStart(12)}  ${v.name.padEnd(24)} ${v.email}  updated ${day(v.updatedAt)}`)
    }
    console.log(`$${total.toLocaleString('en-US').padStart(12)}  total indicated (not commitments)`)
  },
}

const [cmd, ...rest] = process.argv.slice(2)
if (!commands[cmd]) {
  console.log(require('fs').readFileSync(__filename, 'utf8').split('*/')[0])
  process.exit(cmd ? 1 : 0)
}
commands[cmd](flags(rest)).then(() => process.exit(0)).catch(err => { console.error(err.message); process.exit(1) })
