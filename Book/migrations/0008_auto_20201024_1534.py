# Generated by Django 3.0.7 on 2020-10-24 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0007_auto_20201024_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booksource',
            name='book_author',
        ),
        migrations.RemoveField(
            model_name='booksource',
            name='book_last_update_time',
        ),
        migrations.RemoveField(
            model_name='booksource',
            name='book_newest',
        ),
    ]
