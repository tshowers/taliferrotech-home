/**
 * Investor access codes, shared by the function (index.js) and the admin CLI (admin.js).
 *
 * A code is 12 characters from an alphabet with no look-alikes (no 0/O, 1/I/L),
 * shown as XXXX-XXXX-XXXX. The first four characters are stored in the clear as
 * codeId so sign-in can find the record; the whole code is checked against a
 * salted scrypt hash. Codes are never stored in the clear.
 */
const crypto = require('crypto')

const ALPHABET = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'
const LENGTH = 12

function normalize(code) {
  return String(code || '').toUpperCase().replace(/[^A-Z0-9]/g, '')
}

function newCode() {
  let out = ''
  while (out.length < LENGTH) {
    const b = crypto.randomBytes(1)[0]
    if (b < 248) out += ALPHABET[b % ALPHABET.length] // 248 = 8 x 31: no modulo bias
  }
  return out
}

function format(code) {
  return normalize(code).match(/.{1,4}/g).join('-')
}

function codeId(code) {
  return normalize(code).slice(0, 4)
}

function hashCode(code, salt) {
  return crypto.scryptSync(normalize(code), salt, 32).toString('hex')
}

function makeCredential(code) {
  const salt = crypto.randomBytes(16).toString('hex')
  return { codeId: codeId(code), codeSalt: salt, codeHash: hashCode(code, salt) }
}

function checkCode(code, salt, hash) {
  const a = Buffer.from(hashCode(code, salt), 'hex')
  const b = Buffer.from(String(hash || ''), 'hex')
  return a.length === b.length && crypto.timingSafeEqual(a, b)
}

module.exports = { LENGTH, normalize, newCode, format, codeId, makeCredential, checkCode }
