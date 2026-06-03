<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

onMounted(() => {
  const access = route.query.access
  const refresh = route.query.refresh
  if (access && refresh) {
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    authStore.accessToken = access
    authStore.refreshToken = refresh
    authStore.fetchUserProfile().finally(() => router.replace('/'))
  } else {
    router.replace('/login')
  }
})
</script>

<template>
  <div class="oauth-callback">
    <div class="spinner"></div>
    <p>正在完成登录...</p>
  </div>
</template>

<style scoped>
.oauth-callback {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  color: var(--text-secondary-color);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>
