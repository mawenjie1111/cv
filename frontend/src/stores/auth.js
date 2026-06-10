import { computed, reactive } from 'vue'
import { clearSession, loadSession, saveSession } from '../auth/session'
import { fetchCurrentUser, loginRequest } from '../services/api'

const state = reactive({
  token: '',
  user: null,
  initialized: false,
  loading: false,
  error: ''
})

export function useAuth() {
  async function loadSessionState() {
    const session = loadSession(window.localStorage)
    state.token = session.token
    state.user = session.user
    state.initialized = true

    if (state.token && !state.user) {
      try {
        state.user = await fetchCurrentUser()
        saveSession(window.localStorage, { token: state.token, user: state.user })
      } catch {
        logout(false)
      }
    }
  }

  async function login(username, password) {
    state.loading = true
    state.error = ''
    try {
      const result = await loginRequest(username, password)
      state.token = result.access_token
      state.user = result.user
      saveSession(window.localStorage, { token: state.token, user: state.user })
      return result
    } catch (error) {
      state.error = error.message || 'Login failed'
      throw error
    } finally {
      state.loading = false
      state.initialized = true
    }
  }

  function logout() {
    state.token = ''
    state.user = null
    state.error = ''
    state.initialized = true
    clearSession(window.localStorage)
  }

  return {
    state,
    initialized: computed(() => state.initialized),
    isAuthenticated: computed(() => Boolean(state.token)),
    loadSession: loadSessionState,
    login,
    logout
  }
}
