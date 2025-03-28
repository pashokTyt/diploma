from django.db import models  # type: ignore
from django.db.models.functions import Now  # type: ignore
from datetime import datetime


class Region(models.Model):
    name = models.CharField("Регион", max_length=40)
    code = models.CharField("Код региона", max_length=3)

    class Meta:
        db_table = 'region'


class Source(models.Model):
    name = models.CharField("Источник опубликования", max_length=15)
    url_address = models.CharField(
        "Адрес источника опубликования", max_length=60)

    class Meta:
        db_table = 'source'


class PublishedNPA(models.Model):
    # метка опубликован ли НПА
    published = models.BooleanField("Есть ли на право.гов.ру?", default=False)

    name = models.CharField("Название НПА", max_length=None)
    number = models.CharField("Номер НПА", max_length=10)
    publish_date = models.DateField("Дата опубликования")
    write_date = models.DateField("Дата подписания НПА")
    date_now = models.DateField(
        verbose_name='Дата загрузки на портал', default=datetime.now)
    link_to_download = models.CharField(
        "Ссылка на скачивание", max_length=None)

    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name="published_npas"
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="published_npas"
    )

    class Meta:
        db_table = 'published_npa'
        ordering = ['-publish_date']
