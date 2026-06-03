<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getArchive, getStatistics } from '@/api/article'

const router = useRouter()

const archiveData = ref([])
const statistics = ref(null)
const loading = ref(true)
const error = ref(null)

const loadArchive = async () => {
  try {
    const response = await getArchive()
    archiveData.value = response.data
  } catch (err) {
    console.error('加载归档失败:', err)
    error.value = '加载归档失败，请稍后重试'
  }
}

const loadStatistics = async () => {
  try {
    const response = await getStatistics()
    statistics.value = response.data
  } catch (err) {
    console.error('加载统计数据失败:', err)
  }
}

const goToArticle = (id) => {
  router.push(`/article/${id}`)
}

const goToMonthArchive = (year, month) => {
  router.push(`/archive/${year}/${month}`)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([loadArchive(), loadStatistics()])
  } catch (err) {
    console.error('Failed to load archive:', err)
    if (!error.value) error.value = '加载失败，请稍后重试'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="archive-page">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="error" class="error">
      <div class="error-icon">❌</div>
      <p>{{ error }}</p>
    </div>

    <div v-else class="container">
      <div class="archive-layout">
        <div class="archive-main">
          <section class="archive-section">
            <div class="section-header">
              <h1 class="section-title">📅 文章归档</h1>
              <div class="section-line"></div>
            </div>

            <div v-if="archiveData.length === 0" class="empty-state">
              <div class="empty-icon">📭</div>
              <p>暂无文章归档</p>
            </div>

            <div v-else class="archive-list">
              <div
                v-for="yearData in archiveData"
                :key="yearData.year"
                class="archive-year"
              >
                <div class="year-header">
                  <h2 class="year-title">{{ yearData.year }}年</h2>
                  <span class="year-count">{{ yearData.months.reduce((sum, m) => sum + m.count, 0) }}篇文章</span>
                </div>

                <div class="months-container">
                  <div
                    v-for="monthData in yearData.months"
                    :key="monthData.month"
                    class="archive-month"
                  >
                    <div class="month-header" @click="goToMonthArchive(yearData.year, monthData.month)">
                      <h3 class="month-title">{{ monthData.month }}月</h3>
                      <span class="month-count">{{ monthData.count }}篇</span>
                      <span class="expand-icon">▶</span>
                    </div>

                    <div class="month-articles">
                      <div
                        v-for="article in monthData.articles"
                        :key="article.id"
                        class="article-item"
                        @click="goToArticle(article.id)"
                      >
                        <span class="article-date">{{ formatDate(article.created_at) }}</span>
                        <span class="article-title">{{ article.title }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>

        <aside v-if="statistics" class="archive-sidebar">
          <div class="statistics-card">
            <h3 class="stats-title">📊 网站统计</h3>
            
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-icon">📝</div>
                <div class="stat-content">
                  <div class="stat-value">{{ statistics.total_articles }}</div>
                  <div class="stat-label">文章总数</div>
                </div>
              </div>
            </div>

            <div v-if="statistics.articles_by_category && Object.keys(statistics.articles_by_category).length > 0" class="category-stats">
              <h4 class="stats-subtitle">分类统计</h4>
              <div class="category-list">
                <div
                  v-for="(count, category) in statistics.articles_by_category"
                  :key="category"
                  class="category-item"
                >
                  <span class="category-name">{{ category }}</span>
                  <span class="category-count">{{ count }}篇</span>
                </div>
              </div>
            </div>

            <div v-if="statistics.most_viewed && statistics.most_viewed.length > 0" class="popular-articles">
              <h4 class="stats-subtitle">热门文章</h4>
              <div class="popular-list">
                <div
                  v-for="article in statistics.most_viewed.slice(0, 5)"
                  :key="article.id"
                  class="popular-item"
                  @click="goToArticle(article.id)"
                >
                  <span class="popular-title">{{ article.title }}</span>
                </div>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<style scoped>
.archive-page {
  padding: 2rem 0;
  min-height: calc(100vh - 200px);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.loading {
  text-align: center;
  padding: 4rem;
  font-size: 1.2rem;
  color: var(--text-secondary-color);
}

.spinner {
  width: 50px;
  height: 50px;
  margin: 0 auto 1.5rem;
  border: 4px solid var(--border-color);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  text-align: center;
  padding: 4rem;
  color: var(--error-color);
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.archive-layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 2rem;
}

.archive-main {
  min-width: 0;
}

.archive-section {
  background: var(--surface-color);
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 2px 12px var(--shadow-color);
  border: 1px solid var(--border-color);
}

.section-header {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 2rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.section-line {
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  border-radius: 2px;
}

.empty-state {
  text-align: center;
  padding: 4rem;
  color: var(--text-secondary-color);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.archive-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.archive-year {
  border-left: 4px solid var(--primary-color);
  padding-left: 1.5rem;
}

.year-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.year-title {
  font-size: 1.5rem;
  color: var(--text-color);
  font-weight: 600;
}

.year-count {
  color: var(--text-secondary-color);
  font-size: 0.9rem;
}

.months-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.archive-month {
  background: var(--background-color);
  border-radius: 8px;
  overflow: hidden;
}

.month-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
  background: var(--surface-color);
}

.month-header:hover {
  background: var(--background-color);
}

.month-title {
  font-size: 1.1rem;
  color: var(--text-color);
  font-weight: 500;
}

.month-count {
  color: var(--text-secondary-color);
  font-size: 0.9rem;
  margin-right: 0.5rem;
}

.expand-icon {
  color: var(--primary-color);
  font-size: 0.8rem;
  transition: transform 0.3s;
}

.month-header:hover .expand-icon {
  transform: translateX(4px);
}

.month-articles {
  padding: 0.5rem 0;
}

.article-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
  border-left: 3px solid transparent;
}

.article-item:hover {
  background: var(--surface-color);
  border-left-color: var(--primary-color);
  transform: translateX(4px);
}

.article-date {
  color: var(--text-secondary-color);
  font-size: 0.85rem;
  min-width: 120px;
}

.article-title {
  flex: 1;
  color: var(--text-color);
  font-size: 0.95rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.article-views {
  color: var(--text-secondary-color);
  font-size: 0.85rem;
}

.archive-sidebar {
  position: sticky;
  top: 100px;
  height: fit-content;
}

.statistics-card {
  background: var(--surface-color);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px var(--shadow-color);
  border: 1px solid var(--border-color);
}

.stats-title {
  font-size: 1.2rem;
  color: var(--text-color);
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.stats-grid {
  display: grid;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--background-color);
  border-radius: 8px;
}

.stat-icon {
  font-size: 2rem;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.5rem;
  color: var(--text-color);
  font-weight: 700;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-secondary-color);
  margin-top: 0.25rem;
}

.category-stats,
.popular-articles {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.stats-subtitle {
  font-size: 1rem;
  color: var(--text-color);
  margin-bottom: 1rem;
  font-weight: 600;
}

.category-list,
.popular-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: var(--background-color);
  border-radius: 6px;
}

.category-name {
  color: var(--text-color);
  font-size: 0.9rem;
}

.category-count {
  color: var(--text-secondary-color);
  font-size: 0.85rem;
}

.popular-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: var(--background-color);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.popular-item:hover {
  background: var(--surface-color);
  transform: translateX(4px);
}

.popular-title {
  flex: 1;
  color: var(--text-color);
  font-size: 0.9rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-right: 0.5rem;
}

.popular-views {
  color: var(--text-secondary-color);
  font-size: 0.85rem;
}

@media (max-width: 1024px) {
  .archive-layout {
    grid-template-columns: 1fr;
  }
  
  .archive-sidebar {
    display: none;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
  
  .archive-section {
    padding: 1.5rem;
  }
  
  .section-title {
    font-size: 1.5rem;
  }
  
  .article-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .article-date {
    min-width: auto;
  }
}
</style>