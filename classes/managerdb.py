import psycopg2


class DBManager:
    """Класс DBManager должен использовать библиотеку psycopg2 для работы с БД"""

    def get_companies_and_vacancies_count(self, database_name: str, params: dict) -> None:
        """метод получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                   CREATE VIEW vac as
                   SELECT  company.name_company, (SELECT COUNT(*) as count_vacancies FROM vacancies WHERE 
				   company.company_id =vacancies.company_id  ) FROM company GROUP BY company.company_id    ORDER BY count_vacancies DESC

                """)

        with conn.cursor() as cur:
            cur.execute("""
                 SELECT name_company, COUNT(name_company) AS count_vac FROM vac GROUP BY name_company 
                 ORDER BY count_vac DESC

             """)
            records = cur.fetchall()
            for row in records:
                print(f"Наименование компании: {row[0]}, Количество вакансий: {row[1]} ")

        conn.commit()
        conn.close()

    def get_all_vacancies(self, database_name: str, params: dict) -> None:
        """метод получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                SELECT company.name_company, vacancies.name_vacancy, vacancies.salary_from, vacancies.salary_to, vacancies.vacancies_url
                FROM vacancies
                JOIN company USING (company_id)
                ORDER BY company.name_company;
             """)
            records = cur.fetchall()
            for row in records:
                print(
                    f"Наименование компании: {row[0]}, Наименование вакансии: {row[1]}, Зарплата от {row[2]}, Зарплата до {row[3]}, Ссылка на вакансию {row[4]}")

        conn.commit()
        conn.close()

    def get_avg_salary(self, database_name: str, params: dict) -> None:
        """метод получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                       SELECT round(AVG(vacancies.salary_from)) as salary_from ,round(AVG(vacancies.salary_to)) as salary_to FROM vacancies
                    """)
            records = cur.fetchall()
            for row in records:
                print(
                    f"Средняя зарплата по вакансиям зарплаты от {row[0]} и зарплаты до  {row[1]}")

        conn.commit()
        conn.close()

    def get_vacancies_with_higher_salary(self, database_name: str, params: dict) -> None:
        """метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                               SELECT name_vacancy, salary_from, salary_to, vacancies_url
                               FROM vacancies
                               WHERE (SELECT AVG((vacancies.salary_from + vacancies.salary_to) / 2)
                               FROM vacancies) < ((salary_from + salary_to) / 2) ORDER BY salary_from;

                            """)
            records = cur.fetchall()
            for row in records:
                print(
                    f"Наименование вакансии: {row[0]}, Зарплата от {row[1]}, Зарплата до {row[2]}, Ссылка на вакансию {row[3]}")

        conn.commit()
        conn.close()

    def get_vacancies_with_keyword(self, keywords, database_name: str, params: dict) -> None:
        """метод получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                            SELECT name_vacancy, salary_from, salary_to, vacancies_url
                            FROM vacancies
                            WHERE vacancies.name_vacancy LIKE (%s)
                            or vacancies.requirement LIKE (%s)
                            or vacancies.responsibility LIKE (%s)
                            ORDER BY vacancies.salary_to  """,
                        (f'%{keywords}%', f'%{keywords}%', f'%{keywords}%')
                        )
            records = cur.fetchall()
            for row in records:
                print(
                    f"Наименование вакансии: {row[0]}, Зарплата от {row[1]}, Зарплата до {row[2]}, Ссылка на вакансию {row[3]}")

        conn.commit()
        conn.close()
