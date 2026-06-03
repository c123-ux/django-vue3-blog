<script setup>
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getArticle, getArticles } from '@/api/article'
import { getComments, createComment, deleteComment } from '@/api/comment'
import { useSeo } from '@/composables/useSeo'
import { useCommentWebSocket } from '@/composables/useCommentWebSocket'

const route = useRoute()
const router = useRouter()
const { setSeo } = useSeo()

const article = ref(null)
const comments = ref([])
const relatedArticles = ref([])
const allArticles = ref([])
const loading = ref(true)
const newComment = ref('')
const newNickname = ref('')
const replyingTo = ref(null)
const showTableOfContents = ref(false)
const tableOfContents = ref([])
const wsStatus = ref('disconnected')
const activeHeading = ref('')
const copied = ref(false)
const articleUrl = ref('')

const { connected, typingUsers, connect, sendComment: wsSendComment, sendTyping } = useCommentWebSocket(
  () => route.params.id,
  {
    onNewComment: () => loadComments(),
    onDeleteComment: () => loadComments(),
    onError: (msg) => console.warn('WS:', msg),
  }
)

watch(connected, (v) => { wsStatus.value = v ? 'connected' : 'disconnected' })

const currentIndex = computed(() => {
  if (!article.value || !allArticles.value.length) return -1
  return allArticles.value.findIndex(a => a.id === article.value.id)
})

const prevArticle = computed(() => {
  if (currentIndex.value <= 0) return null
  return allArticles.value[currentIndex.value - 1]
})

const nextArticle = computed(() => {
  if (currentIndex.value < 0 || currentIndex.value >= allArticles.value.length - 1) return null
  return allArticles.value[currentIndex.value + 1]
})

const loadArticle = async () => {
  try {
    const response = await getArticle(route.params.id)
    article.value = response.data
    articleUrl.value = window.location.href
    
    const content = article.value.content_html || ''
    const headings = content.match(/<h[1-6][^>]*>.*?<\/h[1-6]>/g) || []
    tableOfContents.value = headings.map((heading, index) => {
      const level = parseInt(heading.match(/<h([1-6])/)[1])
      const text = heading.replace(/<[^>]+>/g, '')
      const id = `heading-${index}`
      return { level, text, id }
    })
    
    if (headings.length > 3) {
      showTableOfContents.value = true
    }

    setSeo({
      title: `${article.value.title} - 技术博客`,
      description: article.value.summary,
      type: 'article',
    })
  } catch (error) {
    console.error('Failed to load article:', error)
  }
}

const loadComments = async () => {
  try {
    const response = await getComments(route.params.id)
    comments.value = response.data
  } catch (error) {
    console.error('Failed to load comments:', error)
  }
}

const loadRelatedArticles = async () => {
  try {
    const response = await getArticles({ page: 1 })
    allArticles.value = response.data.results.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    relatedArticles.value = allArticles.value
      .filter(a => a.id !== article.value?.id)
      .slice(0, 4)
  } catch (error) {
    console.error('Failed to load related articles:', error)
  }
}

const totalComments = computed(() => {
  let count = comments.value.length
  comments.value.forEach(c => {
    count += (c.replies || []).length
  })
  return count
})

const submitComment = async () => {
  if (!newComment.value.trim()) return

  const parentId = replyingTo.value?.id || null
  const nickname = newNickname.value.trim() || '匿名用户'

  if (connected.value && wsSendComment(newComment.value.trim(), parentId)) {
    newComment.value = ''
    replyingTo.value = null
    return
  }
  
  try {
    await createComment({
      article: article.value.id,
      content: newComment.value.trim(),
      nickname: nickname,
      parent: parentId,
    })
    newComment.value = ''
    replyingTo.value = null
    await loadComments()
  } catch (error) {
    console.error('Failed to create comment:', error)
    alert('发表评论失败')
  }
}

const onCommentInput = () => {
  if (connected.value) sendTyping(true)
}

const startReply = (comment) => {
  replyingTo.value = comment
}

const cancelReply = () => {
  replyingTo.value = null
}

