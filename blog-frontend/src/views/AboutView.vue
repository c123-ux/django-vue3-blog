<script setup>
</script>

<template>
  <div class="about-page">
    <div class="container">
      <div class="about-header">
        <div class="header-icon">📖</div>
        <h1>关于我的博客</h1>
        <p class="subtitle">分享技术，记录生活 — 涵盖科技资讯、新闻热点、技术博客、美食、健康、旅游等多元化内容</p>
        <div class="header-decoration"></div>
      </div>

      <div class="about-content">
        <div class="about-section">
          <div class="section-header">
            <h2>📖 关于本站</h2>
            <div class="section-line"></div>
          </div>
          <div class="about-text">
            <p>欢迎来到我的个人博客！这是一个集技术学习、生活分享、信息交流的多元化平台。</p>
            <p>本站不仅是我记录编程学习历程的技术空间，更是一个分享生活感悟、社会资讯、兴趣爱好的综合内容平台。无论你是来寻找 Python、Django、Vue3 等技术的学习者，还是想了解科技资讯、生活技巧、美食分享、健康养生、旅游攻略等内容的普通读者，相信都能在这里找到你感兴趣的内容。</p>
            <p>本站内容涵盖多个领域，每个分类都有丰富的文章和专题：</p>
            <p><strong>📰 新闻资讯：</strong>最新科技新闻、热点事件分析、时事评论，让你快速了解世界动态</p>
            <p><strong>💻 技术博客：</strong>Python、Django、Vue3、前端技术、数据库、DevOps 等技术内容，教程详实，代码完整，原理透彻</p>
            <p><strong>📖 生活百科：</strong>生活技巧分享、实用知识科普、让你的生活更加丰富多彩</p>
            <p><strong>🍜 美食天地：</strong>美食推荐、烹饪技巧、美食文化介绍，满足你的味蕾</p>
            <p><strong>✈️ 旅游攻略：</strong>景点介绍、旅行心得、行程规划，带你看遍美丽风景</p>
            <p><strong>🎬 影视音乐：</strong>电影推荐、音乐分享、影视评论，丰富你的精神生活</p>
            <p><strong>🎮 游戏娱乐：</strong>热门游戏介绍、游戏攻略、游戏心得分享</p>
            <p><strong>💪 健康养生：</strong>健康知识、养生方法、健康生活方式介绍</p>
            <p>博客采用前后端分离架构开发，后端使用 Django + Django REST Framework 提供 API 接口，前端使用 Vue 3 + Vite 构建用户界面。整个项目从零搭建，所有功能都经过精心设计和实现。</p>
            <p>感谢你的访问，愿你在这里有所收获，无论是技术学习还是生活分享，希望都能给你带来价值！</p>
          </div>
        </div>
        <div class="about-section">
          <div class="section-header">
            <h2>📚 本站内容概览</h2>
            <div class="section-line"></div>
          </div>
          <div class="feature-list">
            <div class="feature-item">
              <span class="feature-dot"></span>
              <div class="feature-text">
                <h3>📰 新闻资讯</h3>
                <p>最新科技资讯、社会热点、行业动态，第一时间了解世界变化</p>
              </div>
            </div>
            <div class="feature-item">
              <span class="feature-dot"></span>
              <div class="feature-text">
                <h3>💻 技术博客</h3>
                <p>Python、Django、Vue3 等技术教程和经验分享，详细透彻，易学易懂</p>
              </div>
            </div>
            <div class="feature-item">
              <span class="feature-dot"></span>
              <div class="feature-text">
                <h3>📖 生活百科</h3>
                <p>生活技巧、实用知识、让你的生活更加丰富多彩</p>
              </div>
            </div>
            <div class="feature-item">
              <span class="feature-dot"></span>
              <div class="feature-text">
                <h3>🍜 美食天地</h3>
                <p>美食推荐、烹饪技巧、美食文化，带你品味生活</p>
              </div>
            </div>
            <div class="feature-item">
              <span class="feature-dot"></span>
              <div class="feature-text">
                <h3>✈️ 旅游攻略</h3>
                <p>景点介绍、旅行心得、行程规划，带你看遍美丽风景</p>
              </div>
            </div>
            <div class="feature-item">
              <span class="feature-dot"></span>
              <div class="feature-text">
                <h3>🎬 影视音乐</h3>
                <p>电影推荐、音乐分享、影视评论，丰富你的精神生活</p>
              </div>
            </div>
            <div class="feature-item">
              <span class="feature-dot"></span>
              <div class="feature-text">
                <h3>🎮 游戏娱乐</h3>
                <p>热门游戏、游戏攻略、游戏心得分享，享受娱乐时光</p>
              </div>
            </div>
            <div class="feature-item">
              <span class="feature-dot"></span>
              <div class="feature-text">
                <h3>💪 健康养生</h3>
                <p>健康知识、养生方法、健康生活方式，关注你的身心健康</p>
              </div>
            </div>
            <div class="feature-item">
              <span class="feature-dot"></span>
              <div class="feature-text">
                <h3>📚 教育学习</h3>
                <p>学习方法、教育心得、知识分享，助力你的成长进步</p>
              </div>
            </div>
          </div>
        </div>

        <div class="about-section">
          <div class="section-header">
            <h2>🚀 技术栈</h2>
            <div class="section-line"></div>
          </div>
          <div class="tech-grid">
            <div class="tech-card">
              <div class="tech-icon">🐍</div>
              <h3>后端</h3>
              <ul>
                <li>Django 6.0 — Python 最流行的 Web 框架，提供 ORM、路由、中间件等完整功能</li>
                <li>Django REST Framework — 强大的 API 开发工具，支持序列化、分页、过滤、限流</li>
                <li>SQLite — 轻量级嵌入式数据库，开发阶段无需额外安装数据库服务</li>
              </ul>
            </div>

            <div class="tech-card">
              <div class="tech-icon">🎨</div>
              <h3>前端</h3>
              <ul>
                <li>Vue 3 — 渐进式 JavaScript 框架，Composition API 让代码组织更灵活</li>
                <li>Vite — 下一代前端构建工具，开发时极速热更新</li>
                <li>Pinia — Vue 官方状态管理库，轻量且类型友好</li>
                <li>Vue Router — Vue 官方路由管理，支持历史模式和路由守卫</li>
                <li>Axios — HTTP 请求库，支持拦截器和请求取消</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="about-section">
          <div class="section-header">
            <h2>💡 博客特色</h2>
            <div class="section-line"></div>
          </div>
          <div class="feature-list">
            <div class="feature-item">
              <span class="feature-dot"></span>
              <div class="feature-text">
                <h3>详细的技术文章</h3>
                <p>每篇文章都力求概念清晰、代码完整、原理透彻，像教程一样一步步带你理解，而不是简单罗列代码片段。</p>
              </div>
            </div>
            <div class="feature-item">
              <span class="feature-dot"></span>
              <div class="feature-text">
                <h3>匿名评论互动</h3>
                <p>无需注册登录即可发表评论和回复，降低了交流门槛。你可以自定义昵称，也可以匿名留言。</p>
              </div>
            </div>
            <div class="feature-item">
              <span class="feature-dot"></span>
              <div class="feature-text">
                <h3>文章目录导航</h3>
                <p>长篇文章自动生成目录，点击即可跳转到对应章节，阅读体验更流畅。</p>
              </div>
            </div>
            <div class="feature-item">
              <span class="feature-dot"></span>
              <div class="feature-text">
                <h3>暗色模式</h3>
                <p>支持亮色/暗色主题切换，夜间阅读更舒适，保护你的眼睛。</p>
              </div>
            </div>
            <div class="feature-item">
              <span class="feature-dot"></span>
              <div class="feature-text">
                <h3>响应式设计</h3>
                <p>页面自适应手机、平板、电脑等不同屏幕尺寸，随时随地都能舒适阅读。</p>
              </div>
            </div>
            <div class="feature-item">
              <span class="feature-dot"></span>
              <div class="feature-text">
                <h3>全文搜索</h3>
                <p>输入关键词即可快速搜索文章，方便找到你需要的内容。</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about-page {
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.about-header {
  text-align: center;
  margin-bottom: 3rem;
}

.header-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.about-header h1 {
  font-size: 2.5rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.subtitle {
  font-size: 1.2rem;
  color: var(--text-secondary-color);
  margin-bottom: 1rem;
}

.header-decoration {
  width: 100px;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  margin: 1.5rem auto;
  border-radius: 2px;
}

.about-content {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.about-section {
  background: var(--surface-color);
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 12px var(--shadow-color);
  border: 1px solid var(--border-color);
}

.section-header {
  margin-bottom: 2rem;
}

.about-section h2 {
  font-size: 1.8rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.section-line {
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  border-radius: 2px;
}

.about-text p {
  color: var(--text-secondary-color);
  line-height: 2;
  font-size: 1.05rem;
  margin-bottom: 1rem;
  text-indent: 2em;
}

.about-text p:last-child {
  margin-bottom: 0;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.tech-card {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  padding: 2rem;
  border-radius: 12px;
  transition: transform 0.3s, box-shadow 0.3s;
  box-shadow: 0 4px 12px var(--shadow-color);
}

.tech-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px var(--shadow-color);
}

.tech-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.tech-card h3 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.tech-card ul {
  list-style: none;
  padding: 0;
}

.tech-card li {
  padding: 0.6rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  line-height: 1.5;
  font-size: 0.95rem;
}

.tech-card li:last-child {
  border-bottom: none;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 1rem;
}

.feature-item {
  display: flex;
  gap: 1rem;
  padding: 1.2rem 1.5rem;
  background: var(--background-color);
  border-radius: 10px;
  transition: all 0.3s;
  border: 1px solid var(--border-color);
}

.feature-item:hover {
  border-color: var(--primary-color);
  transform: translateX(6px);
  box-shadow: 0 2px 8px var(--shadow-color);
}

.feature-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--primary-color);
  flex-shrink: 0;
  margin-top: 6px;
}

.feature-text h3 {
  font-size: 1.1rem;
  color: var(--text-color);
  margin-bottom: 0.4rem;
  font-weight: 600;
}

.feature-text p {
  color: var(--text-secondary-color);
  margin: 0;
  line-height: 1.7;
  font-size: 0.95rem;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .about-header h1 {
    font-size: 2rem;
  }

  .about-section {
    padding: 1.5rem;
  }

  .tech-grid {
    grid-template-columns: 1fr;
  }

  .about-text p {
    text-indent: 0;
  }
}
</style>
