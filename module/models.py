from django.db import models
from django.db import connection
from django.contrib.auth import get_user_model


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
                                verbose_name='Создатель')
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
