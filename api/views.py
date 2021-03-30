import aiohttp
import asyncio
import time
import json
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from Book.models import ChapterLists, BookLists, ChapterInfo
from .serializers import ChapterSerializer, InfoSerializer, ChapterSerializers, BookListSerializer
from Book.views import insert_content, update_chapter
from django_redis import get_redis_connection
from django.core.cache import cache
from django.forms.models import model_to_dict
import pickle
from django.db.models import Q
from itertools import chain
from .task import send_email


class Chapter(APIView):

    def get(self, request, *args, **kwargs):
        chapter_id = request.query_params['id']
        chapter = cache.has_key("chapter_" + chapter_id)
        if not chapter:
            try:
                ChapterInfo.objects.get(chapter_id=chapter_id)
                chapter = ChapterLists.objects.get(pk=chapter_id)
            except ChapterInfo.DoesNotExist:
                chapter_info = ChapterLists.objects.only('url').get(pk=chapter_id)
                loop = asyncio.new_event_loop()
                loop.run_until_complete(insert_content(chapter_info.url, chapter_id))
                chapter = ChapterLists.objects.get(pk=chapter_id)
            serializer = ChapterSerializer(chapter, context={'is_list': 0})
            chapter = serializer.data
            cache.set("chapter_" + chapter_id, chapter, 3600000)
        else:
            chapter = cache.get("chapter_" + chapter_id)# 文章id
        return Response(chapter)


class ChapterListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'  # 指定每一页显示多少条
    page_query_param = "page"  # 指定要第几页
    max_page_size = 10000


class ChapterList(APIView):

    def get(self, request, *args, **kwargs):
        # start = time.perf_counter()
        book_id = request.query_params['book_id']#书籍id
        response = {}
        this_book = cache.has_key("book_" + book_id)#查询是否有缓存->书
        if not this_book:#无->查询->序列化->存储
            this_book = BookLists.objects.get(pk=book_id)
            cache.set("book_" + book_id, pickle.dumps(this_book), 3600)
        else:#有->反序列化
            this_book = pickle.loads(cache.get("book_" + book_id))
        # end = time.perf_counter()
        # print("查到书籍信息用时：", end - start)
        if int(time.mktime(this_book.last_update_time.timetuple())) + 21600 < int(time.time()) and int(time.mktime(this_book.last_update_time.timetuple())) + 864000 > int(time.time()):
            # print("是否爬取列表，符合条件一，进入第二层判断")
            if int(time.mktime(this_book.last_crawling_time.timetuple())) + 3600 < int(time.time()):
                # print("是否爬取列表，符合条件二，开始爬取")
                loop = asyncio.new_event_loop()
                loop.run_until_complete(update_chapter(this_book.url, book_id))
                cache.delete("book_" + book_id)
                this_book = BookLists.objects.get(pk=book_id)
                cache.set("book_" + book_id, pickle.dumps(this_book), 3600)
                # end = time.perf_counter()
                # print("爬列表用时：", end - start)
        # end = time.perf_counter()
        # print("不一定走完爬列表用时：", end - start)
        chapter = cache.has_key("chapter_list_" + book_id)  # 查询是否有缓存->书的章节列表
        if not chapter:  # 无->查询->序列化->存储
            chapter = this_book.chapters.select_related().all().only('id', 'name')#反向查询章节列表
            # end = time.perf_counter()
            # print("数据库查询列表用时：", end - start)
            if int(time.mktime(this_book.last_update_time.timetuple())) + 864000 < int(time.time()):
                cache.set("chapter_list_" + book_id, pickle.dumps(chapter), 9999999999)
            else:
                cache.set("chapter_list_" + book_id, pickle.dumps(chapter), 7200)
            # end = time.perf_counter()
            # print("存储列表内容进redis用时：", end - start)
        else:#有->反序列化
            # end = time.perf_counter()
            # print("取redis列表数据前用时:", end - start)
            chapter = pickle.loads(cache.get("chapter_list_" + book_id))
            # end = time.perf_counter()
            # print("取redis列表数据后用时:", end - start)
        # end = time.perf_counter()
        # print("初始化分页前用时：", end - start)
        chapter_page = ChapterListPagination()
        # end = time.perf_counter()
        # print("初始化分页用时：", end - start)
        chapter_list = chapter_page.paginate_queryset(queryset=chapter, request=request, view=self)
        # end = time.perf_counter()
        # print("执行分页用时：", end - start)
        # end = time.perf_counter()
        # print("执行drf序列化器前用时：", end - start)
        serializer = ChapterSerializers(chapter_list, many=True)
        # end = time.perf_counter()
        # print("执行drf序列化器后用时：", end - start)
        book_serializer = InfoSerializer(this_book)
        response['count'] = chapter_page.page.paginator.count
        response['book_info'] = book_serializer.data
        response['list'] = serializer.data
        # end = time.perf_counter()
        # print("数据返回前用时：", end - start)
        return Response(response)


class BookList(APIView):

    def get(self, request, *args, **kwargs):
        key_word = request.query_params['key']
        response = {}
        book_list = BookLists.objects.filter(Q(name__contains=key_word) | Q(author__contains=key_word))[:20]
        serializer = BookListSerializer(book_list, many=True)
        response['list'] = serializer.data
        response['count'] = len(book_list)
        return Response(response)


class SendEmail(APIView):

    def get(self, request):
        task = send_email.delay()
        cache.set('task_id',task.id)
        return Response({"results": "操作成功，正在发送，请稍候..."}, status=200)


