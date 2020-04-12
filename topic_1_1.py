import requests
import json
from pprint import pprint

main_link = 'https://api.github.com'

user_name = 'Natalia1807'
param = {
    'Accept': '*/*'
}

response = requests.get(f'{main_link}/users/{user_name}/repos', params=param)
# print(response.text)
if response.ok:
    data = response.json()
repositories = []
for item in data:
    repositories.append(item['name'])
print(f'У пользователя {user_name} {len(repositories)} репозиториев на GitHab {repositories}')