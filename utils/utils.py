import json
import requests
import psycopg2

def get_vacancy(area: list, text: str) -> json:

    params = {
        'text': f"NAME:{text}",  # Системный администратор
        'per_page': 100,
        'area': area  # зона кемеровская область #47 кемерово # 1238 - междуреченск # 1240 - Новокузнецк
        # 'page':page
    }
    req = requests.get('https://api.hh.ru/vacancies', params=params).json()
    return req



def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    # cur.execute("SELECT datname FROM pg_database WHERE datname = %s", (database_name,))
    # result = cur.fetchone()
    # if result:
    #     # Если база данных существует, удаляем ее
    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)


    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE company (
                company_id SERIAL PRIMARY KEY,
                name_company VARCHAR(100) NOT NULL,
                company_url VARCHAR(100) 

            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                company_id   INT REFERENCES company (company_id),
                name_vacancy VARCHAR(100) NOT NULL,
                salary_from INT,
                salary_to INT,
                requirement    TEXT,
                responsibility TEXT,
                vacancies_url TEXT
            )
        """)

    conn.commit()
    conn.close()

def save_data_to_database(city:int,profession:str,database_name: str, params: dict) ->None:
    """Сохранение данных о каналах и видео в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for vac in get_vacancy(city,profession)['items']:
            name_company=vac['employer']['name']
            company_url = vac['employer']['alternate_url']
            name_vacancy=vac['name']
            if vac["salary"]:
                salary_from =vac['salary']['from'] if vac['salary']['from'] else "0"
                salary_to = vac['salary']['to'] if vac['salary']['to'] else "0"
            else:
                salary_from="0"
                salary_to ="0"
            responsibility=vac['snippet']['responsibility']
            requirement =vac['snippet']['requirement']
            vacancies_url=vac['employer']['vacancies_url']
            cur.execute(
                    """
                    INSERT INTO company (name_company,company_url)
                    VALUES (%s, %s)
                    RETURNING company_id
                    """,
                    (name_company,company_url)
            )

            company_id = cur.fetchone()[0]
            cur.execute(
                            """
                            INSERT INTO vacancies (company_id,name_vacancy, salary_from,salary_to,responsibility,requirement,vacancies_url)
                            VALUES (%s, %s, %s, %s,%s, %s,%s)
                                                                  """,
                    (company_id,name_vacancy, salary_from,salary_to, responsibility, requirement,vacancies_url)
                            )

    conn.commit()
    conn.close()

#"../utils/vacancy.json"







#add_vacancy_for_novokuznetsk_and_mezhdurechensk('Программист')









