# cli.py
import requests

BASE_URL = "http://127.0.0.1:8000"

def show_menu():
    print("""
======================
PASSWORD MANAGER CLI
======================
1. Add new password
2. Retrieve password
3. Update password
4. Exit
""")

while True:
    show_menu()
    choice = input("Choose an option: ")

    if choice == "1":
        site = input("Site name: ")
        username = input("Username: ")
        password = input("Password: ")
        email = input("Email: ")
        res = requests.post(f"{BASE_URL}/add", json={
            "site": site,
            "username": username,
            "password": password,
            "email" : email
        })
        
        print(res.json())

    elif choice == "2":
        site = input("Enter site name: ")
        res = requests.get(f"{BASE_URL}/get/{site}")
        print(res.json())

    elif choice == "3":
        site = input("Enter site name to update: ")
        new_pw = input("Enter new password: ")
        res = requests.put(f"{BASE_URL}/update/{site}", json={"new_password": new_pw})
        print(res.json())

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice! Try again.")
