import logging

import requests
import datetime as datetime
import os
import django
from bs4 import BeautifulSoup  # type: ignore

import asyncio
import aiohttp  # type: ignore
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


from asgiref.sync import sync_to_async

# если импорт перенести наверх, то ничего не будет работать, 
# т.к. джанга генерит ошибку "django.configure не дает использовать models в постороннем модуле"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplom.settings')
django.setup()
from pravo import models


logging.basicConfig(filename='parser.log', level=logging.INFO)

def get_data_pravo_gov_ru(base_url = "http://publication.pravo.gov.ru/api/Documents", 
                          block="region57", start_index=1, 
                          end_index=4, source_name="pravo.gov.ru"):
    try:
        source = models.Source.objects.get(name=source_name)
    except models.Source.DoesNotExist:
        print(f"Источник '{source_name}' не найден в базе данных.")
        return

    region_name = "ОРЛОВСКАЯ ОБЛАСТЬ"
    try:
        region = models.Region.objects.get(name=region_name)
    except models.Region.DoesNotExist:
        print(f"Регион '{region_name}' не найден в базе данных.")
        return

    for index in range(start_index, end_index + 1):
        params = {
            "Block": block,
            "Index": index
        }

        response = requests.get(base_url, params=params)  # type: ignore

        if response.status_code == 200:
            data = response.json()
            documents = data.get("items", [])
            date_current = datetime.now().date()

            for element in documents:
                name = element.get("name")
                number = element.get("number")
                publish_date_str = element.get("documentDate")
                write_date_str = element.get("publishDateShort")

                if 'T' in write_date_str:
                    write_date_str = write_date_str.split(
                        'T')[0]
                if 'T' in publish_date_str:
                    publish_date_str = publish_date_str.split(
                        'T')[0]

                existing_npa = models.PublishedNPA.objects.filter(
                    name=name,
                    number=number,
                    write_date=datetime.strptime(
                        write_date_str, '%Y-%m-%d').date()
                ).first()

                if existing_npa:

                    existing_npa.published = True
                    existing_npa.save()
                else:

                    try:
                        new_record = models.PublishedNPA(
                            published=False,
                            name=name,
                            number=number,
                            publish_date=datetime.strptime(
                                publish_date_str, '%Y-%m-%d').date(),
                            write_date=datetime.strptime(
                                write_date_str, '%Y-%m-%d').date(),
                            date_now=date_current,
                            link_to_download='-',
                            source=source,
                            region=region
                        )
                        new_record.save()

                    except ValueError as e:
                        print(f"Ошибка преобразования даты для {name}: {e}")

    print("pravo-gov-ru собран")

