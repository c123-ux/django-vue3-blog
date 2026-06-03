<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { currentTheme, toggleTheme } from '@/stores/theme'
import ReadingProgress from '@/components/ReadingProgress.vue'
import { getSiteConfig } from '@/api/site'
import { useSeo } from '@/composables/useSeo'

const router = useRouter()
const searchQuery = ref('')
const showSearch = ref(false)
const showMenu = ref(false)
const siteName = ref('我的博客')
const navbarVisible = ref(true)
const lastScrollY = ref(0)
const showBackToTop = ref(false)
const { setSeo } = useSeo()

onMounted(async () => {
  try {
    const res = await getSiteConfig()
    siteName.value = res.data.site_name || '我的博客'
    setSeo({
      title: res.data.site_name,
      description: res.data.site_description,
      keywords: res.data.site_keywords,
    })
  } catch (e) {
    console.warn('Failed to load site config')
  }
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

const handleScroll = () => {
  const currentScrollY = window.scrollY
  if (currentScrollY > 80) {
    navbarVisible.value = currentScrollY < lastScrollY.value
    showBackToTop.value = currentScrollY > 400
  } else {
    navbarVisible.value = true
    showBackToTop.value = false
  }
  lastScrollY.value = currentScrollY
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const toggleSearch = () => {
  showSearch.value = !showSearch.value
  if (showSearch.value) {
    setTimeout(() => {
      document.getElementById('searchInput')?.focus()
    }, 100)
  }
}

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ path: '/search', query: { q: searchQuery.value } })
    showSearch.value = false
    searchQuery.value = ''
  }
}

const handleKeyPress = (e) => {
  if (e.key === 'Enter') {
    handleSearch()
  }
}

const toggleMenu = () => {
  showMenu.value = !showMenu.value
}

const closeMenu = () => {
  showMenu.value = false
}
</script>

<template>
  <div id="app" :class="`theme-${currentTheme}`">
    <ReadingProgress />
    <nav class="navbar" :class="{ 'navbar-hidden': !navbarVisible, 'navbar-shadow': lastScrollY > 10 }">
      <div class="container">
        <router-link to="/" class="logo">
          <span class="logo-text">{{ siteName }}</span>
        </router-link>
        <div class="nav-links" :class="{ 'nav-open': showMenu }">
          <router-link to="/" class="nav-link" @click="closeMenu">
            <span>首页</span>
          </router-link>
          <router-link to="/articles" class="nav-link" @click="closeMenu">
            <span>文章</span>
          </router-link>
          <router-link to="/series" class="nav-link" @click="closeMenu">
            <span>专题</span>
          </router-link>
          <router-link to="/write" class="nav-link nav-link-write" @click="closeMenu">
            <span>✏️ 发布文章</span>
          </router-link>
          <router-link to="/notes" class="nav-link" @click="closeMenu">
            <span>笔记</span>
          </router-link>
          <router-link to="/archive" class="nav-link" @click="closeMenu">
            <span>归档</span>
          </router-link>
          <router-link to="/friends" class="nav-link" @click="closeMenu">
            <span>友链</span>
          </router-link>
          <router-link to="/about" class="nav-link" @click="closeMenu">
            <span>关于</span>
          </router-link>
          <div class="nav-actions">
            <button @click="toggleTheme" class="action-btn" :title="currentTheme === 'light' ? '切换暗色' : '切换亮色'">
              <span class="action-icon">{{ currentTheme === 'light' ? '🌙' : '☀️' }}</span>
            </button>
            <button @click="toggleSearch" class="action-btn" title="搜索">
              <span class="action-icon">🔍</span>
            </button>
          </div>
        </div>
        <div class="nav-right-mobile">
          <button @click="toggleTheme" class="action-btn" :title="currentTheme === 'light' ? '切换暗色' : '切换亮色'">
            <span class="action-icon">{{ currentTheme === 'light' ? '🌙' : '☀️' }}</span>
          </button>
          <button @click="toggleSearch" class="action-btn" title="搜索">
            <span class="action-icon">🔍</span>
          </button>
          <button class="hamburger" :class="{ 'hamburger-active': showMenu }" @click="toggleMenu" aria-label="菜单">
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
          </button>
        </div>
      </div>

      <div v-if="showSearch" class="search-bar">
        <div class="container">
          <div class="search-input-wrapper">
            <input
              id="searchInput"
              v-model="searchQuery"
              @keyup="handleKeyPress"
              placeholder="搜索文章..."
              class="search-input"
            />
            <button @click="handleSearch" class="btn btn-primary search-submit">搜索</button>
            <button @click="toggleSearch" class="search-close">✕</button>
          </div>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <router-view v-slot="{ Component, route }">
        <component :is="Component" :key="route.path" />
      </router-view>
    </main>

    <footer class="footer">
      <div class="container">
        <div class="footer-inner">
          <div class="footer-left">
            <div class="footer-brand">
              <span class="footer-logo">{{ siteName }}</span>
              <span class="footer-heart">❤</span>
              <span class="footer-desc">分享技术，记录生活 — 涵盖Python、Django、Vue3之类的技术、科技资讯、新闻热点、美食、健康、旅游等多元化内容</span>
            </div>
            <div class="footer-links">
              <router-link to="/">首页</router-link>
              <router-link to="/articles">文章</router-link>
              <router-link to="/about">关于</router-link>
              <router-link to="/friends">友链</router-link>
            </div>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; {{ new Date().getFullYear() }} {{ siteName }}. All rights reserved.</p>
          <p class="footer-powered">Powered by Django & Vue3</p>
        </div>
      </div>
    </footer>

    <button
      v-if="showBackToTop"
      class="back-to-top"
      @click="scrollToTop"
      title="回到顶部"
    >
      ↑
    </button>
  </div>
