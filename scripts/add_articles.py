import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_backend.settings')
django.setup()

from apps.articles.models import Article
from django.contrib.auth.models import User

try:
    user = User.objects.get(username='admin')
except User.DoesNotExist:
    user = User.objects.create_superuser('admin', 'admin@example.com', 'password')

articles_data = [
    {
        'title': 'Python 装饰器完全指南',
        'summary': '深入理解 Python 装饰器的原理和应用，包括函数装饰器、类装饰器、装饰器工厂等高级用法。',
        'content': '# Python 装饰器完全指南\n\n## 什么是装饰器\n\n装饰器是 Python 中一种强大的语法特性，用于修改或增强函数、方法或类的行为。\n\n## 基本语法\n\n```python\ndef decorator(func):\n    def wrapper(*args, **kwargs):\n        result = func(*args, **kwargs)\n        return result\n    return wrapper\n```\n\n## 装饰器的应用场景\n\n1. **日志记录** - 自动记录函数调用日志\n2. **性能监控** - 统计函数执行时间\n3. **权限验证** - 检查用户权限\n4. **缓存** - 缓存函数返回结果\n\n装饰器是 Python 中实现代码复用的重要工具。'
    },
    {
        'title': 'Django ORM 高级查询技巧',
        'summary': '掌握 Django ORM 的高级查询技巧，包括 Q 对象、F 对象、聚合查询、子查询等。',
        'content': '# Django ORM 高级查询技巧\n\n## Q 对象\n\nQ 对象允许你使用复杂的逻辑表达式进行查询：\n\n```python\nfrom django.db.models import Q\n\nArticle.objects.filter(Q(title__icontains='python') | Q(summary__icontains='python'))\n```\n\n## F 对象\n\nF 对象允许你引用模型字段的值：\n\n```python\nfrom django.db.models import F\nArticle.objects.filter(id=1).update(views=F('views') + 1)\n```\n\n## 聚合查询\n\n```python\nfrom django.db.models import Count, Avg\nArticle.objects.values('author').annotate(count=Count('id'))\n```'
    },
    {
        'title': 'Vue3 响应式原理详解',
        'summary': '深入剖析 Vue3 的响应式系统，理解 Proxy、Ref、Reactive 的工作原理。',
        'content': '# Vue3 响应式原理详解\n\n## 响应式基础\n\nVue3 使用 ES6 的 Proxy 对象来实现响应式系统：\n\n```javascript\nconst proxy = new Proxy(target, {\n  get(target, key) {\n    track(target, key)\n    return target[key]\n  },\n  set(target, key, value) {\n    target[key] = value\n    trigger(target, key)\n    return true\n  }\n})\n```\n\n## Ref 和 Reactive\n\n```javascript\nimport { ref, reactive } from 'vue'\n\nconst count = ref(0)\nconst state = reactive({ count: 0 })\n```'
    },
    {
        'title': 'Docker 多阶段构建最佳实践',
        'summary': '学习 Docker 多阶段构建技术，优化镜像大小，提升部署效率。',
        'content': '# Docker 多阶段构建最佳实践\n\n## 什么是多阶段构建\n\n多阶段构建允许你在一个 Dockerfile 中使用多个 FROM 语句，每个阶段可以使用不同的基础镜像。\n\n## 基础示例\n\n```dockerfile\nFROM node:18 AS builder\nWORKDIR /app\nCOPY package*.json ./\nRUN npm ci\nCOPY . .\nRUN npm run build\n\nFROM nginx:alpine\nCOPY --from=builder /app/dist /usr/share/nginx/html\n```\n\n## 优势\n\n1. **减小镜像大小** - 只保留必要的运行时依赖\n2. **提高安全性** - 不包含构建工具\n3. **缓存优化** - 利用 Docker 层缓存'
    },
    {
        'title': 'Redis 数据结构实战',
        'summary': '深入了解 Redis 的各种数据结构，包括 String、List、Hash、Set、Sorted Set 的应用场景。',
        'content': '# Redis 数据结构实战\n\n## String 字符串\n\n```bash\nSET user:1:name 'John'\nGET user:1:name\nINCR counter:page:home\n```\n\n## List 列表\n\n```bash\nLPUSH queue:tasks 'task1'\nRPOP queue:tasks\n```\n\n## Hash 哈希\n\n```bash\nHSET user:1 name 'John' age 30\nHGETALL user:1\n```\n\n## Set 集合\n\n```bash\nSADD set:tags 'python' 'django'\nSMEMBERS set:tags\n```\n\n## Sorted Set 有序集合\n\n```bash\nZADD leaderboard 100 'Alice' 95 'Bob'\nZRANGE leaderboard 0 2 WITHSCORES\n```'
    },
    {
        'title': 'Git 工作流最佳实践',
        'summary': '学习团队协作中常用的 Git 工作流，包括 Git Flow、GitHub Flow、GitLab Flow。',
        'content': '# Git 工作流最佳实践\n\n## Git Flow\n\nGit Flow 是一种经典的分支管理策略：\n\n- main (主分支)\n- develop (开发分支)\n- feature/* (功能分支)\n- release/* (发布分支)\n- hotfix/* (热修复分支)\n\n## GitHub Flow\n\nGitHub Flow 更加简洁：\n\n1. 从 main 创建分支\n2. 提交更改\n3. 创建 Pull Request\n4. 代码审查\n5. 合并到 main\n\n## 提交信息规范\n\n使用 Conventional Commits：\n\n- feat: 新功能\n- fix: 修复bug\n- docs: 文档更新\n- refactor: 重构'
    },
    {
        'title': 'Linux 性能调优入门',
        'summary': '学习 Linux 系统性能监控和调优的基本方法，包括 CPU、内存、磁盘、网络优化。',
        'content': '# Linux 性能调优入门\n\n## CPU 监控\n\n```bash\ntop\nmpstat 1 10\nvmstat 1 10\n```\n\n## 内存监控\n\n```bash\nfree -h\n```\n\n## 磁盘 I/O\n\n```bash\niostat -x 1 10\niotop\n```\n\n## 网络监控\n\n```bash\nnetstat -tuln\nss -tuln\n```\n\n## 常用调优参数\n\n编辑 /etc/sysctl.conf：\n\n```conf\nnet.ipv4.tcp_tw_reuse = 1\nnet.ipv4.tcp_fin_timeout = 30\nnet.core.somaxconn = 65535\n```'
    },
    {
        'title': 'RESTful API 设计规范',
        'summary': '掌握 RESTful API 的设计原则和最佳实践，包括资源命名、HTTP 方法、状态码等。',
        'content': '# RESTful API 设计规范\n\n## 资源命名\n\n- 使用名词，而非动词\n- 使用复数形式\n\n```\nGET /api/users\nGET /api/posts/1/comments\n```\n\n## HTTP 方法\n\n| 方法 | 操作 |\n|------|------|\n| GET | 获取资源 |\n| POST | 创建资源 |\n| PUT | 更新资源 |\n| PATCH | 部分更新 |\n| DELETE | 删除资源 |\n\n## 状态码\n\n| 状态码 | 含义 |\n|--------|------|\n| 200 | 请求成功 |\n| 201 | 创建成功 |\n| 400 | 请求错误 |\n| 401 | 未授权 |\n| 404 | 资源不存在 |\n| 500 | 服务器错误 |'
    },
    {
        'title': '单元测试最佳实践',
        'summary': '学习编写高质量单元测试的方法，包括测试覆盖率、Mock、测试模式等。',
        'content': '# 单元测试最佳实践\n\n## AAA 模式\n\n```python\ndef test_add_two_numbers():\n    # Arrange - 准备测试数据\n    calculator = Calculator()\n    \n    # Act - 执行测试\n    result = calculator.add(2, 3)\n    \n    # Assert - 断言结果\n    assert result == 5\n```\n\n## Mock 的使用\n\n```python\nfrom unittest.mock import patch\n\nwith patch('requests.get') as mock_get:\n    mock_get.return_value.status_code = 200\n    result = get_user(1)\n```\n\n## 参数化测试\n\n```python\nimport pytest\n\n@pytest.mark.parametrize('input1, input2, expected', [\n    (1, 2, 3),\n    (0, 0, 0),\n    (-1, 1, 0)\n])\ndef test_add(input1, input2, expected):\n    assert add(input1, input2) == expected\n```'
    },
    {
        'title': '数据库索引优化',
        'summary': '深入理解数据库索引的工作原理，学习索引设计和查询优化的最佳实践。',
        'content': '# 数据库索引优化\n\n## 索引类型\n\n### B-Tree 索引\n\n```sql\nCREATE INDEX idx_users_name ON users(name);\n```\n\n### 复合索引\n\n```sql\nCREATE INDEX idx_orders_user_date ON orders(user_id, created_at);\n```\n\n## 索引设计原则\n\n### 最左前缀原则\n\n索引 (a, b, c)：\n- WHERE a = 1 ✅\n- WHERE a = 1 AND b = 2 ✅\n- WHERE b = 2 ❌\n\n### 索引选择性\n\n高选择性适合索引，低选择性不适合索引。\n\n## 查询优化\n\n```sql\nEXPLAIN SELECT * FROM orders WHERE user_id = 1;\n```\n\n避免在索引列上使用函数。'
    },
    {
        'title': '消息队列入门与实践',
        'summary': '了解消息队列的基本概念和使用场景，学习 RabbitMQ、Kafka 的基本用法。',
        'content': '# 消息队列入门与实践\n\n## 消息队列的作用\n\n1. **解耦** - 生产者和消费者解耦\n2. **异步** - 异步处理任务\n3. **削峰** - 处理突发流量\n4. **重试** - 失败自动重试\n\n## RabbitMQ 入门\n\n```python\nimport pika\n\nconnection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))\nchannel = connection.channel()\nchannel.queue_declare(queue='hello')\nchannel.basic_publish(exchange='', routing_key='hello', body='Hello!')\n```\n\n## Kafka 入门\n\n```bash\nkafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092\nkafka-console-producer.sh --broker-list localhost:9092 --topic test-topic\nkafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test-topic\n```'
    },
    {
        'title': 'CI/CD 实践指南',
        'summary': '学习持续集成和持续部署的最佳实践，包括 GitHub Actions、GitLab CI 的使用。',
        'content': '# CI/CD 实践指南\n\n## CI/CD 流程\n\n代码提交 → 构建 → 测试 → 部署\n\n## GitHub Actions\n\n```yaml\nname: CI/CD\n\non:\n  push:\n    branches: [ main ]\n\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n    - uses: actions/checkout@v4\n    - name: Set up Python\n      uses: actions/setup-python@v5\n      with:\n        python-version: '3.11'\n    - run: pip install -r requirements.txt\n    - run: pytest\n```\n\n## 部署策略\n\n- 蓝绿部署\n- 滚动部署\n- 金丝雀部署'
    },
    {
        'title': 'Python 并发编程',
        'summary': '学习 Python 并发编程的多种方式，包括多线程、多进程、协程等。',
        'content': '# Python 并发编程\n\n## 多线程\n\n```python\nimport threading\n\ndef worker():\n    print('Working...')\n\nthread = threading.Thread(target=worker)\nthread.start()\nthread.join()\n```\n\n## 多进程\n\n```python\nimport multiprocessing\n\ndef worker():\n    print('Working...')\n\nprocess = multiprocessing.Process(target=worker)\nprocess.start()\nprocess.join()\n```\n\n## 协程\n\n```python\nimport asyncio\n\nasync def worker():\n    print('Working...')\n    await asyncio.sleep(1)\n\nasyncio.run(worker())\n```\n\n## asyncio\n\n```python\nasync def fetch(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as response:\n            return await response.text()\n```'
    },
    {
        'title': 'Web 安全入门',
        'summary': '了解常见的 Web 安全漏洞，包括 XSS、CSRF、SQL 注入等的防护方法。',
        'content': '# Web 安全入门\n\n## XSS 攻击\n\n跨站脚本攻击，攻击者在网页中注入恶意脚本。\n\n### 防护方法\n\n- 输入过滤\n- 输出转义\n- 使用 CSP (内容安全策略)\n\n## CSRF 攻击\n\n跨站请求伪造，攻击者诱导用户执行非预期的操作。\n\n### 防护方法\n\n- 使用 CSRF Token\n- 验证 Referer\n- 使用 SameSite Cookie\n\n## SQL 注入\n\n攻击者通过输入恶意 SQL 语句来攻击数据库。\n\n### 防护方法\n\n- 使用参数化查询\n- 使用 ORM\n- 输入验证\n\n## 其他安全措施\n\n- 使用 HTTPS\n- 密码哈希存储\n- 定期安全审计'
    },
    {
        'title': 'React 状态管理',
        'summary': '学习 React 中的状态管理方案，包括 useState、useContext、Redux、Zustand 等。',
        'content': '# React 状态管理\n\n## useState\n\n```jsx\nimport { useState } from 'react'\n\nfunction Counter() {\n  const [count, setCount] = useState(0)\n  return (\n    <button onClick={() => setCount(c => c + 1)}>\n      Count: {count}\n    </button>\n  )\n}\n```\n\n## useContext\n\n```jsx\nconst ThemeContext = createContext('light')\n\nfunction App() {\n  return (\n    <ThemeContext.Provider value='dark'>\n      <ThemedButton />\n    </ThemeContext.Provider>\n  )\n}\n```\n\n## Zustand\n\n```jsx\nimport { create } from 'zustand'\n\nconst useStore = create((set) => ({\n  count: 0,\n  increment: () => set((state) => ({ count: state.count + 1 }))\n}))\n```'
    }
]

for i, data in enumerate(articles_data):
    days_ago = i * 2
    
    article = Article.objects.create(
        title=data['title'],
        summary=data['summary'],
        content=data['content'],
        author=user,
        status='published',
        created_at=datetime.now() - timedelta(days=days_ago),
        updated_at=datetime.now() - timedelta(days=days_ago),
        views=random.randint(10, 500)
    )
    print(f'Created article: {article.title}')

print(f'Successfully created {len(articles_data)} articles!')
