import json
import requests

query = {
    'city': "New York",
    'userId': 1
}

create_query = {
    "username": 'vladislav',
    "balance": 7000
}

# for i in range(1000):

    
req = requests.post('http://127.0.0.1:5000/decrease_balance', json=query)

print(req.text)

    # req = requests.post('http://127.0.0.1:5000/increase_balance', json=query)
    

# req = requests.post('http://127.0.0.1:5000/users', json=create_query)

# req = requests.get('http://127.0.0.1:5000/users')