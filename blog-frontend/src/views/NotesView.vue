<script setup>
import { ref, computed } from 'vue'
import { useSeo } from '@/composables/useSeo'

const { setSeo } = useSeo()

const activeCategory = ref('all')
const searchQuery = ref('')
const expandedId = ref(null)

const categories = [
  { key: 'all', label: '全部', icon: '📋' },
  { key: 'python', label: 'Python', icon: '🐍' },
  { key: 'django', label: 'Django', icon: '🎸' },
  { key: 'vue', label: 'Vue', icon: '💚' },
  { key: 'docker', label: 'Docker', icon: '🐳' },
  { key: 'git', label: 'Git', icon: '🔀' },
  { key: 'linux', label: 'Linux', icon: '🐧' },
  { key: 'database', label: '数据库', icon: '🗄️' },
  { key: 'network', label: '网络/部署', icon: '🌐' },
  { key: 'tools', label: '工具', icon: '🔧' },
]

const notes = [
  {
    id: 1,
    title: 'Python 禁用 SSL 证书验证警告',
    category: 'python',
    tags: ['requests', 'SSL', '警告'],
    problem: '使用 requests 设置 verify=False 时，urllib3 会持续输出 InsecureRequestWarning 警告信息，污染日志输出。',
    solution: '导入 urllib3 的 InsecureRequestWarning 并禁用警告',
    code: `import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

resp = requests.get('https://example.com', verify=False)`,
  },
  {
    id: 2,
    title: 'Python 创建虚拟环境到指定目录',
    category: 'python',
    tags: ['venv', '虚拟环境'],
    problem: '需要在指定路径创建 Python 虚拟环境，并指定 Python 解释器版本。',
    solution: '使用 python -m venv 命令指定目标路径',
    code: `# Windows
python -m venv D:\\projects\\myenv

# Linux/macOS
python3 -m venv /opt/myenv

# 激活虚拟环境
# Windows:
myenv\\Scripts\\activate
# Linux/macOS:
source myenv/bin/activate`,
  },
  {
    id: 3,
    title: 'Python pip 安装超时或速度慢',
    category: 'python',
    tags: ['pip', '镜像源'],
    problem: 'pip 默认从 PyPI 官方源下载，国内访问速度极慢甚至超时失败。',
    solution: '配置国内镜像源，推荐清华、阿里云镜像',
    code: `# 临时使用镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple django

# 永久配置镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 常用镜像源：
# 清华: https://pypi.tuna.tsinghua.edu.cn/simple
# 阿里云: https://mirrors.aliyun.com/pypi/simple
# 豆瓣: https://pypi.douban.com/simple`,
  },
  {
    id: 4,
    title: 'Python 编码错误 UnicodeDecodeError',
    category: 'python',
    tags: ['编码', 'Unicode'],
    problem: '读取文件时出现 UnicodeDecodeError: \'gbk\' codec can\'t decode byte... 或 \'utf-8\' codec can\'t decode...',
    solution: '显式指定文件编码为 utf-8，或使用 errors 参数忽略错误',
    code: `# 方法1：指定编码
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 方法2：忽略无法解码的字符
with open('file.txt', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 方法3：自动检测编码
import chardet
with open('file.txt', 'rb') as f:
    result = chardet.detect(f.read())
    encoding = result['encoding']`,
  },
  {
    id: 5,
    title: 'Python 多进程在 Windows 下报错',
    category: 'python',
    tags: ['multiprocessing', 'Windows'],
    problem: '在 Windows 下使用 multiprocessing 报 RuntimeError 或程序重复执行。',
    solution: 'Windows 下必须使用 if __name__ == "__main__" 保护入口代码',
    code: `from multiprocessing import Process

def worker(name):
    print(f'Worker {name} running')

if __name__ == '__main__':
    p = Process(target=worker, args=('test',))
    p.start()
    p.join()`,
  },
  {
    id: 6,
    title: 'Django 迁移报错或迁移冲突',
    category: 'django',
    tags: ['migrate', '迁移'],
    problem: '执行 makemigrations/migrate 时报错，或迁移文件冲突导致无法继续。',
    solution: '根据不同情况选择合适的修复方式',
    code: `# 1. 查看迁移状态
python manage.py showmigrations

# 2. 伪造迁移（数据库已有表但Django不知道）
python manage.py migrate --fake app_name 0001

# 3. 回滚到指定迁移
python manage.py migrate app_name 0002

# 4. 彻底重置迁移（开发环境，会丢数据！）
# 删除所有迁移文件和数据库，重新来过
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate

# 5. 检查是否有未应用的迁移
python manage.py migrate --list`,
  },
  {
    id: 7,
    title: 'Django CORS 跨域请求被拒绝',
    category: 'django',
    tags: ['CORS', '跨域'],
    problem: '前端请求后端 API 时浏览器报 CORS policy: No Access-Control-Allow-Origin 错误。',
    solution: '安装 django-cors-headers 并正确配置',
    code: `# 1. 安装
pip install django-cors-headers

# 2. settings.py 配置
INSTALLED_APPS = [
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 必须放在最前面
    'django.middleware.common.CommonMiddleware',
    ...
]

# 3. 允许的域名（开发环境可允许所有）
CORS_ALLOW_ALL_ORIGINS = True  # 仅开发环境

# 生产环境指定域名
CORS_ALLOWED_ORIGINS = [
    'https://yourdomain.com',
    'http://localhost:5173',
]

# 4. 允许携带Cookie
CORS_ALLOW_CREDENTIALS = True`,
  },
  {
    id: 8,
    title: 'Django STATIC 和 MEDIA 文件 404',
    category: 'django',
    tags: ['静态文件', 'MEDIA'],
    problem: '部署后静态文件或上传的媒体文件返回 404 Not Found。',
    solution: '检查 STATIC/MEDIA 配置和 URL 路由',
    code: `# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# urls.py（开发环境提供media服务）
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 生产环境收集静态文件
python manage.py collectstatic

# Nginx 配置静态文件服务
# location /static/ { alias /path/to/staticfiles/; }
# location /media/ { alias /path/to/media/; }`,
  },
  {
    id: 9,
    title: 'Django 时区问题导致时间差8小时',
    category: 'django',
    tags: ['时区', 'TIME_ZONE'],
    problem: '数据库中存储的时间和实际时间差8小时，或前端显示时间不正确。',
    solution: '正确配置时区设置，注意 USE_TZ 的影响',
    code: `# settings.py
TIME_ZONE = 'Asia/Shanghai'
USE_TZ = True  # 推荐开启，数据库存UTC，显示时转换

# 如果 USE_TZ=True，在模板/序列化器中转换时区
from django.utils import timezone
now = timezone.now()  # UTC时间
local_time = now.astimezone(timezone.get_current_timezone())

# 如果不想用时区（不推荐）
USE_TZ = False
TIME_ZONE = 'Asia/Shanghai'

# 前端显示时转换UTC时间
# JavaScript:
const localTime = new Date(utcTimeStr).toLocaleString('zh-CN')`,
  },
  {
    id: 10,
    title: 'Django Debug=False 后 500 错误',
    category: 'django',
    tags: ['部署', 'DEBUG'],
    problem: '开发环境正常，设置 DEBUG=False 后页面返回 500 Server Error。',
    solution: 'DEBUG=False 时必须配置 ALLOWED_HOSTS，且静态文件需单独处理',
    code: `# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', '127.0.0.1']

# 常见原因排查：
# 1. ALLOWED_HOSTS 未配置 → 400 Bad Request
# 2. 静态文件未收集 → css/js 404
python manage.py collectstatic

# 3. 查看具体错误（临时开启日志）
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {'handlers': ['file'], 'level': 'DEBUG'},
    },
}`,
  },
  {
    id: 11,
    title: 'Vue3 组件间通信方式总结',
    category: 'vue',
    tags: ['组件通信', 'props', 'emit'],
    problem: '不同层级的 Vue 组件之间需要传递数据，不知道该用哪种方式。',
    solution: '根据组件关系选择合适的通信方式',
    code: `# 1. 父→子：Props
# Parent.vue
<Child :message="msg" />
# Child.vue
const props = defineProps({ message: String })

# 2. 子→父：Emit
# Child.vue
const emit = defineEmits(['update'])
emit('update', newValue)
# Parent.vue
<Child @update="handleUpdate" />

# 3. 跨层级：Provide/Inject
# 祖先组件
provide('theme', ref('dark'))
# 后代组件
const theme = inject('theme')

# 4. 全局状态：Pinia
# stores/counter.js
export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  return { count }
})
# 任意组件
const store = useCounterStore()`,
  },
  {
    id: 12,
    title: 'Vue3 ref 和 reactive 的区别与选择',
    category: 'vue',
    tags: ['ref', 'reactive', '响应式'],
    problem: '不确定该用 ref 还是 reactive 来定义响应式数据。',
    solution: 'ref 用于基本类型和需要重新赋值的对象，reactive 用于不需要重新赋值的复杂对象',
    code: `# ref：可重新赋值，.value 访问
const count = ref(0)
count.value++
const user = ref({ name: 'Tom' })
user.value = { name: 'Jerry' }  // 可以整体替换

# reactive：不需要 .value，但不能整体替换
const state = reactive({ count: 0, list: [] })
state.count++
state.list.push('item')  // OK
// state = { count: 0 }  // 错误！丢失响应式

# 推荐做法：
# 基本类型 → ref
# 对象且需要替换 → ref
# 对象且只修改属性 → reactive
# 从函数返回 → ref（更灵活）`,
  },
  {
    id: 13,
    title: 'Vue3 Vite 开发代理配置',
    category: 'vue',
    tags: ['Vite', '代理', 'proxy'],
    problem: '前端请求后端 API 时出现跨域错误或 404。',
    solution: '在 vite.config.js 中配置开发服务器代理',
    code: `// vite.config.js
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8001',
        changeOrigin: true,
      },
      '/media': {
        target: 'http://127.0.0.1:8001',
        changeOrigin: true,
      },
    }
  }
})

// 前端请求直接用相对路径
axios.get('/api/articles/')
// 实际请求会被代理到 http://127.0.0.1:8001/api/articles/`,
  },
  {
    id: 14,
    title: 'Vue3 路由守卫与权限控制',
    category: 'vue',
    tags: ['路由', '守卫', '权限'],
    problem: '需要根据用户登录状态或角色控制页面访问权限。',
    solution: '使用 Vue Router 的 beforeEach 全局守卫',
    code: `// router/index.js
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.guestOnly && isAuthenticated) {
    next({ name: 'home' })
  } else {
    next()
  }
})

// 路由定义
{
  path: '/admin',
  component: AdminView,
  meta: { requiresAuth: true }
}

// 路由后置守卫：设置页面标题
router.afterEach((to) => {
  document.title = to.meta.title || 'My App'
})`,
  },
  {
    id: 15,
    title: 'Docker 镜像拉取慢或失败',
    category: 'docker',
    tags: ['镜像', '代理', 'pull'],
    problem: 'docker pull 拉取镜像速度极慢或连接超时。',
    solution: '配置 Docker 镜像加速器或使用代理站点',
    code: `# 方法1：配置镜像加速器
# 编辑 /etc/docker/daemon.json（Linux）
# 或 Docker Desktop → Settings → Docker Engine
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}

# 重启 Docker
sudo systemctl restart docker

# 方法2：使用代理站点拉取
docker pull dockerproxy.net/library/nginx:latest
docker tag dockerproxy.net/library/nginx:latest nginx:latest

# 方法3：手动导入导出
docker save -o nginx.tar nginx:latest
docker load -i nginx.tar`,
  },
  {
    id: 16,
    title: 'Docker 清理 <none> 镜像和空间',
    category: 'docker',
    tags: ['清理', 'images', '磁盘'],
    problem: 'Docker 占用磁盘空间越来越大，存在大量 <none> 镜像和停止的容器。',
    solution: '使用 docker system prune 或精确清理',
    code: `# 查看 Docker 磁盘占用
docker system df

# 清理悬空镜像（<none>）
docker image prune -f

# 精确删除悬空镜像
docker rmi $(docker images -f "dangling=true" -q)

# 清理停止的容器
docker container prune -f

# 清理未使用的网络
docker network prune -f

# 一键清理所有未使用资源（慎用！）
docker system prune -a --volumes -f

# 查看具体镜像大小
docker images --format "table {{.Repository}}\\t{{.Tag}}\\t{{.Size}}" | sort -k3 -h`,
  },
  {
    id: 17,
    title: 'Docker 容器内无法连接宿主机服务',
    category: 'docker',
    tags: ['网络', 'host', '连接'],
    problem: 'Docker 容器内访问宿主机的 MySQL/Redis 等服务时连接被拒绝。',
    solution: '使用 host.docker.internal 或宿主机 IP 连接',
    code: `# 方法1：使用特殊域名（Docker Desktop）
# 在容器内连接宿主机
mysql -h host.docker.internal -P 3306 -u root -p

# 方法2：获取宿主机 IP（Linux）
ip addr show docker0 | grep inet
# 通常是 172.17.0.1

# 方法3：使用 host 网络模式
docker run --network host nginx

# docker-compose.yml 示例
services:
  app:
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      - DB_HOST=host.docker.internal`,
  },
  {
    id: 18,
    title: 'Git 撤销最后一次 commit',
    category: 'git',
    tags: ['commit', '撤销', 'reset'],
    problem: '提交了错误的代码，需要撤销最后一次 commit。',
    solution: '根据是否已推送选择不同的撤销方式',
    code: `# 未推送到远程：撤销commit，保留修改
git reset --soft HEAD~1

# 未推送到远程：撤销commit，丢弃修改（危险！）
git reset --hard HEAD~1

# 已推送到远程：创建反向commit
git revert HEAD

# 撤销最近N个commit（未推送）
git reset --soft HEAD~3

# 修改最后一次commit信息
git commit --amend -m "新的commit信息"

# 查看操作历史（可恢复误删commit）
git reflog
git reset --hard abc1234`,
  },
  {
    id: 19,
    title: 'Git 合并冲突解决流程',
    category: 'git',
    tags: ['冲突', 'merge', '解决'],
    problem: 'git merge 或 git pull 时出现合并冲突，不知道如何处理。',
    solution: '按步骤查看冲突文件、手动解决、标记完成',
    code: `# 1. 查看冲突文件
git status

# 2. 打开冲突文件，找到冲突标记
# <<<<<<< HEAD
# 当前分支的代码
# =======
# 合并分支的代码
# >>>>>>> feature-branch

# 3. 手动编辑，保留需要的代码，删除冲突标记

# 4. 标记冲突已解决
git add <冲突文件>

# 5. 完成合并
git commit

# 使用 VS Code 等工具可视化解决冲突更方便
# 推荐插件：GitLens

# 放弃合并，回到合并前
git merge --abort`,
  },
  {
    id: 20,
    title: 'Git .gitignore 不生效',
    category: 'git',
    tags: ['gitignore', '缓存'],
    problem: '已添加 .gitignore 规则，但之前跟踪的文件仍然被 Git 管理。',
    solution: '清除 Git 缓存后重新添加',
    code: `# 清除所有Git缓存
git rm -r --cached .

# 重新添加所有文件
git add .

# 提交
git commit -m "fix: update .gitignore"

# 只清除特定文件缓存
git rm --cached config/local_settings.py
git rm --cached -r node_modules/

# 常用 .gitignore 规则
__pycache__/
*.pyc
.env
node_modules/
dist/
*.sqlite3
media/`,
  },
  {
    id: 21,
    title: 'Linux 查看端口占用和释放端口',
    category: 'linux',
    tags: ['端口', 'lsof', 'kill'],
    problem: '启动服务时提示端口被占用，需要找到并释放端口。',
    solution: '使用 lsof 或 netstat 查找占用进程并 kill',
    code: `# 查看指定端口占用
lsof -i :8001
# 或
netstat -tunlp | grep 8001
# 或
ss -tunlp | grep 8001

# 杀掉占用进程
kill -9 <PID>

# 查看所有监听端口
netstat -tunlp

# 查看指定进程的端口
lsof -p <PID>

# 批量杀掉某端口的进程
fuser -k 8001/tcp`,
  },
  {
    id: 22,
    title: 'Linux 文件权限与 chmod 用法',
    category: 'linux',
    tags: ['权限', 'chmod', 'chown'],
    problem: '执行脚本或访问文件时提示 Permission denied。',
    solution: '使用 chmod 修改文件权限，chown 修改文件所有者',
    code: `# 查看文件权限
ls -la filename
# -rwxr-xr-x  所有者读写执行，组和其他读执行

# 数字方式设置权限
chmod 755 script.sh  # rwxr-xr-x
chmod 644 file.txt   # rw-r--r--
chmod 777 dir/       # rwxrwxrwx（不推荐）

# 字母方式
chmod +x script.sh   # 添加执行权限
chmod -w file.txt    # 移除写权限
chmod u+x script.sh  # 仅所有者可执行

# 递归修改目录权限
chmod -R 755 /var/www/

# 修改文件所有者
chown user:group file.txt
chown -R www-data:www-data /var/www/`,
  },
  {
    id: 23,
    title: 'Linux 磁盘空间不足排查',
    category: 'linux',
    tags: ['磁盘', 'du', 'df'],
    problem: '服务器磁盘空间不足，需要找出占用空间最大的文件和目录。',
    solution: '使用 df 查看分区，du 查看目录大小',
    code: `# 查看磁盘分区使用情况
df -h

# 查看当前目录下各子目录大小
du -h --max-depth=1 / | sort -hr | head -20

# 查看指定目录总大小
du -sh /var/log/

# 查找大于100M的文件
find / -type f -size +100M -exec ls -lh {} \\;

# 清理常见占用空间的目录
sudo journalctl --vacuum-size=100M  # 清理系统日志
docker system prune -a               # 清理Docker
sudo apt clean                       # 清理apt缓存

# 查看已删除但未释放空间的文件
lsof | grep deleted`,
  },
  {
    id: 24,
    title: 'MySQL 常见连接错误解决',
    category: 'database',
    tags: ['MySQL', '连接', '错误'],
    problem: '连接 MySQL 时出现各种错误：Access denied、Lost connection、Too many connections 等。',
    solution: '根据错误类型逐一排查',
    code: `# 1. Access denied for user
# 检查用户名密码，重置密码
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;

# 允许远程连接
CREATE USER 'root'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;

# 2. Lost connection to MySQL server
# 增大超时时间 my.cnf
wait_timeout = 28800
max_allowed_packet = 64M

# 3. Too many connections
# 增大最大连接数
SET GLOBAL max_connections = 500;
# my.cnf 永久生效
max_connections = 500

# 4. Unknown database
CREATE DATABASE mydb CHARACTER SET utf8mb4;`,
  },
  {
    id: 25,
    title: 'SQLite 数据库锁定错误',
    category: 'database',
    tags: ['SQLite', '锁定', '并发'],
    problem: 'Django 开发时出现 database is locked 错误，尤其在并发写入时。',
    solution: '增加超时时间或优化写入逻辑',
    code: `# settings.py 增加超时
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 30,  # 等待锁的超时秒数
        }
    }
}

# 其他解决方案：
# 1. 减少长事务，尽快 commit
# 2. 使用 @transaction.atomic 包裹写入操作
# 3. 生产环境换用 PostgreSQL/MySQL
# 4. WAL 模式提升并发
# 在 Django 启动时执行：
# cursor.execute("PRAGMA journal_mode=WAL")`,
  },
  {
    id: 26,
    title: 'Redis 连接拒绝或超时',
    category: 'database',
    tags: ['Redis', '连接', '超时'],
    problem: '应用连接 Redis 时报 Connection refused 或 Timeout。',
    solution: '检查 Redis 服务状态和配置',
    code: `# 检查 Redis 是否运行
redis-cli ping
# 返回 PONG 表示正常

# 常见问题排查：

# 1. Redis 未启动
sudo systemctl start redis
# 或
redis-server /etc/redis/redis.conf

# 2. 绑定地址限制
# redis.conf 修改
bind 0.0.0.0  # 允许所有IP（注意安全）
# 或指定IP
bind 127.0.0.1 192.168.1.100

# 3. 防火墙阻止
sudo ufw allow 6379

# 4. 设置密码
# redis.conf
requirepass your_password

# Python 连接
import redis
r = redis.Redis(host='localhost', port=6379, password='your_password', decode_responses=True)`,
  },
  {
    id: 27,
    title: 'Nginx 502 Bad Gateway 排查',
    category: 'network',
    tags: ['Nginx', '502', '部署'],
    problem: 'Nginx 反向代理后端服务时报 502 Bad Gateway。',
    solution: '检查后端服务是否运行、端口是否正确、代理配置是否匹配',
    code: `# 1. 检查后端服务是否运行
curl http://127.0.0.1:8001/
# 如果无响应，启动后端服务

# 2. 检查 Nginx 配置
# /etc/nginx/sites-available/myapp
upstream backend {
    server 127.0.0.1:8001;
}
server {
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# 3. 检查 Nginx 错误日志
tail -f /var/log/nginx/error.log

# 4. 测试配置是否正确
nginx -t

# 5. 重载配置
nginx -s reload`,
  },
  {
    id: 28,
    title: 'HTTPS 证书配置与自动续期',
    category: 'network',
    tags: ['HTTPS', 'SSL', 'Let\'s Encrypt'],
    problem: '网站需要配置 HTTPS，并自动续期证书。',
    solution: '使用 Certbot 自动申请和续期 Let\'s Encrypt 免费证书',
    code: `# 1. 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 2. 申请证书（Nginx）
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 3. 自动续期（Certbot 自动添加定时任务）
sudo certbot renew --dry-run  # 测试续期

# 4. 查看定时任务
sudo systemctl status certbot.timer

# 5. 手动续期
sudo certbot renew

# 6. Django SECURE 配置
# settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True`,
  },
  {
    id: 29,
    title: 'VS Code 常用快捷键速查',
    category: 'tools',
    tags: ['VS Code', '快捷键', '效率'],
    problem: '记不住 VS Code 常用快捷键，影响开发效率。',
    solution: '常用快捷键速查表',
    code: `# 通用
Ctrl+Shift+P    命令面板
Ctrl+,          打开设置
Ctrl+\`          打开终端

# 编辑
Alt+↑/↓         移动当前行
Ctrl+D          选中下一个相同词
Ctrl+Shift+L    选中所有相同词
Ctrl+/          切换注释
Alt+Shift+F     格式化代码

# 搜索
Ctrl+F          查找
Ctrl+H          替换
Ctrl+Shift+F    全局搜索

# 导航
Ctrl+P          快速打开文件
Ctrl+G          跳转到行
F12             跳转到定义
Alt+←/→         前进/后退

# 多光标
Alt+Click       添加光标
Ctrl+Alt+↑/↓    上下添加光标`,
  },
  {
    id: 30,
    title: 'Postman/Axios 请求调试技巧',
    category: 'tools',
    tags: ['API', '调试', 'Postman'],
    problem: '开发 API 时需要快速调试请求，排查前后端通信问题。',
    solution: '使用浏览器 DevTools 和代码技巧调试',
    code: `# 浏览器 DevTools 调试
# F12 → Network 面板
# 查看请求URL、状态码、请求头、响应体

# Axios 拦截器打印请求/响应
axios.interceptors.request.use(config => {
  console.log('Request:', config.method?.toUpperCase(), config.url)
  return config
})
axios.interceptors.response.use(
  res => { console.log('Response:', res.status, res.data); return res },
  err => { console.error('Error:', err.response?.status, err.response?.data); return Promise.reject(err) }
)

# Django DRF 开启请求日志
# settings.py
LOGGING = {
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

# curl 快速测试
curl -X GET http://localhost:8001/api/articles/ -H "Authorization: Bearer TOKEN"`,
  },
  {
    id: 31,
    title: 'Python 内存泄漏排查',
    category: 'python',
    tags: ['内存', '性能', 'tracemalloc'],
    problem: 'Python 程序运行一段时间后内存持续增长，疑似内存泄漏。',
    solution: '使用 tracemalloc 和 objgraph 定位内存泄漏',
    code: `import tracemalloc
import linecache

# 启动内存跟踪
tracemalloc.start()

# ... 你的代码 ...

# 获取内存快照
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

for stat in top_stats[:10]:
    print(stat)

# 对比两个快照
snapshot1 = tracemalloc.take_snapshot()
# ... 执行可能泄漏的代码 ...
snapshot2 = tracemalloc.take_snapshot()
for diff in snapshot2.compare_to(snapshot1, 'lineno')[:10]:
    print(diff)

# 使用 objgraph 查看对象引用
# pip install objgraph
import objgraph
objgraph.show_most_common_types(limit=20)`,
  },
  {
    id: 32,
    title: 'Django DRF 分页配置与自定义',
    category: 'django',
    tags: ['DRF', '分页', 'API'],
    problem: 'API 返回数据太多需要分页，或需要自定义分页格式。',
    solution: '配置全局分页和视图级分页',
    code: `# settings.py 全局分页
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# 自定义分页类
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# 视图中使用
class ArticleListView(generics.ListAPIView):
    pagination_class = CustomPagination

# 禁用某个视图的分页
class FriendLinkListView(generics.ListAPIView):
    pagination_class = None

# 返回格式
{
    "count": 100,
    "next": "http://api.example.com/articles/?page=2",
    "previous": null,
    "results": [...]
}`,
  },
  {
    id: 33,
    title: 'Vite 构建后白屏问题',
    category: 'vue',
    tags: ['Vite', '构建', '白屏'],
    problem: 'npm run build 部署后页面白屏，控制台报路径错误。',
    solution: '配置 base 路径和正确部署静态文件',
    code: `// vite.config.js
export default defineConfig({
  base: '/',  // 根目录部署用 '/'，子目录用 '/app/'
})

// 如果部署在子目录
base: '/my-blog/'

// Nginx 配置 SPA 路由
server {
    listen 80;
    server_name yourdomain.com;
    root /var/www/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}

// 检查构建产物
npm run build
ls dist/  // 确认 index.html 和 assets/ 存在

// 本地预览构建结果
npm run preview`,
  },
  {
    id: 34,
    title: 'Git 大文件提交导致仓库过大',
    category: 'git',
    tags: ['大文件', 'git-lfs', '清理'],
    problem: '不小心提交了大文件（视频、数据库等），导致 .git 目录非常大。',
    solution: '使用 git filter-branch 或 BFG 清理历史',
    code: `# 方法1：BFG Repo-Cleaner（推荐，更安全）
# 安装：https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --strip-blobs-bigger-than 50M
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 方法2：git filter-branch
git filter-branch --force --index-filter \\
  'git rm --cached --ignore-unmatch path/to/large/file' \\
  --prune-empty --tag-name-filter cat -- --all

# 方法3：使用 Git LFS 管理大文件
git lfs install
git lfs track "*.psd"
git lfs track "*.mp4"
git add .gitattributes
git commit -m "setup Git LFS"

# 预防：.gitignore 排除大文件
*.mp4
*.zip
*.sqlite3
db.sqlite3`,
  },
  {
    id: 35,
    title: 'Docker Compose 常见启动失败',
    category: 'docker',
    tags: ['docker-compose', '启动', '依赖'],
    problem: 'docker-compose up 时服务启动失败，常见于服务依赖和端口冲突。',
    solution: '配置健康检查和依赖顺序',
    code: `# docker-compose.yml
services:
  db:
    image: mysql:8.0
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 3s
      retries: 10

  web:
    image: myapp
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  redis:
    image: redis:7

# 常见问题：
# 1. 端口冲突 → 修改 ports 映射
ports:
  - "3307:3306"  # 宿主机3307映射容器3306

# 2. 数据持久化
volumes:
  - db_data:/var/lib/mysql

# 3. 环境变量
environment:
  - MYSQL_ROOT_PASSWORD=\${DB_PASSWORD}

# 4. 查看日志
docker-compose logs -f web`,
  },
]

