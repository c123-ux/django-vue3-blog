from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.articles.models import Article
from django.db.models.signals import post_save
from django.dispatch import receiver
import os


class Command(BaseCommand):
    help = '创建示例文章数据'

    def handle(self, *args, **options):
        self.stdout.write('开始创建示例文章...')

        # 获取或创建管理员用户
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@blog.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('1593570abc')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('创建管理员用户: admin'))

        # 示例文章数据
        articles_data = [
            {
                'title': 'Django REST Framework 完全指南',
                'content': '''# Django REST Framework 完全指南

## 简介

Django REST Framework (DRF) 是一个强大且灵活的工具包，用于构建 Web API。

## 为什么选择 DRF？

- **序列化**：将复杂的数据类型（如查询集和模型实例）转换为原生 Python 数据类型
- **认证和权限**：提供多种认证方式和权限控制
- **视图**：提供函数视图和类视图两种方式
- **路由**：自动生成 URL 路由
- **文档**：自动生成 API 文档

## 快速开始

### 安装

```bash
pip install djangorestframework
```

### 配置

在 `settings.py` 中添加：

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

### 创建序列化器

```python
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
```

### 创建视图

```python
from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

### 配置路由

```python
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)

urlpatterns = router.urls
```

## 认证

DRF 提供多种认证方式：

1. **Basic Authentication**
2. **Token Authentication**
3. **Session Authentication**
4. **JWT Authentication**

### JWT 认证配置

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

## 权限

DRF 提供多种权限类：

- `AllowAny`：允许所有用户
- `IsAuthenticated`：只允许认证用户
- `IsAdminUser`：只允许管理员用户
- `IsAuthenticatedOrReadOnly`：认证用户可以读写，未认证用户只能读

## 总结

Django REST Framework 是构建 Web API 的强大工具，它提供了丰富的功能和灵活的配置选项。通过本指南，你应该能够快速上手并构建自己的 API。
''',
                'summary': 'Django REST Framework 是一个强大且灵活的工具包，用于构建 Web API。本文详细介绍 DRF 的核心概念、安装配置、序列化、视图、路由、认证和权限等内容。',
                'cover': None,
                'status': 'published',
            },
            {
                'title': 'Vue3 + Vite 前端开发最佳实践',
                'content': '''# Vue3 + Vite 前端开发最佳实践

## 为什么选择 Vue3 + Vite？

Vue3 带来了许多新特性：
- **Composition API**：更好的代码组织和复用
- **性能提升**：更快的渲染和更小的包体积
- **TypeScript 支持**：更好的类型推断
- **更好的 IDE 支持**：更智能的代码提示

Vite 提供了：
- **极速的开发服务器启动**
- **即时的模块热更新 (HMR)**
- **优化的生产构建**

## 项目初始化

```bash
npm create vite@latest my-vue-app -- --template vue
cd my-vue-app
npm install
npm run dev
```

## Composition API

### setup() 函数

```javascript
import { ref, computed, onMounted } from 'vue'

export default {
  setup() {
    const count = ref(0)
    const doubled = computed(() => count.value * 2)
    
    onMounted(() => {
      console.log('组件已挂载')
    })
    
    return {
      count,
      doubled
    }
  }
}
```

### `<script setup>` 语法糖

```javascript
<script setup>
import { ref, computed } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)
</script>
```

## 状态管理

使用 Pinia 进行状态管理：

```javascript
// stores/counter.js
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0
  }),
  actions: {
    increment() {
      this.count++
    }
  }
})
```

## 路由管理

使用 Vue Router：

```javascript
// router/index.js
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

## API 请求

使用 Axios：

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000
})

// 请求拦截器
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
```

## 性能优化

1. **懒加载组件**
```javascript
const LazyComponent = defineAsyncComponent(() => 
  import('./LazyComponent.vue')
)
```

2. **虚拟滚动**
3. **图片懒加载**
4. **代码分割**

## 总结

Vue3 + Vite 是现代前端开发的优秀选择，它们提供了出色的开发体验和性能。通过遵循最佳实践，你可以构建出高质量的前端应用。
''',
                'summary': 'Vue3 和 Vite 是现代前端开发的优秀组合。本文介绍了 Vue3 的新特性、Composition API、状态管理、路由管理、API 请求和性能优化等最佳实践。',
                'cover': None,
                'status': 'published',
            },
            {
                'title': 'Redis 缓存实战：从入门到精通',
                'content': '''# Redis 缓存实战：从入门到精通

## 什么是 Redis？

Redis (Remote Dictionary Server) 是一个开源的内存数据结构存储系统，可以用作数据库、缓存和消息中间件。

## Redis 的数据类型

### String（字符串）

```bash
SET key value
GET key
INCR key
```

### Hash（哈希）

```bash
HSET user:1 name "张三" age 25
HGET user:1 name
HGETALL user:1
```

### List（列表）

```bash
LPUSH mylist "item1"
RPUSH mylist "item2"
LRANGE mylist 0 -1
```

### Set（集合）

```bash
SADD myset "member1"
SMEMBERS myset
```

### Sorted Set（有序集合）

```bash
ZADD myzset 1 "one"
ZADD myzset 2 "two"
ZRANGE myzset 0 -1 WITHSCORES
```

## Django 中使用 Redis

### 安装依赖

```bash
pip install redis django-redis
```

### 配置

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### 使用缓存

```python
from django.core.cache import cache

# 设置缓存
cache.set('key', 'value', timeout=60)

# 获取缓存
value = cache.get('key')

# 删除缓存
cache.delete('key')
```

### 缓存装饰器

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 缓存 15 分钟
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'articles.html', {'articles': articles})
```

## 缓存策略

### Cache-Aside（旁路缓存）

1. 应用先查缓存
2. 缓存命中，直接返回
3. 缓存未命中，查数据库
4. 将数据写入缓存

### Read-Through（读穿透）

应用通过缓存访问数据，缓存负责从数据库加载数据。

### Write-Through（写穿透）

应用同时写入缓存和数据库。

### Write-Behind（写回）

应用先写缓存，异步写数据库。

## 缓存问题及解决方案

### 缓存穿透

**问题**：查询不存在的数据，导致每次都查数据库。

**解决方案**：
- 布隆过滤器
- 缓存空值
- 请求限流

### 缓存击穿

**问题**：热点 Key 过期，大量请求直接打到数据库。

**解决方案**：
- 设置永不过期
- 互斥锁
- 异步刷新

### 缓存雪崩

**问题**：大量 Key 同时过期，导致数据库压力骤增。

**解决方案**：
- 随机过期时间
- 缓存预热
- 限流降级

## Redis 持久化

### RDB（快照）

```bash
save 900 1
save 300 10
save 60 10000
```

### AOF（追加文件）

```bash
appendonly yes
appendfsync everysec
```

## 总结

Redis 是一个强大的缓存工具，掌握其使用方法和最佳实践对于构建高性能应用至关重要。通过合理使用缓存策略和解决常见问题，可以显著提升应用性能。
''',
                'summary': 'Redis 是一个强大的内存数据结构存储系统，广泛用作缓存、数据库和消息中间件。本文详细介绍 Redis 的数据类型、在 Django 中的使用、缓存策略、常见问题及解决方案。',
                'cover': None,
                'status': 'published',
            },
            {
                'title': 'Celery 异步任务处理详解',
                'content': '''# Celery 异步任务处理详解

## 什么是 Celery？

Celery 是一个强大的分布式任务队列，用于处理异步任务和定时任务。

## Celery 的核心组件

1. **Broker（消息代理）**：负责接收和分发任务消息（如 Redis、RabbitMQ）
2. **Worker（工作进程）**：执行任务的进程
3. **Backend（结果存储）**：存储任务执行结果（如 Redis、Database）
4. **Beat（调度器）**：处理定时任务

## 安装和配置

### 安装依赖

```bash
pip install celery redis
```

### 配置 Celery

```python
# celery.py
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_backend.settings')

app = Celery('blog_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### 在 settings.py 中配置

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
```

## 创建任务

### 基本任务

```python
# tasks.py
from celery import shared_task

@shared_task
def send_email(to, subject, message):
    # 发送邮件逻辑
    print(f"发送邮件到 {to}")
    return f"邮件已发送到 {to}"
```

### 调用任务

```python
# 同步调用
result = send_email('user@example.com', '测试', '这是一封测试邮件')

# 异步调用
result = send_email.delay('user@example.com', '测试', '这是一封测试邮件')

# 获取结果
result.get(timeout=10)
```

## 任务装饰器

### 设置任务名称

```python
@shared_task(name='tasks.send_email')
def send_email(to, subject, message):
    pass
```

### 设置超时时间

```python
@shared_task(time_limit=60)
def long_running_task():
    pass
```

### 设置重试

```python
@shared_task(
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 3, 'countdown': 5}
)
def unreliable_task():
    pass
```

## 定时任务

### 配置定时任务

```python
# celery.py
from celery.schedules import crontab

app.conf.beat_schedule = {
    'send-daily-report': {
        'task': 'tasks.send_daily_report',
        'schedule': crontab(hour=9, minute=0),  # 每天早上 9 点
    },
    'cleanup-cache': {
        'task': 'tasks.cleanup_cache',
        'schedule': crontab(hour=0, minute=0),  # 每天凌晨
    },
}
```

### 启动 Beat

```bash
celery -A blog_backend beat -l info
```

## 任务链和组

### 任务链

```python
from celery import chain

workflow = chain(
    task1.s(),
    task2.s(),
    task3.s()
)
workflow.delay()
```

### 任务组

```python
from celery import group

workflow = group(
    task1.s(),
    task2.s(),
    task3.s()
)
workflow.delay()
```

### Chord（任务组 + 回调）

```python
from celery import chord

workflow = chord(
    [task1.s(), task2.s(), task3.s()],
    callback.s()
)
workflow.delay()
```

## 监控和管理

### Flower

```bash
pip install flower
celery -A blog_backend flower
```

访问 http://localhost:5555 查看监控界面。

## 最佳实践

1. **任务幂等性**：确保任务可以安全地重复执行
2. **错误处理**：合理处理任务异常
3. **日志记录**：记录任务执行日志
4. **资源清理**：及时清理临时资源
5. **任务超时**：设置合理的超时时间

## 总结

Celery 是处理异步任务和定时任务的强大工具。通过合理使用 Celery，可以显著提升应用的性能和用户体验。掌握 Celery 的核心概念和最佳实践对于构建高性能应用至关重要。
''',
                'summary': 'Celery 是一个强大的分布式任务队列，用于处理异步任务和定时任务。本文详细介绍 Celery 的核心组件、安装配置、任务创建、定时任务、任务链和组、监控管理以及最佳实践。',
                'cover': None,
                'status': 'published',
            },
            {
                'title': 'JWT 认证机制深度解析',
                'content': '''# JWT 认证机制深度解析

## 什么是 JWT？

JWT (JSON Web Token) 是一种开放标准 (RFC 7519)，用于在各方之间安全地传输信息。

## JWT 的结构

JWT 由三部分组成，用点 (.) 分隔：

```
Header.Payload.Signature
```

### Header（头部）

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload（负载）

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022
}
```

### Signature（签名）

```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

## JWT 的工作流程

1. 用户登录，服务器验证凭据
2. 服务器生成 JWT 并返回给客户端
3. 客户端存储 JWT（通常在 localStorage 或 Cookie 中）
4. 客户端在后续请求中携带 JWT
5. 服务器验证 JWT 并返回响应

## Django 中使用 JWT

### 安装依赖

```bash
pip install djangorestframework-simplejwt
```

### 配置

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

### 创建视图

```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

## JWT 的优势

1. **无状态**：服务器不需要存储会话信息
2. **跨域**：适合分布式系统
3. **移动端友好**：易于在移动应用中使用
4. **性能**：减少数据库查询

## JWT 的安全考虑

### 1. 使用 HTTPS

始终使用 HTTPS 传输 JWT，防止中间人攻击。

### 2. 设置合理的过期时间

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

### 3. 使用强密钥

```python
SECRET_KEY = 'your-very-secret-key-here'
```

### 4. 实现 Token 刷新

```python
SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

### 5. 实现 Token 撤销

```python
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

def logout(request):
    token = request.auth
    BlacklistedToken.objects.create(token=token)
    return Response({'message': 'Logged out successfully'})
```

## 常见问题

### 1. Token 泄露怎么办？

- 使用短期 Access Token
- 实现 Token 刷新机制
- 监控异常使用

### 2. 如何处理 Token 过期？

- 使用 Refresh Token 获取新的 Access Token
- 在前端实现自动刷新逻辑

### 3. 如何实现权限控制？

```python
from rest_framework.permissions import IsAuthenticated

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'This is a protected endpoint'})
```

## 总结

JWT 是一种强大且灵活的认证机制，适合现代 Web 应用。通过合理配置和安全实践，可以构建安全可靠的认证系统。掌握 JWT 的工作原理和最佳实践对于构建安全的应用至关重要。
''',
                'summary': 'JWT (JSON Web Token) 是一种开放标准，用于在各方之间安全地传输信息。本文详细介绍 JWT 的结构、工作流程、在 Django 中的使用、优势、安全考虑以及常见问题。',
                'cover': None,
                'status': 'published',
            },
            {
                'title': 'Elasticsearch 全文搜索实战',
                'content': '''# Elasticsearch 全文搜索实战

## 什么是 Elasticsearch？

Elasticsearch 是一个基于 Lucene 的分布式搜索和分析引擎，适用于实时搜索、日志分析等场景。

## 核心概念

### 索引 (Index)

索引是相似文档的集合，类似于关系数据库中的数据库。

### 文档 (Document)

文档是索引中的基本单位，类似于关系数据库中的行。

### 字段 (Field)

字段是文档中的属性，类似于关系数据库中的列。

### 映射 (Mapping)

映射定义了文档的结构和字段类型。

## 安装和配置

### 安装 Elasticsearch

```bash
# 使用 Docker
docker run -d \
  --name elasticsearch \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
  elasticsearch:8.0.0
```

### 安装 Python 客户端

```bash
pip install elasticsearch
```

### Django 集成

```bash
pip install django-elasticsearch-dsl
```

## 在 Django 中使用 Elasticsearch

### 定义文档

```python
# documents.py
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Article

@registry.register_document
class ArticleDocument(Document):
    class Index:
        name = 'articles'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Article
        fields = [
            'title',
            'summary',
            'content',
        ]
```

### 创建索引

```bash
python manage.py search_index --create
```

### 搜索文档

```python
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://localhost:9200'])

response = es.search(
    index='articles',
    body={
        'query': {
            'multi_match': {
                'query': 'Django',
                'fields': ['title', 'summary', 'content']
            }
        }
    }
)
```

## 搜索查询

### 基本查询

```python
{
    'query': {
        'match': {
            'title': 'Django'
        }
    }
}
```

### 多字段查询

```python
{
    'query': {
        'multi_match': {
            'query': 'Django REST',
            'fields': ['title', 'summary', 'content']
        }
    }
}
```

### 短语查询

```python
{
    'query': {
        'match_phrase': {
            'title': 'Django REST Framework'
        }
    }
}
```

### 布尔查询

```python
{
    'query': {
        'bool': {
            'must': [
                {'match': {'title': 'Django'}},
                {'match': {'content': 'REST'}}
            ],
            'must_not': [
                {'match': {'status': 'draft'}}
            ]
        }
    }
}
```

### 范围查询

```python
{
    'query': {
        'range': {
            'views': {
                'gte': 100,
                'lte': 1000
            }
        }
    }
}
```

## 聚合查询

### 基本聚合

```python
{
    'query': {
        'match_all': {}
    },
    'aggs': {
        'avg_views': {
            'avg': {'field': 'views'}
        }
    }
}
```

### 分组聚合

```python
{
    'query': {
        'match_all': {}
    },
    'aggs': {
        'by_author': {
            'terms': {'field': 'author_name.keyword'}
        }
    }
}
```

## 性能优化

### 1. 索引优化

```python
settings = {
    'number_of_shards': 1,
    'number_of_replicas': 0,
    'analysis': {
        'analyzer': {
            'ik_max_word': {
                'type': 'custom',
                'tokenizer': 'ik_max_word'
            }
        }
    }
}
```

### 2. 查询优化

- 使用 `filter` 代替 `query` 进行精确匹配
- 限制返回字段
- 使用分页

### 3. 缓存

```python
{
    'query': {
        'bool': {
            'filter': [
                {'term': {'status': 'published'}}
            ]
        }
    }
}
```

## 中文分词

### 安装 IK 分词器

```bash
docker exec -it elasticsearch \
  elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v8.0.0/elasticsearch-analysis-ik-8.0.0.zip
```

### 使用 IK 分词

```python
{
    'query': {
        'match': {
            'content': {
                'query': '中文分词',
                'analyzer': 'ik_max_word'
            }
        }
    }
}
```

## 总结

Elasticsearch 是一个强大的全文搜索引擎，适合处理大规模数据的搜索需求。通过合理配置和优化，可以构建高性能的搜索系统。掌握 Elasticsearch 的核心概念和查询语法对于构建优秀的搜索功能至关重要。
''',
                'summary': 'Elasticsearch 是一个基于 Lucene 的分布式搜索和分析引擎。本文详细介绍 Elasticsearch 的核心概念、安装配置、在 Django 中的使用、搜索查询、聚合查询、性能优化和中文分词等内容。',
                'cover': None,
                'status': 'published',
            },
            {
                'title': 'Docker 容器化部署完整指南',
                'content': '''# Docker 容器化部署完整指南

## 什么是 Docker？

Docker 是一个开源的容器化平台，可以将应用及其依赖打包到轻量级、可移植的容器中。

## Docker 的核心概念

### 镜像 (Image)

镜像是应用的只读模板，包含运行应用所需的所有内容。

### 容器 (Container)

容器是镜像的运行实例，可以启动、停止、删除。

### 仓库 (Repository)

仓库是存储和分发镜像的地方，如 Docker Hub。

## 安装 Docker

### Windows

1. 下载 Docker Desktop for Windows
2. 运行安装程序
3. 重启计算机

### Linux

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

## Docker 基本命令

### 镜像操作

```bash
# 拉取镜像
docker pull nginx

# 查看镜像
docker images

# 删除镜像
docker rmi nginx
```

### 容器操作

```bash
# 运行容器
docker run -d -p 80:80 --name my-nginx nginx

# 查看容器
docker ps

# 停止容器
docker stop my-nginx

# 启动容器
docker start my-nginx

# 删除容器
docker rm my-nginx
```

## Dockerfile

### 基本语法

```dockerfile
# 基础镜像
FROM python:3.12

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 多阶段构建

```dockerfile
# 构建阶段
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 运行阶段
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Docker Compose

### 基本配置

```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: blog
      POSTGRES_USER: blog
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://blog:password@db:5432/blog
      REDIS_URL: redis://redis:6379/0

volumes:
  postgres_data:
```

### 常用命令

```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重新构建
docker-compose build
```

## Django 项目 Docker 化

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "blog_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: blog
      POSTGRES_USER: blog
      POSTGRES_PASSWORD: password

  redis:
    image: redis:7

  web:
    build: .
    command: gunicorn blog_backend.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
```

## 最佳实践

1. **使用轻量级基础镜像**
2. **最小化层数**
3. **利用构建缓存**
4. **使用 .dockerignore**
5. **设置合理的资源限制**
6. **使用健康检查**

## 总结

Docker 是现代应用部署的重要工具，通过容器化可以简化部署流程、提高环境一致性。掌握 Docker 的核心概念和最佳实践对于构建可扩展的应用至关重要。
''',
                'summary': 'Docker 是一个开源的容器化平台，可以将应用及其依赖打包到轻量级、可移植的容器中。本文详细介绍 Docker 的核心概念、基本命令、Dockerfile、Docker Compose、Django 项目 Docker 化和最佳实践。',
                'cover': None,
                'status': 'published',
            },
            {
                'title': 'Python 异步编程完全指南',
                'content': '''# Python 异步编程完全指南

## 什么是异步编程？

异步编程是一种编程范式，允许程序在等待某些操作（如 I/O）完成时执行其他任务。

## 同步 vs 异步

### 同步编程

```python
import time

def task(name, duration):
    print(f"开始任务 {name}")
    time.sleep(duration)
    print(f"完成任务 {name}")

task("A", 2)
task("B", 1)
task("C", 3)
```

### 异步编程

```python
import asyncio

async def task(name, duration):
    print(f"开始任务 {name}")
    await asyncio.sleep(duration)
    print(f"完成任务 {name}")

async def main():
    await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 3)
    )

asyncio.run(main())
```

## asyncio 基础

### Event Loop

Event Loop 是异步编程的核心，负责调度和执行协程。

```python
import asyncio

async def hello():
    print("Hello")

loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.close()
```

### 协程 (Coroutine)

协程是使用 `async def` 定义的函数。

```python
async def my_coroutine():
    print("协程开始")
    await asyncio.sleep(1)
    print("协程结束")
```

### await 关键字

`await` 用于暂停协程的执行，等待异步操作完成。

```python
async def fetch_data():
    data = await async_http_client.get('https://api.example.com')
    return data
```

## 并发执行

### asyncio.gather()

```python
import asyncio

async def task(name, delay):
    await asyncio.sleep(delay)
    print(f"任务 {name} 完成")

async def main():
    await asyncio.gather(
        task("A", 1),
        task("B", 2),
        task("C", 1.5)
    )

asyncio.run(main())
```

### asyncio.create_task()

```python
import asyncio

async def task(name, delay):
    await asyncio.sleep(delay)
    print(f"任务 {name} 完成")

async def main():
    task1 = asyncio.create_task(task("A", 1))
    task2 = asyncio.create_task(task("B", 2))
    task3 = asyncio.create_task(task("C", 1.5))
    
    await task1
    await task2
    await task3

asyncio.run(main())
```

## 异步 HTTP 请求

### 使用 aiohttp

```python
import aiohttp
import asyncio

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = [
        'https://api.example.com/1',
        'https://api.example.com/2',
        'https://api.example.com/3',
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            print(result)

asyncio.run(main())
```

### 使用 httpx

```python
import httpx
import asyncio

async def fetch_url(client, url):
    response = await client.get(url)
    return response.text

async def main():
    urls = [
        'https://api.example.com/1',
        'https://api.example.com/2',
        'https://api.example.com/3',
    ]
    
    async with httpx.AsyncClient() as client:
        tasks = [fetch_url(client, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            print(result)

asyncio.run(main())
```

## 异步数据库操作

### 使用 asyncpg (PostgreSQL)

```python
import asyncpg
import asyncio

async def query_database():
    conn = await asyncpg.connect('postgresql://user:password@localhost/db')
    
    rows = await conn.fetch('SELECT * FROM users')
    
    for row in rows:
        print(row)
    
    await conn.close()

asyncio.run(query_database())
```

### 使用 aiomysql (MySQL)

```python
import aiomysql
import asyncio

async def query_database():
    conn = await aiomysql.connect(
        host='localhost',
        user='user',
        password='password',
        db='db'
    )
    
    async with conn.cursor() as cursor:
        await cursor.execute('SELECT * FROM users')
        rows = await cursor.fetchall()
        
        for row in rows:
            print(row)
    
    conn.close()

asyncio.run(query_database())
```

## 异步文件操作

### 使用 aiofiles

```python
import aiofiles
import asyncio

async def read_file(filename):
    async with aiofiles.open(filename, 'r') as f:
        content = await f.read()
        return content

async def write_file(filename, content):
    async with aiofiles.open(filename, 'w') as f:
        await f.write(content)

async def main():
    content = await read_file('input.txt')
    await write_file('output.txt', content)

asyncio.run(main())
```

## 错误处理

### try-except

```python
import asyncio

async def risky_operation():
    try:
        await asyncio.sleep(1)
        raise ValueError("出错了")
    except ValueError as e:
        print(f"捕获到错误: {e}")
    finally:
        print("清理资源")

asyncio.run(risky_operation())
```

### asyncio.wait_for()

```python
import asyncio

async def long_operation():
    await asyncio.sleep(10)

async def main():
    try:
        await asyncio.wait_for(long_operation(), timeout=5.0)
    except asyncio.TimeoutError:
        print("操作超时")

asyncio.run(main())
```

## 最佳实践

1. **避免阻塞操作**：不要在协程中使用阻塞函数
2. **合理使用并发**：不要创建过多的并发任务
3. **正确处理异常**：使用 try-except 处理错误
4. **资源管理**：使用 async with 管理资源
5. **性能测试**：测试异步代码的性能

## 总结

Python 异步编程是构建高性能应用的重要工具。通过合理使用 asyncio 和相关库，可以显著提升 I/O 密集型应用的性能。掌握异步编程的核心概念和最佳实践对于构建高效的应用至关重要。
''',
                'summary': '异步编程是一种编程范式，允许程序在等待某些操作完成时执行其他任务。本文详细介绍 Python 异步编程的基础、asyncio、并发执行、异步 HTTP 请求、异步数据库操作、异步文件操作、错误处理和最佳实践。',
                'cover': None,
                'status': 'published',
            },
        ]

        # 创建文章
        created_count = 0
        for article_data in articles_data:
            # 检查是否已存在相同标题的文章
            if not Article.objects.filter(title=article_data['title']).exists():
                article = Article.objects.create(
                    author=admin_user,
                    **article_data
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ 创建文章: {article.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'✗ 文章已存在: {article_data["title"]}'))

        self.stdout.write(self.style.SUCCESS(f'\n成功创建 {created_count} 篇文章！'))
        self.stdout.write('现在可以访问 http://localhost:5174/ 查看文章列表')