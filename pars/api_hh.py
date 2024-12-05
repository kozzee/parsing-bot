import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'  #тут я пытаюсь притворяться браузером
}

url = 'https://hh.ru/search/vacancy?text=python&salary=&ored_clusters=true&enable_snippets=true&area=1&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line'  #ссылка по которой буду парсить
response = requests.get(url, headers=headers)
html_code = response.text
bs = BeautifulSoup(html_code, 'html.parser')


def get_number_of_vacation(): #функция возвращает количество найденный вакансий
    number_element = bs.find('h1', {'data-qa': 'title'})

    # Извлекаем текст из элемента и очищаем его
    if number_element:
        # Убираем пробелы и текст внутри тега <span>
        vacancies_text = number_element.get_text(strip=True)
        # Оставляем только число (удаляем всё, кроме цифр и пробелов)
        vacancies_number = ''.join(filter(str.isdigit, vacancies_text))
    return vacancies_number



def extract_vacancies():
    vacancies = [] #здесь будут данные вакансий
    containers = bs.find_all("div", {"class": "vacancy-info--ieHKDTkezpEj0Gsx"}) #разбить страницу по вакансиям
    for container in containers:

        title_element = container.find("h2", {"data-qa": "bloko-header-2"})
        if title_element is not None:
            title = title_element.text.strip()
        else:
            continue
        
        employer_element = container.find("a", {"data-qa": "vacancy-serp__vacancy-employer"})
        if employer_element is not None:
            employer = employer_element.text.strip()
        else:
            continue
        
        description_elements = container.find_all("div", {"data-qa": "vacancy-serp__vacancy_snippet_responsibility"})
        if len(description_elements) > 0: #проверка есть ли описание
            description = description_elements[0].text.strip()
            requirement_elements = container.find_all("div", {"data-qa": "vacancy-serp__vacancy_snippet_requirement"})
            if len(requirement_elements) > 0:
                description += "\n\nТребования:\n" + requirement_elements[0].text.strip()
        else:
            description = ""

        link_block = container.select_one('a[data-qa="serp-item__title"]')
        link_url = link_block['href'] if link_block else ''

        vacancies.append({
            'title': title,
            'employer': employer,
            'description': description,
            'link': link_url
        })
    
    return vacancies

vacancies = extract_vacancies()
for vacancy in vacancies:
    print(f"Название вакансии: {vacancy['title']}")
    print(f"Работодатель: {vacancy['employer']}")
    print(f"Ссылка на вакансию: {vacancy['link']}")
    print(f"Описание вакансии: {vacancy['description']}")
    print("\n")