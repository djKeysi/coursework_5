import requests
import json
from utils.utils import  create_database,save_data_to_database,run_interface
from sql_queries.config import config
from classes.managerdb import DBManager


def main():
    params = config()
    create_database('hh_mzk_nvk',params)
    dbmanager = DBManager()
    print("Добро пожаловать в программу получения списка вакансий в IT cфере по городам Кемеровской области,\n а именно Междуреченска и Новокузнецка")


    user_input = input("""У вас есть два города по которым вы можете вывести информацию по вакансиям
                                    1 - Междуреченск
                                    2 - Новокузнецк
                                    0 - Выход\n""")
    flag = True
    if user_input == "1":
        user_prof = input("Введите название вакансии, например Программист, Системный администратор\n")
        save_data_to_database(1238, user_prof, 'hh_mzk_nvk', params)
        while flag:
            user_questions = input("""                  Что вы хотите найти?
                                                           1 - Список всех компаний и количество вакансий у каждой компании.
                                                           2 - Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
                                                           3 - Среднюю зарплату по вакансиям в данном городе.
                                                           4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям в данном городе.
                                                           5 - Найти вакансию по ключевому слову.
                                                           0 - Выход\n""")
            run_interface(dbmanager, params,user_questions)
            if user_questions == "0":
                flag = False
    elif user_input == "2":
        user_prof = input("Введите название вакансии, например Программист, Системный администратор\n")
        save_data_to_database(1240, user_prof, 'hh_mzk_nvk', params)
        while flag:
            user_questions = input("""                  Что вы хотите найти?
                                                                      1 - Список всех компаний и количество вакансий у каждой компании.
                                                                      2 - Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
                                                                      3 - Среднюю зарплату по вакансиям в данном городе.
                                                                      4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям в данном городе.
                                                                      5 - Найти вакансию по ключевому слову.
                                                                      0 - Выход\n""")
            run_interface(dbmanager, params, user_questions)
            if user_questions == "0":
                flag = False












if __name__ == '__main__':

    main()