const filteredNotes = computed(() => {
  let result = notes
  if (activeCategory.value !== 'all') {
    result = result.filter(n => n.category === activeCategory.value)
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(n =>
      n.title.toLowerCase().includes(q) ||
      n.tags.some(t => t.toLowerCase().includes(q)) ||
      n.problem.toLowerCase().includes(q)
    )
  }
  return result
})

const toggleExpand = (id) => {
  expandedId.value = expandedId.value === id ? null : id
}

const getCategoryLabel = (key) => {
  const cat = categories.find(c => c.key === key)
  return cat ? cat.label : key
}

const getCategoryIcon = (key) => {
  const cat = categories.find(c => c.key === key)
  return cat ? cat.icon : '📌'
}

setSeo({ title: '开发笔记', description: '技术速查笔记，记录开发中常见问题与解决方案' })
</script>

<template>
  <div class="notes-page">
    <header class="notes-header">
      <h1 class="page-title">📝 开发笔记</h1>
      <p class="page-desc">技术速查手册，记录开发中常见问题与解决方案</p>
    </header>

    <div class="notes-toolbar">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input
          v-model="searchQuery"
          placeholder="搜索笔记标题、标签或问题..."
          class="search-input"
        />
      </div>
      <div class="category-tabs">
        <button
          v-for="cat in categories"
          :key="cat.key"
          :class="['cat-btn', { active: activeCategory === cat.key }]"
          @click="activeCategory = cat.key"
        >
          <span class="cat-icon">{{ cat.icon }}</span>
          <span class="cat-label">{{ cat.label }}</span>
        </button>
      </div>
    </div>

    <div class="notes-stats">
      <span class="stat-item">共 <strong>{{ filteredNotes.length }}</strong> 条笔记</span>
      <span v-if="searchQuery" class="stat-item search-hint">搜索: "{{ searchQuery }}"</span>
    </div>

    <div class="notes-list">
      <div
        v-for="note in filteredNotes"
        :key="note.id"
        :class="['note-card', { expanded: expandedId === note.id }]"
      >
        <div class="note-card-header" @click="toggleExpand(note.id)">
          <div class="note-card-left">
            <span class="note-cat-badge">{{ getCategoryIcon(note.category) }} {{ getCategoryLabel(note.category) }}</span>
            <h3 class="note-card-title">{{ note.title }}</h3>
          </div>
          <span :class="['expand-icon', { rotated: expandedId === note.id }]">▶</span>
        </div>

        <div class="note-card-tags">
          <span v-for="tag in note.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>

        <div v-if="expandedId === note.id" class="note-card-body">
          <div class="note-section">
            <h4 class="section-label">❓ 问题描述</h4>
            <p class="section-text">{{ note.problem }}</p>
          </div>
          <div class="note-section">
            <h4 class="section-label">✅ 解决方案</h4>
            <p class="section-text">{{ note.solution }}</p>
          </div>
          <div class="note-section">
            <h4 class="section-label">💻 代码示例</h4>
            <pre class="code-block"><code>{{ note.code }}</code></pre>
          </div>
        </div>
      </div>

      <div v-if="!filteredNotes.length" class="empty-state">
        <p>🔍 没有找到匹配的笔记</p>
        <p class="empty-hint">试试其他关键词或分类</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.notes-page {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.notes-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

.page-desc {
  color: var(--text-secondary-color);
  font-size: 1.05rem;
}

.notes-toolbar {
  margin-bottom: 1.5rem;
}

.search-box {
  position: relative;
  margin-bottom: 1rem;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1rem;
}

.search-input {
  width: 100%;
  padding: 0.85rem 1rem 0.85rem 2.8rem;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  background: var(--surface-color);
  color: var(--text-color);
  font-size: 0.95rem;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.15);
}

