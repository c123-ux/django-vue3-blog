from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Comment


class CommentReplySerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'article', 'parent', 'content', 'nickname',
            'author_name', 'created_at'
        ]

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.username
        return obj.nickname


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'article', 'parent', 'content', 'nickname',
            'author_name', 'is_approved',
            'replies_count', 'replies', 'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'is_approved']

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.username
        return obj.nickname

    def get_replies_count(self, obj):
        return obj.replies.filter(is_approved=True).count()

    def get_replies(self, obj):
        replies = obj.replies.filter(is_approved=True).select_related('author')
        return CommentReplySerializer(replies, many=True).data


class CommentCreateSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(max_length=50, required=False, default='匿名用户')

    class Meta:
        model = Comment
        fields = ['article', 'parent', 'content', 'nickname']

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("评论内容不能为空")
        if len(value) > 1000:
            raise serializers.ValidationError("评论内容不能超过1000字")
        return value

    def validate_nickname(self, value):
        if not value.strip():
            return '匿名用户'
        return value.strip()

    def validate_parent(self, value):
        if value and value.parent is not None:
            raise serializers.ValidationError("仅支持二级回复")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['author'] = request.user
            if not validated_data.get('nickname') or validated_data['nickname'] == '匿名用户':
                validated_data['nickname'] = request.user.username
        validated_data['is_approved'] = True
        return super().create(validated_data)
