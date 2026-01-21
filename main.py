#BankApp

import json

class User:
    def __init__(self,login,password,money):
        self.login=login
        self.password=password
        self.money=money

    def to_dict(self):
        return self.__dict__

def login():
    

def create():

def main():
    print("Hello! Welcome at Bank!")
    print("Select an activity: ")
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