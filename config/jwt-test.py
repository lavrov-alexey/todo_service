import requests

DOMAIN = 'http://127.0.0.1:8000'


def get_url(url):
    return f'{DOMAIN}{url}'


response = requests.post(get_url('/api-jwt-token/'), data={"username": "AUTO_SU", "password": "gfhjkm1234"})
result = response.json()
# это короткоживущий токен для использования в текущих запросах на сервер
access_token = result['access']
print(f'Первый токен: {access_token=}')
# это долгоживущий токен для обновления короткоживущего
refresh_token = result['refresh']
print(f'refresh {refresh_token=}')

# Авторизуемся с короткоживущим токеном
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get(get_url('/api/projects'), headers=headers)
print(f'{response=}')

# Обновляем токен
response = requests.post(get_url('/api-jwt-token/refresh/'), data={'refresh': refresh_token})
print(f'Обновляем JWT токен:\n{response.status_code=},\n{response.text=}')
result = response.json()
# обновленный короткоживущий токен
access_token = result['access']
print(f'Обновленный токен:\n{access_token=},\n{refresh_token=}')

# Авторизуемся с новым короткоживущим токеном
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get(get_url('/api/projects'), headers=headers)
print(f'{response=}')
