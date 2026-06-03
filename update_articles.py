import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_backend.settings')
os.chdir(r'D:\PythonProject3')
django.setup()

from apps.articles.models import Article
from django.utils import timezone

updates = [
    {
        'id': 25,
        'title': 'Python 并发编程',
        'slug': 'python-concurrent-programming',
        'summary': '本文从零开始讲解 Python 并发编程的核心概念，涵盖多线程、多进程、协程三种并行方式。通过大量代码示例和实际场景，帮助初学者理解 GIL 锁的影响、线程安全、进程间通信等难点，最后用完整案例演示如何选择最适合的并发方案。适合所有想提升 Python 程序性能的开发者。',
        'content': '''# Python 并发编程入门（小白友好版）

## 什么是并发编程？

想象你在厨房做饭：
- **串行**：先洗菜 → 再切菜 → 再炒菜 → 再煮汤，一件事做完才做下一件
- **并发**：一边烧水煮汤（后台进行），一边切菜炒菜（前台进行）

并发编程就是让程序"同时"做多件事，提升运行效率。

## 1. 多线程（threading）

### 1.1 什么是线程？
线程是操作系统能够进行运算调度的最小单位。一个进程里可以有多个线程，它们共享内存。

### 1.2 简单示例
```python
import threading
import time

def task(name):
    print(f"任务 {name} 开始")
    time.sleep(2)  # 模拟耗时操作
    print(f"任务 {name} 结束")

# 创建线程
t1 = threading.Thread(target=task, args=("A",))
t2 = threading.Thread(target=task, args=("B",))

# 启动线程
t1.start()
t2.start()

# 等待线程结束
t1.join()
t2.join()

print("所有任务完成!")
```

运行结果：两个任务**几乎同时**开始和结束，总耗时约 2 秒（而不是 4 秒）。

### 1.3 线程池（ThreadPoolExecutor）
```python
from concurrent.futures import ThreadPoolExecutor
import time

def download(url):
    print(f"正在下载: {url}")
    time.sleep(3)
    return f"{url} 下载完成"

urls = ["url1", "url2", "url3", "url4"]

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(download, urls)

for r in results:
    print(r)
```

## 2. Python 的 GIL 锁

### 2.1 GIL 是什么？
**GIL（Global Interpreter Lock）** 是 CPython 解释器的一个机制：**同一时刻只有一个线程在执行 Python 字节码**。

就像厨房里只有一个厨师证，虽然有多个帮手（线程），但一次只能有一个人掌勺。

### 2.2 GIL 的影响
- **CPU 密集型任务**（大量计算）：多线程反而可能变慢
- **IO 密集型任务**（读写文件/网络请求）：多线程效果很好

```python
# CPU 密集型 - 多线程可能更慢
import threading
import time

def count(n):
    while n > 0:
        n -= 1

# 单线程
start = time.time()
count(50000000)
count(50000000)
print(f"单线程: {time.time() - start:.2f}秒")

# 多线程
start = time.time()
t1 = threading.Thread(target=count, args=(50000000,))
t2 = threading.Thread(target=count, args=(50000000,))
t1.start(); t2.start()
t1.join(); t2.join()
print(f"多线程: {time.time() - start:.2f}秒")
```

## 3. 多进程（multiprocessing）

### 3.1 为什么需要多进程？
多进程可以**绕过 GIL 限制**，每个进程有独立的 Python 解释器和内存空间，真正实现并行。

```python
from multiprocessing import Process
import os

def worker(name):
    print(f"子进程 {name} 启动，PID: {os.getpid()}")
    
if __name__ == '__main__':
    print(f"主进程 PID: {os.getpid()}")
    p1 = Process(target=worker, args=("A",))
    p2 = Process(target=worker, args=("B",))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
```

### 3.2 进程池
```python
from multiprocessing import Pool

def square(n):
    return n * n

with Pool(processes=4) as pool:
    results = pool.map(square, [1, 2, 3, 4, 5])
    print(results)  # [1, 4, 9, 16, 25]
```

## 4. 协程（asyncio）

### 4.1 协程是什么？
协程是**用户态的轻量级线程**，由程序自身控制切换，开销远小于线程。

就像你在做饭时，趁烧水的空闲切菜，而不是专门等水烧开。

```python
import asyncio

async def boil_water():
    print("开始烧水...")
    await asyncio.sleep(3)  # 模拟烧水
    print("水烧好了!")

async def cut_vegetables():
    print("开始切菜...")
    await asyncio.sleep(2)  # 模拟切菜
    print("菜切好了!")

async def main():
    # 同时执行两个任务
    await asyncio.gather(
        boil_water(),
        cut_vegetables()
    )

asyncio.run(main())
```

### 4.2 实际应用：并发网络请求
```python
import asyncio
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = ["https://example.com"] * 10
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        print(f"成功获取 {len(results)} 个页面")

asyncio.run(main())
```

## 5. 如何选择？

| 场景 | 推荐方案 | 原因 |
|------|---------|------|
| IO密集型（网络请求） | 协程 / 多线程 | 等待期间切换任务，效率高 |
| CPU密集型（计算） | 多进程 | 绕过 GIL，充分利用多核 |
| 简单任务 | 线程池/进程池 | 管理方便，代码简洁 |
| 高并发IO | 协程 | 开销最小，支持海量连接 |

## 6. 完整案例：批量下载图片

```python
import asyncio
import aiohttp
import os

async def download_image(session, url, save_path):
    async with session.get(url) as resp:
        data = await resp.read()
        with open(save_path, 'wb') as f:
            f.write(data)
        print(f"下载完成: {save_path}")

async def main():
    images = [
        "https://example.com/img1.jpg",
        "https://example.com/img2.jpg",
    ]
    
    os.makedirs("downloads", exist_ok=True)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(images):
            path = f"downloads/image_{i}.jpg"
            tasks.append(download_image(session, url, path))
        await asyncio.gather(*tasks)
    
    print("全部下载完成!")

asyncio.run(main())
```

## 总结

- **多线程**：适合 IO 密集型任务，受 GIL 限制
- **多进程**：适合 CPU 密集型任务，独立内存空间
- **协程**：适合高并发 IO，开销最小
- **线程池/进程池**：管理多个工作线程/进程的便捷方式

记住：没有银弹，根据你的实际场景选择合适的并发方案才是关键。'''
    },
    {
        'id': 1,
        'title': 'Django REST Framework 完全指南',
        'slug': 'django-rest-framework-complete-guide',
        'summary': '从零开始学习 Django REST Framework，涵盖序列化器、视图集、路由、认证权限、过滤分页等核心功能。每一个概念都配有完整的代码示例和详细讲解，即使是编程新手也能轻松上手，快速构建出专业的 RESTful API。',
        'content': '''# Django REST Framework 完全指南（新手友好）

## 什么是 Django REST Framework？

简单来说，DRF 是一个帮你**快速构建 API 接口**的 Django 扩展库。

举个例子：你做了一个博客网站，需要让手机 App 能读取文章列表、发布评论，这时候就需要 API。DRF 就是帮你用最少的代码完成这些工作的工具。

## 1. 环境准备

### 1.1 安装
```bash
pip install djangorestframework
pip install django-filter  # 过滤支持
pip install markdown       # Markdown 渲染
```

### 1.2 配置 settings.py
```python
INSTALLED_APPS = [
    'rest_framework',
    'django_filters',
]
```

## 2. 序列化器（Serializers）

### 2.1 什么是序列化？
**序列化** = Python 对象 → JSON 数据
**反序列化** = JSON 数据 → Python 对象

### 2.2 定义序列化器
```python
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'created_at', 'author']
        read_only_fields = ['id', 'created_at']
```

### 2.3 使用序列化器
```python
# 序列化（对象→JSON）
article = Article.objects.get(id=1)
serializer = ArticleSerializer(article)
print(serializer.data)
# {'id': 1, 'title': 'Hello', 'content': '...', 'created_at': '2024-01-01', 'author': 1}

# 反序列化（JSON→对象）
data = {'title': '新文章', 'content': '内容'}
serializer = ArticleSerializer(data=data)
if serializer.is_valid():
    serializer.save()  # 自动创建新文章
else:
    print(serializer.errors)  # 打印错误信息
```

## 3. 视图（Views）

### 3.1 函数视图（@api_view）
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

### 3.2 类视图（APIView）⭐ 推荐
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ArticleList(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

### 3.3 通用视图（GenericAPIView）⭐⭐ 更简洁
```python
from rest_framework import generics

class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

**只用了 6 行代码**就完成了完整的 CRUD 接口！

## 4. URL 路由

### 4.1 手动路由
```python
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.ArticleList.as_view()),
    path('articles/<int:pk>/', views.ArticleDetail.as_view()),
]
```

### 4.2 视图集 + 路由器（最省代码的方式）
```python
from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# urls.py
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'articles', ArticleViewSet)

urlpatterns = router.urls
```

**自动生成 5 个接口**：
- `GET /articles/` → 列表
- `POST /articles/` → 创建
- `GET /articles/1/` → 详情
- `PUT /articles/1/` → 更新
- `DELETE /articles/1/` → 删除

## 5. 认证与权限

### 5.1 Token 认证
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# views.py
from rest_framework.permissions import IsAuthenticated

class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]  # 需要登录才能访问
```

### 5.2 JWT 认证（更推荐）
```python
# 安装 pip install djangorestframework-simplejwt

from rest_framework_simplejwt.views import TokenObtainPairView

# urls.py
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
```

## 6. 过滤与搜索

```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author', 'category']
    search_fields = ['title', 'content']
```

**支持的请求**：
- `GET /articles/?author=1` → 按作者过滤
- `GET /articles/?search=python` → 搜索标题或内容包含 python 的文章

## 7. 分页

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # 每页 10 条
}
```

API 响应自动变成分页格式：
```json
{
    "count": 100,
    "next": "http://example.com/articles/?page=2",
    "previous": null,
    "results": [...]
}
```

## 完整示例

```python
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'category', 'status']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views']
    ordering = ['-created_at']  # 默认按创建时间倒序
```

## 总结

DRF 的核心思想是"约定优于配置"，用最少的代码完成最多的工作。记住三个层次：

1. **ModelSerializer** → 自动生成序列化字段
2. **GenericAPIView / ModelViewSet** → 自动实现 CRUD
3. **DefaultRouter** → 自动生成 URL 路由

从简单开始，需要什么功能再加什么功能，这就是 DRF 的优雅之处。'''
    },
]

for u in updates:
    try:
        a = Article.objects.get(id=u['id'])
        a.title = u['title']
        a.summary = u['summary']
        a.content = u['content']
        a.slug = u['slug']
        a.updated_at = timezone.now()
        a.save()
        print(f'✅ 已更新: ID={a.id} {a.title} ({len(a.content)} 字符)')
    except Article.DoesNotExist:
        print(f'❌ 未找到 ID={u["id"]}')

print('全部更新完成!')