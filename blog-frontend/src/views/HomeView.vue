<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getArticles, getStatistics, getTags, getCategories } from '@/api/article'
import { getSiteConfig, getFriendLinks } from '@/api/site'

const router = useRouter()
const articles = ref([])
const loading = ref(true)
const siteConfig = ref(null)
const friendLinks = ref([])
const popularTags = ref([])
const categories = ref([])
const statistics = ref(null)
const pagination = ref({
  count: 0,
  next: null,
  previous: null,
})

const hotArticles = ref([])

const tagColors = [
  '#FF8C42', '#FFB347', '#6BCB77', '#4ECDC4',
  '#FF6B6B', '#FFA07A', '#F4A460', '#87CEEB', '#DDA0DD'
]

const getTagColor = (index) => tagColors[index % tagColors.length]

const runningDays = computed(() => {
  if (!siteConfig.value?.start_date) return 0
  const start = new Date(siteConfig.value.start_date)
  const now = new Date()
  return Math.floor((now - start) / (1000 * 60 * 60 * 24))
})

const loadSiteData = async () => {
  const [siteRes, linksRes, tagsRes, catRes] = await Promise.allSettled([
    getSiteConfig(),
    getFriendLinks(),
    getTags(),
    getCategories(),
  ])
  if (siteRes.status === 'fulfilled') {
    siteConfig.value = siteRes.value.data
  }
  if (linksRes.status === 'fulfilled') {
    friendLinks.value = linksRes.value.data?.results || linksRes.value.data || []
  }
  if (tagsRes.status === 'fulfilled') {
    popularTags.value = (tagsRes.value.data?.results || []).slice(0, 30)
  }
  if (catRes.status === 'fulfilled') {
    categories.value = catRes.value.data?.results || []
  }
}

