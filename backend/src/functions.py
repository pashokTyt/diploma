import os
import django
from rapidfuzz import fuzz
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplom.settings')
django.setup()
from pravo import models


def update_published_flags():
    queryset = models.PublishedNPA.objects.all()

    # НПА из источника "ИПС Законодательство"
    ips_data = queryset.filter(source__name__iexact="ИПС Законодательство")

    # Неопубликованные НПА из других источников (published=False)
    other_unpublished_npas = queryset.filter(
        published=False
    ).exclude(source__name__iexact="ИПС Законодательство")

    updated_count = 0

    for other_npa in other_unpublished_npas:
        found_match = False

        for ips_npa in ips_data:

            
            # Или fuzzy-сравнение названий с порогом 85
            name_score = fuzz.token_sort_ratio(other_npa.name, ips_npa.name)
            other_number = str(other_npa.number).strip()
            ips_number = str(ips_npa.number).strip()

            if name_score > 65 and other_number == ips_number:
                found_match = True
                break

        if found_match:
            other_npa.published = True
            other_npa.save(update_fields=['published'])
            updated_count += 1

    print(f"Обновлено меток published для {updated_count} НПА.")



import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplom.settings')
django.setup()
from pravo import models
from django.db.models import Count
from django.db import transaction

def remove_duplicates():
    total_deleted = 0

    # Получаем все источники
    sources = models.PublishedNPA.objects.values_list('source', flat=True).distinct()

    for source_id in sources:
        # Находим все записи для источника, сгруппированные по (name, number, publish_date)
        duplicates_qs = (
            models.PublishedNPA.objects
            .filter(source_id=source_id)
            .values('name', 'number', 'publish_date')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        for dup in duplicates_qs:
            # Для каждой группы дубликатов получаем все id
            records = models.PublishedNPA.objects.filter(
                source_id=source_id,
                name=dup['name'],
                number=dup['number'],
                publish_date=dup['publish_date']
            ).order_by('id')  # сортируем, чтобы оставить первый

            ids = list(records.values_list('id', flat=True))
            ids_to_delete = ids[1:]  # оставляем первый

            with transaction.atomic():
                deleted_count, _ = models.PublishedNPA.objects.filter(id__in=ids_to_delete).delete()
                total_deleted += deleted_count

            print(f"Источник {source_id}: удалено {len(ids_to_delete)} дубликатов для НПА '{dup['name']}' номер {dup['number']} дата {dup['publish_date']}")

    print(f"Всего удалено дубликатов: {total_deleted}")
    

if __name__ == "__main__":
    update_published_flags()
    remove_duplicates()



