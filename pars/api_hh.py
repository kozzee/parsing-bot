import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

url = 'https://hh.ru/search/vacancy?text=python&salary=&ored_clusters=true&enable_snippets=true&area=1&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line'
response = requests.get(url, headers=headers)
html = response.text
print(html)