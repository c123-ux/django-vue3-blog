from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Comment
from apps.articles.models import Article


class CommentModelTest(TestCase):
    """评论模型测试"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.article = Article.objects.create(title='测试文章', content='内容', author=self.user, status='published')
    
    def test_create_comment(self):
        comment = Comment.objects.create(article=self.article, author=self.user, content='这是一条评论')
        self.assertEqual(comment.content, '这是一条评论')
        self.assertTrue(comment.is_approved)
    
    def test_nested_comment(self):
        parent = Comment.objects.create(article=self.article, author=self.user, content='父评论')
        child = Comment.objects.create(article=self.article, parent=parent, author=self.user, content='子评论')
        self.assertEqual(child.parent, parent)
        self.assertEqual(parent.replies.count(), 1)
    
    def test_get_replies_count(self):
        parent = Comment.objects.create(article=self.article, author=self.user, content='父评论')
        Comment.objects.create(article=self.article, parent=parent, author=self.user, content='回复1')
        Comment.objects.create(article=self.article, parent=parent, author=self.user, content='回复2')
        self.assertEqual(parent.get_replies_count(), 2)


class CommentAPITest(APITestCase):
    """评论 API 测试"""
    
    def setUp(self):
        # 确保每次测试开始时评论表是空的
        Comment.objects.all().delete()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.article = Article.objects.create(title='测试文章', content='内容', author=self.user, status='published')
    
    def _get_comment_results(self, response):
        data = response.data
        return data if isinstance(data, list) else data.get('results', [])

    def test_list_comments_empty(self):
        """测试获取评论列表接口正常"""
        response = self.client.get(f'/api/comments/article/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self._get_comment_results(response), [])

    def test_list_comments_with_data(self):
        """测试有数据的评论列表"""
        Comment.objects.create(article=self.article, author=self.user, content='测试评论', is_approved=True)
        response = self.client.get(f'/api/comments/article/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(self._get_comment_results(response)), 1)

    def test_list_comments_unapproved(self):
        """测试不显示未审核评论"""
        response1 = self.client.get(f'/api/comments/article/{self.article.id}/')
        count_before = len(self._get_comment_results(response1))
        
        # 创建一个未审核评论
        Comment.objects.create(article=self.article, author=self.user, content='未审核', is_approved=False)
        
        # 再次获取，数量应该不变
        response2 = self.client.get(f'/api/comments/article/{self.article.id}/')
        self.assertEqual(len(self._get_comment_results(response2)), count_before)
    
    def test_create_comment_authenticated(self):
        """测试创建评论（已登录）"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/comments/create/', {
            'article': self.article.id,
            'content': '新评论'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_comment_unauthenticated(self):
        """测试创建评论（未登录）"""
        response = self.client.post('/api/comments/create/', {
            'article': self.article.id,
            'content': '新评论'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_comment_empty_content(self):
        """测试创建空内容评论"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/comments/create/', {
            'article': self.article.id,
            'content': ''
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_comment_too_long(self):
        """测试创建超长评论"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/comments/create/', {
            'article': self.article.id,
            'content': 'a' * 1001
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_comment_by_author(self):
        """测试作者删除自己的评论"""
        comment = Comment.objects.create(article=self.article, author=self.user, content='待删除评论')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/comments/{comment.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_comment_by_other_user(self):
        """测试其他用户不能删除评论"""
        comment = Comment.objects.create(article=self.article, author=self.user, content='测试评论')
        other_user = User.objects.create_user(username='other', password='pass123')
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(f'/api/comments/{comment.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_nested_comment(self):
        """测试创建嵌套评论"""
        parent = Comment.objects.create(article=self.article, author=self.user, content='父评论')
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/comments/create/', {
            'article': self.article.id,
            'parent': parent.id,
            'content': '回复评论'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        child = Comment.objects.latest('id')
        self.assertEqual(child.parent, parent)
