<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getOAuthUrl } from '@/api/extras'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({ username: '', password: '' })
const error = ref('')
const loading = ref(false)
const oauthLoading = ref('')

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  try {
    await authStore.login(form.value)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}

const handleOAuth = async (provider) => {
  oauthLoading.value = provider
  error.value = ''
  try {
    const res = await getOAuthUrl(provider)
    if (res.data.authorization_url) {
      window.location.href = res.data.authorization_url
    }
  } catch (err) {
    error.value = err.response?.data?.error || `${provider} 登录暂不可用，请检查 OAuth 配置`
  } finally {
    oauthLoading.value = ''
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-box">
      <button @click="router.push('/')" class="close-btn" title="关闭并返回首页">✕</button>
      <h1 class="login-title">用户登录</h1>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div v-if="error" class="error-message">{{ error }}</div>
        
        <div class="form-group">
          <label for="username">用户名</label>
          <input id="username" v-model="form.username" type="text" required placeholder="请输入用户名" />
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input id="password" v-model="form.password" type="password" required placeholder="请输入密码" />
        </div>
        
        <button type="submit" :disabled="loading" class="btn-login">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>

      <div class="oauth-section">
        <div class="oauth-divider"><span>或使用第三方登录</span></div>
        <div class="oauth-buttons">
          <button
            type="button"
            class="btn-oauth btn-github"
            :disabled="!!oauthLoading"
            @click="handleOAuth('github')"
          >
            {{ oauthLoading === 'github' ? '跳转中...' : '🐙 GitHub 登录' }}
          </button>
          <button
            type="button"
            class="btn-oauth btn-wechat"
            :disabled="!!oauthLoading"
            @click="handleOAuth('wechat')"
          >
            {{ oauthLoading === 'wechat' ? '跳转中...' : '💬 微信登录' }}
          </button>
        </div>
      </div>
      
      <p class="register-link">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-box {
  position: relative;
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 36px;
  height: 36px;
  background: #f0f0f0;
  border: none;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
  color: #666;
}

.login-title {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label { color: #555; font-weight: 500; }

.form-group input {
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 6px;
  text-align: center;
}

.btn-login {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
}

.oauth-section { margin-top: 1.5rem; }

.oauth-divider {
  text-align: center;
  color: #999;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.oauth-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.btn-oauth {
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
}

.btn-github:hover { border-color: #333; background: #f6f8fa; }
.btn-wechat:hover { border-color: #07c160; background: #f0fff5; }

.register-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.register-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}
</style>
