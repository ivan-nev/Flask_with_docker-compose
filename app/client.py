import requests

# response = requests.get('http://127.0.0.1:5000')
# print(response.status_code)
# print(response.text)
#
# response = requests.post('http://127.0.0.1:5000/hello', json={'w':'h'}, headers={'token':'some_token'},
#                          params={'ke1':'1', 'key 2':'2'})
# print(response.status_code)
# print(response.json())

#создать пользователя
response = requests.post('http://127.0.0.1:5000/users', json={'username':'user_3', 'password':'45df!gKlasdx_'})
print(response.status_code)
print(response.json())

# response = requests.get('http://127.0.0.1:5000/users/1')
# print(response.status_code)
# print(response.json())
#
# response = requests.patch('http://127.0.0.1:5000/users/13', json={'username':'user','password':'123'})
# print(response.status_code)
# print(response.json())

response = requests.get('http://127.0.0.1:5000/users/13')
print(response.status_code)
print(response.json())
#
# response = requests.delete('http://127.0.0.1:5000/users/5')
# print(response.status_code)
# print(response.json())

# response = requests.get('http://127.0.0.1:5000/adv/1')
# print(response.status_code)
# print(response.json())

#создать статью
response = requests.post('http://127.0.0.1:5000/adv/', json={'title':'title 13', 'description':'kakayta hren', 'id_user':'13'})
print(response.status_code)
print(response.json())

# response = requests.get('http://127.0.0.1:5000/adv/4')
# print(response.status_code)
# print(response.json())

# response = requests.patch('http://127.0.0.1:5000/adv/11', json={'title':'super_puper','description':'123','id_user':5})
# print(response.status_code)
# print(response.json())

# response = requests.delete('http://127.0.0.1:5000/adv/1')
# print(response.status_code)
# print(response.json())