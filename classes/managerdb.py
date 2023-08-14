import psycopg2



class DBManager:

    """Класс DBManager должен использовать библиотеку psycopg2 для работы с БД"""
    def get_companies_and_vacancies_count(self,database_name: str, params: dict) -> None:
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



    def get_all_vacancies(self,database_name: str, params: dict):
        """метод получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            sqlite_select_query = """SELECT * from company"""
            cur.execute(sqlite_select_query)
            records = cur.fetchall()
            print("Всего строк:  ", len(records))
            print("Вывод каждой строки")
            for row in records:
                print("ID:", row)
                #print("ID:", row[1])

        conn.commit()
        conn.close()

    def get_avg_salary(self):
        """метод получает среднюю зарплату по вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self):
        """метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self):
        """метод получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        pass



