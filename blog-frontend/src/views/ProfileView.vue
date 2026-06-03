<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const user = ref(null)
const loading = ref(true)
const error = ref(null)

const loadUserProfile = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await fetch('http://localhost:8000/api/auth/profile/', {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })
    
    if (response.ok) {
      user.value = await response.json()
    } else {
      throw new Error('Failed to load profile')
    }
  } catch (err) {
    error.value = err.message
    console.error('Failed to load profile:', err)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

onMounted(() => {
  loadUserProfile()
})
</script>

<template>
  <div class="profile-page">
    <div class="container">
      <div class="profile-header">
        <h1>个人中心</h1>
        <p class="subtitle">管理您的个人信息和设置</p>
      </div>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>
      
      <div v-else-if="error" class="error">
        <p>❌ {{ error }}</p>
        <button @click="loadUserProfile" class="btn-retry">重试</button>
      </div>
      
      <div v-else-if="user" class="profile-content">
        <div class="profile-card">
          <div class="profile-avatar">
            <div class="avatar-placeholder">
              {{ user.username?.charAt(0).toUpperCase() }}
            </div>
          </div>
          <div class="profile-info">
            <h2 class="username">{{ user.username }}</h2>
            <p class="email">{{ user.email }}</p>
            <div class="user-stats">
              <div class="stat-item">
                <span class="stat-icon">📝</span>
                <span class="stat-label">文章数</span>
                <span class="stat-value">0</span>
              </div>
              <div class="stat-item">
                <span class="stat-icon">💬</span>
                <span class="stat-label">评论数</span>
                <span class="stat-value">0</span>
              </div>
              <div class="stat-item">
                <span class="stat-icon">👁️</span>
                <span class="stat-label">阅读量</span>
                <span class="stat-value">0</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="profile-sections">
          <div class="profile-section">
            <h3>📋 基本信息</h3>
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">用户名</span>
                <span class="info-value">{{ user.username }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">邮箱</span>
                <span class="info-value">{{ user.email }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">用户ID</span>
                <span class="info-value">{{ user.id }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">注册时间</span>
                <span class="info-value">{{ formatDate(user.date_joined) }}</span>
              </div>
            </div>
          </div>
          
          <div class="profile-section">
            <h3>🔐 账户设置</h3>
            <div class="settings-list">
              <div class="setting-item">
                <span class="setting-label">修改密码</span>
                <button class="btn-setting">修改</button>
              </div>
              <div class="setting-item">
                <span class="setting-label">邮箱验证</span>
                <span class="setting-status verified">✓ 已验证</span>
              </div>
              <div class="setting-item">
                <span class="setting-label">两步验证</span>
                <span class="setting-status unverified">✗ 未启用</span>
              </div>
            </div>
          </div>
          
          <div class="profile-section">
            <h3>📊 活动统计</h3>
            <div class="activity-grid">
              <div class="activity-item">
                <div class="activity-icon">📝</div>
                <div class="activity-content">
                  <h4>我的文章</h4>
                  <p>查看和管理您的文章</p>
                </div>
                <button class="btn-activity">查看</button>
              </div>
              <div class="activity-item">
                <div class="activity-icon">💬</div>
                <div class="activity-content">
                  <h4>我的评论</h4>
                  <p>查看您的评论历史</p>
                </div>
                <button class="btn-activity">查看</button>
              </div>
              <div class="activity-item">
                <div class="activity-icon">⭐</div>
                <div class="activity-content">
                  <h4>收藏夹</h4>
                  <p>查看收藏的文章</p>
                </div>
                <button class="btn-activity">查看</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.profile-header {
  text-align: center;
  margin-bottom: 3rem;
}

.profile-header h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
}

.loading {
  text-align: center;
  padding: 3rem;
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 1rem;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  text-align: center;
  padding: 3rem;
  color: #e74c3c;
}

.btn-retry {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-retry:hover {
  background: #5568d3;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.profile-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  display: flex;
  gap: 2rem;
  align-items: center;
}

.profile-avatar {
  flex-shrink: 0;
}

.avatar-placeholder {
  width: 120px;
  height: 120px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: bold;
}

.profile-info {
  flex: 1;
}

.username {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.email {
  opacity: 0.9;
  margin-bottom: 1.5rem;
}

.user-stats {
  display: flex;
  gap: 2rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stat-icon {
  font-size: 1.5rem;
}

.stat-label {
  opacity: 0.9;
}

.stat-value {
  font-weight: bold;
  font-size: 1.2rem;
}

.profile-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.profile-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.profile-section h3 {
  font-size: 1.3rem;
  color: #333;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #667eea;
}

.info-grid {
  display: grid;
  gap: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.8rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.info-label {
  color: #666;
  font-weight: 500;
}

.info-value {
  color: #333;
  font-weight: bold;
}

.settings-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.setting-label {
  color: #333;
  font-weight: 500;
}

.setting-status {
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.setting-status.verified {
  background: #d4edda;
  color: #155724;
}

.setting-status.unverified {
  background: #f8d7da;
  color: #721c24;
}

.btn-setting {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-setting:hover {
  background: #5568d3;
}

.activity-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
  transition: background 0.3s;
}

.activity-item:hover {
  background: #e9ecef;
}

.activity-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-content h4 {
  font-size: 1rem;
  color: #333;
  margin-bottom: 0.3rem;
}

.activity-content p {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
}

.btn-activity {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-activity:hover {
  background: #5568d3;
}
</style>