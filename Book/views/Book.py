import aiohttp
import asyncio
from django.core import serializers
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from bs4 import BeautifulSoup
from Book.models import BookLists, ChapterLists, BookClassification, ChapterInfo, BookSource
import time
import os
import aiofiles
from django.conf import settings
import hashlib
from typing import List, Dict
from lxml import etree, html
from html.parser import HTMLParser
from Book.serializers import BookSourceSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction


async def search_book_http(book_name: str, source: Dict) -> List[Dict[str, str]]:
    async with aiohttp.ClientSession() as session:
        url = source.search_url.replace('{keys}', book_name)
        async with session.get(url=url) as resp:
            con = await resp.text()
            data = etree.HTML(con)
            book_list = data.xpath(source.book_info_common)
            book_info_xpath = source.book_info.split('\r\n')
            book_lists = []
            if len(book_list) == 0:
                return []
            for v in book_list:
                book = {
                    'name': v.xpath(book_info_xpath[0])[0],
                    'url': v.xpath(book_info_xpath[1])[0] if v.xpath(book_info_xpath[1])[0].find(
                        'http') >= 0 else source.domain + v.xpath(book_info_xpath[1])[0],
                    'author': v.xpath(book_info_xpath[2])[0],
                    'newest_chapter': v.xpath(book_info_xpath[3])[0],
                    'last_time': v.xpath(book_info_xpath[4])[0] if book_info_xpath[4] != '0' else '0',
                    'source_id': source.id
                }
                book_lists.append(book)
            return book_lists


@require_http_methods(['GET'])
def search_book(request):
    results = {}
    book_name = request.GET['book_name']
    source_id = request.GET['source_id']
    try:
        source = BookSource.objects.get(pk=source_id)
    except BookSource.DoesNotExist:
        source = BookSource.objects.get(pk=1)
    loop = asyncio.new_event_loop()
    book_list = loop.run_until_complete(search_book_http(book_name, source=source))
    if len(book_list) == 0:
        results['code'] = 0
        results['msg'] = '查不到此书！'
        results['count'] = 0
    else:
        results['code'] = 1
        results['msg'] = '书籍列表下发成功！'
        results['count'] = len(book_list)
        results['list'] = book_list
    return JsonResponse(results)


async def add_book(book_data) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=book_data['url']) as resp:
            if resp.status == 404:
                return False
            con = await resp.text()
            source = BookSource.objects.get(pk=book_data['source_id'])
            data = etree.HTML(con)
            # soup = BeautifulSoup(con, 'lxml')
            # book_types = soup.select('.ffw tr td')
            # book_type = book_types[4].a.string
            # classification = BookClassification.objects.filter(name=book_type)
            # if not classification.exists():
            #     book_type_url = book_types[4].a.get('href')
            #     classification = BookClassification.objects.create(name=book_type, url=book_type_url)
            # else:
            #     classification = classification[0]
            classification = BookClassification.objects.get(pk=1)
            name = book_data['book_name']
            author = book_data['author']
            book = BookLists.objects.filter(name=name, author=author)
            if book:
                return False
            else:
                if book_data['last_update_time'] == '0':
                    last_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                else:
                    last_time = book_data['last_update_time'].replace('/', '-') if book_data['last_update_time'].find(
                    '/') >= 0 else book_data['last_update_time']
                newest_chapter = book_data['newest_chapter']
                introduction = data.xpath(source.book_intro)[0]
                if introduction is None:
                    introduction = '暂无'
                chapter_list = data.xpath(source.book_chapter_list)
                cover = data.xpath(source.book_cover)[0]
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                async with session.get(cover) as img:
                    img = await img.read()
                    md5_str = name + '-' + author
                    m = hashlib.md5()
                    b = md5_str.encode(encoding='utf-8')
                    m.update(b)
                    md5 = m.hexdigest()
                    file_path = settings.COVER_IMG + '/' + md5 + '/'
                    is_exists = os.path.exists(file_path)
                    if not is_exists:
                        os.makedirs(file_path)
                    async with aiofiles.open(file_path + 'cover.jpg', 'wb') as f:
                        await f.write(img)
                        await f.close()
                        img_url = '/static/images/' + md5 + '/cover.jpg'
                books = BookLists.objects.create(name=name, author=author, url=book_data['url'],
                                                 introduction=introduction, newest_chapter=newest_chapter,
                                                 last_update_time=last_time, chapter_num=len(chapter_list),
                                                 create_time=create_time, cover=img_url, name_author_md5=md5,
                                                 classification=classification, source_id=source.id)
                chapter_lists = []
                chapter_list_url = data.xpath(source.book_chapter_list_url)
                for c_list in chapter_list:
                    chapter_url = chapter_list_url[chapter_list.index(c_list)]
                    chapter_lists.append(
                        ChapterLists(
                            name=c_list,
                            url=chapter_url if chapter_url.find('http') >= 0 else source.domain + chapter_url,
                            book=books,
                            source=source
                        )
                    )
                ChapterLists.objects.bulk_create(chapter_lists)
                return True


@require_http_methods(['POST'])
def add_search_book(request):
    data = eval(request.body)
    loop = asyncio.new_event_loop()
    book_list = loop.run_until_complete(add_book(data))
    return JsonResponse({'results': book_list})


