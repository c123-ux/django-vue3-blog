<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { createArticle, uploadImage, getCategories, getTags, getSeries } from '@/api/article'

const router = useRouter()

const form = ref({
  title: '',
  content: '',
  nickname: '',
  category_id: null,
  tag_ids: [],
  series_id: null,
  summary: '',
  cover: ''
})

const categories = ref([])
const tags = ref([])
const series = ref([])
const loading = ref(false)
const uploading = ref(false)
const success = ref(false)
const coverImageInput = ref(null)
const contentImageInput = ref(null)
const tagInput = ref('')

const loadOptions = async () => {
  try {
    const [catRes, tagRes, seriesRes] = await Promise.all([
      getCategories(), 
      getTags(),
      getSeries()
    ])
    categories.value = catRes.data
    tags.value = tagRes.data
    series.value = seriesRes.data
  } catch (error) {
    console.error('Failed to load options:', error)
  }
}

// 保存文章
const saveArticle = async () => {
  if (!form.value.title.trim()) {
    alert('请输入文章标题')
    return
  }
  if (!form.value.content.trim()) {
    alert('请输入文章内容')
    return
  }
  
  loading.value = true
  try {
    const articleData = {
      ...form.value
    }
    // 如果没有输入昵称，留空让后端使用默认值
    if (!articleData.nickname.trim()) {
      delete articleData.nickname
    }
    // 如果没有输入摘要，留空
    if (!articleData.summary.trim()) {
      delete articleData.summary
    }
    
    const response = await createArticle(articleData)
    success.value = true
    setTimeout(() => {
      router.push('/')
    }, 2000)
  } catch (error) {
    console.error('Failed to save article:', error)
    alert('发布失败：' + (error.response?.data?.detail || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 处理封面图片上传
const handleCoverUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  if (!file.type.startsWith('image/')) {
    alert('请选择图片文件')
    return
  }
  
  if (file.size > 5 * 1024 * 1024) {
    alert('图片大小不能超过 5MB')
    return
  }
  
  uploading.value = true
  try {
    const response = await uploadImage(file)
    form.value.cover = response.data.url
    alert('封面上传成功！')
  } catch (error) {
    console.error('Failed to upload cover:', error)
    alert('封面上传失败')
  } finally {
    uploading.value = false
  }
}

// 处理内容中图片上传
const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  if (!file.type.startsWith('image/')) {
    alert('请选择图片文件')
    return
  }
  
  if (file.size > 5 * 1024 * 1024) {
    alert('图片大小不能超过 5MB')
    return
  }
  
  uploading.value = true
  try {
    const response = await uploadImage(file)
    const imageUrl = response.data.url
    
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
    alert('图片上传失败')
  } finally {
    uploading.value = false
    event.target.value = ''
  }
}

const insertAtCursor = (before, after = '') => {
  const textarea = document.getElementById('content')
  const startPos = textarea.selectionStart
  const endPos = textarea.selectionEnd
  const selectedText = form.value.content.substring(startPos, endPos)
  
  form.value.content = 
    form.value.content.substring(0, startPos) +
    before + selectedText + after +
    form.value.content.substring(endPos)
  
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
const insertImageBtn = () => {
  if (contentImageInput.value) {
    contentImageInput.value.click()
  }
}

// 处理标签输入
const handleTagInput = (event) => {
  const value = event.target.value
  // 检测中英文逗号
  if (value.includes(',') || value.includes('，')) {
    // 按中英文逗号分割
    const tagNames = value.split(/[,，]/).map(t => t.trim()).filter(t => t)
    if (tagNames.length > 0) {
      // 获取最后一个标签名（用户可能还在输入）
      const lastTag = tagNames[tagNames.length - 1]
      const previousTags = tagNames.slice(0, -1)
      
      // 处理之前的标签
      previousTags.forEach(tagName => {
        addTagByName(tagName)
      })
      
      // 保留最后一个标签在输入框中
      tagInput.value = lastTag
    }
  }
}

// 通过名称添加标签（如果不存在则创建）
const addTagByName = (tagName) => {
  // 查找现有标签
  const existingTag = tags.value.find(t => t.name.toLowerCase() === tagName.toLowerCase())
  if (existingTag) {
    // 如果标签已存在且未被选中，则选中它
    if (!form.value.tag_ids.includes(existingTag.id)) {
      form.value.tag_ids.push(existingTag.id)
    }
  } else {
    // 如果标签不存在，创建一个临时标签对象
    const newTag = {
      id: 'new_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
      name: tagName,
      slug: tagName.toLowerCase().replace(/\s+/g, '-'),
      is_new: true
    }
    tags.value.push(newTag)
    form.value.tag_ids.push(newTag.id)
  }
}

// 获取标签名称
const getTagName = (tagId) => {
  const tag = tags.value.find(t => t.id === tagId)
  return tag ? tag.name : ''
}

// 移除标签
const removeTag = (tagId) => {
  const index = form.value.tag_ids.indexOf(tagId)
  if (index > -1) {
    form.value.tag_ids.splice(index, 1)
  }
}

// 处理输入框失去焦点
const handleTagBlur = () => {
  if (tagInput.value.trim()) {
    addTagByName(tagInput.value.trim())
    tagInput.value = ''
  }
}

// 处理回车键
const handleTagEnter = (event) => {
  if (event.key === 'Enter') {
    event.preventDefault()
    if (tagInput.value.trim()) {
      addTagByName(tagInput.value.trim())
      tagInput.value = ''
    }
  }
}

onMounted(() => {
  loadOptions()
})
</script>

<template>
  <div class="guest-editor">
    <div class="container">
      <div v-if="success" class="success-message">
        <h1>🎉 发布成功！</h1>
        <p>文章已成功发布，即将跳转到首页...</p>
      </div>
      
      <div v-else>
        <h1 class="page-title">📝 发布文章</h1>
        <p class="page-desc">任何人都可以在这里发布文章，可以选择匿名或填写昵称</p>
        
        <form @submit.prevent="saveArticle" class="editor-form">
          <div class="form-section">
            <h3 class="section-title">基本信息</h3>
            
            <div class="form-group">
              <label for="nickname">你的昵称（可选）</label>
              <input
                id="nickname"
                v-model="form.nickname"
                type="text"
                placeholder="匿名用户"
              />
              <span class="hint">不填写则显示为「匿名用户」</span>
            </div>
            
            <div class="form-group">
              <label for="title">文章标题 *</label>
              <input
                id="title"
                v-model="form.title"
                type="text"
                placeholder="请输入文章标题"
                required
              />
            </div>
            
            <div class="form-group">
              <label>封面图片（可选）</label>
              <div class="cover-upload">
                <input
                  type="file"
                  ref="coverImageInput"
                  @change="handleCoverUpload"
                  accept="image/*"
                  style="display: none"
                />
                <div v-if="form.cover" class="cover-preview">
                  <img :src="form.cover" alt="封面预览" />
                  <button type="button" @click="form.cover = ''" class="remove-cover">
                    移除封面
                  </button>
                </div>
                <button 
                  v-else 
                  type="button" 
                  @click="coverImageInput?.click()" 
                  class="upload-btn"
                >
                  🖼️ 上传封面图片
                </button>
              </div>
            </div>
            
            <div class="form-group">
              <label for="summary">文章摘要（可选）</label>
              <textarea
                id="summary"
                v-model="form.summary"
                placeholder="简单描述一下这篇文章..."
                rows="3"
              ></textarea>
            </div>
          </div>
          
          <div class="form-section">
            <h3 class="section-title">文章内容</h3>
            
            <div class="form-group">
              <label for="content">正文（支持 Markdown）*</label>
              <div class="toolbar">
                <button type="button" @click="insertBold" class="toolbar-btn" title="加粗文字：选中文字后点击，或直接点击输入">
                  <strong>B</strong>
                </button>
                <button type="button" @click="insertItalic" class="toolbar-btn" title="斜体文字：选中文字后点击，或直接点击输入">
                  <em>I</em>
                </button>
                <button type="button" @click="insertHeading" class="toolbar-btn" title="插入标题：在行首添加 ## 创建二级标题">
                  H
                </button>
                <button type="button" @click="insertLink" class="toolbar-btn" title="添加链接：点击后输入网址，格式为 [文字](网址)">
                  🔗
                </button>
                <button type="button" @click="insertCode" class="toolbar-btn" title="插入代码：单行用反引号，多行用三个反引号包裹">
                  &lt;/&gt;
                </button>
                <button type="button" @click="insertImageBtn" class="toolbar-btn" title="上传图片：选择本地图片文件（支持JPG、PNG等，最大5MB）">
                  🖼️
                </button>
                <input
                  type="file"
                  ref="contentImageInput"
                  @change="handleImageUpload"
                  accept="image/*"
                  style="display: none"
                />
              </div>
              <textarea
                id="content"
                v-model="form.content"
                placeholder="# 开始写作...&#10;&#10;支持 Markdown 语法，用 # 表示标题，用 ** 表示加粗"
                rows="12"
                required
              ></textarea>
            </div>
          </div>
          
          <div class="form-section">
            <h3 class="section-title">分类和标签</h3>
            
            <div class="form-row">
              <div class="form-group">
                <label for="category">分类</label>
                <select id="category" v-model="form.category_id">
                  <option :value="null">未分类</option>
                  <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                    {{ cat.icon }} {{ cat.name }}
                  </option>
                  <option value="other">其他</option>
                </select>
              </div>
              <div class="form-group">
                <label for="series">专题</label>
                <select id="series" v-model="form.series_id">
                  <option :value="null">不加入专题</option>
                  <option v-for="s in series" :key="s.id" :value="s.id">
                    {{ s.title }}
                  </option>
                  <option value="other">其他</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label>标签（可选）</label>
              <input
                type="text"
                v-model="tagInput"
                @input="handleTagInput"
                @blur="handleTagBlur"
                @keydown="handleTagEnter"
                class="tag-input"
              />
              <div v-if="form.tag_ids.length > 0" class="tag-preview">
                <span v-for="tagId in form.tag_ids" :key="tagId" class="tag-preview-item">
                  {{ getTagName(tagId) }}
                  <button type="button" @click="removeTag(tagId)" class="tag-remove">×</button>
                </span>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="router.back()" class="btn-cancel">
              取消
            </button>
            <button type="submit" :disabled="loading" class="btn-submit">
              {{ loading ? '发布中...' : '立即发布' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.guest-editor {
  padding: 2rem 0;
  min-height: 100vh;
  background: linear-gradient(135deg, #FFF9F0 0%, #FFE8D6 100%);
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.page-title {
  font-size: 2rem;
  color: #2C3E50;
  margin-bottom: 0.5rem;
  text-align: center;
}

.page-desc {
  text-align: center;
  color: #5D6D7E;
  margin-bottom: 2rem;
}

.success-message {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(255, 140, 66, 0.15);
}

.success-message h1 {
  font-size: 2rem;
  color: #FF8C42;
  margin-bottom: 1rem;
}

.success-message p {
  color: #5D6D7E;
  font-size: 1.1rem;
}

.editor-form {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(255, 140, 66, 0.1);
}

.form-section {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
}

.form-section:last-of-type {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section-title {
  font-size: 1.2rem;
  color: #2C3E50;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #FF8C42;
  display: inline-block;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2C3E50;
  font-weight: 600;
  font-size: 0.95rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #FFE8D6;
  border-radius: 12px;
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.3s;
  box-sizing: border-box;
  background: #FFF9F0;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #FF8C42;
  box-shadow: 0 0 0 3px rgba(255, 140, 66, 0.15);
  background: white;
}

.form-group textarea {
  resize: vertical;
  font-family: 'Courier New', monospace;
  line-height: 1.6;
}

.hint {
  display: block;
  margin-top: 0.3rem;
  font-size: 0.85rem;
  color: #888;
}

.cover-upload {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cover-preview {
  position: relative;
  display: inline-block;
}

.cover-preview img {
  max-width: 100%;
  max-height: 200px;
  border-radius: 8px;
  border: 2px solid #e0e0e0;
}

.remove-cover {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: rgba(255, 0, 0, 0.9);
  color: white;
  border: none;
  padding: 0.3rem 0.8rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
}

.upload-btn {
  padding: 1rem;
  background: #FFF5E6;
  border: 2px dashed #FFB347;
  border-radius: 12px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.upload-btn:hover {
  border-color: #FF8C42;
  background: #FFE8D6;
  color: #FF8C42;
}

.toolbar {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  padding: 0.75rem;
  background: #FFF5E6;
  border-radius: 12px;
  flex-wrap: wrap;
}

.toolbar-btn {
  padding: 0.5rem 0.9rem;
  border: 1px solid #FFE8D6;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.toolbar-btn:hover {
  background: #FF8C42;
  color: white;
  border-color: #FF8C42;
  transform: translateY(-1px);
}

.tag-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.tag-checkbox {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  background: #f5f7fa;
  border-radius: 20px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.tag-checkbox:hover {
  background: #e8ecf5;
}

.tag-checkbox:has(input:checked) {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.tag-checkbox input {
  cursor: pointer;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.btn-cancel {
  padding: 0.9rem 2rem;
  border: 2px solid #FFE8D6;
  background: white;
  color: #5D6D7E;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1rem;
  font-weight: 500;
}

.btn-cancel:hover {
  border-color: #FFB347;
  color: #FF8C42;
  background: #FFF5E6;
}

.btn-submit {
  padding: 0.9rem 2.5rem;
  background: linear-gradient(135deg, #FF8C42 0%, #FFB347 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(255, 140, 66, 0.3);
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 140, 66, 0.4);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.tag-input {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s;
  box-sizing: border-box;
  background: white;
}

.tag-input:focus {
  outline: none;
  border-color: #FF8C42;
  box-shadow: 0 0 0 3px rgba(255, 140, 66, 0.15);
}

.tag-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding: 0.5rem;
  background: #FFF5E6;
  border-radius: 8px;
  min-height: 2.5rem;
}

.tag-preview:empty {
  display: none;
}

.tag-preview-item {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.3rem 0.8rem;
  background: linear-gradient(135deg, #FF8C42 0%, #FFB347 100%);
  color: white;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
  animation: tagAppear 0.3s ease;
}

@keyframes tagAppear {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.tag-remove {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1.1rem;
  line-height: 1;
  padding: 0;
  margin-left: 0.2rem;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.tag-remove:hover {
  opacity: 1;
  transform: scale(1.2);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .guest-editor {
    padding: 1rem 0;
  }
  
  .container {
    padding: 0 1rem;
  }
  
  .page-title {
    font-size: 1.6rem;
  }
  
  .editor-form {
    padding: 1.5rem 1rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column-reverse;
  }
  
  .btn-cancel,
  .btn-submit {
    width: 100%;
    padding: 1rem;
  }
  
  .toolbar {
    gap: 0.3rem;
  }
  
  .toolbar-btn {
    padding: 0.4rem 0.6rem;
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 1.4rem;
  }
  
  .editor-form {
    padding: 1rem;
    border-radius: 8px;
  }
  
  .section-title {
    font-size: 1.1rem;
  }
  
  .tag-selector {
    gap: 0.5rem;
  }
  
  .tag-checkbox {
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
  }
}
</style>
