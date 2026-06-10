<template>
  <main class="app-shell">
    <header class="topbar">
      <div>
        <p class="eyebrow">Authenticated</p>
        <h1>Application Home</h1>
      </div>
      <button class="secondary" type="button" @click="auth.logout()">Log out</button>
    </header>

    <section class="workspace">
      <div>
        <p class="label">Signed in as</p>
        <h2>{{ auth.state.user?.display_name || auth.state.user?.username }}</h2>
        <p class="muted">{{ auth.state.user?.username }}</p>
      </div>
      <div>
        <p class="label">API</p>
        <p class="muted">FastAPI protected routes are available with the stored bearer token.</p>
      </div>
    </section>
  </main>
</template>

<script setup>
import { useAuth } from '../stores/auth'

const auth = useAuth()
</script>