.category-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.cat-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.45rem 0.9rem;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  background: var(--surface-color);
  color: var(--text-color);
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
}

.cat-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.cat-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.cat-icon {
  font-size: 0.9rem;
}

.cat-label {
  font-weight: 500;
}

.notes-stats {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: var(--text-secondary-color);
}

.search-hint {
  color: var(--primary-color);
}

.notes-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.note-card {
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
}

.note-card:hover {
  border-color: var(--primary-color);
  box-shadow: 0 2px 12px var(--shadow-color);
}

.note-card.expanded {
  border-color: var(--primary-color);
}

.note-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  cursor: pointer;
  user-select: none;
}

.note-card-left {
  flex: 1;
  min-width: 0;
}

.note-cat-badge {
  display: inline-block;
  padding: 0.15rem 0.6rem;
  background: var(--background-color);
  border-radius: 10px;
  font-size: 0.75rem;
  color: var(--text-secondary-color);
  margin-bottom: 0.4rem;
}

.note-card-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.expand-icon {
  font-size: 0.7rem;
  color: var(--text-secondary-color);
  transition: transform 0.3s;
  flex-shrink: 0;
  margin-left: 1rem;
}

.expand-icon.rotated {
  transform: rotate(90deg);
}

.note-card-tags {
  padding: 0 1.25rem 0.75rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}

