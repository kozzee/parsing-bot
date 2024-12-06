import requests

def simple_clean(text):
    if text is None:
        return ''  # Возвращаем пустую строку или любое другое значение по умолчанию
    
    return text.replace('<highlighttext>', '').replace('</highlighttext>', '')


def get_token_api():
    
    headers = {
        'HH-User-Agent': 'MyApp/1.0 (contact@example.com)'}
    # URL для получения токена
    url = 'https://api.hh.ru/token'

    # Замените 'YOUR_CLIENT_ID' и 'YOUR_CLIENT_SECRET' на ваши данные
    data = {
        'grant_type': 'client_credentials',  # Тип авторизации
        'client_id': 'P7D2ORKJR7UN6DL6NAL743IAO1KEDU1C3AA6SKJSSBLG9ALBNSN9FF6OQL0B2DH2',       # Идентификатор клиента
        'client_secret': 'TLT1NPOHSOVN9Q42U1GA26R6T6M6QP7PRQAG9VD80ES0PQ7JN13PGKFRFT4OLO4Q' # Секрет клиента
    }

    # Выполняем POST-запрос для получения токена
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['access_token']
        return access_token
    else: print('Ошибка получения токена')


def get_vacancies(page=0):

    url = 'https://api.hh.ru/vacancies'
    auth = 'APPLNR71F4DBJBQGBCDIADJR1U1D2B34NCF8MTNSTBILGLV18NI5SJT41M5KSUT6'
    print(auth)
    vacan = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Authorization': f'Bearer {auth}',       
    }

    # Параметры запроса (только area)
    params = {
        'area': 1,       # Регион
        'per_page': 10,  # Количество вакансий на странице
        'page': page,        # Номер страницы\
        'text': 'python'
    }

    try:
        # Отправляем GET-запрос
        response = requests.get(url, headers=headers, params=params)
        # Проверяем статус-код ответа
        if response.status_code == 200:
            vacancies = response.json()

            for vacancy in vacancies.get('items', []):
                vacancy_title = vacancy['name']  # Название вакансии
                vacancy_url = vacancy['alternate_url']  # Ссылка на вакансию
                employer_name = vacancy['employer']['name']  # Название работодателя
                des = vacancy.get('snippet', {}).get('responsibility', 'Нет описания')  # Описание обязанностей
                description = simple_clean(des)

                vacan.append({
                    'title': vacancy_title,
                    'employer': employer_name,
                    'description': description,
                    'link': vacancy_url
                })
        else:
            print(f"Ошибка {response.status_code}: {response.text}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    return vacan