const handleDeleteComment = async (commentId) => {
  if (!confirm('确定要删除这条评论吗？')) return
  try {
    await deleteComment(commentId)
    await loadComments()
  } catch (error) {
    console.error('Failed to delete comment:', error)
    alert('删除评论失败')
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const scrollToHeading = (id) => {
  const element = document.getElementById(id)
  if (element) {
    const yOffset = -80
    const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset
    window.scrollTo({ top: y, behavior: 'smooth' })
  }
}

const goToArticle = (id) => {
  router.push(`/article/${id}`)
}

const handleTocScroll = () => {
  const headings = tableOfContents.value
  for (let i = headings.length - 1; i >= 0; i--) {
    const el = document.getElementById(headings[i].id)
    if (el && el.getBoundingClientRect().top <= 120) {
      activeHeading.value = headings[i].id
      return
    }
  }
  if (headings.length) activeHeading.value = headings[0].id
}

const copyCode = async (button, code) => {
  try {
    await navigator.clipboard.writeText(code)
    button.textContent = '已复制'
    button.style.background = '#10b981'
    setTimeout(() => {
      button.textContent = '复制'
      button.style.background = ''
    }, 2000)
  } catch {
    button.textContent = '失败'
  }
}

const setupCodeBlocks = () => {
  nextTick(() => {
    document.querySelectorAll('.article-content pre').forEach((pre) => {
      if (pre.querySelector('.code-copy-btn')) return
      const code = pre.querySelector('code')
      if (!code) return
      const lang = code.className.replace(/^language-/, '') || 'code'
      const langBadge = document.createElement('div')
      langBadge.className = 'code-lang-badge'
      langBadge.textContent = lang
      pre.style.position = 'relative'
      pre.prepend(langBadge)
      const btn = document.createElement('button')
      btn.className = 'code-copy-btn'
      btn.textContent = '复制'
      btn.addEventListener('click', () => copyCode(btn, code.textContent))
      pre.appendChild(btn)
    })
  })
}

onMounted(async () => {
  loading.value = true
  await Promise.all([loadArticle(), loadComments()])
  if (article.value) {
    await loadRelatedArticles()
    setupCodeBlocks()
  }
  loading.value = false
  window.addEventListener('scroll', handleTocScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleTocScroll)
})
</script>

<template>
  <div class="article-detail">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="article" class="container">
      <div class="breadcrumb">
        <router-link to="/">首页</router-link>
        <span class="breadcrumb-sep">›</span>
        <router-link to="/articles">文章</router-link>
        <span class="breadcrumb-sep">›</span>
        <span class="breadcrumb-current">{{ article.title }}</span>
      </div>
      <div class="article-layout">
        <div class="article-main">
          <article class="article-card">
            <header class="article-header">
              <div class="article-tags">
                <span v-if="article.is_top" class="tag">置顶</span>
                <span v-if="article.category" class="tag">{{ article.category.name }}</span>
                <span v-for="tag in article.tags || []" :key="tag.id" class="tag tag-outline">{{ tag.name }}</span>
              </div>
              <h1 class="article-title">{{ article.title }}</h1>
              <div class="article-meta">
                <span class="meta-item">
                  <span class="icon">👤</span>
                  {{ article.author?.username || article.author_name || '匿名' }}
                </span>
                <span class="meta-item">
                  <span class="icon">📅</span>
                  {{ formatDate(article.created_at) }}
                </span>
                <span class="meta-item">
                  <span class="icon">💬</span>
                  {{ totalComments }} 评论
                </span>
              </div>
            </header>
            
            <div v-if="article.cover" class="article-cover">
              <img :src="article.cover" :alt="article.title" />
              <div class="cover-overlay"></div>
            </div>
            
            <div class="article-content" v-html="article.content_html"></div>
            
            <div class="article-footer">
            </div>
          </article>

          <section class="comments-section">
            <div class="section-header">
              <h2 class="section-title">💬 评论 ({{ totalComments }})</h2>
              <span v-if="connected" class="ws-badge" title="实时评论已连接">🟢 实时</span>
              <div class="section-line"></div>
            </div>
            
            <div class="comment-form">
              <div class="form-header">
                <span class="form-label">发表评论</span>
                <span class="form-tip">文明发言，友善交流</span>
              </div>
              <div v-if="replyingTo" class="replying-to">
                <span>回复 @{{ replyingTo.author_name }}</span>
                <button class="btn-cancel-reply" @click="cancelReply">✕</button>
              </div>
              <div class="nickname-row">
                <input
                  v-model="newNickname"
                  type="text"
                  placeholder="昵称（留空则匿名）"
                  class="nickname-input"
                  maxlength="50"
                />
              </div>
              <textarea
                v-model="newComment"
                :placeholder="replyingTo ? `回复 @${replyingTo.author_name}...` : '写下你的评论...'"
                rows="4"
                @input="onCommentInput"
              ></textarea>
              <p v-if="typingUsers.length" class="typing-hint">{{ typingUsers.join('、') }} 正在输入...</p>
              <div class="form-footer">
                <span class="char-count">{{ newComment.length }} 字</span>
                <button @click="submitComment()" class="btn-submit">
                  <span class="icon">✍️</span>
                  {{ replyingTo ? '回复' : '发表评论' }}
                </button>
              </div>
            </div>
            
            <div v-if="comments.length > 0" class="comments-list">
              <div v-for="comment in comments" :key="comment.id" class="comment-thread">
                <div class="comment-item">
                  <div class="comment-avatar">
                    <span>{{ comment.author_name?.charAt(0)?.toUpperCase() || 'U' }}</span>
                  </div>
                  <div class="comment-body">
                    <div class="comment-header">
                      <strong class="comment-author">{{ comment.author_name }}</strong>
                      <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                    </div>
                    <p class="comment-content">{{ comment.content }}</p>
                    <div class="comment-actions">
                      <button class="btn-reply" @click="startReply(comment)">回复</button>
                      <button class="btn-delete" @click="handleDeleteComment(comment.id)">删除</button>
                    </div>
                  </div>
                </div>

                <div v-if="comment.replies?.length" class="comment-replies">
                  <div v-for="reply in comment.replies" :key="reply.id" class="comment-item reply-item">
                    <div class="comment-avatar reply-avatar">
                      <span>{{ reply.author_name?.charAt(0)?.toUpperCase() || 'U' }}</span>
                    </div>
                    <div class="comment-body">
                      <div class="comment-header">
                        <strong class="comment-author">{{ reply.author_name }}</strong>
                        <span v-if="reply.parent_author" class="reply-indicator">回复 @{{ reply.parent_author }}</span>
                        <span class="comment-date">{{ formatDate(reply.created_at) }}</span>
                      </div>
                      <p class="comment-content">{{ reply.content }}</p>
                      <div class="comment-actions">
                        <button class="btn-reply" @click="startReply(reply)">回复</button>
                        <button class="btn-delete" @click="handleDeleteComment(reply.id)">删除</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="empty-comments">
              <div class="empty-icon">💭</div>
              <p>还没有评论，快来抢沙发吧！</p>
            </div>
          </section>
          
          <section class="article-nav">
            <div class="nav-links">
              <div v-if="prevArticle" class="nav-item prev" @click="router.push(`/article/${prevArticle.id}`)">
                <span class="nav-arrow">←</span>
                <div class="nav-info">
                  <span class="nav-label">上一篇</span>
                  <span class="nav-title">{{ prevArticle.title }}</span>
                </div>
              </div>
              <div v-else class="nav-item disabled">
                <span class="nav-arrow">←</span>
                <div class="nav-info">
                  <span class="nav-label">上一篇</span>
                  <span class="nav-title">没有了</span>
                </div>
              </div>
              <div v-if="nextArticle" class="nav-item next" @click="router.push(`/article/${nextArticle.id}`)">
                <div class="nav-info">
                  <span class="nav-label">下一篇</span>
                  <span class="nav-title">{{ nextArticle.title }}</span>
                </div>
                <span class="nav-arrow">→</span>
              </div>
              <div v-else class="nav-item disabled">
                <div class="nav-info">
                  <span class="nav-label">下一篇</span>
                  <span class="nav-title">没有了</span>
                </div>
                <span class="nav-arrow">→</span>
              </div>
            </div>
          </section>
          
          <section v-if="relatedArticles.length > 0" class="related-articles">
            <div class="section-header">
              <h2 class="section-title">📚 相关推荐</h2>
              <div class="section-line"></div>
            </div>
            <div class="related-grid">
              <div
                v-for="related in relatedArticles"
                :key="related.id"
                class="related-card"
                @click="goToArticle(related.id)"
              >
                <div v-if="related.cover" class="related-cover">
                  <img :src="related.cover" :alt="related.title" />
                </div>
                <div class="related-content">
                  <h3 class="related-title">{{ related.title }}</h3>
                  <div class="related-meta">
                    <span>💬 {{ related.comments_count || 0 }}</span>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
        
        <aside v-if="showTableOfContents" class="article-sidebar">
          <div class="toc-section">
            <h3 class="toc-title">📑 目录</h3>
            <ul class="toc-list">
              <li
                v-for="item in tableOfContents"
                :key="item.id"
                :class="[`toc-level-${item.level}`, { active: activeHeading === item.id }]"
                @click="scrollToHeading(item.id)"
              >
                {{ item.text }}
              </li>
            </ul>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<style scoped>
.article-detail {
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-muted-color);
  margin-bottom: 16px;
}

.breadcrumb a {
  color: var(--text-secondary-color);
  text-decoration: none;
  transition: color 0.25s;
}

.breadcrumb a:hover {
  color: var(--primary-color);
}

.breadcrumb-sep {
  color: var(--text-muted-color);
  font-size: 14px;
}

.breadcrumb-current {
  color: var(--text-color);
  font-weight: 500;
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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

.article-layout {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 2rem;
}

.article-main {
  min-width: 0;
}

.article-card {
  background: var(--surface-color);
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 2px 12px var(--shadow-color);
  border: 1px solid var(--border-color);
  margin-bottom: 2rem;
}

.article-header {
  margin-bottom: 2rem;
}

.article-tags {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tag {
  padding: 0.3rem 0.8rem;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.tag-outline {
  background: var(--background-color);
  color: var(--text-secondary-color);
  border: 1px solid var(--border-color);
}

.article-title {
  font-size: 2.5rem;
  color: #2C3E50;
  margin-bottom: 1rem;
  line-height: 1.3;
  font-weight: 700;
}

.article-meta {
  display: flex;
  gap: 2rem;
  color: #5D6D7E;
  font-size: 0.95rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.icon {
  font-size: 1.1rem;
}

.article-cover {
  margin-bottom: 2rem;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 4px 16px rgba(255, 140, 66, 0.15);
}

.article-cover img {
  width: 100%;
  max-height: 450px;
  object-fit: cover;
  transition: transform 0.5s;
}

.article-cover:hover img {
  transform: scale(1.02);
}

.cover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, transparent 0%, rgba(0, 0, 0, 0.2) 100%);
}

.article-content {
  line-height: 1.9;
  color: var(--text-color);
  font-size: 1.05rem;
}

.article-content :deep(h1),
.article-content :deep(h2),
.article-content :deep(h3),
.article-content :deep(h4),
.article-content :deep(h5),
.article-content :deep(h6) {
  margin-top: 2rem;
  margin-bottom: 1rem;
  color: var(--text-color);
  font-weight: 600;
  line-height: 1.4;
}

.article-content :deep(h1) { font-size: 2rem; }
.article-content :deep(h2) { font-size: 1.75rem; }
.article-content :deep(h3) { font-size: 1.5rem; }
.article-content :deep(h4) { font-size: 1.25rem; }

.article-content :deep(p) {
  margin-bottom: 1.2rem;
}

.article-content :deep(code) {
  background: var(--background-color);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  border: 1px solid var(--border-color);
}

.article-content :deep(pre code) {
  background: none;
  padding: 0;
  border: none;
}

.article-content :deep(blockquote) {
  border-left: 4px solid var(--primary-color);
  padding-left: 1.5rem;
  margin: 1.5rem 0;
  color: var(--text-secondary-color);
  font-style: italic;
}

.article-content :deep(ul),
.article-content :deep(ol) {
  margin: 1rem 0;
  padding-left: 2rem;
}

.article-content :deep(li) {
  margin-bottom: 0.5rem;
}

.article-content :deep(a) {
  color: var(--primary-color);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.3s;
}

.article-content :deep(a:hover) {
  border-bottom-color: var(--primary-color);
}

.article-content :deep(img) {
  max-width: 100%;
  border-radius: 8px;
  margin: 1.5rem 0;
}

.article-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
}

.article-content :deep(th),
.article-content :deep(td) {
  border: 1px solid var(--border-color);
  padding: 0.8rem;
  text-align: left;
}

.article-content :deep(th) {
  background: var(--background-color);
  font-weight: 600;
}

.article-footer {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border-color);
}

.section-header {
  margin-bottom: 2rem;
  position: relative;
}

.ws-badge {
  position: absolute;
  right: 0;
  top: 0;
  font-size: 0.8rem;
  color: #22c55e;
}

.typing-hint {
  font-size: 0.85rem;
  color: var(--text-secondary-color);
  margin: -0.5rem 0 0.5rem;
  font-style: italic;
}

.section-title {
  font-size: 1.5rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.section-line {
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  border-radius: 2px;
}

.comments-section {
  background: var(--surface-color);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 12px var(--shadow-color);
  border: 1px solid var(--border-color);
  margin-bottom: 2rem;
}

.comment-form {
  margin-bottom: 2rem;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.form-label {
  font-weight: 600;
  color: var(--text-color);
}

.form-tip {
  color: var(--text-secondary-color);
  font-size: 0.9rem;
}

.comment-form textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  font-size: 1rem;
  resize: vertical;
  margin-bottom: 1rem;
  background: var(--background-color);
  color: var(--text-color);
  transition: border-color 0.3s;
}

.nickname-row {
  margin-bottom: 0.75rem;
}

.nickname-input {
  width: 100%;
  max-width: 300px;
  padding: 0.6rem 1rem;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  font-size: 0.95rem;
  background: var(--background-color);
  color: var(--text-color);
  transition: border-color 0.3s;
  outline: none;
}

.nickname-input:focus {
  border-color: var(--primary-color);
}

.comment-form textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.char-count {
  color: var(--text-secondary-color);
  font-size: 0.9rem;
}

.btn-submit {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--shadow-color);
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.comment-thread {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.comment-item {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: var(--background-color);
  border-radius: 8px;
  transition: all 0.3s;
}

.comment-replies {
  margin-left: 3rem;
  padding-left: 1rem;
  border-left: 2px solid var(--border-color);
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.reply-item {
  padding: 1rem 1.25rem;
}

.reply-avatar {
  width: 36px;
  height: 36px;
  font-size: 1rem;
}

.reply-indicator {
  color: var(--primary-color);
  font-size: 0.85rem;
  font-weight: 500;
}

.replying-to {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.6rem 1rem;
  margin-bottom: 0.75rem;
  background: var(--background-color);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 0.9rem;
  color: var(--primary-color);
}

.btn-cancel-reply {
  background: none;
  border: none;
  color: var(--text-secondary-color);
  cursor: pointer;
  font-size: 1rem;
  padding: 0 0.25rem;
  line-height: 1;
  transition: color 0.2s;
}

.btn-cancel-reply:hover {
  color: var(--text-color);
}

.btn-reply {
  background: none;
  border: none;
  color: var(--text-secondary-color);
  cursor: pointer;
  font-size: 0.85rem;
  padding: 2px 8px;
  border-radius: 4px;
  transition: all 0.2s;
}

.btn-reply:hover {
  color: var(--primary-color);
  background: var(--tag-bg);
}

.btn-delete {
  background: none;
  border: none;
  color: var(--text-secondary-color);
  cursor: pointer;
  font-size: 0.85rem;
  padding: 2px 8px;
  border-radius: 4px;
  transition: all 0.2s;
  margin-left: 4px;
}

.btn-delete:hover {
  color: #e74c3c;
  background: #fff5f5;
}

.comment-actions {
  display: flex;
  gap: 2px;
  margin-top: 4px;
}

.comment-item:hover {
  box-shadow: 0 2px 8px var(--shadow-color);
}

.comment-avatar {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.comment-body {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.comment-author {
  color: var(--text-color);
  font-size: 1rem;
}

.comment-date {
  color: var(--text-secondary-color);
  font-size: 0.9rem;
}

.comment-content {
  color: var(--text-color);
  line-height: 1.6;
  margin: 0;
}

.empty-comments {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary-color);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.article-nav {
  background: var(--surface-color);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px var(--shadow-color);
  border: 1px solid var(--border-color);
  margin-bottom: 2rem;
}

.nav-links {
  display: flex;
  justify-content: space-between;
  gap: 2rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  cursor: pointer;
  padding: 1rem;
  border-radius: 8px;
  transition: all 0.3s;
  flex: 1;
}

.nav-item:hover:not(.disabled) {
  background: var(--background-color);
  transform: translateY(-2px);
}

.nav-item.disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.nav-item.prev {
  justify-content: flex-start;
}

.nav-item.next {
  justify-content: flex-end;
}

.nav-arrow {
  font-size: 1.5rem;
  color: var(--primary-color);
  font-weight: bold;
}

.nav-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.nav-label {
  font-size: 0.85rem;
  color: var(--text-secondary-color);
}

.nav-title {
  font-size: 1rem;
  color: var(--text-color);
  font-weight: 500;
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.related-articles {
  background: var(--surface-color);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 12px var(--shadow-color);
  border: 1px solid var(--border-color);
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.related-card {
  cursor: pointer;
  transition: all 0.3s;
  border-radius: 8px;
  overflow: hidden;
  background: var(--background-color);
}

.related-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px var(--shadow-color);
}

.related-cover {
  height: 150px;
  overflow: hidden;
}

.related-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.related-card:hover .related-cover img {
  transform: scale(1.05);
}

.related-content {
  padding: 1rem;
}

.related-title {
  font-size: 1rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.related-meta {
  display: flex;
  gap: 1rem;
  color: var(--text-secondary-color);
  font-size: 0.85rem;
}

.article-sidebar {
  position: sticky;
  top: 100px;
  height: fit-content;
}

.toc-section {
  background: var(--surface-color);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px var(--shadow-color);
  border: 1px solid var(--border-color);
}

.toc-title {
  font-size: 1.1rem;
  color: var(--text-color);
  margin-bottom: 1rem;
  font-weight: 600;
}

.toc-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.toc-list li {
  padding: 0.5rem 0;
  color: var(--text-secondary-color);
  cursor: pointer;
  transition: all 0.3s;
  border-left: 2px solid transparent;
  padding-left: 1rem;
}

.toc-list li:hover {
  color: var(--primary-color);
  border-left-color: var(--primary-color);
  padding-left: 1.5rem;
}

.toc-list li.active {
  color: #10b981;
  border-left-color: #10b981;
  font-weight: 600;
}

.article-content :deep(pre) {
  background: var(--background-color);
  padding: 16px;
  padding-top: 36px;
  border-radius: 8px;
  overflow-x: auto;
  border: 1px solid var(--border-color);
  margin: 16px 0;
  position: relative;
}

.article-content :deep(pre .code-lang-badge) {
  position: absolute;
  top: 0;
  left: 0;
  padding: 4px 12px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted-color);
  background: var(--border-color);
  border-radius: 8px 0 8px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.article-content :deep(pre .code-copy-btn) {
  position: absolute;
  top: 4px;
  right: 4px;
  padding: 3px 10px;
  font-size: 11px;
  color: var(--text-muted-color);
  background: var(--border-color);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.25s ease, background 0.25s ease;
}

.article-content :deep(pre:hover .code-copy-btn) {
  opacity: 1;
}

.toc-level-1 {
  font-weight: 600;
  font-size: 1rem;
}

.toc-level-2 {
  padding-left: 1.5rem;
  font-size: 0.95rem;
}

.toc-level-3 {
  padding-left: 2.5rem;
  font-size: 0.9rem;
}

@media (max-width: 1024px) {
  .article-layout {
    grid-template-columns: 1fr;
  }
  
  .article-sidebar {
    display: none;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
  
  .article-card {
    padding: 1.5rem;
  }
  
  .article-title {
    font-size: 1.8rem;
  }
  
  .article-meta {
    gap: 1rem;
  }
  
  .related-grid {
    grid-template-columns: 1fr;
  }
}
</style>