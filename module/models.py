from django.db import models
from django.db import connection
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


NULLABLE = {'blank': True, 'null': True}


class Subject(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название темы')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='slug', **NULLABLE)
    description = models.TextField(verbose_name='Краткое писание', blank=True)

    def __str__(self):
        return f'{self.title} - {self.slug}'

    class Meta:
        verbose_name = 'тема'
        verbose_name_plural = 'темы'
        ordering = ['title']

    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(
                f'ALTER SEQUENCE '
                f'catalog_statusproduct_id_seq RESTART WITH 1;'
                )


class Block(models.Model):
    creator = models.ForeignKey(get_user_model(), related_name='courses_created', on_delete=models.CASCADE,
                                verbose_name='Владелец')
    subject = models.ForeignKey(Subject, related_name='blocks', on_delete=models.CASCADE, verbose_name='Тема')
    title = models.CharField(max_length=200, verbose_name='Название блока')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='slug', **NULLABLE)
    description = models.TextField(verbose_name='Краткое описание', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'блок'
        verbose_name_plural = 'блоки'
        ordering = ['-created']

    def __str__(self):
        return f'{self.title} - {self.slug}'

    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(
                f'ALTER SEQUENCE '
                f'catalog_statusproduct_id_seq RESTART WITH 1;'
                )


class Module(models.Model):
    course = models.ForeignKey(Block, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(verbose_name='Краткое описание', blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(
                f'ALTER SEQUENCE '
                f'catalog_statusproduct_id_seq RESTART WITH 1;'
                )

class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':(
                                     'text',
                                     'video',
                                     'image',
                                     'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')


class ItemBase(models.Model):
    creator = models.ForeignKey(get_user_model(),
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE,
                              verbose_name='Владелец')
    title = models.CharField(max_length=250, verbose_name='Название')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField(verbose_name='Текст')


class File(ItemBase):
    file = models.FileField(upload_to='files', verbose_name='PDF файл', **NULLABLE)


class Image(ItemBase):
    file = models.FileField(upload_to='images', verbose_name='Изображение', **NULLABLE)


class Video(ItemBase):
    url = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
