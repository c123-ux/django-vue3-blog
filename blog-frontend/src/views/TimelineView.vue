<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getArticles } from '@/api/article'

const router = useRouter()
const allArticles = ref([])
const loading = ref(true)

const groupedArticles = computed(() => {
  const groups = {}
  allArticles.value.forEach(article => {
    const date = new Date(article.created_at)
    const yearMonth = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
    const year = date.getFullYear()
    
    if (!groups[year]) {
      groups[year] = {}
    }
    if (!groups[year][yearMonth]) {
      groups[year][yearMonth] = {
        articles: [],
        count: 0
      }
    }
    groups[year][yearMonth].articles.push(article)
    groups[year][yearMonth].count++
  })
  
  return groups
})

const years = computed(() => {
  return Object.keys(groupedArticles.value).sort((a, b) => b - a)
})

const loadArticles = async () => {
  try {
    loading.value = true
    const response = await getArticles({ page: 1, page_size: 100 })
    allArticles.value = response.data.results || []
  } catch (error) {
    console.error('Failed to load articles:', error)
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

const getMonthName = (yearMonth) => {
  const [year, month] = yearMonth.split('-')
  const monthNames = ['一月', '二月', '三月', '四月', '五月', '六月', 
                      '七月', '八月', '九月', '十月', '十一月', '十二月']
  return monthNames[parseInt(month) - 1]
}

const goToArticle = (id) => {
  router.push(`/article/${id}`)
}

onMounted(() => {
  loadArticles()
})
</script>

<template>
  <div class="timeline-page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">📅 文章归档</h1>
        <p class="page-desc">按时间线整理的所有文章</p>
      </div>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>
      
      <div v-else class="timeline-container">
        <div v-for="year in years" :key="year" class="year-section">
          <div class="year-header">
            <span class="year-badge">{{ year }}</span>
            <span class="year-count">共 {{ Object.keys(groupedArticles[year]).length }} 个月</span>
          </div>
          
          <div class="timeline">
            <div v-for="(data, yearMonth) in groupedArticles[year]" :key="yearMonth" class="timeline-item">
              <div class="timeline-marker">
                <div class="marker-dot"></div>
                <div class="marker-line"></div>
              </div>
              <div class="timeline-content">
                <div class="month-header">
                  <h3 class="month-title">{{ getMonthName(yearMonth) }}</h3>
                  <span class="month-count">{{ data.count }} 篇</span>
                </div>
                <div class="articles-list">
                  <div
                    v-for="article in data.articles"
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
      </div>
    </div>
  </div>
</template>

<style scoped>
.timeline-page {
  padding: 2rem 0;
  min-height: calc(100vh - 200px);
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2.5rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.page-desc {
  color: var(--text-secondary-color);
  font-size: 1.1rem;
}

.loading {
  text-align: center;
  padding: 4rem;
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

.timeline-container {
  position: relative;
}

.year-section {
  margin-bottom: 3rem;
}

.year-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.year-badge {
  font-size: 2rem;
  font-weight: bold;
  color: var(--primary-color);
}

.year-count {
  color: var(--text-secondary-color);
  font-size: 0.9rem;
}

.timeline {
  position: relative;
  padding-left: 30px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 8px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--border-color);
}

.timeline-item {
  position: relative;
  margin-bottom: 2rem;
}

.timeline-marker {
  position: absolute;
  left: -26px;
  top: 0;
}

.marker-dot {
  width: 16px;
  height: 16px;
  background: var(--primary-color);
  border-radius: 50%;
  border: 3px solid var(--surface-color);
  box-shadow: 0 0 0 2px var(--primary-color);
}

.marker-line {
  width: 2px;
  height: 100%;
  background: var(--border-color);
  margin-left: 7px;
  margin-top: 4px;
}

.timeline-content {
  background: var(--surface-color);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px var(--shadow-color);
  border: 1px solid var(--border-color);
}

.month-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid var(--border-color);
}

.month-title {
  font-size: 1.2rem;
  color: var(--text-color);
  font-weight: 600;
}

.month-count {
  color: var(--primary-color);
  font-size: 0.9rem;
  font-weight: 500;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.article-item {
  display: grid;
  grid-template-columns: 120px 1fr 80px;
  gap: 1rem;
  padding: 0.8rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  align-items: center;
}

.article-item:hover {
  background: var(--background-color);
  transform: translateX(4px);
}

.article-date {
  color: var(--text-secondary-color);
  font-size: 0.85rem;
}

.article-title {
  color: var(--text-color);
  font-size: 0.95rem;
  transition: color 0.3s;
}

.article-item:hover .article-title {
  color: var(--primary-color);
}

.article-views {
  color: var(--text-secondary-color);
  font-size: 0.85rem;
  text-align: right;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .article-item {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .article-views {
    text-align: left;
  }
}
</style>