</template>

<style>
:root {
  --primary-color: #FF8C42;
  --secondary-color: #FFB347;
  --accent-color: #6BCB77;
  --background-color: #FFF9F0;
  --surface-color: #FFFFFF;
  --text-color: #2C3E50;
  --text-secondary-color: #5D6D7E;
  --text-muted-color: #95A5A6;
  --border-color: #E8DCC8;
  --shadow-color: rgba(255, 140, 66, 0.15);
  --header-bg: #FFFFFF;
  --footer-bg: #FFF8F0;
  --footer-text: #8B7355;
  --tag-bg: #FFF5E6;
  --card-radius: 16px;
}

.theme-dark {
  --primary-color: #FF8C42;
  --secondary-color: #FFB347;
  --accent-color: #6BCB77;
  --background-color: #2C3E50;
  --surface-color: #34495E;
  --text-color: #ECF0F1;
  --text-secondary-color: #BDC3C7;
  --text-muted-color: #7F8C8D;
  --border-color: #4A5B6C;
  --shadow-color: rgba(0, 0, 0, 0.3);
  --header-bg: #34495E;
  --footer-bg: #2C3E50;
  --footer-text: #BDC3C7;
  --tag-bg: #4A5B6C;
  --card-radius: 16px;
}
</style>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: var(--header-bg);
  border-bottom: 1px solid var(--border-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.navbar-hidden {
  transform: translateY(-100%);
}

.navbar-shadow {
  box-shadow: 0 2px 8px var(--shadow-color);
}

.navbar .container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 56px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 700;
  color: var(--text-color);
  text-decoration: none;
  flex-shrink: 0;
}

.logo:hover {
  color: var(--primary-color);
}

.nav-links {
  display: flex;
  gap: 4px;
  align-items: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 14px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary-color);
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.25s ease;
  white-space: nowrap;
}

.nav-link:hover {
  color: var(--primary-color);
  background: var(--tag-bg);
}

.nav-link.nav-link-write {
  background: linear-gradient(135deg, #FF8C42 0%, #FFB347 100%);
  color: white;
  padding: 6px 16px;
  font-weight: 600;
  border-radius: 20px;
}

.nav-link.nav-link-write:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 140, 66, 0.3);
}

.nav-link.router-link-active,
.nav-link.router-link-exact-active {
  color: var(--primary-color);
  background: rgba(255, 140, 66, 0.1);
  font-weight: 600;
}

