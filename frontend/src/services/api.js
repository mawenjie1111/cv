import { loadSession } from '../auth/session.js'

export const API_BASE_URL = import.meta.env?.VITE_API_BASE_URL || 'http://localhost:8000/api'

const ERROR_MESSAGES = {
  account_not_found: '账号不存在',
  invalid_password: '密码错误',
  account_disabled: '账号已禁用',
  registration_not_implemented: '注册功能暂未开放'
}

export function createApiError(body) {
  const nestedDetail = typeof body?.detail === 'object' && body?.detail !== null ? body.detail : null
  const errorCode = body?.error_code || nestedDetail?.error_code || ''
  const detail =
    typeof body?.detail === 'string'
      ? body.detail
      : typeof nestedDetail?.message === 'string'
        ? nestedDetail.message
        : 'Request failed'

  const error = new Error(ERROR_MESSAGES[errorCode] || detail)
  error.code = errorCode
  error.detail = detail
  return error
}

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
    throw createApiError(body)
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
