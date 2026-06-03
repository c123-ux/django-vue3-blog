<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCategories, getStatistics } from '@/api/article'

const router = useRouter()
const categories = ref([])
const hotArticles = ref([])
const loading = ref(true)

const loadData = async () => {
  try {
    loading.value = true
    const [catRes, statsRes] = await Promise.all([
      getCategories(),
      getStatistics(),
    ])
    categories.value = catRes.data
    hotArticles.value = statsRes.data?.most_viewed || []
  } catch (error) {
    console.error('Failed to load categories:', error)
  } finally {
    loading.value = false
  }
}

const goToCategory = (category) => {
  router.push({
    path: '/search',
    query: { category: category.slug }
  })
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="category-page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">📚 技术专题</h1>
        <p class="page-desc">按技术分类浏览文章，参考 izone 专题页设计</p>
      </div>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>
      
      <div v-else class="category-grid">
        <div
          v-for="cat in categories"
          :key="cat.id"
          class="category-card"
          @click="goToCategory(cat)"
        >
          <div class="category-icon" :style="{ background: `linear-gradient(135deg, ${cat.color}, ${cat.color}dd)` }">
            {{ cat.icon }}
          </div>
          <h3 class="category-name">{{ cat.name }}</h3>
          <p class="category-desc">{{ cat.description || '暂无描述' }}</p>
          <p class="category-count">{{ cat.article_count || 0 }} 篇文章</p>
        </div>
      </div>
      
      <div v-if="hotArticles.length" class="featured-section">
        <h2 class="section-title">🔥 热门文章</h2>
        <div class="featured-grid">
          <div
            v-for="article in hotArticles.slice(0, 6)"
            :key="article.id"
            class="featured-card"
            @click="router.push(`/article/${article.id}`)"
          >
            <div v-if="article.cover" class="featured-cover">
              <img :src="article.cover" :alt="article.title" />
            </div>
            <div class="featured-content">
              <h4 class="featured-title">{{ article.title }}</h4>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.category-page {
  padding: 2rem 0;
  min-height: calc(100vh - 200px);
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

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.category-card {
  background: var(--surface-color);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid var(--border-color);
}

.category-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px var(--shadow-color);
}

.category-icon {
  width: 70px;
  height: 70px;
  margin: 0 auto 1rem;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.category-name {
  font-size: 1.2rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.category-desc {
  color: var(--text-secondary-color);
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.category-count {
  color: var(--primary-color);
  font-size: 0.9rem;
  font-weight: 500;
}

.featured-section {
  margin-top: 3rem;
}

.section-title {
  font-size: 1.5rem;
  color: var(--text-color);
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.featured-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.featured-card {
  background: var(--surface-color);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid var(--border-color);
}

.featured-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px var(--shadow-color);
}

.featured-cover {
  width: 100%;
  height: 140px;
  overflow: hidden;
}

.featured-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.featured-card:hover .featured-cover img {
  transform: scale(1.08);
}

.featured-content {
  padding: 1rem 1.2rem;
}

.featured-title {
  font-size: 1.1rem;
  color: var(--text-color);
  margin-bottom: 0.8rem;
  font-weight: 600;
  line-height: 1.4;
}

.featured-meta {
  color: var(--text-secondary-color);
  font-size: 0.85rem;
}
</style>
