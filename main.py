import requests
import json
from classes.managerdb import create_database,save_data_to_database
from sql_queries.config import config


def main():
    params = config()
    create_database('hh_mzk_nvk',params)


    user_input = input("""У вас есть два города по которым вы можете вывести информацию по вакансиям
                            1 - Междуреченск
                            2 - Новокузнецк\n""")
    if user_input == "1":
        save_data_to_database(1238, 'Программист', 'hh_mzk_nvk', params)
    else:
        save_data_to_database(1240, 'Программист', 'hh_mzk_nvk', params)

if __name__ == '__main__':
    main()