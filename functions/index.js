/**
 * investorRoom: the password gate behind taliferro.tech/investor-room.
 *
 * The videos sit in a private bucket (gs://taliferro-investor-room). A correct
 * password gets short-lived signed links; nothing in Hosting points at the files.
 * Hosting rewrites POST /api/investor-room here, so the page calls it same-origin.
 *
 * Change the password: firebase functions:secrets:set INVESTOR_ROOM_PASSWORD
 * then redeploy: firebase deploy --only functions:investor-room
 */
const crypto = require('crypto')
const { onRequest } = require('firebase-functions/v2/https')
const { defineSecret } = require('firebase-functions/params')
const { initializeApp } = require('firebase-admin/app')
const { getStorage } = require('firebase-admin/storage')

initializeApp()

const PASSWORD = defineSecret('INVESTOR_ROOM_PASSWORD')
const BUCKET = 'taliferro-investor-room'
const LINK_TTL_MS = 2 * 60 * 60 * 1000

// Shown in this order. file is the object name in the bucket.
const VIDEOS = [
  { id: 'angel', title: 'For angel investors', file: 'todd-docs-angel.mp4' },
  { id: 'investor', title: 'For seed investors', file: 'todd-docs-investor.mp4' },
]

// Per-instance brake on guessing: 8 misses per IP per 15 minutes.
const MAX_MISSES = 8
const WINDOW_MS = 15 * 60 * 1000
const misses = new Map()

function blocked(ip) {
  const m = misses.get(ip)
  if (!m || Date.now() - m.first > WINDOW_MS) return false
  return m.count >= MAX_MISSES
}

function recordMiss(ip) {
  const m = misses.get(ip)
  if (!m || Date.now() - m.first > WINDOW_MS) misses.set(ip, { first: Date.now(), count: 1 })
  else m.count++
}

function matches(given, expected) {
  const a = crypto.createHash('sha256').update(String(given)).digest()
  const b = crypto.createHash('sha256').update(String(expected)).digest()
  return crypto.timingSafeEqual(a, b)
}

exports.investorRoom = onRequest(
  { region: 'us-central1', secrets: [PASSWORD], maxInstances: 2, memory: '256MiB' },
  async (req, res) => {
    res.set('Cache-Control', 'no-store')
    if (req.method !== 'POST') return res.status(405).json({ error: 'method' })

    const ip = (req.get('x-forwarded-for') || req.ip || '').split(',')[0].trim()
    if (blocked(ip)) return res.status(429).json({ error: 'wait' })

    const password = req.body && req.body.password
    if (typeof password !== 'string' || !password || !matches(password.trim(), PASSWORD.value().trim())) {
      recordMiss(ip)
      return res.status(401).json({ error: 'password' })
    }
    misses.delete(ip)

    const bucket = getStorage().bucket(BUCKET)
    const expires = Date.now() + LINK_TTL_MS
    const videos = await Promise.all(VIDEOS.map(async v => {
      const [url] = await bucket.file(v.file).getSignedUrl({ version: 'v4', action: 'read', expires })
      return { id: v.id, title: v.title, url }
    }))
    res.json({ videos, expires })
  }
)
