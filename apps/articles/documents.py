import os
import logging

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Article
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

USE_ELASTICSEARCH = os.environ.get('USE_ELASTICSEARCH', 'false').lower() == 'true'


class ArticleDocument(Document):
    """文章 Elasticsearch 文档"""
    author = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
    })

    class Index:
        name = 'articles'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Article
        fields = ['title', 'content', 'summary', 'status', 'views', 'created_at', 'updated_at']
        related_models = [User]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, User):
            return related_instance.articles.all()


if USE_ELASTICSEARCH:
    try:
        from elasticsearch import Elasticsearch
        hosts = os.environ.get('ELASTICSEARCH_HOSTS', 'http://localhost:9200').split(',')
        if Elasticsearch(hosts, request_timeout=3).ping():
            registry.register_document(ArticleDocument)
            logger.info('Elasticsearch document registry enabled')
    except Exception as e:
        logger.warning('Elasticsearch unavailable, document registry disabled: %s', e)
