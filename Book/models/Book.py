from django.db import models
from django.utils.html import format_html
import django.utils.timezone as timezone
from django.db.models import Count
from django.contrib.admin import ModelAdmin


class BookClassification(models.Model):
    name = models.CharField("分类名称", max_length=100)
    sort = models.PositiveSmallIntegerField("排序", default=1)
    url = models.CharField("分类地址", max_length=200, default='')
    num = models.PositiveSmallIntegerField("每次抓取数量", default=10)

    class Meta:
        verbose_name = "书籍分类"
        verbose_name_plural = "书籍分类"
        db_table = "book_class"
        ordering = ['id']

    def __str__(self):
        return self.name

    def book_number(self):
        book_count = self.booklists_set.count()
        return book_count
    book_number.short_description = "书籍数量"

    def add_books(self):
        return format_html('<a class="changelink" @click="add_books({},{})" v-loading.fullscreen.lock="fullscreenLoading" href="javascript:;">一键加书</a>', "'"+self.url+"'", self.num)
    add_books.short_description = "操作"


class BookSource(models.Model):
    name = models.CharField("书源名称", max_length=100, default='')
    domain = models.CharField("书源域名", max_length=100, default='')
    search_url = models.CharField("搜索地址", max_length=255, default='')
    book_info_common = models.TextField("书籍信息公共链接", default='')
    book_info = models.TextField("书籍信息(逗号分隔,书名，地址，作者，最新章，时间)", default='')
    book_cover = models.TextField("封面", default='')
    book_intro = models.TextField("简介", default='')
    book_chapter_list = models.TextField("章节列表", default='')
    book_chapter_list_url = models.TextField("章节列表链接", default='')
    book_chapter_info = models.TextField("章节详情", default='')
    book_last_time = models.TextField("最后更新时间", default='')

    class Meta:
        verbose_name = "书源列表"
        verbose_name_plural = "书源列表"
        db_table = 'book_source'
        ordering = ['id']

    def __str__(self):
        return self.name

    def book_number(self):
        book_count = self.booklists_set.count()
        return book_count
    book_number.short_description = "书籍数量"


class BookLists(models.Model):
    name = models.CharField("书籍名称", max_length=50)
    name_author_md5 = models.CharField("文件夹得md5", max_length=32, default=0)
    author = models.CharField("作者", max_length=30)
    cover = models.CharField("书籍封面", max_length=255)
    url = models.CharField("书籍地址", max_length=255)
    introduction = models.TextField("简介", default='')
    newest_chapter = models.CharField("最新章节", max_length=100)
    last_update_time = models.DateTimeField("最后更新时间", default=timezone.now)
    chapter_num = models.PositiveSmallIntegerField("章节总数")
    create_time = models.DateTimeField("添加时间")
    last_crawling_time = models.DateTimeField("最后爬取时间", default=timezone.now)
    classification = models.ForeignKey(BookClassification, on_delete=models.CASCADE, default=1)
    source = models.ForeignKey(BookSource, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = "书籍列表"
        verbose_name_plural = "书籍列表"
        db_table = "book_list"
        ordering = ['id']

    def __str__(self):
        return self.name

    def show_cover(self):
        return format_html('<img src="{}" style="width:60px;">', self.cover)
    show_cover.short_description = "头像"

    def buttons(self):
        return format_html('<a class="changelink" @click="update_chapter({},{})" v-loading.fullscreen.lock="fullscreenLoading" href="javascript:;">更新章节</a>', "'"+self.url+"'", self.id)

    buttons.short_description = "操作"

    def target_chpter(self):
        return format_html('<a href="/#/chapter/{}" target="_blank">跳转</a>',self.id)

    target_chpter.short_description = "书籍目录"


class ChapterLists(models.Model):
    name = models.CharField("章节名称", max_length=200)
    url = models.CharField("章节地址", max_length=255)
    book = models.ForeignKey(BookLists, on_delete=models.CASCADE, default=1, related_name='chapters')
    source = models.ForeignKey(BookSource, on_delete=models.CASCADE, default=1, related_name='sources')

    class Meta:
        verbose_name = "章节列表"
        verbose_name_plural = "章节列表"
        db_table = "book_chapter_list"
        ordering = ['id']

    def __str__(self):
        return self.name


class ChapterInfo(models.Model):
    content = models.TextField("章节内容")
    words_number = models.SmallIntegerField("章节字数", default=0)
    chapter_id = models.IntegerField("章节id", default=0)

    class Meta:
        db_table = "book_chapter_info"
        ordering = ['id']

