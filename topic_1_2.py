import requests
import json
#https://api.vk.com/method/users.get?user_id=210700286&v=5.52
#https://api.vk.com/method/friends.getOnline?v=5.52&access_token=
method_name = 'groups.get'
main_link = 'https://api.vk.com/method/'
#https://api.vk.com/method/METHOD_NAME?PARAMETERS&access_token=ACCESS_TOKEN&v=V
access_token_1 = '2b54fb037dd998aca92d679baa5fe6d595df6664740416cc73dfb4286fbebfa0956c20d10c089026fe497'
param = {
    'access_token': access_token_1,
    'v': 5.52
}

response = requests.get(f'{main_link}/{method_name}?extended=1', params=param)
#print(response.text)

if response.ok:
    data = response.json()
group_name = []
t = data["response"]["items"]
#print(t)
for item in t:
    group_name.append(item["name"])

print(f'Пользователь Наталья Андреева состоит в {data["response"]["count"]} группах ВК c названиями: {group_name}')

