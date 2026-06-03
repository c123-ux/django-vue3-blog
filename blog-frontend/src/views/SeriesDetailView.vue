<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getSeriesDetail } from '@/api/article'

const route = useRoute()
const router = useRouter()
const series = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await getSeriesDetail(route.params.slug)
    series.value = res.data
  } catch (e) {
    console.error('Failed to load series:', e)
  } finally {
    loading.value = false
  }
})

const goToArticle = (id) => {
  router.push(`/article/${id}`)
}
</script>

<template>
  <div class="series-detail-page">
    <div class="container">
      <div v-if="loading" class="loading">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <div v-else-if="!series" class="empty-state">
        <div class="empty-icon">📚</div>
        <h2>专题不存在</h2>
        <router-link to="/series" class="back-link">返回专题列表</router-link>
      </div>

      <template v-else>
        <div class="series-header">
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
            <h1 class="series-title">{{ series.title }}</h1>
            <p class="series-desc">{{ series.description }}</p>
            <div class="series-meta">
              <span class="meta-item">📄 {{ series.article_count }} 篇文章</span>
            </div>
            <router-link to="/series" class="back-link">← 返回专题列表</router-link>
          </div>
        </div>

        <div class="article-list">
          <div
            v-for="article in series.articles"
            :key="article.id"
            class="article-card"
            @click="goToArticle(article.id)"
          >
            <div v-if="article.cover" class="article-cover">
              <img :src="article.cover" :alt="article.title" />
            </div>
            <div class="article-body">
              <div class="article-header">
                <h2 class="article-title">{{ article.title }}</h2>
                <span class="article-category" v-if="article.category_name">{{ article.category_name }}</span>
              </div>
              <p class="article-summary">{{ article.summary }}</p>
              <div class="article-footer">
                <div class="article-meta">
                  <span class="meta-item">👤 {{ article.author_name }}</span>
                  <span class="meta-item">📅 {{ new Date(article.created_at).toLocaleDateString('zh-CN') }}</span>
                  <span class="meta-item">💬 {{ article.comments_count }}</span>
                  <span class="meta-item">⏱️ {{ article.reading_time }} 分钟</span>
                </div>
                <div class="article-tags" v-if="article.tags?.length">
                  <span class="tag" v-for="tag in article.tags" :key="tag.id">{{ tag.name }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.series-detail-page {
  padding: 2rem 0;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
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
  padding: 4rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.series-header {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  padding: 2rem;
  background: var(--surface-color);
  border-radius: 12px;
  box-shadow: 0 2px 8px var(--shadow-color);
}

.series-cover {
  width: 120px;
  height: 120px;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.8);
}

.series-info {
  flex: 1;
}

.series-title {
  font-size: 1.5rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

.series-desc {
  color: var(--text-secondary-color);
  line-height: 1.6;
  margin-bottom: 1rem;
}

.series-meta {
  margin-bottom: 1rem;
}

.meta-item {
  font-size: 0.9rem;
  color: var(--text-secondary-color);
}

.back-link {
  color: var(--primary-color);
  text-decoration: none;
  font-size: 0.9rem;
}

.back-link:hover {
  text-decoration: underline;
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.article-card {
  background: var(--surface-color);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px var(--shadow-color);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
}

.article-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px var(--shadow-color);
}

.article-cover {
  width: 200px;
  min-height: 160px;
  flex-shrink: 0;
  overflow: hidden;
}

.article-cover img {
  width: 100%;
  height: 100%;
  min-height: 160px;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.article-card:hover .article-cover img {
  transform: scale(1.08);
}

.article-body {
  flex: 1;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.article-title {
  font-size: 1.2rem;
  color: var(--text-color);
  font-weight: 600;
}

.article-category {
  font-size: 0.8rem;
  padding: 0.2rem 0.6rem;
  background: var(--primary-color);
  color: white;
  border-radius: 4px;
  white-space: nowrap;
}

.article-summary {
  color: var(--text-secondary-color);
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.article-meta {
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
}

.article-meta .meta-item {
  font-size: 0.8rem;
}

.article-tags {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.tag {
  font-size: 0.75rem;
  padding: 0.15rem 0.5rem;
  background: var(--background-color);
  color: var(--primary-color);
  border-radius: 4px;
}

@media (max-width: 768px) {
  .series-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .article-header {
    flex-direction: column;
  }

  .article-footer {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>