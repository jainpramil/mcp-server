import requests

url = "http://127.0.0.1:8000/tools/get_leave_balance"
data = {"employee_id": "E001"}

response = requests.post(url, json=data)
print(response.json())