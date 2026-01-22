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
    while True:
        try:
            username=input("Inser a username: ")
            if not username:
                print("The username can not be empty.")
                continue

            try:
                with open("data.json","r",encoding="utf-8") as file:
                    data=json.load(file)
                for user in data:
                    if user["user"]==username:
                        print("User was found.")
                        return user 

                    print("Not found.")
                    return None

            except FileNotFoundError:
                print("File not found.")
                data=[]
                return None

        except FileNotFoundError:
            print("File was not found.")
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