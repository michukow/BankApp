#BankApp

import json, hashlib
from datetime import datetime

class User:
    def __init__(self,username,password,money,transactions=[]):
        self.username=username
        self.password=password
        self.money=money
        self.transactions=transactions

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
        if user["username"]==username:
            password=input("Insert password: ").strip()

            if user["password"]==hashlib.sha256(password.encode()).hexdigest():
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
        print("3 - Deposit money")
        print("4 - Log out")
        print()

        choice=str(input("Choose option: "))

        if choice=="1":
            withdraw(username)
        elif choice=="2":
            change_password(username)
        elif choice=="3":
            deposit(username)
        elif choice=="4":
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

    while True:
        try:
            withdraw_value=float(input("Insert value to withdraw: ").strip())
            if not username or withdraw_value<=0:
                print("Insert valid value!")
                continue
            break
        except ValueError:
            print("An error occured. Try again.")

    for user in data:
        if user["username"]==username:
            if user["money"]>=withdraw_value:
                user["money"]-=withdraw_value

                transaction={
                    "type": "withdraw",
                    "amount": withdraw_value,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "balance_after": user["money"]
                }

                if "transactions" not in user:
                    user["transactions"]=[]

                user["transactions"].append(transaction)

                with open("data.json","w",encoding="utf-8") as file:
                    json.dump(data,file,indent=4)

                print(f"Money withdrawn. Current balance: {user['money']}")
                return
            else:
                print("Not enough money.")
                return

#deposit
def deposit(username):
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data=json.load(file)
    except FileNotFoundError:
        print("File not found.")
        return None

    while True:
        try:
            money_to_deposit=float(input("Insert a money to deposit: "))
            if not money_to_deposit or money_to_deposit<=0:
                print("Please, insert valid amount.")
                continue
            break
        except ValueError:
            print("An error occured. Try again.")

    for user in data:
        if user["username"]==username:
            user["money"]+=money_to_deposit

            transaction={
                "type": "deposit",
                "amount": money_to_deposit,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "balance_after": user["money"]
            }

            if "transactions" not in user:
                user["transactions"]=[]

            user["transactions"].append(transaction)

            with open("data.json","w",encoding="utf-8") as file:
                json.dump(data,file,indent=4)

            print(f"Money deposited. Current balance: {user['money']}")
            return

#change password
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
        if user["username"]==username:
            user["password"]=hashlib.sha256(changed_password.encode()).hexdigest()
            with open("data.json","w",encoding="utf-8") as file:
                json.dump(data,file,indent=4)
            print("Password changed successfully.")
            return

#create new account
def register():
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data=json.load(file)
    except FileNotFoundError:
        print("File not found.")
        return None

    #username
    while True:
        try:
            new_username=input("Insert a username: ")
            if not new_username:
                print("The username can not be empty.")
                continue
            if len(new_username)<=3:
                print("Username is too short. Try logner one - more than 3 chars.")
                continue
            if any(user["username"] == new_username for user in data):
                print("Username already exists.")
                continue
            break
        except ValueError:
            print("An error occured. Try again!")

    #password
    while True:
        try:
            new_password=input("Insert a password: ")
            if not new_password:
                print("The password should not be empty.")
                continue
            if len(new_password)<=3:
                print("The length of password should be more than 3.")
                continue
            break
        except ValueError:
            print("An error occured. Try again!")

    #money
    while True:
        try:
            new_money=float(input("Insert amount of money: "))
            if not new_money or new_money<0:
                print("You should deposit some money")
                continue
            break
        except ValueError:
            print("An error occured. Try again!")
    
    #creating account
    account=User(new_username,hashlib.sha256(new_password.encode()).hexdigest(),new_money)

    try:
        with open("data.json","r",encoding="utf-8") as file:
            data=json.load(file)

    except FileNotFoundError:
        print("File not found.")
        return None

    data.append(account.to_dict())

    with open("data.json","w",encoding="utf-8") as file:
        json.dump(data,file,indent=4,ensure_ascii=False)

    print(f"New account was added successfully!")

def main():
    print("Hello! Welcome at Bank!")
    print("Select an activity: ")

    while True:
        print()
        print("1 - Login in")
        print("2 - Register account")
        print("3 - Exit")
        print()

        choice=str(input("Choose option: "))

        if choice=="1":
            login()
        elif choice=="2":
            register()
        elif choice=="3":
            break
        else:
            print("Select valid option.")

if __name__ == "__main__":
    main()