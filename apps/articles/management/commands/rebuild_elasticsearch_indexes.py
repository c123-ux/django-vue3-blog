from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.registries import registry
from apps.articles.models import Article
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = '重建Elasticsearch索引'

    def add_arguments(self, parser):
        parser.add_argument(
            '--models',
            nargs='+',
            type=str,
            help='指定要重建索引的模型',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='强制重建索引（删除现有索引）',
        )

    def handle(self, *args, **options):
        # 获取要重建的索引
        if options['models']:
            models = []
            for model_name in options['models']:
                try:
                    app_label, model_name = model_name.split('.')
                    model = registry.apps.get_model(app_label, model_name)
                    models.append(model)
                except ValueError:
                    self.stdout.write(
                        self.style.ERROR(f'Invalid model name: {model_name}. Expected format: app.model')
                    )
                    continue
        else:
            models = [Article]  # 默认只处理文章模型

        # 重建索引
        for model in models:
            label = f"{model._meta.app_label}.{model._meta.label_lower}"
            if label in registry._models:
                doc = registry._models[label][0]()
                if options['force']:
                    self.stdout.write(f'Deleting index for {label}...')
                    doc._index.delete(ignore=404)
                
                self.stdout.write(f'Indexing {label}...')
                doc.update()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully indexed {label}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'No document found for {label}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully rebuilt Elasticsearch indexes')
        )