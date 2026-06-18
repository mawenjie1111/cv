import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { clearSession, createEmptySession, loadSession, saveSession, SESSION_KEY } from '../src/auth/session.js'
import { createApiError } from '../src/services/api.js'

function createStorage() {
  const values = new Map()
  return {
    getItem(key) {
      return values.has(key) ? values.get(key) : null
    },
    setItem(key, value) {
      values.set(key, value)
    },
    removeItem(key) {
      values.delete(key)
    }
  }
}

const storage = createStorage()
assert.deepEqual(createEmptySession(), { token: '', user: null })
assert.deepEqual(loadSession(storage), { token: '', user: null })

saveSession(storage, { token: 'abc', user: { username: 'admin' } })
assert.equal(storage.getItem(SESSION_KEY), '{"token":"abc","user":{"username":"admin"}}')
assert.deepEqual(loadSession(storage), { token: 'abc', user: { username: 'admin' } })

clearSession(storage)
assert.deepEqual(loadSession(storage), { token: '', user: null })

const accountNotFoundError = createApiError({
  detail: 'Account not found',
  error_code: 'account_not_found'
})
assert.equal(accountNotFoundError.message, '账号不存在')
assert.equal(accountNotFoundError.code, 'account_not_found')

const routerSource = await readFile(new URL('../src/router/index.js', import.meta.url), 'utf8')
assert.match(routerSource, /requiresAuth:\s*true/)
assert.match(routerSource, /name:\s*'login'/)

console.log('Frontend verification passed')
