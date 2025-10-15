import requests

url: str = "http://127.0.0.1:8000/todos/"
url2: str = f"http://127.0.0.1:8000/todos/{2}"

new_todo: dict = {
    "id": 1,
    "title" : "Doing homework",
    "description" : "need to finish OS module 6 notes",
    "completed": False,
}


response = requests.post(url=url, json=new_todo)

if response.status_code == 404:
    print(f"Error with API call: {response.status_code} | {response.text}")
else:
    print("No Errors")
    print(response.json())

response2 = requests.get(url2)
if response2.status_code == 404:
    print(f"Error with API call: {response2.status_code} | {response2.text}")
else:
    print("No Errors")
    print(response2.json())
