import requests
import json
import psycopg2
from utils.utils import read_to_json,get_vacancy
from typing import Any


class DBManager:

    # def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432',
    #              table_name: str = 'repos_stats'):
    #     self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    #     self.cur = self.conn.cursor()
    #     self.table_name = table_name
    #
    #     self._create_table()




    """Класс DBManager должен использовать библиотеку psycopg2 для работы с БД"""
    def get_companies_and_vacancies_count(self):
        """метод получает список всех компаний и количество вакансий у каждой компании."""

    def get_all_vacancies(self):
        """метод получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        pass

    def get_avg_salary(self):
        """метод получает среднюю зарплату по вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self):
        """метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self):
        """метод получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        pass


DBmanager = DBManager()
#print(DBmanager.get_companies_and_vacancies_count())


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    # cur.execute("SELECT datname FROM pg_database WHERE datname = %s", (database_name,))
    # result = cur.fetchone()
    # if result:
    #     # Если база данных существует, удаляем ее
    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)


    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE company (
                company_id SERIAL PRIMARY KEY,
                name_company VARCHAR(100) NOT NULL,
                discription TEXT,
                company_url VARCHAR(100) 

            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                company_id   INT REFERENCES company (company_id),
                name_vacancy VARCHAR(100) NOT NULL,
                salary_from TEXT,
                salary_to TEXT,
                requirement    TEXT,
                responsibility TEXT,
                vacancies_url TEXT
            )
        """)

    conn.commit()
    conn.close()


def fill_to_database():
    #with open("../utils/vacancy.json", 'r', encoding='utf-8') as file:
        #file_mzk = json.load(file)
    #     count = 0
        for member in get_vacancy(1240,"Программист")['items']:
            #if member.get('employer') is not None:
            print(member['employer']['name'])
            print(member['name'])
            #print(member['snippet']['responsibility'])
           # print(member['employer']['vacancies_url'])
            if member.get("salary", "") is not None:
                if member.get("salary", {}).get("to") is None:
                    print(str(member.get("salary", {}).get("from", "")))
                else:
                    print(str(member.get("salary", {}).get("to", "")))
            else:
                print("-")

#print(get_vacancy(1240,"Программист"))
#fill_to_database()

def hh():
    for member in get_vacancy(1240, "Программист")['items']:
        # if member.get('employer') is not None:
        print(member['employer']['name'])
        print(member['name'])
        # print(member['snippet']['responsibility'])
        # print(member['employer']['vacancies_url'])
        if member.get("salary", "") is not None:
            if member.get("salary", {}).get("to") is None:
                print(type(str(member.get("salary", {}).get("from", ""))))
            else:
                print(type(str(member.get("salary", {}).get("to", ""))))
        else:
            print("-")
hh()






def save_data_to_database(city:int,profession:str,database_name: str, params: dict):
    """Сохранение данных о каналах и видео в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for vac in get_vacancy(city,profession)['items']:
            name_company=vac['employer']['name']
           #discription = vac['address']['description']
            company_url = vac['employer']['alternate_url']
            name_vacancy=vac['name']
            salary_from = str(vac['salary'].get('from', "0"))
            salary_to = str(vac['salary'].get('to', "0"))
            # salary_to = str(vac.get("salary", {}).get("from"))
            # salary_from = str(vac.get("salary", {}).get("to"))
            responsibility=vac['snippet']['responsibility']
            requirement =vac['snippet']['requirement']
            vacancies_url=vac['employer']['vacancies_url']
            cur.execute(
                    """
                    INSERT INTO company (name_company,discription,company_url)
                    VALUES (%s, %s, %s)
                    RETURNING company_id
                    """,
                    (name_company,"ffff",company_url)
            )

            company_id = cur.fetchone()[0]
            if vac.get("salary", "") is None:
                cur.execute(
                            """
                            INSERT INTO vacancies (company_id,name_vacancy, salary_from,salary_to,responsibility,requirement,vacancies_url)
                            VALUES (%s, %s, %s, %s,%s, %s,%s)
                                                                  """,
                    (company_id,name_vacancy, 0,0, responsibility, requirement,vacancies_url)
                            )
            elif vac.get("salary", {}).get("to") is None:
                cur.execute(
                    """
                    INSERT INTO vacancies (company_id,name_vacancy, salary_from,salary_to,responsibility,requirement,vacancies_url)
                    VALUES (%s, %s, %s, %s,%s, %s,%s)
                                                          """,
                    (company_id, name_vacancy, salary_from, 0, responsibility, requirement, vacancies_url)
                )
            elif vac.get("salary", {}).get("from") is None:
                cur.execute(
                    """
                    INSERT INTO vacancies (company_id,name_vacancy, salary_from,salary_to,responsibility,requirement,vacancies_url)
                    VALUES (%s, %s, %s, %s,%s, %s,%s)
                                                          """,
                    (company_id, name_vacancy, 0, salary_to, responsibility, requirement, vacancies_url)
                )
            else:
                cur.execute(
                    """
                    INSERT INTO vacancies (company_id,name_vacancy, salary_from,salary_to,responsibility,requirement,vacancies_url)
                    VALUES (%s, %s, %s, %s,%s, %s,%s)
                                                          """,
                    (company_id, name_vacancy, salary_from, salary_to, responsibility, requirement, vacancies_url)
                )

    conn.commit()
    conn.close()