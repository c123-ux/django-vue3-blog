from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    tags_list = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            'id', 'title', 'content', 'tags', 'tags_list',
            'is_public', 'author_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['author']

    def get_tags_list(self, obj):
        return obj.get_tags_list()


class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'content', 'tags', 'is_public']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)
