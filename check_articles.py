import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_backend.settings')
import django
django.setup()

from apps.articles.models import Article

def check_articles():
    print("检查数据库中的文章...")
    total_articles = Article.objects.count()
    published_articles = Article.objects.filter(status='published').count()
    
    print(f"文章总数: {total_articles}")
    print(f"已发布文章: {published_articles}")
    
    print("\n已发布的文章:")
    for article in Article.objects.filter(status='published')[:10]:
        print(f"- {article.title} (ID: {article.id})")
    
    if total_articles == 0:
        print("\n⚠️  数据库中没有文章，请确保后端服务正在运行并尝试再次添加示例数据。")

if __name__ == "__main__":
    check_articles()