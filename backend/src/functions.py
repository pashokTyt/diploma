import os
import django
from rapidfuzz import fuzz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplom.settings')
django.setup()
from pravo import models


def compare_npa():
    queryset = models.PublishedNPA.objects.all()
    pravo_gov_ru_data = queryset.filter(source__name__iexact="pravo.gov.ru")
    no_pravo_data = queryset.exclude(source__name__iexact="pravo.gov.ru")

    published_npa = set()
    not_published_npa = set()

    for npa in no_pravo_data:
        best_match = None
        best_score = 0

        for pravo_npa in pravo_gov_ru_data:
            name_score = fuzz.token_sort_ratio(npa.name, pravo_npa.name)
            if npa.number == pravo_npa.number and npa.write_date == pravo_npa.write_date:
                score = name_score + 100
            else:
                score = name_score

            if score > best_score:
                best_score = score
                best_match = pravo_npa

        if best_score > 80:
            published_npa.add((npa.name, npa.number, npa.write_date))
            npa.published = True
            npa.save()
        else:
            not_published_npa.add((npa.name, npa.number, npa.write_date))

    return published_npa, not_published_npa

published, not_published = compare_npa()
print("Опубликованные НПА:", published)
print("Неопубликованные НПА:", not_published)