# async def update_chapter(url: str, bookid: int) -> bool:
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as resp:
#             con = await resp.text(encoding='gbk')
#             soup = BeautifulSoup(con, 'lxml')
#             book_types = soup.select('.ffw tr td')
#             chapter_list = soup.select('.conter')[0]  # 获取div
#             chapter_list.find('table').extract()  # 删除不需要标签
#             chapter_list.select('.tt1')[0].extract()
#             chapter_list = chapter_list.find_all('a')  # 获取最终列表
#             last_time = book_types[6].string
#             newest_chapter = book_types[7].a.string
#             this_book = BookLists.objects.get(id=bookid)
#             last_crawling_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#             if this_book.chapter_num == len(chapter_list):
#                 BookLists.objects.filter(id=bookid).update(last_update_time=last_time, chapter_num=len(chapter_list),
#                                                            newest_chapter=newest_chapter,
#                                                            last_crawling_time=last_crawling_time)
#                 return False
#             else:
#                 chapter_lists = []
#                 for list in chapter_list[this_book.chapter_num:]:
#                     chapter_lists.append(
#                         ChapterLists(
#                             name=list.string,
#                             url=settings.DOMAIN + list.get('href'),
#                             book=this_book
#                         )
#                     )
#                 ChapterLists.objects.bulk_create(chapter_lists)
#                 BookLists.objects.filter(id=bookid).update(last_update_time=last_time, chapter_num=len(chapter_list),
#                                                            newest_chapter=newest_chapter,
#                                                            last_crawling_time=last_crawling_time)
#                 return True

async def update_chapter(source_id: int, book_id: int) -> bool:
    # 获取书源信息
    source = BookSource.objects.get(pk=source_id)
    # 获取章节信息
    chapter = BookLists.objects.get(pk=book_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(chapter.url) as resp:
            try:
                con = await resp.text()
            except UnicodeDecodeError:
                con = await resp.text(encoding='gbk')
            # 使用xpath
            result_data = etree.HTML(con)
            # 获取章节列表链接
            chapter_list = result_data.xpath(source.book_chapter_list)
            chapter_list_urls = result_data.xpath(source.book_chapter_list_url)
            # 获取最后更新时间和爬取时间
            last_crawl_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(result_data.xpath(source.book_last_time))
            last_update_time = result_data.xpath(source.book_last_time)[0]
            new_time = last_update_time.split('：')
            if len(new_time) > 1:
                last_update_time = new_time[1]
                if last_update_time.find('/') >= 0:
                    last_update_time = last_update_time.replace('/', '-')
                # last_update_time.replace('/', '-') if last_update_time.find('/') >= 0 else last_update_time
            # print(last_update_time)
            # if last_update_time.find("更新时间") >=0 or last_update_time.find("更新时间：") >=0:
            #     last_update_time = last_update_time.replace('更新时间：','')
            #     last_update_time = last_update_time.replace('更新时间','')
            #     last_update_time = last_update_time.replace('“', '')
            #     last_update_time = last_update_time.replace('”', '')
            chapter_list_count = len(chapter_list)
            # 如果没有更新
            if chapter_list_count == chapter.chapter_num:
                # 这里不用更新最新章节
                BookLists.objects.filter(id=book_id).update(last_update_time=last_update_time, chapter_num=chapter_list_count,
                                                                           last_crawling_time=last_crawl_time)
                return False
            else:
                chapter_lists = []
                # 创建一个新的集合jieq
                for val in chapter_list[chapter.chapter_num:]:
                    i = chapter_list.index(val)
                    chapter_lists.append(
                        ChapterLists(
                            name=val,
                            url=chapter_list_urls[i] if chapter_list_urls[i].find('http') >=0 else source.domain + chapter_list_urls[i],
                            book=chapter
                        )
                    )
            with transaction.atomic():
                # 一次性写入
                ChapterLists.objects.bulk_create(chapter_lists)
                # 更新书籍列表
                BookLists.objects.filter(id=book_id).update(last_update_time=last_update_time,
                                                            chapter_num=chapter_list_count,
                                                            newest_chapter=chapter_lists[-1].name,
                                                            last_crawling_time=last_crawl_time)
            return True


@require_http_methods(['POST'])
def update_book_chapter(request):
    data = eval(request.body)
    loop = asyncio.new_event_loop()
    source_id = BookLists.objects.get(pk=data['id']).source_id
    chapter = loop.run_until_complete(update_chapter(source_id, data['id']))
    return JsonResponse({'results': chapter})


async def batch_add_books(index: int, count: int) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.DOMAIN + "/xiaoshuodaquan/") as resp:
            con = await resp.text(encoding='gbk')
            soup = BeautifulSoup(con, 'lxml')
            lists = soup.select('.novellist')[index - 1].ul.find_all('li')
            num = 0
            for book in lists:
                if num >= count:
                    break
                book_url = book.find('a').get('href')
                try:
                    BookLists.objects.get(url=settings.DOMAIN + book_url)
                except BookLists.DoesNotExist:
                    await add_book(book_url)
                    num += 1
            return True


@require_http_methods(['GET'])
def batch_add_book(request):
    loop = asyncio.new_event_loop()
    batch = loop.run_until_complete(batch_add_books(int(request.GET['index']), int(request.GET['count'])))
    return JsonResponse({'results': batch})


async def insert_content(url: str, chapter_id: int) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                con = await resp.text()
            except UnicodeDecodeError:
                con = await resp.text(encoding='gbk')
            data = etree.HTML(con)
            chapter = ChapterLists.objects.get(pk=chapter_id)
            source = BookSource.objects.get(pk=chapter.source_id)
            contents = data.xpath(source.book_chapter_info)[0]
            contents = html.tostring(contents)
            contents = HTMLParser().unescape(contents.decode())
            words_number = len(contents)
            results = ChapterInfo.objects.create(content=contents, words_number=words_number, chapter_id=chapter_id)
            if results:
                return True
            else:
                return False


class BookList(APIView):

    def get(self, request, *args, **kwargs):
        source_model = BookSource.objects.all()
        source = BookSourceSerializer(source_model, many=True)
        return Response(source.data)