.tag {
  display: inline-block;
  padding: 0.15rem 0.55rem;
  background: var(--primary-color);
  color: white;
  border-radius: 10px;
  font-size: 0.72rem;
  font-weight: 500;
}

.note-card-body {
  padding: 0 1.25rem 1.25rem;
  border-top: 1px solid var(--border-color);
  padding-top: 1rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

.note-section {
  margin-bottom: 1rem;
}

.note-section:last-child {
  margin-bottom: 0;
}

.section-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-color);
  margin: 0 0 0.4rem;
}

.section-text {
  font-size: 0.9rem;
  color: var(--text-secondary-color);
  line-height: 1.6;
  margin: 0;
}

.code-block {
  background: #1e1e2e;
  color: #cdd6f4;
  padding: 1rem 1.25rem;
  border-radius: 8px;
  overflow-x: auto;
  font-size: 0.82rem;
  line-height: 1.6;
  margin: 0;
  font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
}

.code-block code {
  white-space: pre;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-secondary-color);
}

.empty-hint {
  font-size: 0.9rem;
  margin-top: 0.5rem;
  opacity: 0.7;
}

@media (max-width: 768px) {
  .notes-page {
    padding: 1rem;
  }
  .page-title {
    font-size: 1.5rem;
  }
  .category-tabs {
    overflow-x: auto;
    flex-wrap: nowrap;
    padding-bottom: 0.5rem;
  }
  .note-card-header {
    padding: 0.85rem 1rem;
  }
  .note-card-body {
    padding: 0 1rem 1rem;
    padding-top: 0.75rem;
  }
  .code-block {
    font-size: 0.75rem;
    padding: 0.75rem;
  }
}
</style>
