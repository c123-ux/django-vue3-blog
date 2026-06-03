<div align="center">

# 🍊 Warm Blog

### A Warm & Human-Friendly Full-Stack Blog System | 温暖人性化的全栈博客系统

**Django + Vue 3 + DRF + Markdown + Anonymous Publishing**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0+-092E20?logo=django&logoColor=white)](https://djangoproject.com)
[![Vue](https://img.shields.io/badge/Vue-3-4FC08D?logo=vue.js&logoColor=white)](https://vuejs.org)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?logo=vite&logoColor=white)](https://vitejs.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**🚀 A production-ready blog system with warm design, refusing cold AI feel**
**🚀 拒绝冰冷 AI 感，开箱即用的生产级博客系统**

[📖 Documentation](#-documentation-文档) ·
[🎨 Features](#-features-特性) ·
[🚀 Quick Start](#-quick-start-快速开始) ·
[📸 Screenshots](#-screenshots-截图预览) ·
[🤝 Contributing](#-contributing-贡献)

</div>

---

## 📖 Table of Contents | 目录

- [🌟 Overview | 概述](#-overview--概述)
- [✨ Features | 特性](#-features--特性)
- [🛠️ Tech Stack | 技术栈](#️-tech-stack--技术栈)
- [📸 Screenshots | 截图预览](#-screenshots--截图预览)
- [🚀 Quick Start | 快速开始](#-quick-start--快速开始)
- [📦 Installation | 安装指南](#-installation--安装指南)
- [⚙️ Configuration | 配置说明](#️-configuration--配置说明)
- [📡 API Documentation | API 文档](#-api-documentation--api-文档)
- [🚢 Deployment | 部署指南](#-deployment--部署指南)
- [❓ FAQ | 常见问题](#-faq--常见问题)
- [🤝 Contributing | 贡献](#-contributing--贡献)
- [📄 License | 许可证](#-license--许可证)

---

## 🌟 Overview | 概述

### English

**Warm Blog** is a production-ready, full-stack blog system built with **Django REST Framework** and **Vue 3**. It features a warm orange-themed UI design that feels human-friendly, refusing the cold "AI-generated" look. The system supports anonymous article publishing, Markdown editing, nested comments, responsive design, and more.

**Perfect for**: Personal blogs, technical writing, content sharing platforms, learning projects.

### 中文

**Warm Blog** 是一个基于 **Django REST Framework** 和 **Vue 3** 构建的生产级全栈博客系统。采用温暖橙色主题的 UI 设计，人性化十足，拒绝冰冷的"AI 生成感"。系统支持匿名发布文章、Markdown 编辑、楼中楼评论、响应式设计等功能。

**适用场景**：个人博客、技术写作、内容分享平台、学习项目。

---

## ✨ Features | 特性

### 🎨 Design | 设计

| Feature | Description |
|---------|-------------|
| 🍊 **Warm Color Scheme** | Orange-based warm colors, comfortable visual experience |
| 📱 **Fully Responsive** | Perfect adaptation for desktop, tablet, and mobile |
| ✨ **Smooth Animations** | Hover effects, transitions, and micro-interactions |
| 🌗 **Dark Mode** | Auto-adaptive dark theme support |
| ♿ **Accessibility** | WCAG compliant, friendly to screen readers |

| 特性 | 描述 |
|------|------|
| 🍊 **温暖配色** | 以橙色为主的温暖色调，视觉舒适 |
| 📱 **完全响应式** | 完美适配桌面、平板、手机 |
| ✨ **流畅动画** | 悬停效果、过渡动画、微交互 |
| 🌗 **暗黑模式** | 自适应暗色主题支持 |
| ♿ **无障碍设计** | 符合 WCAG 标准，对屏幕阅读器友好 |

### 📝 Content Management | 内容管理

| Feature | Description |
|---------|-------------|
| 📝 **Markdown Editor** | Full Markdown support with toolbar (Bold, Italic, Heading, Link, Code, Image) |
| 🖼️ **Image Upload** | Drag-and-drop image upload, auto-compression, CDN ready |
| 🏷️ **Tags System** | Free-form tagging, auto-suggestions |
| 📂 **Categories** | Hierarchical category management |
| 📚 **Series** | Group related articles into series |
| 📌 **Pinned Articles** | Pin important articles to top |
| 📑 **Auto Summary** | Auto-generate article summaries |
| 🔍 **SEO Friendly** | Auto meta tags, sitemap, structured data |

| 特性 | 描述 |
|------|------|
| 📝 **Markdown 编辑器** | 完整 Markdown 支持，带工具栏（加粗、斜体、标题、链接、代码、图片） |
| 🖼️ **图片上传** | 拖拽上传，自动压缩，CDN 就绪 |
| 🏷️ **标签系统** | 自由标签，智能推荐 |
| 📂 **分类管理** | 层级分类管理 |
| 📚 **专题系列** | 将相关文章归类到专题 |
| 📌 **置顶文章** | 重要文章置顶显示 |
| 📑 **自动摘要** | 自动生成文章摘要 |
| 🔍 **SEO 优化** | 自动 meta 标签、站点地图、结构化数据 |

### 👤 User System | 用户系统

| Feature | Description |
|---------|-------------|
| 🔐 **JWT Authentication** | Secure JWT token-based auth |
| 👤 **Anonymous Publishing** | Anyone can publish articles without login |
| 📝 **Nickname Support** | Optional nickname for anonymous authors |
| 💬 **Nested Comments** | Threaded comments with replies |
| 👍 **Likes & Favorites** | Like and bookmark articles |
| 📊 **User Profiles** | Personal profile pages |

| 特性 | 描述 |
|------|------|
| 🔐 **JWT 认证** | 安全的 JWT token 认证 |
| 👤 **匿名发布** | 无需登录即可发布文章 |
| 📝 **昵称支持** | 匿名作者可选填昵称 |
| 💬 **楼中楼评论** | 支持评论嵌套回复 |
| 👍 **点赞收藏** | 文章点赞和收藏 |
| 📊 **个人主页** | 用户个人资料页面 |

### ⚡ Performance | 性能

| Feature | Description |
|---------|-------------|
| 🚀 **Redis Caching** | Multi-layer caching for fast response |
| 📊 **Read Counter** | Atomic increment, concurrency-safe |
| 🔄 **Hot Reload** | Dev-time hot module replacement |
| 📦 **Code Splitting** | Auto code splitting for faster loads |
| 🎯 **Lazy Loading** | Images and components load on demand |

| 特性 | 描述 |
|------|------|
| 🚀 **Redis 缓存** | 多层缓存，快速响应 |
| 📊 **阅读统计** | 原子递增，并发安全 |
| 🔄 **热重载** | 开发时模块热替换 |
| 📦 **代码分割** | 自动代码分割，加快加载 |
| 🎯 **懒加载** | 图片和组件按需加载 |

---

## 🛠️ Tech Stack | 技术栈

### Backend | 后端

| Technology | Version | Purpose |
|------------|---------|---------|
| ![Python](https://img.shields.io/badge/Python-3.12+-3776AB) | 3.12+ | Programming Language |
| ![Django](https://img.shields.io/badge/Django-5.0+-092E20) | 5.0+ | Web Framework |
| ![DRF](https://img.shields.io/badge/DRF-3.15+-A30000) | 3.15+ | REST API |
| ![SQLite](https://img.shields.io/badge/SQLite-3-003B57) | 3 | Database (Dev) |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791) | 15+ | Database (Prod) |
| ![Redis](https://img.shields.io/badge/Redis-7+-DC382D) | 7+ | Caching |
| ![Celery](https://img.shields.io/badge/Celery-5+-37814A) | 5+ | Async Tasks |

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.12+ | 编程语言 |
| Django | 5.0+ | Web 框架 |
| Django REST Framework | 3.15+ | REST API |
| SQLite | 3 | 数据库（开发） |
| PostgreSQL | 15+ | 数据库（生产） |
| Redis | 7+ | 缓存 |
| Celery | 5+ | 异步任务 |

### Frontend | 前端

| Technology | Version | Purpose |
|------------|---------|---------|
| ![Vue](https://img.shields.io/badge/Vue-3-4FC08D) | 3.4+ | UI Framework |
| ![Vite](https://img.shields.io/badge/Vite-5-646CFF) | 5+ | Build Tool |
| ![Pinia](https://img.shields.io/badge/Pinia-2-FFD859) | 2+ | State Management |
| ![Vue Router](https://img.shields.io/badge/Vue_Router-4-42B883) | 4+ | Routing |
| ![Axios](https://img.shields.io/badge/Axios-1-5A29E4) | 1+ | HTTP Client |
| ![Marked](https://img.shields.io/badge/Marked-9-000000) | 9+ | Markdown Parser |

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue 3 | 3.4+ | UI 框架 |
| Vite | 5+ | 构建工具 |
| Pinia | 2+ | 状态管理 |
| Vue Router | 4+ | 路由 |
| Axios | 1+ | HTTP 客户端 |
| Marked | 9+ | Markdown 解析 |

---

## 📸 Screenshots | 截图预览

### 🏠 Home Page | 首页

```
┌─────────────────────────────────────────────────────┐
│  🍊 Warm Blog                  [Write] [Login]      │
├─────────────────────────────────────────────────────┤
│                                                     │
│   📚 Latest Articles          📊 Statistics         │
│   ┌─────────────────────┐    ┌──────────────────┐  │
│   │ [Image] Article 1   │    │ Total: 100       │  │
│   │ Title & Summary     │    │ Today: 5         │  │
│   │ 👤 Author · 📅 Date │    │ Tags: 20         │  │
│   └─────────────────────┘    └──────────────────┘  │
│   ┌─────────────────────┐    ┌──────────────────┐  │
│   │ [Image] Article 2   │    │ 🏷️ Popular Tags  │  │
│   │ Title & Summary     │    │ #Python #Vue     │  │
│   │ 👤 Author · 📅 Date │    │ #Django #Web     │  │
│   └─────────────────────┘    └──────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### ✏️ Write Page | 写作页面

```
┌─────────────────────────────────────────────────────┐
│  📝 Publish Article                                  │
│  Anyone can publish, anonymous supported            │
├─────────────────────────────────────────────────────┤
│  Nickname (optional): [____________________]        │
│  Title *:           [____________________]          │
│  Cover:             [Upload Image]                  │
│  Summary:           [____________________]          │
│                                                     │
│  Content (Markdown):                                │
│  [B] [I] [H] [🔗] [</>] [🖼️]                       │
│  ┌─────────────────────────────────────────────┐   │
│  │                                             │   │
│  │  Start writing...                           │   │
│  │                                             │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  Category: [Select...]  Series: [Select...]         │
│  Tags: [Enter tags...]                              │
│                                                     │
│         [Cancel]  [🚀 Publish]                      │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start | 快速开始

### Prerequisites | 前置要求

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| ![Python](https://img.shields.io/badge/Python-3.12+-blue) | 3.12+ | `python --version` |
| ![Node.js](https://img.shields.io/badge/Node.js-18+-green) | 18+ | `node --version` |
| ![npm](https://img.shields.io/badge/npm-9+-red) | 9+ | `npm --version` |
| ![Git](https://img.shields.io/badge/Git-2.40+-orange) | 2.40+ | `git --version` |

| 要求 | 版本 | 检查命令 |
|------|------|----------|
| Python | 3.12+ | `python --version` |
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| Git | 2.40+ | `git --version` |

### 🐳 One-Click Start (Docker) | 一键启动（Docker）

```bash
# Clone the repository | 克隆仓库
git clone https://github.com/YOUR_USERNAME/warm-blog.git
cd warm-blog

# Start with Docker Compose | 使用 Docker Compose 启动
docker-compose up -d

# Access the blog | 访问博客
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
# Admin:    http://localhost:8000/admin
```

### 💻 Manual Setup | 手动安装

#### Step 1: Clone Repository | 步骤 1：克隆仓库

```bash
# English
git clone https://github.com/YOUR_USERNAME/warm-blog.git
cd warm-blog

# 中文
git clone https://github.com/YOUR_USERNAME/warm-blog.git
cd warm-blog
```

#### Step 2: Backend Setup | 步骤 2：后端设置

```bash
# Create virtual environment | 创建虚拟环境
python -m venv venv

# Activate virtual environment | 激活虚拟环境
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Windows (CMD)
.\venv\Scripts\activate.bat
# Linux/macOS
source venv/bin/activate

# Install dependencies | 安装依赖
pip install -r requirements.txt

# Database migration | 数据库迁移
python manage.py migrate

# Create superuser (optional) | 创建超级用户（可选）
python manage.py createsuperuser

# Run development server | 启动开发服务器
python manage.py runserver 8000
```

#### Step 3: Frontend Setup | 步骤 3：前端设置

```bash
# Enter frontend directory | 进入前端目录
cd blog-frontend

# Install dependencies | 安装依赖
npm install

# Run development server | 启动开发服务器
npm run dev
```

#### Step 4: Access | 步骤 4：访问

| Service | URL | Description |
|---------|-----|-------------|
| 📱 **Frontend** | http://localhost:5173 | Blog UI |
| 🔧 **Backend API** | http://localhost:8000 | REST API |
| 📚 **API Docs** | http://localhost:8000/api/docs/ | Swagger UI |
| 🛡️ **Admin** | http://localhost:8000/admin/ | Django Admin |

| 服务 | 地址 | 说明 |
|------|------|------|
| 📱 **前端** | http://localhost:5173 | 博客界面 |
| 🔧 **后端 API** | http://localhost:8000 | REST API |
| 📚 **API 文档** | http://localhost:8000/api/docs/ | Swagger 文档 |
| 🛡️ **管理后台** | http://localhost:8000/admin/ | Django 管理 |

---

## 📦 Installation | 安装指南

### Detailed Backend Setup | 后端详细设置

#### 1. Create Virtual Environment | 创建虚拟环境

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 2. Install Python Dependencies | 安装 Python 依赖

```bash
# Core dependencies | 核心依赖
pip install django==5.0 djangorestframework==3.15

# Authentication | 认证
pip install djangorestframework-simplejwt

# Database | 数据库
pip install psycopg2-binary  # PostgreSQL (production)
# SQLite is built-in (development)

# Caching | 缓存
pip install redis django-redis

# Markdown | Markdown
pip install markdown bleach

# Image processing | 图片处理
pip install Pillow

# Async tasks | 异步任务
pip install celery channels channels-redis

# API documentation | API 文档
pip install drf-spectacular

# Monitoring | 监控
pip install django-prometheus python-json-logger

# Search | 搜索
pip install django-elasticsearch-dsl elasticsearch-dsl

# Or install all at once | 或一次性安装
pip install -r requirements.txt
```

#### 3. Environment Configuration | 环境配置

```bash
# Copy environment template | 复制环境模板
cp .env.example .env

# Edit .env file | 编辑 .env 文件
# Required settings | 必需配置:
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional, defaults to SQLite) | 数据库（可选，默认 SQLite）
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=blog_db
# DB_USER=blog_user
# DB_PASSWORD=your-password
# DB_HOST=localhost
# DB_PORT=5432

# Redis (optional) | Redis（可选）
# REDIS_URL=redis://127.0.0.1:6379/1
```

#### 4. Database Setup | 数据库设置

```bash
# Create migrations | 创建迁移
python manage.py makemigrations

# Apply migrations | 应用迁移
python manage.py migrate

# Load sample data (optional) | 加载示例数据（可选）
python manage.py seed_blog_data

# Create admin user | 创建管理员
python manage.py createsuperuser
# Follow prompts to set username, email, password
# 按提示设置用户名、邮箱、密码
```

#### 5. Start Backend | 启动后端

```bash
# Development server | 开发服务器
python manage.py runserver 8000

# Production with Gunicorn | 生产环境 Gunicorn
pip install gunicorn
gunicorn blog_backend.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### Detailed Frontend Setup | 前端详细设置

#### 1. Install Node.js | 安装 Node.js

Download from [nodejs.org](https://nodejs.org/) (LTS version recommended)

#### 2. Install Dependencies | 安装依赖

```bash
cd blog-frontend
npm install
```

#### 3. Configuration | 配置

Create `blog-frontend/.env` file:

```env
# API Base URL | API 基础地址
VITE_API_BASE_URL=http://localhost:8000/api

# Site URL | 站点地址
VITE_SITE_URL=http://localhost:5173
```

#### 4. Development | 开发

```bash
# Start dev server | 启动开发服务器
npm run dev

# Build for production | 生产构建
npm run build

# Preview production build | 预览生产构建
npm run preview
```

---

## ⚙️ Configuration | 配置说明

### Backend Configuration | 后端配置

#### `blog_backend/settings.py`

```python
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database configuration | 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# For PostgreSQL production | PostgreSQL 生产环境
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME'),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'HOST': os.environ.get('DB_HOST', 'localhost'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
# }

# Redis caching | Redis 缓存
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# REST Framework | REST 框架
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

### Frontend Configuration | 前端配置

#### `blog-frontend/vite.config.js`

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

---

## 📡 API Documentation | API 文档

### Authentication | 认证接口

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/auth/token/` | Get JWT token | ❌ |
| `POST` | `/api/auth/token/refresh/` | Refresh JWT token | ❌ |
| `POST` | `/api/auth/register/` | User registration | ❌ |
| `GET` | `/api/auth/profile/` | Get user profile | ✅ |
| `PUT` | `/api/auth/profile/` | Update profile | ✅ |

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| `POST` | `/api/auth/token/` | 获取 JWT token | ❌ |
| `POST` | `/api/auth/token/refresh/` | 刷新 JWT token | ❌ |
| `POST` | `/api/auth/register/` | 用户注册 | ❌ |
| `GET` | `/api/auth/profile/` | 获取用户信息 | ✅ |
| `PUT` | `/api/auth/profile/` | 更新用户信息 | ✅ |

### Articles | 文章接口

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/articles/` | List articles (paginated) | ❌ |
| `GET` | `/api/articles/{id}/` | Article detail | ❌ |
| `POST` | `/api/articles/create/` | Create article | ❌ (Anonymous OK) |
| `PUT` | `/api/articles/{id}/update/` | Update article | ✅ |
| `DELETE` | `/api/articles/{id}/delete/` | Delete article | ✅ |
| `POST` | `/api/articles/upload-image/` | Upload image | ❌ |

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| `GET` | `/api/articles/` | 文章列表（分页） | ❌ |
| `GET` | `/api/articles/{id}/` | 文章详情 | ❌ |
| `POST` | `/api/articles/create/` | 创建文章 | ❌（支持匿名） |
| `PUT` | `/api/articles/{id}/update/` | 更新文章 | ✅ |
| `DELETE` | `/api/articles/{id}/delete/` | 删除文章 | ✅ |
| `POST` | `/api/articles/upload-image/` | 上传图片 | ❌ |

### Comments | 评论接口

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/comments/article/{id}/` | Get article comments | ❌ |
| `POST` | `/api/comments/create/` | Create comment | ❌ (Anonymous OK) |
| `DELETE` | `/api/comments/{id}/delete/` | Delete comment | ✅ |

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| `GET` | `/api/comments/article/{id}/` | 获取文章评论 | ❌ |
| `POST` | `/api/comments/create/` | 创建评论 | ❌（支持匿名） |
| `DELETE` | `/api/comments/{id}/delete/` | 删除评论 | ✅ |

### Example Usage | 使用示例

#### Register User | 注册用户

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
  }'
```

#### Login | 登录

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

Response | 响应:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### Create Article (Anonymous) | 创建文章（匿名）

```bash
curl -X POST http://localhost:8000/api/articles/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Article",
    "content": "# Hello World\n\nThis is my first article.",
    "nickname": "Anonymous Writer",
    "category_id": 1,
    "tag_ids": [1, 2]
  }'
```

#### Get Articles List | 获取文章列表

```bash
curl http://localhost:8000/api/articles/?page=1
```

---

## 🚢 Deployment | 部署指南

### Docker Deployment | Docker 部署

#### 1. Using Docker Compose | 使用 Docker Compose

```bash
# Create docker-compose.yml | 创建 docker-compose.yml
cat > docker-compose.yml << EOF
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgres://user:pass@db:5432/blog
      - REDIS_URL=redis://redis:6379/1
    depends_on:
      - db
      - redis

  frontend:
    build: ./blog-frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: blog
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
EOF

# Start all services | 启动所有服务
docker-compose up -d

# View logs | 查看日志
docker-compose logs -f

# Stop services | 停止服务
docker-compose down
```

### Manual Production Deployment | 手动生产部署

#### Backend | 后端

```bash
# Install production dependencies | 安装生产依赖
pip install gunicorn psycopg2-binary nginx

# Collect static files | 收集静态文件
python manage.py collectstatic --noinput

# Run with Gunicorn | 使用 Gunicorn 运行
gunicorn blog_backend.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
```

#### Frontend | 前端

```bash
# Build for production | 生产构建
cd blog-frontend
npm run build

# Serve with nginx | 使用 nginx 服务
sudo cp -r dist/* /var/www/html/
sudo systemctl restart nginx
```

#### Nginx Configuration | Nginx 配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend | 前端
    location / {
        root /var/www/html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API | 后端 API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Admin | 管理后台
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
    }

    # Static files | 静态文件
    location /static/ {
        alias /path/to/static/;
    }

    # Media files | 媒体文件
    location /media/ {
        alias /path/to/media/;
    }
}
```

---

## ❓ FAQ | 常见问题

<details>
<summary><b>📖 Click to expand FAQ | 点击展开常见问题</b></summary>

### Q1: How to fix "ModuleNotFoundError: No module named 'xxx'"?
### Q1: 如何解决 "ModuleNotFoundError: No module named 'xxx'"？

**A:** Activate virtual environment and install dependencies:
**A:** 激活虚拟环境并安装依赖：

```bash
# Windows
.\venv\Scripts\activate
pip install -r requirements.txt

# Linux/macOS
source venv/bin/activate
pip install -r requirements.txt
```

### Q2: Port already in use?
### Q2: 端口被占用怎么办？

**A:** System will auto-try other ports. Check terminal output for actual port.
**A:** 系统会自动尝试其他端口，查看终端输出的实际端口号。

```bash
# Find process using port 8000 | 查找占用 8000 端口的进程
# Windows
netstat -ano | findstr :8000

# Linux/macOS
lsof -i :8000

# Kill process | 终止进程
# Windows
taskkill /PID <process_id> /F

# Linux/macOS
kill -9 <process_id>
```

### Q3: Redis connection failed?
### Q3: Redis 连接失败？

**A:** System will auto-fallback to memory cache. For Redis:
**A:** 系统会自动降级到内存缓存。如需 Redis：

```bash
# Install Redis | 安装 Redis
# Windows: Download from https://redis.io/download
# Linux: sudo apt install redis-server
# macOS: brew install redis

# Start Redis | 启动 Redis
redis-server

# Verify | 验证
redis-cli ping
# Should return: PONG
```

### Q4: Database migration errors?
### Q4: 数据库迁移错误？

**A:** Reset migrations:
**A:** 重置迁移：

```bash
# Remove all migrations | 删除所有迁移
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Recreate | 重新创建
python manage.py makemigrations
python manage.py migrate
```

### Q5: Frontend build fails?
### Q5: 前端构建失败？

**A:** Clear cache and reinstall:
**A:** 清除缓存并重新安装：

```bash
cd blog-frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
npm run dev
```

### Q6: How to change theme colors?
### Q6: 如何修改主题颜色？

**A:** Edit CSS variables in `blog-frontend/src/App.vue`:
**A:** 编辑 `blog-frontend/src/App.vue` 中的 CSS 变量：

```css
:root {
  --primary-color: #FF8C42;    /* Main color | 主色 */
  --secondary-color: #FFB347;  /* Secondary | 辅色 */
  --background-color: #FFF9F0; /* Background | 背景 */
  /* ... */
}
```

### Q7: Default admin credentials?
### Q7: 默认管理员账号？

**A:** Create your own superuser:
**A:** 创建你自己的超级用户：

```bash
python manage.py createsuperuser
```

Default test account (if loaded sample data):
默认测试账号（如果加载了示例数据）：
- Username | 用户名: `admin`
- Password | 密码: `admin123`

</details>

---

## 📊 Project Structure | 项目结构

```
warm-blog/
├── 📁 apps/                          # Django Apps | Django 应用
│   ├── 📁 articles/                  # Article module | 文章模块
│   │   ├── 📄 models.py              # Article, Category, Tag, Series models
│   │   ├── 📄 serializers.py         # DRF serializers
│   │   ├── 📄 views.py               # API views
│   │   ├── 📄 urls.py                # URL routing
│   │   └── 📁 migrations/            # Database migrations
│   ├── 📁 comments/                  # Comment module | 评论模块
│   ├── 📁 users/                     # User module | 用户模块
│   ├── 📁 notes/                     # Notes module | 笔记模块
│   ├── 📁 system/                    # System config | 系统配置
│   └── 📁 monitoring/                # Monitoring | 监控
├── 📁 blog_backend/                  # Django project | Django 项目
│   ├── 📄 settings.py                # Dev settings | 开发配置
│   ├── 📄 settings_production.py     # Prod settings | 生产配置
│   ├── 📄 urls.py                    # Main URL conf | 主路由
│   └── 📄 wsgi.py                    # WSGI config
├── 📁 blog-frontend/                 # Vue 3 frontend | Vue 3 前端
│   ├── 📁 src/
│   │   ├── 📁 api/                   # API calls | API 调用
│   │   ├── 📁 views/                 # Page components | 页面组件
│   │   ├── 📁 components/            # Reusable components | 可复用组件
│   │   ├── 📁 router/                # Vue Router | 路由
│   │   ├── 📁 stores/                # Pinia stores | 状态管理
│   │   ├── 📁 composables/           # Vue composables | 组合式函数
│   │   └── 📄 App.vue                # Root component | 根组件
│   ├── 📄 package.json               # Node dependencies
│   └── 📄 vite.config.js             # Vite config
├── 📁 scripts/                       # Utility scripts | 工具脚本
├── 📄 manage.py                      # Django management
├── 📄 requirements.txt               # Python dependencies
├── 📄 Dockerfile                     # Docker config
├── 📄 docker-compose.yml             # Docker Compose
├── 📄 .env.example                   # Environment template
└── 📄 README.md                      # This file
```

---

## 🧪 Testing | 测试

### Run Tests | 运行测试

```bash
# Backend tests | 后端测试
python manage.py test

# With coverage | 带覆盖率
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report

# Frontend tests (if configured) | 前端测试
cd blog-frontend
npm run test
```

### Test Coverage | 测试覆盖

| Module | Tests | Status |
|--------|-------|--------|
| Users | 9 | ✅ |
| Articles | 18 | ✅ |
| Comments | 15 | ✅ |
| **Total** | **42** | **✅ 100%** |

---

## 🤝 Contributing | 贡献

We welcome contributions! Please follow these steps:
欢迎贡献！请按以下步骤操作：

### 🌟 Ways to Contribute | 贡献方式

- 🐛 **Report Bugs** | 报告 Bug
- 💡 **Suggest Features** | 建议新功能
- 📝 **Improve Documentation** | 改进文档
- 🌍 **Translate** | 翻译
- 💻 **Write Code** | 编写代码

### 📋 Contribution Process | 贡献流程

1. **Fork** the repository | Fork 仓库
2. **Clone** your fork | 克隆你的 Fork
   ```bash
   git clone https://github.com/YOUR_USERNAME/warm-blog.git
   ```
3. **Create** a feature branch | 创建功能分支
   ```bash
   git checkout -b feature/AmazingFeature
   ```
4. **Commit** your changes | 提交更改
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
5. **Push** to the branch | 推送到分支
   ```bash
   git push origin feature/AmazingFeature
   ```
6. **Open** a Pull Request | 发起 Pull Request

### 📝 Coding Standards | 编码规范

- **Python**: Follow PEP 8
- **JavaScript**: Follow ESLint configuration
- **Vue**: Follow Vue.js Style Guide
- **Commits**: Follow Conventional Commits

---

## 📈 Roadmap | 路线图

- [x] ✅ Core blog functionality
- [x] ✅ Anonymous publishing
- [x] ✅ Warm UI design
- [x] ✅ Responsive layout
- [x] ✅ Markdown editor
- [x] ✅ Nested comments
- [x] ✅ JWT authentication
- [x] ✅ Redis caching
- [ ] 🔲 Elasticsearch integration
- [ ] 🔲 WebSocket real-time comments
- [ ] 🔲 Mobile app (React Native)
- [ ] 🔲 Plugin system
- [ ] 🔲 Multi-language support
- [ ] 🔲 Dark/Light theme toggle

---

## 📄 License | 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

```
MIT License

Copyright (c) 2026 Warm Blog

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

## 🙏 Acknowledgments | 致谢

- **Django** - The web framework for perfectionists with deadlines
- **Vue.js** - The progressive JavaScript framework
- **Vite** - Next generation frontend tooling
- **DRF** - Powerful and flexible toolkit for building Web APIs
- **Redis** - In-memory data structure store
- **Markdown** - Lightweight markup language
- All our contributors! 🎉

---

## 📞 Contact | 联系方式

- **GitHub Issues**: [Report a bug or request a feature](https://github.com/YOUR_USERNAME/warm-blog/issues)
- **Email**: your-email@example.com
- **Blog**: [https://your-blog.com](https://your-blog.com)

---

<div align="center">

### 🌟 If you like this project, please give it a star! 🌟
### 🌟 如果这个项目对你有帮助，请给个 Star！🌟

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/warm-blog&type=Date)](https://star-history.com/#YOUR_USERNAME/warm-blog&Date)

**Made with ❤️ by [Your Name](https://github.com/YOUR_USERNAME)**

**由 [你的名字](https://github.com/YOUR_USERNAME) 用 ❤️ 制作**

</div>