def get_data_min_just(url = 'https://pravo-search.minjust.ru/bigs/portal.html#%7B%22filter%22:null,%22groups%22:%5B%22%D0%A2%D0%B5%D0%BA%D1%83%D1%89%D0%B8%D0%B5%20%D1%80%D0%B5%D0%B4%D0%B0%D0%BA%D1%86%D0%B8%D0%B8%22%5D,%22dateFrom%22:null,%22dateTo%22:null,%22sortOrder%22:%22desc%22,%22sortField%22:%22document_date_edition%22,%22groupField%22:null,%22joinFrom%22:null,%22joinTo%22:null,%22type%22:%22MULTIQUERY%22,%22multiqueryRequest%22:%7B%22queryRequests%22:%5B%7B%22type%22:%22Q%22,%22request%22:%22%7B%5C%22mode%5C%22:%5C%22EXTENDED%5C%22,%5C%22typeRequests%5C%22:%5B%7B%5C%22fieldRequests%5C%22:%5B%7B%5C%22name%5C%22:%5C%22document_subject_rf_cat%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22%D0%9E%D1%80%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C%5C%22,%5C%22sQuery%5C%22:null%7D%5D,%5C%22mode%5C%22:%5C%22AND%5C%22,%5C%22name%5C%22:%5C%22%D0%9F%D1%80%D0%B0%D0%B2%D0%BE%D0%B2%D1%8B%D0%B5%20%D0%B0%D0%BA%D1%82%D1%8B%5C%22,%5C%22typesMode%5C%22:%5C%22AND%5C%22%7D%5D%7D%22,%22operator%22:%22AND%22,%22queryRequestRole%22:%22CATEGORIES%22%7D,%7B%22type%22:%22SQ%22,%22queryId%22:%220e9d52f7-f799-4297-b3e1-b3c6ceacb494%22,%22operator%22:%22AND%22%7D%5D%7D,%22simpleSearchFieldsBundle%22:%22test1%22,%22noOrpho%22:false%7D', 
                      region_name='ОРЛОВСКАЯ ОБЛАСТЬ', source_name='min-just'):
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--incognito")
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "resultOuter"))
    )

    req_text = driver.page_source
    soup = BeautifulSoup(req_text, "lxml")

    legal_act = soup.find_all("div", class_="bgs-result")

    try:
        source = models.Source.objects.get(name=source_name)
    except models.Source.DoesNotExist:
        print(f"Источник '{source_name}' не найден в базе данных.")
        return

    try:
        region = models.Region.objects.get(name=region_name)
    except models.Region.DoesNotExist:
        print(f"Регион '{region_name}' не найден в базе данных.")
        return

    for act in legal_act:
        header_link = act.find("a", class_="resultHeader openCardLink")

        if header_link is not None:
            name = header_link.text.strip()
            number = header_link.text.split("№")[1].strip().split(
                ' ')[0] if "№" in header_link.text else "N/A"
            date = header_link.text.split("от")[1].strip().split(
                ' ')[0] if "от" in header_link.text else "N/A"
            date_post = soup.find(class_='wrap').find_next_sibling(
            ).find_next_sibling().find_next_sibling().text.strip()

            try:
                write_date = datetime.strptime(date_post, '%d.%m.%Y').date()
                publish_date = datetime.strptime(date, '%d.%m.%Y').date()
            except ValueError as e:
                print(f"Ошибка преобразования даты: {e}")
                continue

            existing_npa = models.PublishedNPA.objects.filter(
                name=name,
                number=number,
                write_date=write_date
            ).first()

            if existing_npa:
                existing_npa.published = True
                existing_npa.save()
            else:
                new_record = models.PublishedNPA(
                    published=False,
                    name=name,
                    number=number,
                    publish_date=publish_date,
                    write_date=write_date,
                    date_now=datetime.now().date(),
                    link_to_download=header_link.get("href"),
                    source=source,
                    region=region
                )
                new_record.save()

    driver.quit()
    print("Min-just собран")

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81",
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_data_orel_region(url="shit", region_name="ОРЛОВСКАЯ ОБЛАСТЬ", source_name="orel-region"):
    orel_url = "https://orel-region.ru"

    async with aiohttp.ClientSession() as session:
        req_text = await fetch(session, url="https://orel-region.ru/index.php?head=17&part=61&page=")
        soup = BeautifulSoup(req_text, "lxml")

        page_count = int(soup.find("div", class_="pagenavig").text.split(":")[
                         1].split(".")[0])

        tasks = []
        for page in range(0, page_count)[0:10]:
            page_url = f"https://orel-region.ru/index.php?head=17&part=61&page={
                page}"
            tasks.append(fetch(session, page_url))

        pages_content = await asyncio.gather(*tasks)

        sources = {source.name: source for source in await sync_to_async(list)(models.Source.objects.all())}
        regions = {region.name: region for region in await sync_to_async(list)(models.Region.objects.all())}

        for page_content in pages_content:
            soup = BeautifulSoup(page_content, "html.parser")

            legal_act_orel_region = soup.find_all("div", class_="textdoc")

            for act in legal_act_orel_region:
                name = act.get_text().split("[")[0]
                date_info = act.find(
                    "span", class_="textCream").text.split("от")

                if len(date_info) > 1:
                    date = date_info[1].strip()
                else:
                    print(f"Не удалось найти дату для акта: {name}")
                    continue

                number = act.find("span", class_="textCream").text.split("№")[
                    1].split("от")[0].strip()
                date_post_info = act.find("font").text.split(":")

                if len(date_post_info) > 1:
                    date_post = date_post_info[1].strip()
                    if 'T' in date_post:
                        date_post = date_post.split(
                            'T')[0]
                else:
                    print(f"Не удалось найти дату поста для акта: {name}")
                    continue

                try:
                    publish_date = datetime.strptime(date, '%d.%m.%Y').date()
                except ValueError as e:
                    print(
                        f"Ошибка преобразования даты публикации для {name}: {e}")
                    continue

                try:
                    write_date = datetime.strptime(
                        date_post, '%d.%m.%Y').date()
                except ValueError as e:
                    print(
                        f"Ошибка преобразования даты подписания для {name}: {e}")
                    continue

                existing_npa_query = models.PublishedNPA.objects.filter(
                    name=name,
                    number=number,
                    write_date=write_date,
                    publish_date=publish_date
                )

                existing_npa = await sync_to_async(existing_npa_query.first)()

                if existing_npa:
                    existing_npa.published = True
                    await sync_to_async(existing_npa.save)()
                else:
                    link_to_download = act.find("a")
                    if link_to_download:
                        link_to_download = link_to_download.get("href")
                    else:
                        link_to_download = ""
                    try:
                        new_record = models.PublishedNPA(
                            published=False,
                            name=name,
                            number=number,
                            publish_date=publish_date,
                            write_date=write_date,
                            date_now=datetime.now().date(),
                            link_to_download=link_to_download,
                            source=sources.get(source_name),
                            region=regions.get(region_name)
                        )
                        await sync_to_async(new_record.save)()

                    except ValueError as e:
                        print(f"Ошибка преобразования даты для {name}: {e}")
    print("Orel_region собран")

