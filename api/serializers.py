from rest_framework import serializers
from Book.models import ChapterLists, BookLists, BookClassification, ChapterInfo
from django.db.models import Count
from django.core.cache import cache
import pickle
import asyncio
from Book.views import insert_content


class BookClassSerializer(serializers.Serializer):
    name = serializers.CharField(label="分类名称", max_length=100)
    sort = serializers.IntegerField(label="排序",)
    url = serializers.CharField(label="分类地址", max_length=200)

    class Meta:
        model = BookClassification
        fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLists
        fields = ['id', 'name', 'author', 'cover', 'introduction', 'newest_chapter', 'last_update_time']


class InfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(label="id")
    name = serializers.CharField(label="书籍名称", max_length=50)
    author = serializers.CharField(label="作者", max_length=30)
    cover = serializers.CharField(label="书籍封面", max_length=30)
    introduction = serializers.CharField(label="简介", max_length=1000)

    class Meta:
        model = BookLists
        fields = '__all__'


class ChapterInfoSerializers(serializers.Serializer):
    content = serializers.CharField(label="章节内容")
    words_number = serializers.IntegerField(label="章节字数", default=0)
    chapter_id = serializers.IntegerField(label="章节id", default=0)


    class Meta:
        model = ChapterInfo
        fields = ['content', 'word_number']


class ChapterSerializer(serializers.Serializer):
    id = serializers.IntegerField(label="id")
    name = serializers.CharField(label="章节名称", max_length=200)
    url = serializers.CharField(label="章节地址", max_length=255)
    type_name = serializers.CharField(source='book.classification.name')
    book = InfoSerializer()

    class Meta:
        model = ChapterLists
        fields = ['id', 'name', 'url']

    def to_representation(self, instance):
        data = super(ChapterSerializer, self).to_representation(instance)
        if self.context['is_list'] == 0:
            next = ChapterLists.objects.filter(id__gt=data['id'], book_id=data['book']['id']).first()
            if next:
                data['next'] = next.id
            else:
                data['next'] = 0
            prev = ChapterLists.objects.filter(id__lt=data['id'], book_id=data['book']['id']).order_by('-id').first()
            if prev:
                data['prev'] = prev.id
            else:
                data['prev'] = 0
            prev_count = ChapterLists.objects.filter(id__lt=data['id'], book_id=data['book']['id']).aggregate(Count('id'))
            if prev_count:
                data['prev_count'] = prev_count['id__count']
            else:
                data['prev_count'] = 0
            chapter = cache.has_key("chapter_info_" + str(data['id']))
            if not chapter:
                try:
                    chapter_info = ChapterInfo.objects.get(chapter_id=data['id'])
                except ChapterInfo.DoesNotExist:
                    loop = asyncio.new_event_loop()
                    loop.run_until_complete(insert_content(data['url'], data['id']))
                    chapter_info = ChapterInfo.objects.get(chapter_id=data['id'])
                cache.set("chapter_info_" + str(data['id']), pickle.dumps(chapter_info), 3600000)
            else:
                chapter_info = pickle.loads(cache.get("chapter_info_" + str(data['id'])))  # 文章id
            data['content'] =chapter_info.content
            data['words_number'] =chapter_info.words_number
        return data


class ChapterSerializers(serializers.ModelSerializer):
    class Meta:
        model = ChapterLists
        fields = ['id', 'name']

