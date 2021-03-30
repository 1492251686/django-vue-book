# coding:utf-8
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 指定Django默认配置文件模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NanShan.settings')

# 为我们的项目myproject创建一个Celery实例。这里不指定broker容易出现错误。
app = Celery('NanShan')

# 这里指定从django的settings.py里读取celery配置
app.config_from_object('NanShan.settings', namespace="CELERY")

# 自动从所有已注册的django app中加载任务
app.autodiscover_tasks()