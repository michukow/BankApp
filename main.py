#BankApp

import json

class User:
    def __init__(self,id_number,login,password,money=0):
        self.id_number=id_number
        self.login=login
        self.password=password
        self.money=money

    def to_dict(self):
        return self.__dict__

def login():
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data=json.load(file)
    except FileNotFoundError:
        print("File not found.")
        return None

    username=input("Insert username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return None

    for user in data:
        if user["user"]==username:
            password=input("Insert password: ").strip()

            if user["password"]==password:
                print("Login successful.")
                user_menu(username)
                return username
            else:
                print("Invalid password.")
                return None

    print("Username was not found.")
    return None

#When user is logged ...
def user_menu(username):
    print("Select an activity: ")
    while True:
        print()
        print("1 - Withdraw")
        print("2 - Change password")
        print("3 - Log out")
        print()

        choice=str(input("Choose option: "))

        if choice=="1":
            withdraw(username)
        elif choice=="2":
            change_password(username)
        elif choice=="3":
            break
        else:
            print("Select valid option.")

#Withdraw
def withdraw(username):
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data=json.load(file)
    except FileNotFoundError:
        print("File not found.")
        return None

    withdraw_value=float(input("Insert value to withdraw: ").strip())
    if not username or withdraw_value<=0:
        print("Insert valid value!")
        return None

    for user in data:
        if user["user"]==username:
            if user["money"]>=withdraw_value:
                user["money"]-=withdraw_value

                with open("data.json","w",encoding="utf-8") as file:
                    json.dump(data,file,indent=4)

                print(f"Money withdrawn. Current balance: {user['money']}")
                return
            else:
                print("Not enough money.")
                return

def change_password(username):
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data=json.load(file)
    except FileNotFoundError:
        print("File not found.")
        return None

    changed_password=input("Insert new password: ").strip()

    if not changed_password:
        print("Insert valid password!")
        return None

    for user in data:
        if user["user"]==username:
            user["password"] = changed_password
            with open("data.json","w",encoding="utf-8") as file:
                json.dump(data,file,indent=4)
            print("Password changed successfully.")
            return

def main():
    print("Hello! Welcome at Bank!")
    print("Select an activity: ")

    while True:
        print()
        print("1 - Login in")
        print("2 - Exit")
        print()

        choice=str(input("Choose option: "))

        if choice=="1":
            login()
        elif choice=="2":
            break
        else:
            print("Select valid option.")


if __name__ == "__main__":
    main()