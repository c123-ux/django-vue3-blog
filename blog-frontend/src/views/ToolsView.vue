<script setup>import { ref, computed } from 'vue';
const activeTool = ref('markdown');
const markdownInput = ref('# Hello World\n\nThis is a **markdown** editor.\n\n- List item 1\n- List item 2\n\n```python\nprint("Hello")\n```');
const jsonInput = ref('{"name": "John", "age": 30, "city": "New York"}');
const jsonError = ref('');
const urlInput = ref('');
const urlOutput = ref('');
const urlEncode = ref(true);
const base64Input = ref('');
const base64Output = ref('');
const base64Encode = ref(true);
const timestamp = ref('');
const dateOutput = ref('');
const passwordLength = ref(12);
const passwordIncludeUppercase = ref(true);
const passwordIncludeLowercase = ref(true);
const passwordIncludeNumbers = ref(true);
const passwordIncludeSymbols = ref(true);
const generatedPassword = ref('');
const tools = [
 { id: 'markdown', name: 'Markdown 编辑器', icon: '📝', category: '办公工具' },
 { id: 'json', name: 'JSON 格式化', icon: '📄', category: '开发工具' },
 { id: 'url', name: 'URL 编码/解码', icon: '🔗', category: '开发工具' },
 { id: 'base64', name: 'Base64 编码/解码', icon: '🔐', category: '开发工具' },
 { id: 'timestamp', name: '时间戳转换', icon: '⏰', category: '辅助工具' },
 { id: 'password', name: '密码生成器', icon: '🔑', category: '安全工具' },
];
const markdownPreview = computed(() => {
 let text = markdownInput.value;
 text = text.replace(/^### (.*$)/gim, '<h3>$1</h3>');
 text = text.replace(/^## (.*$)/gim, '<h2>$1</h2>');
 text = text.replace(/^# (.*$)/gim, '<h1>$1</h1>');
 text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
 text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
 text = text.replace(/^- (.*$)/gim, '<li>$1</li>');
 text = text.replace(/<\/li>\n<li>/g, '</li><li>');
 text = text.replace(/(<li>.*<\/li>)/gm, '<ul>$1</ul>');
 text = text.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
 text = text.replace(/^> (.*$)/gim, '<blockquote>$1</blockquote>');
 text = text.replace(/\n/g, '<br>');
 return text;
});
const formatJson = () => {
 try {
 const parsed = JSON.parse(jsonInput.value);
 jsonInput.value = JSON.stringify(parsed, null, 2);
 jsonError.value = '';
 }
 catch (e) {
 jsonError.value = 'JSON 格式错误: ' + e.message;
 }
};
const minifyJson = () => {
 try {
 const parsed = JSON.parse(jsonInput.value);
 jsonInput.value = JSON.stringify(parsed);
 jsonError.value = '';
 }
 catch (e) {
 jsonError.value = 'JSON 格式错误: ' + e.message;
 }
};
const toggleUrl = () => {
 if (urlEncode.value) {
 urlOutput.value = encodeURIComponent(urlInput.value);
 }
 else {
 urlOutput.value = decodeURIComponent(urlInput.value);
 }
};
const toggleBase64 = () => {
 try {
 if (base64Encode.value) {
 base64Output.value = btoa(unescape(encodeURIComponent(base64Input.value)));
 }
 else {
 base64Output.value = decodeURIComponent(escape(atob(base64Input.value)));
 }
 }
 catch (e) {
 base64Output.value = '转换失败: ' + e.message;
 }
};
const convertTimestamp = () => {
 if (timestamp.value) {
 const ts = parseInt(timestamp.value);
 if (!isNaN(ts)) {
 const date = new Date(ts * 1000);
 dateOutput.value = date.toLocaleString('zh-CN', {
 year: 'numeric',
 month: '2-digit',
 day: '2-digit',
 hour: '2-digit',
 minute: '2-digit',
 second: '2-digit'
 });
 }
 else {
 dateOutput.value = '无效的时间戳';
 }
 }
};
const getCurrentTimestamp = () => {
 timestamp.value = Math.floor(Date.now() / 1000).toString();
 convertTimestamp();
};
const generatePassword = () => {
 let charset = '';
 if (passwordIncludeUppercase.value)
 charset += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
 if (passwordIncludeLowercase.value)
 charset += 'abcdefghijklmnopqrstuvwxyz';
 if (passwordIncludeNumbers.value)
 charset += '0123456789';
 if (passwordIncludeSymbols.value)
 charset += '!@#$%^&*()_+-=[]{}|;:,.<>?';
 if (!charset) {
 generatedPassword.value = '请至少选择一种字符类型';
 return;
 }
 let password = '';
 const array = new Uint32Array(passwordLength.value);
 crypto.getRandomValues(array);
 for (let i = 0; i < passwordLength.value; i++) {
 password += charset[array[i] % charset.length];
 }
 generatedPassword.value = password;
};
const copyToClipboard = async (text) => {
 try {
 await navigator.clipboard.writeText(text);
 alert('已复制到剪贴板');
 }
 catch (err) {
 console.error('复制失败:', err);
 }
};
</script>

<template>
  <div class="tools-page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">🛠️ 在线工具</h1>
        <p class="page-desc">实用工具集合，提升你的工作效率</p>
      </div>
      
      <div class="tools-grid">
        <div
          v-for="tool in tools"
          :key="tool.id"
          @click="activeTool = tool.id"
          :class="['tool-card', { active: activeTool === tool.id }]"
        >
          <div class="tool-icon">{{ tool.icon }}</div>
          <div class="tool-info">
            <h3 class="tool-name">{{ tool.name }}</h3>
            <span class="tool-category">{{ tool.category }}</span>
          </div>
        </div>
      </div>
      
      <div class="tool-content">
        <div v-if="activeTool === 'markdown'" class="tool-panel">
          <div class="panel-header">
            <h2 class="panel-title">📝 Markdown 编辑器</h2>
          </div>
          <div class="editor-container">
            <div class="editor-left">
              <textarea
                v-model="markdownInput"
                class="editor-textarea"
                placeholder="在此输入 Markdown..."
              ></textarea>
            </div>
            <div class="editor-right">
              <div class="preview-header">预览</div>
              <div
                class="preview-content"
                v-html="markdownPreview"
              ></div>
            </div>
          </div>
        </div>
        
        <div v-if="activeTool === 'json'" class="tool-panel">
          <div class="panel-header">
            <h2 class="panel-title">📄 JSON 格式化</h2>
            <div class="panel-actions">
              <button @click="formatJson" class="action-btn">格式化</button>
              <button @click="minifyJson" class="action-btn">压缩</button>
            </div>
          </div>
          <div v-if="jsonError" class="error-message">{{ jsonError }}</div>
          <textarea
            v-model="jsonInput"
            class="json-textarea"
            placeholder="在此输入 JSON..."
          ></textarea>
        </div>
        
        <div v-if="activeTool === 'url'" class="tool-panel">
          <div class="panel-header">
            <h2 class="panel-title">🔗 URL 编码/解码</h2>
          </div>
          <div class="converter-container">
            <div class="converter-row">
              <input
                v-model="urlInput"
                @input="toggleUrl"
                class="converter-input"
                placeholder="输入 URL..."
              />
            </div>
            <div class="converter-switch">
              <button
                @click="urlEncode = !urlEncode; toggleUrl()"
                class="switch-btn"
              >
                {{ urlEncode ? '编码 → 解码' : '解码 → 编码' }}
              </button>
            </div>
            <div class="converter-row">
              <input
                v-model="urlOutput"
                readonly
                class="converter-output"
                placeholder="结果..."
              />
              <button @click="copyToClipboard(urlOutput)" class="copy-btn">📋</button>
            </div>
          </div>
        </div>
        
        <div v-if="activeTool === 'base64'" class="tool-panel">
          <div class="panel-header">
            <h2 class="panel-title">🔐 Base64 编码/解码</h2>
          </div>
          <div class="converter-container">
            <div class="converter-row">
              <input
                v-model="base64Input"
                @input="toggleBase64"
                class="converter-input"
                placeholder="输入文本..."
              />
            </div>
            <div class="converter-switch">
              <button
                @click="base64Encode = !base64Encode; toggleBase64()"
                class="switch-btn"
              >
                {{ base64Encode ? '编码 → 解码' : '解码 → 编码' }}
              </button>
            </div>
            <div class="converter-row">
              <input
                v-model="base64Output"
                readonly
                class="converter-output"
                placeholder="结果..."
              />
              <button @click="copyToClipboard(base64Output)" class="copy-btn">📋</button>
            </div>
          </div>
        </div>
        
        <div v-if="activeTool === 'timestamp'" class="tool-panel">
          <div class="panel-header">
            <h2 class="panel-title">⏰ 时间戳转换</h2>
            <button @click="getCurrentTimestamp" class="action-btn">获取当前时间戳</button>
          </div>
          <div class="timestamp-container">
            <div class="timestamp-row">
              <label>时间戳 (秒)</label>
              <input
                v-model="timestamp"
                @input="convertTimestamp"
                class="timestamp-input"
                placeholder="输入时间戳..."
              />
            </div>
            <div class="timestamp-row">
              <label>日期时间</label>
              <input
                v-model="dateOutput"
                readonly
                class="timestamp-output"
                placeholder="转换结果..."
              />
            </div>
          </div>
        </div>
        
        <div v-if="activeTool === 'password'" class="tool-panel">
          <div class="panel-header">
            <h2 class="panel-title">🔑 密码生成器</h2>
          </div>
          <div class="password-container">
            <div class="password-options">
              <div class="option-row">
                <label>密码长度</label>
                <input
                  v-model.number="passwordLength"
                  type="range"
                  min="4"
                  max="64"
                  class="length-slider"
                />
                <span class="length-value">{{ passwordLength }}</span>
              </div>
              <div class="option-row">
                <label>
                  <input v-model="passwordIncludeUppercase" type="checkbox" />
                  包含大写字母 (A-Z)
                </label>
              </div>
              <div class="option-row">
                <label>
                  <input v-model="passwordIncludeLowercase" type="checkbox" />
                  包含小写字母 (a-z)
                </label>
              </div>
              <div class="option-row">
                <label>
                  <input v-model="passwordIncludeNumbers" type="checkbox" />
                  包含数字 (0-9)
                </label>
              </div>
              <div class="option-row">
                <label>
                  <input v-model="passwordIncludeSymbols" type="checkbox" />
                  包含特殊字符 (!@#$%)
                </label>
              </div>
            </div>
            <div class="password-result">
              <input
                v-model="generatedPassword"
                readonly
                class="password-input"
                placeholder="生成的密码..."
              />
              <div class="password-actions">
                <button @click="generatePassword" class="action-btn">生成密码</button>
                <button @click="copyToClipboard(generatedPassword)" class="action-btn">复制</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tools-page {
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
  margin-bottom: 2rem;
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

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.tool-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--surface-color);
  border-radius: 12px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s;
}

.tool-card:hover {
  border-color: var(--primary-color);
  box-shadow: 0 4px 12px var(--shadow-color);
}

.tool-card.active {
  border-color: var(--primary-color);
  background: rgba(102, 126, 234, 0.1);
}

.tool-icon {
  font-size: 1.8rem;
}

.tool-info {
  display: flex;
  flex-direction: column;
}

.tool-name {
  font-size: 1rem;
  color: var(--text-color);
  font-weight: 600;
  margin: 0;
}

.tool-category {
  font-size: 0.8rem;
  color: var(--text-secondary-color);
}

.tool-content {
  background: var(--surface-color);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  padding: 1.5rem;
}

.tool-panel {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.panel-title {
  font-size: 1.3rem;
  color: var(--text-color);
  margin: 0;
}

.panel-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.3s;
}

.action-btn:hover {
  background: var(--secondary-color);
}

.editor-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  height: 400px;
}

.editor-left, .editor-right {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
}

.editor-textarea {
  width: 100%;
  height: 100%;
  padding: 1rem;
  border: none;
  background: var(--background-color);
  color: var(--text-color);
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 0.9rem;
  resize: none;
}

.editor-textarea:focus {
  outline: none;
}

.preview-header {
  padding: 0.8rem 1rem;
  background: var(--background-color);
  border-bottom: 1px solid var(--border-color);
  font-weight: 600;
  color: var(--text-color);
}

.preview-content {
  padding: 1rem;
  height: calc(100% - 45px);
  overflow-y: auto;
  color: var(--text-color);
}

.preview-content h1 {
  font-size: 1.5rem;
  margin-top: 0;
}

.preview-content h2 {
  font-size: 1.3rem;
}

.preview-content h3 {
  font-size: 1.1rem;
}

.preview-content ul {
  padding-left: 1.5rem;
}

.preview-content pre {
  background: var(--background-color);
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
}

.preview-content blockquote {
  border-left: 4px solid var(--primary-color);
  padding-left: 1rem;
  color: var(--text-secondary-color);
}

.json-textarea {
  width: 100%;
  height: 300px;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--background-color);
  color: var(--text-color);
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 0.9rem;
  resize: none;
}

.json-textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.error-message {
  padding: 0.8rem;
  background: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.converter-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.converter-row {
  display: flex;
  gap: 0.5rem;
}

.converter-input, .converter-output {
  flex: 1;
  padding: 0.8rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 0.95rem;
  background: var(--background-color);
  color: var(--text-color);
}

.converter-input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.converter-output {
  background: rgba(102, 126, 234, 0.1);
  border-color: var(--primary-color);
}

.switch-btn {
  align-self: center;
  padding: 0.5rem 1.5rem;
  background: var(--background-color);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  color: var(--text-color);
  cursor: pointer;
  transition: all 0.3s;
}

.switch-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.copy-btn {
  padding: 0.8rem 1rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
}

.copy-btn:hover {
  background: var(--secondary-color);
}

.timestamp-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.timestamp-row {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.timestamp-row label {
  font-size: 0.9rem;
  color: var(--text-secondary-color);
}

.timestamp-input, .timestamp-output {
  padding: 0.8rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 0.95rem;
  background: var(--background-color);
  color: var(--text-color);
}

.timestamp-input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.timestamp-output {
  background: rgba(39, 174, 96, 0.1);
  border-color: #27ae60;
}

.password-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.password-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.option-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.option-row label {
  font-size: 0.95rem;
  color: var(--text-color);
  cursor: pointer;
}

.length-slider {
  flex: 1;
}

.length-value {
  min-width: 3rem;
  text-align: center;
  font-weight: 600;
  color: var(--primary-color);
}

.password-result {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.password-input {
  padding: 1rem;
  border: 2px solid var(--primary-color);
  border-radius: 8px;
  font-size: 1.1rem;
  font-family: 'Monaco', 'Menlo', monospace;
  background: rgba(102, 126, 234, 0.1);
  color: var(--text-color);
}

.password-actions {
  display: flex;
  gap: 0.5rem;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .editor-container {
    grid-template-columns: 1fr;
    height: auto;
  }
  
  .editor-left, .editor-right {
    height: 200px;
  }
  
  .password-container {
    grid-template-columns: 1fr;
  }
}
</style>