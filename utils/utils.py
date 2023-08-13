import json
import requests

def get_vacancy(area: list, text: str) -> json:

    params = {
        'text': f"NAME:{text}",  # Системный администратор
        'per_page': 100,
        'area': area  # зона кемеровская область #47 кемерово # 1238 - междуреченск # 1240 - Новокузнецк
        # 'page':page
    }
    req = requests.get('https://api.hh.ru/vacancies', params=params).json()
    return req

def add_vacancy_for_novokuznetsk_and_mezhdurechensk(text:str) -> None:
    """Добавление вакансий из моих родных городов Новокузнецк и Междуреченск """
    with open("vacancy.json", 'w', encoding='utf-8') as file:
        json.dump(get_vacancy(1238,text), file, indent=2, ensure_ascii=False)
    with open("vacancy.json", 'r', encoding='utf-8') as file:
        file_mzk = json.load(file)
    file_mzk['items'].append(get_vacancy(1240, text))
    with open("vacancy.json", 'w', encoding='utf-8') as file:
        json.dump(file_mzk, file, indent=2, ensure_ascii=False)


def read_to_json():
    with open("vacancy.json", 'r', encoding='utf-8') as file:
        file_mzk_nvk = json.load(file)
    return file_mzk_nvk

#"../utils/vacancy.json"







#add_vacancy_for_novokuznetsk_and_mezhdurechensk('Программист')









