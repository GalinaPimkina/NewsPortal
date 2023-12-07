# Generated by Django 4.2.5 on 2023-12-07 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_remove_post_category_delete_postcategory_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_through', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category')),
                ('post_through', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(null=True, through='news.PostCategory', to='news.category'),
        ),
    ]
