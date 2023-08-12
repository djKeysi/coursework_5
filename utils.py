import requests

class DBManager:
    """Класс DBManager должен использовать библиотеку psycopg2 для работы с БД"""
    def get_companies_and_vacancies_count(self):
        """метод получает список всех компаний и количество вакансий у каждой компании."""
        pass

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