const loadArticles = async (page = 1) => {
  try {
    loading.value = true
    const response = await getArticles({ page })
    articles.value = response.data.results
    pagination.value = {
      count: response.data.count,
      next: response.data.next,
      previous: response.data.previous,
    }
    if (!hotArticles.value.length && response.data.results.length) {
      hotArticles.value = [...response.data.results]
        .sort((a, b) => b.views - a.views)
        .slice(0, 10)
    }
  } catch (error) {
    console.error('Failed to load articles:', error)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes} 分钟前`
  if (hours < 24) return `${hours} 小时前`
  if (days < 7) return `${days} 天前`
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

const goToArticle = (id) => {
  router.push(`/article/${id}`)
}

const nextPage = () => {
  if (pagination.value.next) {
    const url = new URL(pagination.value.next)
    const page = url.searchParams.get('page')
    loadArticles(page)
  }
}

const prevPage = () => {
  if (pagination.value.previous) {
    const url = new URL(pagination.value.previous)
    const page = url.searchParams.get('page')
    loadArticles(page)
  }
}

const searchByTag = (tag) => {
  const tagName = typeof tag === 'string' ? tag : tag.name
  router.push({ path: '/search', query: { q: tagName } })
}

const goToCategory = (slug) => {
  router.push({ path: '/search', query: { category: slug } })
}

const currentPage = computed(() => {
  if (!pagination.value.previous && pagination.value.next) return 1
  if (pagination.value.previous) {
    const url = new URL(pagination.value.previous)
    const p = parseInt(url.searchParams.get('page') || '1')
    return p + 1
  }
  return 1
})

const totalPages = computed(() => {
  return Math.ceil(pagination.value.count / 10) || 1
})

const pageNumbers = computed(() => {
  const current = currentPage.value
  const total = totalPages.value
  const pages = []
  const start = Math.max(1, current - 2)
  const end = Math.min(total, current + 2)
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

const goToPage = (page) => {
  loadArticles(page)
}

onMounted(() => {
  loadSiteData()
  loadArticles()
})
</script>

<template>
  <div class="home">
    <div class="container">
      <div class="main-layout">
        <div class="content-area">
          <div class="section-header">
            <h1 class="page-title">最新文章</h1>
            <p class="page-desc">分享技术，记录生活</p>
          </div>

          <div v-if="loading" class="loading">
            <div class="loading-spinner"></div>
            <p>加载中...</p>
          </div>

          <div v-else-if="articles.length > 0" class="article-list">
            <div
              v-for="article in articles"
              :key="article.id"
              class="article-card"
              @click="goToArticle(article.id)"
            >
              <div class="article-media">
                <div class="article-thumb">
                  <img v-if="article.cover" :src="article.cover" :alt="article.title" class="thumb-img" />
                  <div v-else class="thumb-placeholder">
                    {{ article.title.charAt(0) }}
                  </div>
                </div>
                <div class="article-body">
                  <div class="article-header">
                    <div class="article-meta-top">
                      <span v-if="article.is_top" class="badge badge-top">置顶</span>
                      <span v-if="article.category_name" class="badge badge-category">{{ article.category_name }}</span>
                    </div>
                    <h2 class="article-title">{{ article.title }}</h2>
                  </div>
                  <p class="article-summary">{{ article.summary }}</p>
                  <div class="article-footer">
                    <div class="article-meta">
                      <span class="meta-item">
                        <span class="meta-avatar">{{ (article.author_name || '匿').charAt(0) }}</span>
                        {{ article.author_name || '匿名' }}
                      </span>
                      <span class="meta-divider"></span>
                      <span class="meta-item">{{ formatDate(article.created_at) }}</span>
                      <span class="meta-divider"></span>
                      <span class="meta-item">{{ article.comments_count || 0 }} 评论</span>
                    </div>
                    <span class="read-more">阅读全文 →</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="empty-state">
            <div class="empty-icon">📝</div>
            <h3>暂无文章</h3>
            <p>还没有发布任何文章，敬请期待！</p>
          </div>

          <div v-if="articles.length > 0" class="pagination">
            <button
              @click="prevPage"
              :disabled="!pagination.previous"
              class="btn-page"
            >
              ‹ 上一页
            </button>
            <div class="page-numbers">
              <button
                v-for="page in pageNumbers"
                :key="page"
                @click="goToPage(page)"
                :class="['btn-page-num', { active: page === currentPage }]"
              >
                {{ page }}
              </button>
            </div>
            <button
              @click="nextPage"
              :disabled="!pagination.next"
              class="btn-page"
            >
              下一页 ›
            </button>
          </div>
        </div>

        <aside class="sidebar">
          <div class="sidebar-card" v-if="hotArticles.length">
            <div class="card-header">
              <span class="header-title">昨日热榜</span>
            </div>
            <div class="card-body">
              <ol class="hot-list">
                <li
                  v-for="(article, index) in hotArticles.slice(0, 10)"
                  :key="article.id"
                  @click="goToArticle(article.id)"
                  class="hot-item"
                  :class="`hot-rank-${index + 1}`"
                >
                  <span class="hot-num">{{ index + 1 }}</span>
                  <span class="hot-title">{{ article.title }}</span>
                </li>
              </ol>
            </div>
          </div>

          <div class="sidebar-card" v-if="categories.length">
            <div class="card-header">
              <span class="header-title">文章分类</span>
            </div>
            <div class="card-body">
              <ul class="category-list">
                <li
                  v-for="cat in categories"
                  :key="cat.id"
                  @click="goToCategory(cat.slug)"
                  class="category-item"
                >
                  <span class="category-name">{{ cat.name }}</span>
                  <span class="category-count">{{ cat.article_count || 0 }}</span>
                </li>
              </ul>
            </div>
          </div>

          <div class="sidebar-card" v-if="popularTags.length">
            <div class="card-header">
              <span class="header-title">标签云</span>
            </div>
            <div class="card-body">
              <div class="tags-cloud">
                <span
                  v-for="(tag, index) in popularTags"
                  :key="tag.id"
                  class="tag-cloud-item"
                  :style="{ color: getTagColor(index) }"
                  @click="searchByTag(tag)"
                >{{ tag.name }}</span>
              </div>
            </div>
          </div>

          <div class="sidebar-card" v-if="siteConfig?.notice">
            <div class="card-header">
              <span class="header-title">网站公告</span>
            </div>
            <div class="card-body">
              <div class="notice-content">
                <p v-for="(line, i) in (siteConfig.notice || '').split('\n').filter(Boolean)" :key="i">{{ line }}</p>
              </div>
            </div>
          </div>

          <div class="sidebar-card" v-if="friendLinks.length">
            <div class="card-header">
              <span class="header-title">技术参考文档</span>
            </div>
            <div class="card-body">
              <p class="friend-links-intro">这是本项目开发中用到的技术栈官方文档，方便大家学习和参考！</p>
              <ul class="friend-links">
                <li v-for="link in friendLinks" :key="link.id">
                  <a :href="link.url" target="_blank" rel="noopener">{{ link.name }}</a>
                </li>
              </ul>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  padding: 24px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.main-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 24px;
  align-items: start;
}

.content-area {
  min-width: 0;
}

.section-header {
  margin-bottom: 20px;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 4px;
}

.page-desc {
  font-size: 13px;
  color: var(--text-muted-color);
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.article-card {
  background: var(--surface-color);
  border-radius: var(--card-radius);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid var(--border-color);
}

.article-card:hover {
  box-shadow: 0 8px 24px rgba(255, 140, 66, 0.2);
  transform: translateY(-4px);
}

.article-media {
  display: flex;
  gap: 0;
}

.article-thumb {
  width: 200px;
  min-height: 150px;
  flex-shrink: 0;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.thumb-img {
  width: 100%;
  height: 100%;
  min-height: 150px;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.article-card:hover .thumb-img {
  transform: scale(1.08);
}

.thumb-placeholder {
  font-size: 40px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.7);
}

.article-body {
  flex: 1;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  position: relative;
}

.article-body::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 20px;
  right: 20px;
  height: 2px;
  background: var(--border-color);
  background-image: linear-gradient(90deg, var(--primary-color), var(--primary-color));
  background-repeat: no-repeat;
  background-size: 0 2px;
  background-position: left bottom;
  transition: background-size 0.4s ease;
}

.article-card:hover .article-body::after {
  background-size: 100% 2px;
}

.article-header {
  margin-bottom: 8px;
}

.article-meta-top {
  display: flex;
  gap: 6px;
  margin-bottom: 6px;
}

.badge {
  display: inline-block;
  padding: 2px 8px;
  font-size: 11px;
  font-weight: 600;
  border-radius: 3px;
}

.badge-top {
  background: #f59e0b;
  color: #fff;
}

.badge-category {
  background: var(--accent-color);
  color: #fff;
}

.article-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-color);
  line-height: 1.5;
  transition: color 0.3s;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-card:hover .article-title {
  color: var(--primary-color);
}

.article-summary {
  font-size: 13px;
  color: var(--text-secondary-color);
  line-height: 1.7;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-muted-color);
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
}

.meta-avatar {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--primary-color);
  color: #fff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 600;
}

.meta-divider {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: var(--border-color);
}

.read-more {
  font-size: 13px;
  font-weight: 500;
  color: var(--primary-color);
  opacity: 0;
  transform: translateX(-8px);
  transition: all 0.3s ease;
  white-space: nowrap;
}

.article-card:hover .read-more {
  opacity: 1;
  transform: translateX(0);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 24px;
  padding: 16px;
}

.btn-page {
  padding: 6px 14px;
  border: 1px solid var(--border-color);
  background: var(--surface-color);
  color: var(--text-secondary-color);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.25s ease;
  font-size: 13px;
  font-weight: 500;
}

.btn-page:hover:not(:disabled) {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.btn-page:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 4px;
}

.btn-page-num {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border-color);
  background: var(--surface-color);
  color: var(--text-secondary-color);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.25s ease;
  font-size: 13px;
}

.btn-page-num:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.btn-page-num.active {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: #fff;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sidebar-card {
  background: var(--surface-color);
  border-radius: var(--card-radius);
  overflow: hidden;
  border: 1px solid var(--border-color);
  box-shadow: 0 2px 8px rgba(255, 140, 66, 0.08);
}

.card-header {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-color);
  position: relative;
  background: linear-gradient(135deg, #FFF9F0 0%, #FFE8D6 100%);
}

.header-title {
  font-size: 14px;
  font-weight: 600;
  color: #2C3E50;
  padding-bottom: 12px;
  display: block;
  border-bottom: 2px solid #FF8C42;
  margin-bottom: -14px;
}

.card-body {
  padding: 14px 16px;
}

.blog-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-bottom: 14px;
}

.blog-link-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 10px 4px;
  background: #FFF5E6;
  border-radius: 10px;
  text-decoration: none;
  font-size: 12px;
  color: #5D6D7E;
  transition: all 0.25s ease;
}

.blog-link-item:hover {
  background: #FF8C42;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 140, 66, 0.3);
}

.link-icon {
  font-size: 18px;
}

.blog-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.stat-item {
  text-align: center;
  padding: 8px 4px;
}

.stat-number {
  display: block;
  font-size: 20px;
  font-weight: 700;
  color: var(--text-color);
  line-height: 1.3;
}

.stat-label {
  font-size: 11px;
  color: var(--text-muted-color);
}

.hot-list {
  list-style: none;
  padding: 0;
  margin: 0;
  counter-reset: hot-counter;
}

.hot-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 7px 0;
  cursor: pointer;
  transition: all 0.25s ease;
  border-bottom: 1px solid var(--border-color);
  position: relative;
  counter-increment: hot-counter;
}

.hot-item:last-child {
  border-bottom: none;
}

.hot-item:hover {
  padding-left: 4px;
}

.hot-num {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
  margin-top: 1px;
  background: var(--text-muted-color);
}

.hot-rank-1 .hot-num { background: #ef4444; }
.hot-rank-2 .hot-num { background: #f97316; }
.hot-rank-3 .hot-num { background: #f59e0b; }
.hot-rank-4 .hot-num,
.hot-rank-5 .hot-num,
.hot-rank-6 .hot-num,
.hot-rank-7 .hot-num { background: #64748b; }

.hot-title {
  font-size: 13px;
  color: var(--text-color);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.hot-item:hover .hot-title {
  color: var(--primary-color);
}

.category-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  cursor: pointer;
  transition: all 0.25s ease;
  border-bottom: 1px solid var(--border-color);
}

.category-item:last-child {
  border-bottom: none;
}

.category-item:hover {
  padding-left: 4px;
  color: #FF8C42;
}

.category-name {
  font-size: 13px;
  color: #2C3E50;
  position: relative;
  padding-left: 14px;
  transition: color 0.25s ease;
}

.category-name::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-top: 4px solid transparent;
  border-bottom: 4px solid transparent;
  border-left: 5px solid #FFB347;
  transition: border-left-color 0.25s ease;
}

.category-item:hover .category-name::before {
  border-left-color: #FF8C42;
}

.category-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  height: 20px;
  padding: 0 6px;
  font-size: 11px;
  font-weight: 600;
  color: #fff;
  background: var(--accent-color);
  border-radius: 10px;
}

.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  line-height: 1;
}

.tag-cloud-item {
  display: inline-block;
  padding: 3px 8px;
  font-size: 12px;
  border-radius: 3px;
  background: var(--tag-bg);
  cursor: pointer;
  transition: all 0.25s ease;
  line-height: 1.6;
}

.tag-cloud-item:hover {
  background: var(--primary-color) !important;
  color: #fff !important;
}

.notice-content {
  font-size: 13px;
  color: var(--text-secondary-color);
  line-height: 1.8;
}

.notice-content p {
  margin-bottom: 4px;
}

.friend-links-intro {
  font-size: 12px;
  color: var(--text-muted-color);
  margin-bottom: 12px;
  line-height: 1.6;
}

.friend-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.friend-links li {
  flex: 0 0 auto;
}

.friend-links a {
  display: block;
  padding: 4px 12px;
  font-size: 12px;
  color: var(--text-secondary-color);
  background: var(--tag-bg);
  border-radius: 4px;
  text-decoration: none;
  transition: all 0.25s ease;
}

.friend-links a:hover {
  background: var(--primary-color);
  color: #fff;
}

@media (max-width: 1024px) {
  .main-layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    order: 2;
  }
}

@media (max-width: 768px) {
  .home {
    padding: 16px 0;
  }

  .container {
    padding: 0 12px;
  }

  .article-media {
    flex-direction: column;
  }

  .article-thumb {
    width: 100%;
    height: 120px;
  }

  .article-body {
    padding: 14px;
  }

  .article-title {
    font-size: 16px;
  }

  .article-meta {
    gap: 6px;
    font-size: 11px;
  }

  .read-more {
    display: none;
  }

  .pagination {
    gap: 8px;
    flex-wrap: wrap;
  }

  .blog-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>