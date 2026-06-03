from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_category_series_tag_article_is_top_article_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='articles',
                to='auth.user',
                verbose_name='作者',
            ),
        ),
        migrations.AddField(
            model_name='article',
            name='nickname',
            field=models.CharField(
                default='匿名用户',
                max_length=50,
                verbose_name='昵称',
            ),
        ),
    ]
