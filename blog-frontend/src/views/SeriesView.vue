<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getSeriesList } from '@/api/article'

const router = useRouter()
const seriesList = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await getSeriesList()
    seriesList.value = res.data?.results || []
  } catch (e) {
    console.error('Failed to load series:', e)
  } finally {
    loading.value = false
  }
})

const goToSeries = (slug) => {
  router.push(`/series/${slug}`)
}
</script>

<template>
  <div class="series-page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">📚 专题系列</h1>
        <p class="page-desc">按主题整理的文章集合，方便系统学习</p>
        <div class="header-line"></div>
      </div>

      <div v-if="loading" class="loading">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <div v-else-if="seriesList.length === 0" class="empty-state">
        <div class="empty-icon">📚</div>
        <h2>暂无专题</h2>
        <p>还没有创建任何专题系列</p>
      </div>

      <div v-else class="series-grid">
        <div
          v-for="series in seriesList"
          :key="series.id"
          class="series-card"
          @click="goToSeries(series.slug)"
        >
          <div class="series-cover">
            <img 
              v-if="series.cover" 
              :src="series.cover" 
              :alt="series.title"
              class="cover-image"
            />
            <div v-else class="cover-placeholder">{{ series.title.charAt(0) }}</div>
          </div>
          <div class="series-info">
            <h3 class="series-title">{{ series.title }}</h3>
            <p class="series-desc">{{ series.description }}</p>
            <div class="series-meta">
              <span class="article-count">📄 {{ series.article_count }} 篇文章</span>
              <span class="view-btn">查看详情 →</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.series-page {
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

.page-desc {
  color: var(--text-secondary-color);
  margin-bottom: 1rem;
}

.header-line {
  height: 3px;
  width: 80px;
  margin: 0 auto;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  border-radius: 2px;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary-color);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: var(--surface-color);
  border-radius: 12px;
  box-shadow: 0 2px 8px var(--shadow-color);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h2 {
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: var(--text-secondary-color);
}

.series-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.5rem;
}

.series-card {
  background: var(--surface-color);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px var(--shadow-color);
  cursor: pointer;
  transition: all 0.3s ease;
}

.series-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px var(--shadow-color);
}

.series-cover {
  height: 140px;
  overflow: hidden;
  position: relative;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-placeholder {
  height: 100%;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.8);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.series-info {
  padding: 1.2rem;
}

.series-title {
  font-size: 1.2rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.series-desc {
  font-size: 0.9rem;
  color: var(--text-secondary-color);
  margin-bottom: 1rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.series-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.8rem;
  border-top: 1px solid var(--border-color);
}

.article-count {
  font-size: 0.85rem;
  color: var(--text-secondary-color);
}

.view-btn {
  font-size: 0.9rem;
  color: var(--primary-color);
  font-weight: 500;
}

@media (max-width: 768px) {
  .series-grid {
    grid-template-columns: 1fr;
  }
}
</style>