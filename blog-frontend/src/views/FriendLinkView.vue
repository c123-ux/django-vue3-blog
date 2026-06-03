<script setup>
import { ref, computed, onMounted } from 'vue'
import { getFriendLinks } from '@/api/site'

const friendLinks = ref([])
const loading = ref(true)

const getTechLogo = (name) => {
  if (!name) return null
  const logoMap = {
    'Python': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg',
    'Django': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg',
    'REST': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg',
    'Vue': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vuejs/vuejs-original.svg',
    'Vite': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vite/vite-original.svg',
    'Pinia': 'https://pinia.vuejs.org/logo.svg',
    'Router': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vuejs/vuejs-original.svg',
    'Axios': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg',
    'SQLite': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg',
    'HTML': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg',
    'CSS': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg',
    'JavaScript': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg',
    'Markdown': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/markdown/markdown-original.svg',
    'Git': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg',
    'GitHub': 'https://github.githubassets.com/images/modules/logos_page/Octocat.png',
    'VS': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg',
    'Code': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg',
    'Stack': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/stackoverflow/stackoverflow-original.svg',
    'Overflow': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/stackoverflow/stackoverflow-original.svg',
    'Figma': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/figma/figma-original.svg',
    'Can I Use': 'https://caniuse.com/img/favicon-128.png',
    'CodePen': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/codepen/codepen-original.svg'
  }
  
  for (const key in logoMap) {
    if (name.includes(key)) {
      return logoMap[key]
    }
  }
  
  return null
}

const backendLinks = computed(() =>
  friendLinks.value.filter(l => l && l.order >= 1 && l.order <= 9)
)

const frontendLinks = computed(() =>
  friendLinks.value.filter(l => l && l.order >= 10 && l.order <= 19)
)

const toolLinks = computed(() =>
  friendLinks.value.filter(l => l && l.order >= 20)
)

onMounted(async () => {
  try {
    const res = await getFriendLinks()
    console.log('Friend links response:', res)
    const data = res.data
    friendLinks.value = Array.isArray(data) ? data : (data.results || [])
    console.log('Loaded friend links:', friendLinks.value)
  } catch (e) {
    console.error('Failed to load friend links', e)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="friend-link-page">
    <div class="container">
      <div class="page-header">
        <div class="header-icon">🔗</div>
        <h1>友情链接</h1>
        <p class="subtitle">项目所用技术的官方文档与推荐资源</p>
        <div class="header-decoration"></div>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>正在加载...</p>
      </div>

      <template v-else>
        <div v-if="backendLinks.length" class="links-section">
          <div class="section-header">
            <h2>🐍 后端技术文档</h2>
            <div class="section-line"></div>
          </div>
          <div class="links-grid">
            <a
              v-for="link in backendLinks"
              :key="link.id"
              :href="link.url"
              target="_blank"
              rel="noopener noreferrer"
              class="friend-card"
            >
              <div class="card-avatar">
                <img 
                  v-if="getTechLogo(link.name)" 
                  :src="getTechLogo(link.name)" 
                  :alt="link.name" 
                  class="avatar-logo"
                />
                <span 
                  v-else
                  class="avatar-letter"
                >{{ (link.name || '?').charAt(0) }}</span>
              </div>
              <div class="card-info">
                <h3 class="card-name">{{ link.name }}</h3>
                <p class="card-desc">{{ link.description || '暂无简介' }}</p>
              </div>
              <div class="card-visit">
                <span class="visit-icon">↗</span>
              </div>
            </a>
          </div>
        </div>

        <div v-if="frontendLinks.length" class="links-section">
          <div class="section-header">
            <h2>🎨 前端技术文档</h2>
            <div class="section-line"></div>
          </div>
          <div class="links-grid">
            <a
              v-for="link in frontendLinks"
              :key="link.id"
              :href="link.url"
              target="_blank"
              rel="noopener noreferrer"
              class="friend-card"
            >
              <div class="card-avatar">
                <img 
                  v-if="getTechLogo(link.name)" 
                  :src="getTechLogo(link.name)" 
                  :alt="link.name" 
                  class="avatar-logo"
                />
                <span 
                  v-else
                  class="avatar-letter"
                >{{ (link.name || '?').charAt(0) }}</span>
              </div>
              <div class="card-info">
                <h3 class="card-name">{{ link.name }}</h3>
                <p class="card-desc">{{ link.description || '暂无简介' }}</p>
              </div>
              <div class="card-visit">
                <span class="visit-icon">↗</span>
              </div>
            </a>
          </div>
        </div>

        <div v-if="toolLinks.length" class="links-section">
          <div class="section-header">
            <h2>🛠️ 推荐工具</h2>
            <div class="section-line"></div>
          </div>
          <div class="links-grid">
            <a
              v-for="link in toolLinks"
              :key="link.id"
              :href="link.url"
              target="_blank"
              rel="noopener noreferrer"
              class="friend-card"
            >
              <div class="card-avatar">
                <img 
                  v-if="getTechLogo(link.name)" 
                  :src="getTechLogo(link.name)" 
                  :alt="link.name" 
                  class="avatar-logo"
                />
                <span 
                  v-else
                  class="avatar-letter"
                >{{ (link.name || '?').charAt(0) }}</span>
              </div>
              <div class="card-info">
                <h3 class="card-name">{{ link.name }}</h3>
                <p class="card-desc">{{ link.description || '暂无简介' }}</p>
              </div>
              <div class="card-visit">
                <span class="visit-icon">↗</span>
              </div>
            </a>
          </div>
        </div>

        <div v-if="!backendLinks.length && !frontendLinks.length && !toolLinks.length" class="empty-state">
          <div class="empty-icon">🔗</div>
          <h2>暂无友情链接</h2>
          <p>正在加载友情链接数据...</p>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.friend-link-page {
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.header-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.page-header h1 {
  font-size: 2.5rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.subtitle {
  font-size: 1.2rem;
  color: var(--text-secondary-color);
  margin-bottom: 1rem;
}

.header-decoration {
  width: 100px;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  margin: 1.5rem auto;
  border-radius: 2px;
}

.loading-state {
  text-align: center;
  padding: 4rem 0;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  margin: 0 auto 1.5rem;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  color: var(--text-secondary-color);
  font-size: 1.1rem;
}

.links-section {
  margin-bottom: 3rem;
}

.section-header {
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 1.8rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.section-line {
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  border-radius: 2px;
}

.links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.friend-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: var(--surface-color);
  border-radius: 12px;
  box-shadow: 0 2px 12px var(--shadow-color);
  border: 1px solid var(--border-color);
  text-decoration: none;
  color: var(--text-color);
  transition: all 0.3s;
}

.friend-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 24px var(--shadow-color);
  border-color: var(--primary-color);
}

.card-avatar {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
}

.avatar-logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 6px;
  display: block;
}

.avatar-letter {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  display: none;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-info {
  flex: 1;
  min-width: 0;
}

.card-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 0.3rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-desc {
  font-size: 0.9rem;
  color: var(--text-secondary-color);
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-visit {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--background-color);
  border: 1px solid var(--border-color);
  transition: all 0.3s;
}

.friend-card:hover .card-visit {
  background: var(--primary-color);
  border-color: var(--primary-color);
}

.visit-icon {
  font-size: 1rem;
  color: var(--text-secondary-color);
  transition: color 0.3s;
}

.friend-card:hover .visit-icon {
  color: white;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .links-grid {
    grid-template-columns: 1fr;
  }
}
</style>
