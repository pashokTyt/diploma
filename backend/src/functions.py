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
            if name_score > 85:
                found_match = True
                break

        if found_match:
            other_npa.published = True
            other_npa.save(update_fields=['published'])
            updated_count += 1

    print(f"Обновлено меток published для {updated_count} НПА.")


if __name__ == "__main__":
    update_published_flags()