.nav-link.nav-link-write.router-link-active,
.nav-link.nav-link-write.router-link-exact-active {
  background: linear-gradient(135deg, #FF8C42 0%, #FFB347 100%);
  color: white;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-left: 8px;
  padding-left: 12px;
  border-left: 1px solid var(--border-color);
}

.action-btn {
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.25s ease;
  color: var(--text-secondary-color);
}

.action-btn:hover {
  background: var(--tag-bg);
  color: var(--primary-color);
}

.action-icon {
  font-size: 16px;
  line-height: 1;
}

.nav-right-mobile {
  display: none;
  align-items: center;
  gap: 4px;
}

.hamburger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  width: 34px;
  height: 34px;
  background: none;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  padding: 8px;
  transition: background 0.25s ease;
}

.hamburger:hover {
  background: var(--tag-bg);
}

.hamburger-line {
  display: block;
  width: 100%;
  height: 2px;
  background: var(--text-secondary-color);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.hamburger-active .hamburger-line:nth-child(1) {
  transform: rotate(45deg) translate(4px, 4px);
}

.hamburger-active .hamburger-line:nth-child(2) {
  opacity: 0;
}

.hamburger-active .hamburger-line:nth-child(3) {
  transform: rotate(-45deg) translate(4px, -4px);
}

.search-bar {
  border-top: 1px solid var(--border-color);
  padding: 12px 0;
  animation: slideDown 0.2s ease;
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  max-width: 600px;
  margin: 0 auto;
}

.search-input {
  flex: 1;
  padding: 8px 14px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 14px;
  background: var(--background-color);
  color: var(--text-color);
  transition: border-color 0.3s;
  outline: none;
}

.search-input:focus {
  border-color: var(--primary-color);
}

.search-submit {
  flex-shrink: 0;
}

.search-close {
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  color: var(--text-secondary-color);
  font-size: 16px;
  transition: all 0.25s ease;
}

.search-close:hover {
  background: var(--tag-bg);
  color: var(--primary-color);
}

.main-content {
  min-height: calc(100vh - 160px);
  padding-top: 56px;
  background: var(--background-color);
  transition: background-color 0.3s ease;
}

.footer {
  background: var(--footer-bg);
  color: var(--footer-text);
  padding: 32px 0 20px;
}

.footer-inner {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.footer-left {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 8px;
}

.footer-logo {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
}

.footer-heart {
  color: #ff2152;
  font-size: 14px;
  animation: pulse 1.2s ease-in-out infinite;
  display: inline-block;
}

.footer-desc {
  font-size: 13px;
  color: var(--footer-text);
}

.footer-links {
  display: flex;
  gap: 20px;
}

.footer-links a {
  font-size: 13px;
  color: var(--footer-text);
  text-decoration: none;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: var(--primary-color);
}

.footer-bottom {
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}

.footer-powered {
  color: rgba(255, 255, 255, 0.3);
}

.back-to-top {
  position: fixed;
  bottom: 32px;
  right: 32px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  box-shadow: 0 2px 8px var(--shadow-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: var(--text-secondary-color);
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 999;
}

.back-to-top:hover {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: #fff;
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(255, 140, 66, 0.4);
}

@media (max-width: 768px) {
  .nav-links {
    display: none;
    position: fixed;
    top: 56px;
    left: 0;
    right: 0;
    bottom: 0;
    flex-direction: column;
    background: var(--surface-color);
    padding: 16px;
    gap: 4px;
    overflow-y: auto;
    z-index: 999;
  }

  .nav-links.nav-open {
    display: flex;
  }

  .nav-link {
    width: 100%;
    justify-content: flex-start;
    padding: 10px 16px;
    font-size: 15px;
  }

  .nav-actions {
    display: none;
  }

  .nav-right-mobile {
    display: flex;
  }

  .hamburger {
    display: flex;
  }

  .footer-inner {
    flex-direction: column;
    gap: 20px;
  }

  .footer-right {
    text-align: left;
  }

  .footer-bottom {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }

  .back-to-top {
    bottom: 20px;
    right: 20px;
  }
}
</style>