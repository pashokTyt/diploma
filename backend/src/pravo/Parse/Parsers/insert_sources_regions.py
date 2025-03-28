from datetime import datetime
import psycopg2

block = {
    "РЕСПУБЛИКА АДЫГЕЯ": "region01",
    "РЕСПУБЛИКА АЛТАЙ": "region04",
    "РЕСПУБЛИКА БАШКОРТОСТАН": "region02",
    "РЕСПУБЛИКА БУРЯТИЯ": "region03",
    "РЕСПУБЛИКА ДАГЕСТАН": "region05",
    "ДОНЕЦКАЯ НАРОДНАЯ РЕСПУБЛИКА": "region80",
    "РЕСПУБЛИКА ИНГУШЕТИЯ": "region06",
    "КАБАРДИНО-БАЛКАРСКАЯ РЕСПУБЛИКА": "region07",
    "РЕСПУБЛИКА КАЛМЫКИЯ": "region08",
    "КАРАЧАЕВО-ЧЕРКЕССКАЯ РЕСПУБЛИКА": "region09",
    "РЕСПУБЛИКА КАРЕЛИЯ": "region10",
    "РЕСПУБЛИКА КОМИ": "region11",
    "РЕСПУБЛИКА КРЫМ": "region91",
    "ЛУГАНСКАЯ НАРОДНАЯ РЕСПУБЛИКА": "region81",
    "РЕСПУБЛИКА МАРИЙ ЭЛ": "region12",
    "РЕСПУБЛИКА МОРДОВИЯ": "region13",
    "РЕСПУБЛИКА САХА (ЯКУТИЯ)": "region14",
    "РЕСПУБЛИКА СЕВЕРНАЯ ОСЕТИЯ - АЛАНИЯ": "region15",
    "РЕСПУБЛИКА ТАТАРСТАН": "region16",
    "РЕСПУБЛИКА ТЫВА": "region17",
    "УДМУРТСКАЯ РЕСПУБЛИКА": "region18",
    "РЕСПУБЛИКА ХАКАСИЯ": "region19",
    "ЧЕЧЕНСКАЯ РЕСПУБЛИКА": "region20",
    "КАЛУЖСКАЯ ОБЛАСТЬ": "region40",
    "КЕМЕРОВСКАЯ ОБЛАСТЬ - КУЗБАСС": "region42",
    "КИРОВСКАЯ ОБЛАСТЬ": "region43",
    "КОСТРОМСКАЯ ОБЛАСТЬ": "region44",
    "КУРГАНСКАЯ ОБЛАСТЬ": "region45",
    "КУРСКАЯ ОБЛАСТЬ": "region46",
    "ЛЕНИНГРАДСКАЯ ОБЛАСТЬ": "region47",
    "ЛИПЕЦКАЯ ОБЛАСТЬ": "region48",
    "МАГАДАНСКАЯ ОБЛАСТЬ": "region49",
    "МОСКОВСКАЯ ОБЛАСТЬ": "region50",
    "МУРМАНСКАЯ ОБЛАСТЬ": "region51",
    "НИЖЕГОРОДСКАЯ ОБЛАСТЬ": "region52",
    "НОВГОРОДСКАЯ ОБЛАСТЬ": "region53",
    "НОВОСИБИРСКАЯ ОБЛАСТЬ": "region54",
    "ОМСКАЯ ОБЛАСТЬ": "region55",
    # ст 39 ЗАКОН ОРЕНБУРГСКОЙ ОБЛАСТИ УСТАВ (ОСНОВНОЙ ЗАКОН) ОРЕНБУРГСКОЙ ОБЛАСТИ Принят решением Законодательного Собрания Оренбургской области от 25 октября 2000 г. N 724
    "ОРЕНБУРГСКАЯ ОБЛАСТЬ": "region56",
    # Закон Орловской области от 15.04.2003 N 319-ОЗ (ред. от 03.11.2022) "О правотворчестве и нормативных правовых актах Орловской области" (принят ООСНД 04.04.2003) (вместе с "Правилами юридико-технического оформления проектов нормативных правовых актов") (с изм. и доп., вступающими в силу с 01.01.2023) статья 56
    "ОРЛОВСКАЯ ОБЛАСТЬ": "region57",
    "ПЕНЗЕНСКАЯ ОБЛАСТЬ": "region58",
    "ПСКОВСКАЯ ОБЛАСТЬ": "region60",
    "РОСТОВСКАЯ ОБЛАСТЬ": "region61",
    "РЯЗАНСКАЯ ОБЛАСТЬ": "region62",
    "САМАРСКАЯ ОБЛАСТЬ": "region63",
    "САРАТОВСКАЯ ОБЛАСТЬ": "region64",
    "ЧУВАШСКАЯ РЕСПУБЛИКА - ЧУВАШИЯ": "region21",
    "АЛТАЙСКИЙ КРАЙ": "region22",
    "ЗАБАЙКАЛЬСКИЙ КРАЙ": "region75",
    "КАМЧАТСКИЙ КРАЙ": "region41",
    "КРАСНОДАРСКИЙ КРАЙ": "region23",
    "КРАСНОЯРСКИЙ КРАЙ": "region24",
    "ПЕРМСКИЙ КРАЙ": "region59",
    "ПРИМОРСКИЙ КРАЙ": "region25",
    "СТАВРОПОЛЬСКИЙ КРАЙ": "region26",
    "ХАБАРОВСКИЙ КРАЙ": "region27",
    "АМУРСКАЯ ОБЛАСТЬ": "region28",
    "АРХАНГЕЛЬСКАЯ ОБЛАСТЬ": "region29",
    "АСТРАХАНСКАЯ ОБЛАСТЬ": "region30",
    "БЕЛГОРОДСКАЯ ОБЛАСТЬ": "region31",
    "БРЯНСКАЯ ОБЛАСТЬ": "region32",
    "ВЛАДИМИРСКАЯ ОБЛАСТЬ": "region33",
    "ВОЛГОГРАДСКАЯ ОБЛАСТЬ": "region34",
    "ВОЛОГОДСКАЯ ОБЛАСТЬ": "region35",
    "ВОРОНЕЖСКАЯ ОБЛАСТЬ": "region36",
    "ЗАПОРОЖСКАЯ ОБЛАСТЬ": "region85",
    "ИВАНОВСКАЯ ОБЛАСТЬ": "region37",
    "ИРКУТСКАЯ ОБЛАСТЬ": "region38",
    "КАЛИНИНГРАДСКАЯ ОБЛАСТЬ": "region39",
    "САХАЛИНСКАЯ ОБЛАСТЬ": "region65",
    "СВЕРДЛОВСКАЯ ОБЛАСТЬ": "region66",
    "СМОЛЕНСКАЯ ОБЛАСТЬ": "region67",
    "ТАМБОВСКАЯ ОБЛАСТЬ": "region68",
    "ТВЕРСКАЯ ОБЛАСТЬ": "region69",
    "ТОМСКАЯ ОБЛАСТЬ": "region70",
    "ТУЛЬСКАЯ ОБЛАСТЬ": "region71",
    "ТЮМЕНСКАЯ ОБЛАСТЬ": "region72",
    "УЛЬЯНОВСКАЯ ОБЛАСТЬ": "region73",
    "ХЕРСОНСКАЯ ОБЛАСТЬ": "region84",
    "ЧЕЛЯБИНСКАЯ ОБЛАСТЬ": "region74",
    "ЯРОСЛАВСКАЯ ОБЛАСТЬ": "region76",
    "МОСКВА": "region77",
    "САНКТ-ПЕТЕРБУРГ": "region78",
    "СЕВАСТОПОЛЬ": "region92",
    "ЕВРЕЙСКАЯ АВТОНОМНАЯ ОБЛАСТЬ": "region79",
    "НЕНЕЦКИЙ АВТОНОМНЫЙ ОКРУГ": "region83",
    "ХАНТЫ-МАНСИЙСКИЙ АВТОНОМНЫЙ ОКРУГ - ЮГРА": "region86",
    "ЧУКОТСКИЙ АВТОНОМНЫЙ ОКРУГ": "region87",
    "ЯМАЛО-НЕНЕЦКИЙ АВТОНОМНЫЙ ОКРУГ": "region89"
}
# нужно собрать еще кучу дополнительных данных - как минимум кто принял