from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re

def get_data_IPS():
    # тут начались танцы с бубном, сайт подгружает все динамически, поэтому нашел ЮРЛ, который возвращает html, в котором таблица со всеми НПА
    url = "http://pravo.gov.ru/proxy/ips/?list_itself=&bpas=r015700&a3=&a3type=1&a3value=&a6=&a6type=1&a6value=&a15=113000053&a15type=1&a15value=%CE%F0%EB%EE%E2%F1%EA%E0%FF+%EE%E1%EB%E0%F1%F2%FC&a7type=4&a7from=26.03.2025&a7to=02.04.2025&a7date=&a8=&a8type=1&a1=&a0=&a16=&a16type=1&a16value=&a17=&a17type=1&a17value=&a4=&a4type=1&a4value=&a23=&a23type=1&a23value=&textpres=&sort=7&x=62&y=10&page=firstlast"
    try:
        response = requests.get(url)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        exit()

    with open("page_source.html", "w", encoding="utf-8") as file:
        file.write(response.text)

    with open("page_source.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    table = soup.find("table", class_="list_elem even")

    if table:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            for col in cols:
                if col.find("div", class_="l_link"):
                    link_div = col.find("div", class_="l_link")
                    name = link_div.find("a").text.strip()

                    match = re.search(r'№\s*(\d+)', name)
                    if match:
                        number = match.group(1)
                    else:
                        number = "Номер не найден"

                    publish_date_str = "26.03.2025" 
                    write_date_str = "26.03.2025"
                    date_current = datetime.today().date()
                    link_to_download = '-'

                    source_name = "ИПС Законодательство"
                    try:
                        source_instance = models.Source.objects.get(name=source_name)
                    except models.Source.DoesNotExist:
                        source_instance = models.Source.objects.create(name=source_name, url_address="http://example.com")

                    region_name = "ОРЛОВСКАЯ ОБЛАСТЬ"
                    try:
                        region_instance = models.Region.objects.get(name=region_name)
                    except models.Region.DoesNotExist:
                        region_instance = models.Region.objects.create(name=region_name, code="57")

                    try:
                        new_record = models.PublishedNPA(
                            published=False,
                            name=name,
                            number=number,
                            publish_date=datetime.strptime(publish_date_str, '%d.%m.%Y').date(),
                            write_date=datetime.strptime(write_date_str, '%d.%m.%Y').date(),
                            date_now=date_current,
                            link_to_download=link_to_download,
                            source=source_instance,
                            region=region_instance
                        )
                        new_record.save()
                    except Exception as e:
                        print(f"Ошибка при сохранении записи: {e}")
    else:
        print("Таблица не найдена")




def parse_orel_npa():
    logging.info('Парсер запущен')
    try:
        get_data_pravo_gov_ru()
    except ValueError as e:
        print(f'Ошибка парсинга с pravo.gov.ru: {e}')
    
    try: 
        get_data_min_just()
    except ValueError as e:
                print(f"Ошибка парсинга с min-just: {e}")
                
    try:
        asyncio.run(get_data_orel_region())
    except ValueError as e:
                print(f"Ошибка парсинга с  orel-region: {e}")
    
    try:
        get_data_IPS()
    except ValueError as e:
                print(f"Ошибка парсинга с  ИПС Законодательство: {e}")
                
                
    logging.info('Парсер завершил работу')

if __name__ == "__main__":
    parse_orel_npa()
    