export const SESSION_KEY = 'fastapi-vue-login-session'

export function createEmptySession() {
  return {
    token: '',
    user: null
  }
}

export function saveSession(storage, session) {
  storage.setItem(SESSION_KEY, JSON.stringify(session))
}

export function loadSession(storage) {
  const raw = storage.getItem(SESSION_KEY)
  if (!raw) {
    return createEmptySession()
  }

  try {
    const session = JSON.parse(raw)
    return {
      token: typeof session.token === 'string' ? session.token : '',
      user: session.user && typeof session.user === 'object' ? session.user : null
    }
  } catch {
    return createEmptySession()
  }
}

export function clearSession(storage) {
  storage.removeItem(SESSION_KEY)
}