sources = [
    {"name": "pravo.gov.ru", "url_address": "https://pravo.gov.ru"},
    {"name": "orel-region", "url_address": "https://orel-region.ru"},
    {"name": "min-just", "url_address": "http://pravo-minjust.ru/"}
]

""" orel """


def regions_to_db(data):
    try:
        conn = psycopg2.connect(
            dbname="NPA",
            user="user_yapa",
            password="qazwsxQAZWSX",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        for name, code in data.items():
            try:
                code=code.split("region")[1]
                cursor.execute('''
                    INSERT INTO region (name, code) VALUES (%s, %s)
                ''', (name, code))
                
            except psycopg2.Error as e:
                print(f"Ошибка при сохранении региона '{name}': {e}")

        conn.commit()
        print("Regions inserted.")

    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def sources_to_db(data):
    try:
        conn = psycopg2.connect(
            dbname="NPA",
            user="user_yapa",
            password="qazwsxQAZWSX",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        for source in data:
            try:
                cursor.execute('''
                    INSERT INTO source (name, url_address) VALUES (%s, %s)
                ''', (
                    source['name'],
                    source['url_address']
                ))
            except psycopg2.Error as e:
                print(f"Ошибка при сохранении источника '{
                      source['name']}': {e}")

        conn.commit()
        print("Sources inserted.")

    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    """ sources_to_db(sources) """
    regions_to_db(block)
