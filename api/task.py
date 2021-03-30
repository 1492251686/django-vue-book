from NanShan.celery import app as celery_app
import time
import math
from django.core.mail import send_mail, EmailMultiAlternatives
from Book.views import update_chapter
from Book.models import BookLists
import asyncio


@celery_app.task
def send_email():
    start = time.perf_counter()
    book_list = BookLists.objects.only('url').all()
    for book in book_list:
        try:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(update_chapter(book.url, book.id))
        except Exception:
            continue
    end = time.perf_counter()
    times = int(end - start)
    minutes = math.floor(times / 60)
    seconds = times - minutes*60
    send_mail(
        "更新书籍执行结束！",
        "本次更新书籍" + str(len(book_list)) + "本,共计用时:" + str(minutes) + "分钟" + str(seconds) + "秒",
        "3105341961@qq.com",
        ["1492251686@qq.com"]
    )