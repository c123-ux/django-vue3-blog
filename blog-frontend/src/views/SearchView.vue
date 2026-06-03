<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchArticles, getArticles } from '@/api/article'

const route = useRoute()
const router = useRouter()

const articles = ref([])
const relatedArticles = ref([])
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const categorySlug = ref('')

const performSearch = async () => {
  const query = route.query.q
  const category = route.query.category

  if (!query && !category) {
    articles.value = []
    relatedArticles.value = []
    return
  }

  try {
    loading.value = true
    error.value = null
    searchQuery.value = query || ''
    categorySlug.value = category || ''

    let response
    if (query) {
      response = await searchArticles(query)
      articles.value = response.data.results || []
      relatedArticles.value = response.data.related || []
    } else {
      response = await getArticles({ category })
      articles.value = response.data.results || []
      relatedArticles.value = []
    }
  } catch (err) {
    console.error('搜索失败:', err)
    error.value = '搜索失败，请稍后再试'
    articles.value = []
    relatedArticles.value = []
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

const goToArticle = (id) => {
  router.push(`/article/${id}`)
}

const highlightText = (text, query) => {
  if (!text || !query) return text
  const regex = new RegExp(`(${query})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
}

watch(
  () => [route.query.q, route.query.category],
  () => {
    performSearch()
  },
  { immediate: true }
)
</script>

<template>
  <div class="search-page">
    <div class="container">
      <div class="search-header">
        <h1>🔍 搜索结果</h1>
        <p class="search-info">
          <span v-if="searchQuery">搜索关键词: <strong>"{{ searchQuery }}"</strong></span>
          <span v-if="articles.length > 0" class="result-count">找到 {{ articles.length }} 篇相关文章</span>
        </p>
      </div>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>搜索中...</p>
      </div>
      
      <div v-else-if="error" class="error">
        <p>❌ {{ error }}</p>
        <button @click="performSearch(searchQuery)" class="btn-retry">重试</button>
      </div>
      
      <div v-else-if="articles.length === 0" class="empty-state">
        <div class="empty-icon">🔍</div>
        <h2>未找到相关文章</h2>
        <p>尝试使用其他关键词搜索</p>
        <button @click="router.push('/')" class="btn-back">返回首页</button>
      </div>
      
      <div v-else class="search-results">
        <div
          v-for="article in articles"
          :key="article.id"
          class="search-result-item"
          @click="goToArticle(article.id)"
        >
          <div v-if="article.cover" class="result-cover">
            <img :src="article.cover" :alt="article.title" />
          </div>
          <div class="result-content">
            <h2 class="result-title" v-html="highlightText(article.title, searchQuery)"></h2>
            <p class="result-summary" v-html="highlightText(article.summary, searchQuery)"></p>
            <div class="result-meta">
              <span class="author">👤 {{ article.author_name }}</span>
              <span class="date">📅 {{ formatDate(article.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="relatedArticles.length > 0" class="related-section">
        <div class="related-header">
          <h3 class="related-title">📚 相关内容推荐</h3>
          <div class="related-line"></div>
        </div>
        <div class="related-grid">
          <div
            v-for="article in relatedArticles"
            :key="article.id"
            class="related-card"
            @click="goToArticle(article.id)"
          >
            <h4 class="related-card-title">{{ article.title }}</h4>
            <p class="related-card-summary">{{ article.summary }}</p>
            <div class="related-card-meta">
              <span class="related-author">{{ article.author_name }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="search-tips">
        <h3>💡 搜索技巧</h3>
        <ul>
          <li>使用具体的关键词可以获得更准确的结果</li>
          <li>搜索支持标题、内容和摘要</li>
          <li>如果找不到相关文章，尝试使用同义词</li>
          <li>搜索不区分大小写</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.search-page {
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.search-header {
  margin-bottom: 2rem;
}

.search-header h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.search-info {
  color: #666;
  font-size: 1.1rem;
}

.search-info strong {
  color: #667eea;
  font-weight: bold;
}

.result-count {
  margin-left: 1rem;
  padding-left: 1rem;
  border-left: 2px solid #667eea;
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

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h2 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #666;
  margin-bottom: 1.5rem;
}

.btn-back {
  padding: 0.8rem 2rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
}

.btn-back:hover {
  background: #5568d3;
}

.search-results {
  display: grid;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.search-result-item {
  display: flex;
  gap: 1.5rem;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.search-result-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.result-cover {
  width: 200px;
  height: 150px;
  flex-shrink: 0;
  overflow: hidden;
  border-radius: 4px;
}

.result-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.result-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.result-title {
  font-size: 1.3rem;
  color: #333;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.result-title mark {
  background: #fff3cd;
  color: #856404;
  padding: 0 2px;
  border-radius: 2px;
}

.result-summary {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.result-summary mark {
  background: #fff3cd;
  color: #856404;
  padding: 0 2px;
  border-radius: 2px;
}

.result-meta {
  display: flex;
  gap: 1.5rem;
  color: #999;
  font-size: 0.9rem;
}

.related-section {
  margin: 3rem 0;
}

.related-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.related-title {
  font-size: 1.4rem;
  color: #333;
  font-weight: 600;
}

.related-line {
  flex: 1;
  height: 3px;
  background: linear-gradient(90deg, #667eea, #f093fb);
  border-radius: 2px;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.related-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  border: 1px solid #e9ecef;
}

.related-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  border-color: #667eea;
}

.related-card-title {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 0.8rem;
  line-height: 1.4;
  font-weight: 600;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.related-card-summary {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.related-card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #999;
  font-size: 0.85rem;
}

.related-author {
  padding: 0.2rem 0.6rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.related-views {
  font-weight: 500;
}

.search-tips {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.search-tips h3 {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 1rem;
}

.search-tips ul {
  list-style: none;
  padding: 0;
}

.search-tips li {
  padding: 0.5rem 0;
  color: #666;
  position: relative;
  padding-left: 1.5rem;
}

.search-tips li::before {
  content: '•';
  position: absolute;
  left: 0.5rem;
  color: #667eea;
  font-weight: bold;
}

@media (max-width: 768px) {
  .search-result-item {
    flex-direction: column;
  }
  
  .result-cover {
    width: 100%;
    height: 200px;
  }
  
  .result-meta {
    flex-wrap: wrap;
    gap: 1rem;
  }
}
</style>