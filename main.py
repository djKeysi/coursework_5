import requests
import json
from utils.utils import create_database, save_data_to_database, run_interface
from sql_queries.config import config
from classes.managerdb import DBManager


def main():
    params = config()
    create_database('hh_mzk_nvk', params)
    dbmanager = DBManager()
    print(
        "Добро пожаловать в программу получения списка вакансий в IT cфере по городам Кемеровской области,\n а именно Междуреченска и Новокузнецка")
    flag = True
    flag_back = True

    while flag:
        flag_back = True
        user_input = input("""У вас есть два города по которым вы можете вывести информацию по вакансиям
                                    1 - Междуреченск
                                    2 - Новокузнецк
                                    0 - Выход\n""")
        if user_input == "1":
            user_prof = input("Введите название вакансии, например Программист, Системный администратор\n")
            save_data_to_database(1238, user_prof, 'hh_mzk_nvk', params)
            run_interface(dbmanager, params, flag_back)

        elif user_input == "2":
            user_prof = input("Введите название вакансии, например Программист, Системный администратор\n")
            save_data_to_database(1240, user_prof, 'hh_mzk_nvk', params)
            run_interface(dbmanager, params, flag_back)
        elif user_input == "0":
            flag = False


if __name__ == '__main__':
    main()


