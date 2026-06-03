<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { createArticle, getArticle, updateArticle, uploadImage, getCategories, getTags } from '@/api/article'

const router = useRouter()
const route = useRoute()

const form = ref({
  title: '',
  content: '',
  status: 'draft',
  is_top: false,
  category_id: null,
  tag_ids: [],
})
const categories = ref([])
const tags = ref([])
const loading = ref(false)
const isEdit = ref(false)
const uploading = ref(false)

const loadOptions = async () => {
  try {
    const [catRes, tagRes] = await Promise.all([getCategories(), getTags()])
    categories.value = catRes.data
    tags.value = tagRes.data
  } catch (error) {
    console.error('Failed to load options:', error)
  }
}

// 加载文章（编辑模式）
const loadArticle = async () => {
  if (!route.params.id) return
  
  try {
    isEdit.value = true
    const response = await getArticle(route.params.id)
    const article = response.data
    form.value = {
      title: article.title,
      content: article.content,
      status: article.status,
      is_top: article.is_top || false,
      category_id: article.category?.id || null,
      tag_ids: (article.tags || []).map(t => t.id),
    }
  } catch (error) {
    console.error('Failed to load article:', error)
    alert('加载文章失败')
  }
}

// 保存文章
const saveArticle = async () => {
  if (!form.value.title.trim() || !form.value.content.trim()) {
    alert('标题和内容不能为空')
    return
  }
  
  loading.value = true
  try {
    if (isEdit.value) {
      await updateArticle(route.params.id, form.value)
      alert('更新成功！')
    } else {
      await createArticle(form.value)
      alert('创建成功！')
    }
    router.push('/')
  } catch (error) {
    console.error('Failed to save article:', error)
    alert('保存失败：' + (error.response?.data?.detail || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 处理图片上传
const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    alert('请选择图片文件')
    return
  }
  
  // 验证文件大小（5MB）
  if (file.size > 5 * 1024 * 1024) {
    alert('图片大小不能超过 5MB')
    return
  }
  
  uploading.value = true
  try {
    const response = await uploadImage(file)
    const imageUrl = response.data.url
    
    // 在光标位置插入图片 Markdown 语法
    const textarea = document.getElementById('content')
    const startPos = textarea.selectionStart
    const endPos = textarea.selectionEnd
    const imageMarkdown = `\n![图片](${imageUrl})\n`
    
    form.value.content = 
      form.value.content.substring(0, startPos) +
      imageMarkdown +
      form.value.content.substring(endPos)
    
    alert('图片上传成功！')
  } catch (error) {
    console.error('Failed to upload image:', error)
    alert('图片上传失败：' + (error.response?.data?.error || '未知错误'))
  } finally {
    uploading.value = false
    // 清空文件选择
    event.target.value = ''
  }
}

// 工具栏功能
const insertAtCursor = (before, after = '') => {
  const textarea = document.getElementById('content')
  const startPos = textarea.selectionStart
  const endPos = textarea.selectionEnd
  const selectedText = form.value.content.substring(startPos, endPos)
  
  form.value.content = 
    form.value.content.substring(0, startPos) +
    before + selectedText + after +
    form.value.content.substring(endPos)
  
  // 恢复光标位置
  setTimeout(() => {
    textarea.focus()
    textarea.setSelectionRange(startPos + before.length, endPos + before.length)
  }, 0)
}

const insertBold = () => insertAtCursor('**', '**')
const insertItalic = () => insertAtCursor('*', '*')
const insertHeading = () => insertAtCursor('## ', '')
const insertLink = () => {
  const url = prompt('请输入链接地址:')
  if (url) {
    insertAtCursor('[', `](${url})`)
  }
}
const insertCode = () => insertAtCursor('`', '`')
const insertImage = () => {
  const fileInput = document.querySelector('input[type="file"]')
  if (fileInput) {
    fileInput.click()
  }
}

onMounted(() => {
  loadOptions()
  loadArticle()
})
</script>

<template>
  <div class="editor">
    <div class="container">
      <h1 class="page-title">{{ isEdit ? '编辑文章' : '写文章' }}</h1>
      
      <form @submit.prevent="saveArticle" class="editor-form">
        <div class="form-group">
          <label for="title">标题</label>
          <input
            id="title"
            v-model="form.title"
            type="text"
            placeholder="请输入文章标题"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="content">内容（支持 Markdown）</label>
          <div class="toolbar">
            <button type="button" @click="insertBold" class="toolbar-btn" title="加粗">
              <strong>B</strong>
            </button>
            <button type="button" @click="insertItalic" class="toolbar-btn" title="斜体">
              <em>I</em>
            </button>
            <button type="button" @click="insertHeading" class="toolbar-btn" title="标题">
              H
            </button>
            <button type="button" @click="insertLink" class="toolbar-btn" title="链接">
              🔗
            </button>
            <button type="button" @click="insertCode" class="toolbar-btn" title="代码">
              &lt;/&gt;
            </button>
            <button type="button" @click="insertImage" class="toolbar-btn" title="上传图片">
              🖼️
            </button>
            <input
              type="file"
              ref="fileInput"
              @change="handleImageUpload"
              accept="image/*"
              style="display: none"
            />
          </div>
          <textarea
            id="content"
            v-model="form.content"
            placeholder="# 开始写作...&#10;&#10;支持 Markdown 语法"
            rows="20"
            required
          ></textarea>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="category">分类</label>
            <select id="category" v-model="form.category_id">
              <option :value="null">未分类</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label for="status">状态</label>
            <select id="status" v-model="form.status">
              <option value="draft">草稿</option>
              <option value="published">发布</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label>标签</label>
          <div class="tag-selector">
            <label v-for="tag in tags" :key="tag.id" class="tag-checkbox">
              <input type="checkbox" :value="tag.id" v-model="form.tag_ids" />
              {{ tag.name }}
            </label>
          </div>
        </div>

        <div class="form-group checkbox-group">
          <label>
            <input type="checkbox" v-model="form.is_top" />
            置顶文章
          </label>
        </div>
        
        <div class="form-actions">
          <button type="button" @click="router.back()" class="btn-cancel">
            取消
          </button>
          <button type="submit" :disabled="loading" class="btn-save">
            {{ loading ? '保存中...' : (isEdit ? '更新' : '发布') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.editor {
  padding: 2rem 0;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
}

.page-title {
  font-size: 2rem;
  color: #333;
  margin-bottom: 2rem;
}

.editor-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.tag-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.tag-checkbox {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.4rem 0.8rem;
  background: #f5f5f5;
  border-radius: 20px;
  font-size: 0.9rem;
  cursor: pointer;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.form-group textarea {
  resize: vertical;
  font-family: 'Courier New', monospace;
  line-height: 1.6;
}

.toolbar {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: #f5f5f5;
  border-radius: 6px;
}

.toolbar-btn {
  padding: 0.4rem 0.8rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.toolbar-btn:hover {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn-cancel {
  padding: 0.75rem 2rem;
  border: 2px solid #e0e0e0;
  background: white;
  color: #666;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-cancel:hover {
  border-color: #999;
  color: #333;
}

.btn-save {
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.3s;
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-2px);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
