# Generated by Django 3.0.7 on 2020-10-24 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booklists',
            name='source',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Book.BookSource'),
        ),
        migrations.AddField(
            model_name='booksource',
            name='domain',
            field=models.CharField(default='', max_length=100, verbose_name='书源域名'),
        ),
        migrations.AddField(
            model_name='booksource',
            name='name',
            field=models.CharField(default='', max_length=100, verbose_name='书源名称'),
        ),
        migrations.AddField(
            model_name='booksource',
            name='search_url',
            field=models.CharField(default='', max_length=255, verbose_name='搜索地址'),
        ),
        migrations.AddField(
            model_name='chapterlists',
            name='source',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='Book.BookSource'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_author',
            field=models.CharField(default='', max_length=200, verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_chapter_info',
            field=models.CharField(default='', max_length=200, verbose_name='章节详情'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_chapter_list',
            field=models.CharField(default='', max_length=200, verbose_name='章节列表'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_chapter_list_url',
            field=models.CharField(default='', max_length=200, verbose_name='章节列表链接'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_cover',
            field=models.CharField(default='', max_length=200, verbose_name='封面'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_intro',
            field=models.CharField(default='', max_length=200, verbose_name='简介'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_last_update_time',
            field=models.CharField(default='', max_length=200, verbose_name='最后更新时间'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_name',
            field=models.CharField(default='', max_length=200, verbose_name='书名'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_newest',
            field=models.CharField(default='', max_length=200, verbose_name='最新章节'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_url',
            field=models.CharField(default='', max_length=200, verbose_name='地址'),
        ),
    ]
