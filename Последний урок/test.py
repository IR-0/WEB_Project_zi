import requests
from requests import get, post, delete


out = 0
"""
print(get('http://localhost:5000/api/jobs').json())
print(post('http://localhost:5000/api/jobs', json={'id': 16,
                                                   'job': 'Описание работы',
                                                   'team_leader': 7,
                                                   'work_size': 58,
                                                   'collaborators': '6, 7, 4',
                                                   'is_finished': False}).json())
print(get('http://localhost:5000/api/jobs').json())
# Ошибочный запрос, переданы только 2 параметра
print(post('http://localhost:5000/api/jobs', json={'id': 14,
                                                   'job': 'Все сложно'}).json())
# отсутствие данных json
print(post('http://localhost:5000/api/jobs').json())
# указанный ID уже существует в БД
print(post('http://localhost:5000/api/jobs', json={'id': 3,
                                                   'job': 'Описание работы',
                                                   'team_leader': 5,
                                                   'work_size': 58,
                                                   'collaborators': '6, 7, 4',
                                                   'is_finished': False}).json())
print(get('http://localhost:5000/api/jobs').json())
"""
out = 1
"""
print(get('http://localhost:5000/api/users').json())

print(get('http://localhost:5000/api/users/6').json())  # true

print(get('http://localhost:5000/api/users/-7').json())  # false

print(get('http://localhost:5000/api/users/first').json())  # false

print(post('http://localhost:5000/api/users', json={'name': 'buddy', 'surname': 'doew', 'age': 31,
                                                    'position': 'electrogypsy', 'speciality': 'pizza',
                                                    'address': 'module_1', 'email': 'aeaeauoa@mail.com',
                                                    'hasged_password': '123'}).json())  # true
print(post('http://localhost:5000/api/users', json={}).json())  # false
print(post('http://localhost:5000/api/users', json={'speciality': 'pizza'}).json())  # false
print()
print(get('http://localhost:5000/api/users').json())
print(delete('http://localhost:5000/api/users/4').json())  # Nah
print(get('http://localhost:5000/api/users/4').json())
"""
out = 2
"""
print(get('http://localhost:5000/api/jobs').json())

print(get('http://localhost:5000/api/jobs/1').json())  # true

print(get('http://localhost:5000/api/jobs/-7').json())  # false

print(get('http://localhost:5000/api/jobs/first').json())  # false

print(post('http://localhost:5000/api/jobs', json={'job': 'buddy"s work', 'team_leader': 1, 'work_size': 2,
                                                   'collaborators': 'all', 'is_finished': False}).json())  # true
print(post('http://localhost:5000/api/jobs', json={}).json())  # false
print(post('http://localhost:5000/api/jobss', json={'job': 'pizza'}).json())  # false
print()
print(get('http://localhost:5000/api/jobs').json())
print(delete('http://localhost:5000/api/jobs/4').json())  # Nah
print(get('http://localhost:5000/api/jobs/4').json())
"""
'''
out = 3

print(get('http://localhost:5000/api/jobs').json())

print(delete('http://localhost:5000/api/deljobs/3').json())  # true
print(delete('http://localhost:5000/api/deljobs/-3').json())  # false
print(delete('http://localhost:5000/api/deljobs/third').json())  # false
print(delete('http://localhost:5000/api/deljobs/').json())  # false

print(get('http://localhost:5000/api/jobs').json())
'''

print(get('http://127.0.0.1:5000/news'))
