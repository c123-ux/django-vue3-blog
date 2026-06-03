import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
import logging

logger = logging.getLogger(__name__)


class CommentConsumer(AsyncWebsocketConsumer):
    """
    评论WebSocket消费者
    实现实时评论功能
    """
    
    async def connect(self):
        self.article_id = self.scope['url_route']['kwargs']['article_id']
        self.comment_group_name = f'comments_{self.article_id}'
        
        # 检查用户是否已认证
        if isinstance(self.scope['user'], AnonymousUser):
            await self.close()
            return
        
        # 加入评论组
        await self.channel_layer.group_add(
            self.comment_group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f'用户 {self.scope["user"].username} 连接到文章 {self.article_id} 的评论组')
    
    async def disconnect(self, close_code):
        # 离开评论组
        await self.channel_layer.group_discard(
            self.comment_group_name,
            self.channel_name
        )
        logger.info(f'用户 {self.scope["user"].username} 断开文章 {self.article_id} 的评论组')
    
    async def receive(self, text_data):
        """
        接收客户端消息
        """
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'new_comment':
                await self.handle_new_comment(data)
            elif message_type == 'typing':
                await self.handle_typing(data)
            elif message_type == 'delete_comment':
                await self.handle_delete_comment(data)
                
        except json.JSONDecodeError:
            logger.error('收到无效的JSON消息')
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': '无效的消息格式'
            }))
        except Exception as e:
            logger.error(f'处理消息时出错：{str(e)}')
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': '处理消息时出错'
            }))
    
    async def handle_new_comment(self, data):
        """
        处理新评论
        """
        content = data.get('content')
        parent_id = data.get('parent_id')
        
        if not content:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': '评论内容不能为空'
            }))
            return
        
        # 保存评论到数据库
        comment = await self.save_comment(content, parent_id)
        
        if comment:
            # 广播新评论到所有连接的客户端
            await self.channel_layer.group_send(
                self.comment_group_name,
                {
                    'type': 'comment_message',
                    'comment': comment,
                    'user': self.scope['user'].username
                }
            )
    
    async def handle_typing(self, data):
        """
        处理用户正在输入状态
        """
        is_typing = data.get('is_typing', False)
        
        await self.channel_layer.group_send(
            self.comment_group_name,
            {
                'type': 'typing_message',
                'user': self.scope['user'].username,
                'is_typing': is_typing
            }
        )
    
    async def handle_delete_comment(self, data):
        """
        处理删除评论
        """
        comment_id = data.get('comment_id')
        
        if not comment_id:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': '评论ID不能为空'
            }))
            return
        
        # 删除评论
        success = await self.delete_comment(comment_id)
        
        if success:
            # 广播删除消息
            await self.channel_layer.group_send(
                self.comment_group_name,
                {
                    'type': 'delete_message',
                    'comment_id': comment_id,
                    'user': self.scope['user'].username
                }
            )
    
    async def comment_message(self, event):
        """
        发送评论消息到客户端
        """
        await self.send(text_data=json.dumps({
            'type': 'new_comment',
            'comment': event['comment'],
            'user': event['user']
        }))
    
    async def typing_message(self, event):
        """
        发送输入状态消息到客户端
        """
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': event['user'],
            'is_typing': event['is_typing']
        }))
    
    async def delete_message(self, event):
        """
        发送删除消息到客户端
        """
        await self.send(text_data=json.dumps({
            'type': 'delete_comment',
            'comment_id': event['comment_id'],
            'user': event['user']
        }))
    
    @database_sync_to_async
    def save_comment(self, content, parent_id):
        """
        异步保存评论到数据库
        """
        try:
            from apps.comments.models import Comment
            from apps.articles.models import Article
            
            article = Article.objects.get(id=self.article_id)
            
            comment = Comment.objects.create(
                article=article,
                author=self.scope['user'],
                content=content,
                parent_id=parent_id if parent_id else None
            )
            
            # 序列化评论数据
            from apps.comments.serializers import CommentSerializer
            serializer = CommentSerializer(comment)
            
            return serializer.data
            
        except Article.DoesNotExist:
            logger.error(f'文章 {self.article_id} 不存在')
            return None
        except Exception as e:
            logger.error(f'保存评论时出错：{str(e)}')
            return None
    
    @database_sync_to_async
    def delete_comment(self, comment_id):
        """
        异步删除评论
        """
        try:
            from apps.comments.models import Comment
            
            comment = Comment.objects.get(id=comment_id)
            
            # 检查权限
            if comment.author != self.scope['user']:
                return False
            
            comment.delete()
            return True
            
        except Comment.DoesNotExist:
            logger.error(f'评论 {comment_id} 不存在')
            return False
        except Exception as e:
            logger.error(f'删除评论时出错：{str(e)}')
            return False