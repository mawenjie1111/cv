<template>
  <main class="auth-page">
    <div class="auth-grid">
      <section class="auth-visual" aria-hidden="true">
        <div class="visual-stage">
          <div class="visual-badge visual-badge--mail">
            <svg viewBox="0 0 24 24" fill="none">
              <rect x="3" y="5" width="18" height="14" rx="3" />
              <path d="M6.5 8.5 12 12.5l5.5-4" />
            </svg>
          </div>
          <div class="visual-badge visual-badge--spark">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M7 7h3M14 7h3M5 12h4M15 12h4M8 17h3M13 17h3" />
            </svg>
          </div>
          <div class="visual-badge visual-badge--resume">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M7 8h10M7 12h10M7 16h6" />
            </svg>
          </div>

          <svg class="visual-art" viewBox="0 0 680 560" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="panelStroke" x1="0%" x2="100%">
                <stop offset="0%" stop-color="#2867ff" />
                <stop offset="100%" stop-color="#7da8ff" />
              </linearGradient>
              <linearGradient id="panelFill" x1="10%" y1="0%" x2="90%" y2="100%">
                <stop offset="0%" stop-color="#ffffff" />
                <stop offset="100%" stop-color="#e7efff" />
              </linearGradient>
              <linearGradient id="shirtFill" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#2f6cff" />
                <stop offset="100%" stop-color="#234ed8" />
              </linearGradient>
            </defs>
            <path d="M158 453 320 360l171 99-163 88a41 41 0 0 1-39 0Z" fill="url(#panelFill)" opacity=".88" />
            <path d="M160 452 323 357l170 97-163 90a42 42 0 0 1-39 0l-131-74" fill="none" stroke="url(#panelStroke)" stroke-width="2.4" stroke-linejoin="round" />
            <path d="M188 261 350 168l148 84-161 93-149-84Z" fill="#fff" opacity=".72" />
            <path d="M188 261 350 168l148 84-161 93-149-84Z" fill="none" stroke="url(#panelStroke)" stroke-width="2.4" stroke-linejoin="round" />
            <path d="M216 228v159M365 146v159M515 231v159" fill="none" stroke="#c7dafd" stroke-dasharray="8 8" stroke-width="1.8" />
            <path d="M212 469V299c0-11 6-21 16-26l124-71c10-6 23-6 33 0l57 33" fill="white" opacity=".9" />
            <path d="M212 469V299c0-11 6-21 16-26l124-71c10-6 23-6 33 0l57 33" fill="none" stroke="#2867ff" stroke-width="2.6" stroke-linejoin="round" />
            <rect x="235" y="315" width="34" height="48" rx="6" fill="#dfe9ff" />
            <path d="M292 320h81M292 349h74M292 379h98M235 410h156M235 438h139M235 466h126" fill="none" stroke="#80a9ff" stroke-linecap="round" stroke-width="5.4" />
            <ellipse cx="442" cy="458" rx="40" ry="18" fill="#edf3ff" />
            <path d="M442 394c13 0 23 10 23 23 0 18-23 37-23 37s-23-19-23-37c0-13 10-23 23-23Z" fill="#2a64ff" />
            <circle cx="442" cy="418" r="8" fill="#ffffff" />
            <path d="M405 460c16 13 58 13 74 0M392 477c22 19 90 19 112 0" fill="none" stroke="#2867ff" stroke-linecap="round" stroke-width="3" />
            <circle cx="325" cy="160" r="30" fill="#ffd0b3" />
            <path d="M303 149c-6-24 38-42 58-20 20-9 31 22 7 25-1 19-19 13-23 7-9 5-23 2-28-12-5 3-10 3-14 0Z" fill="#1f2e69" />
            <path d="M293 212c6-16 19-25 39-25 19 0 33 9 40 27l16 63h-97l2-65Z" fill="url(#shirtFill)" />
            <path d="M298 274c12 17 52 20 78 6" fill="none" stroke="#1d48cc" stroke-linecap="round" stroke-width="3" />
            <path d="m362 230 42 0-13 92-48-1 19-91Z" fill="#ffffff" stroke="#6e95ff" stroke-linejoin="round" stroke-width="2.4" />
            <path d="M372 232h16l-3 7h-15Z" fill="#2c67ff" />
            <path d="M285 279c-3 31-6 67-15 111-7 33-15 76-21 119h31c18-70 35-148 46-231M359 280c3 37 8 89 13 135 4 35 10 67 16 95h31c-6-40-10-84-12-123-2-44-5-80-10-108" fill="#1e2d63" />
            <path d="M270 512h47M387 512h43" fill="none" stroke="#1b2758" stroke-linecap="round" stroke-width="4.8" />
            <path d="M298 221c-15 11-23 25-27 53M387 225c12 14 18 29 21 47" fill="none" stroke="#2d61e5" stroke-linecap="round" stroke-width="6" />
          </svg>
        </div>
      </section>

      <section class="auth-card" aria-labelledby="login-title">
        <h1 id="login-title">&#31616;&#21382;&#24110;</h1>
        <form class="login-form" @submit.prevent="submit">
          <label class="field">
            <span class="sr-only">&#25163;&#26426;&#21495;&#25110;&#37038;&#31665;</span>
            <span class="field-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="8" r="4" />
                <path d="M4 20c1.8-4 5-6 8-6s6.2 2 8 6" />
              </svg>
            </span>
            <input
              v-model="username"
              name="username"
              autocomplete="username"
              placeholder="&#25163;&#26426;&#21495;/&#37038;&#31665;"
              required
            />
          </label>

          <label class="field">
            <span class="sr-only">&#23494;&#30721;</span>
            <span class="field-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none">
                <rect x="5" y="10" width="14" height="10" rx="2" />
                <path d="M8 10V8a4 4 0 0 1 8 0v2" />
              </svg>
            </span>
            <input
              v-model="password"
              name="password"
              type="password"
              autocomplete="current-password"
              placeholder="&#23494;&#30721;"
              required
            />
          </label>

          <p class="channel-copy">&#27714;&#32844;&#19987;&#23646;&#36890;&#36947;</p>
          <p v-if="auth.state.error" class="error" role="alert">{{ auth.state.error }}</p>

          <button class="login-submit" type="submit" :disabled="auth.state.loading">
            {{ auth.state.loading ? loadingLabel : submitLabel }}
          </button>

          <div class="login-links" aria-label="&#30331;&#24405;&#36741;&#21161;&#25805;&#20316;">
            <button type="button" class="text-link">&#24536;&#35760;&#23494;&#30721;?</button>
            <button type="button" class="text-link text-link--primary">&#27880;&#20876;&#36134;&#21495;</button>
          </div>
        </form>
      </section>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../stores/auth'

const auth = useAuth()
const route = useRoute()
const router = useRouter()
const username = ref('')
const password = ref('')
const submitLabel = '\u767b\u5f55'
const loadingLabel = '\u767b\u5f55\u4e2d...'

async function submit() {
  try {
    await auth.login(username.value, password.value)
    router.push(route.query.redirect || { name: 'dashboard' })
  } catch {
    // Errors are surfaced through auth.state.error.
  }
}
</script>
