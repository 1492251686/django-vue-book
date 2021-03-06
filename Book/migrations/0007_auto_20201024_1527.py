# Generated by Django 3.0.7 on 2020-10-24 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0006_auto_20201024_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booksource',
            name='book_author',
            field=models.TextField(default='', verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_chapter_info',
            field=models.TextField(default='', verbose_name='章节详情'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_chapter_list',
            field=models.TextField(default='', verbose_name='章节列表'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_chapter_list_url',
            field=models.TextField(default='', verbose_name='章节列表链接'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_cover',
            field=models.TextField(default='', verbose_name='封面'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_info',
            field=models.TextField(default='', verbose_name='书籍信息(逗号分隔,书名，地址，作者，最新章，时间)'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_info_common',
            field=models.TextField(default='', verbose_name='书籍信息公共链接'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_intro',
            field=models.TextField(default='', verbose_name='简介'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_last_update_time',
            field=models.TextField(default='', verbose_name='最后更新时间'),
        ),
        migrations.AlterField(
            model_name='booksource',
            name='book_newest',
            field=models.TextField(default='', verbose_name='最新章节'),
        ),
    ]
