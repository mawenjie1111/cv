import { loadSession } from '../auth/session'

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

async function request(path, options = {}) {
  const headers = new Headers(options.headers || {})
  headers.set('Content-Type', 'application/json')

  const session = loadSession(window.localStorage)
  if (session.token) {
    headers.set('Authorization', `Bearer ${session.token}`)
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers
  })

  const body = await response.json().catch(() => null)
  if (!response.ok) {
    const message = body?.detail || 'Request failed'
    throw new Error(message)
  }
  return body
}

export function loginRequest(username, password) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password })
  })
}

export function fetchCurrentUser() {
  return request('/users/me')
}
