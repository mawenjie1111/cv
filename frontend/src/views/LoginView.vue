<template>
  <main class="auth-page">
    <section class="login-panel" aria-labelledby="login-title">
      <p class="eyebrow">FastAPI + Vue</p>
      <h1 id="login-title">Sign in</h1>
      <form class="login-form" @submit.prevent="submit">
        <label>
          Username
          <input v-model="username" name="username" autocomplete="username" required />
        </label>
        <label>
          Password
          <input v-model="password" name="password" type="password" autocomplete="current-password" required />
        </label>
        <p v-if="auth.state.error" class="error" role="alert">{{ auth.state.error }}</p>
        <button type="submit" :disabled="auth.state.loading">
          {{ auth.state.loading ? 'Signing in...' : 'Sign in' }}
        </button>
      </form>
    </section>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../stores/auth'

const auth = useAuth()
const route = useRoute()
const router = useRouter()
const username = ref('admin')
const password = ref('admin123')

async function submit() {
  await auth.login(username.value, password.value)
  router.push(route.query.redirect || { name: 'dashboard' })
}
</script>
