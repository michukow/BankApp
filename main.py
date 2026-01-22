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
                return user
            else:
                print("Invalid password.")
                return None

    print("Username was not found.")
    return None

def create():
    print("Creating account...")

def main():
    print("Hello! Welcome at Bank!")
    print("Select an activity: ")

    while True:
        print()
        print("1 - Login in")
        print("2 - Create new account")
        print()

        choice=str(input("Choose option: "))

        if choice=="1":
            login()
        elif choice=="2":
            create()
        else:
            print("Select valid option.")


if __name__ == "__main__":
    main()