import json,hashlib,string,os
from datetime import datetime,timedelta

class User:
    def __init__(self,username,password,money,login_last,transactions=None,salt=None):
        self.username=username
        self.password=password
        self.salt=salt
        self.money=money
        self.transactions=transactions or []
        self.login_last=login_last

    def to_dict(self):
        return self.__dict__

def load(file_name):
    try:
        with open(file_name,"r",encoding="utf-8") as file:
            data=json.load(file)
            return data
    except (FileNotFoundError,json.JSONDecodeError):
        print(f"An error occured.")
        return []

def save(file_name,info):
    try:
        with open(file_name,"w",encoding="utf-8") as file:
            json.dump(info,file,indent=4,ensure_ascii=False)
    except FileNotFoundError:
        print("File not found")

def validate_password():
    #password for user michau: IamBoomer123!
    small_letters=string.ascii_lowercase
    great_letters=string.ascii_uppercase
    digits="1234567890"
    special="!@#$%^&*()-_+=|,./';[]{}:?><"

    while True:
        changed_password=input("Insert new password: ").strip()
        if len(changed_password)<=8:
            print("The password is too short. Try again!")
            continue
        if not any(char in special for char in changed_password):
            print("The password does not contain special characters. Try again.")
            continue
        if not any(char in small_letters for char in changed_password):
            print("The password does not contain small letters. Try again.")
            continue
        if not any(char in great_letters for char in changed_password):
            print("The password does not contain great letters. Try again.")
            continue
        if not any(char in digits for char in changed_password):
            print("The password does not contain digits. Try again.")
            continue
        return changed_password

def hash_password(password,salt=None):
    if salt is None:
        salt=os.urandom(16).hex()
    hashed_password=hashlib.sha256((salt+password).encode()).hexdigest()
    return hashed_password,salt

def check_password(password,stored_hash,salt):
    return hashlib.sha256((salt+password).encode()).hexdigest()==stored_hash

def login():
    data=load("data.json") or []

    username=input("Insert username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return None

    for user in data:
        if user["username"]==username:

            user.setdefault("failed_attempts",0)
            user.setdefault("blocked",False)
            user.setdefault("block_date",None)

            if user["blocked"]:
                if user["block_date"]:
                    block_time=datetime.strptime(user["block_date"],"%Y-%m-%d %H:%M:%S")

                    if datetime.now()-block_time>=timedelta(days=3):
                        user["blocked"]=False
                        user["failed_attempts"]=0
                        user["block_date"]=None
                        save("data.json", data)
                    else:
                        print("Account is blocked. Try again later.")
                        return None
            
            password=input("Insert password: ").strip()

            if check_password(password,user["password"],user["salt"]):
                print("Login successful.")
                print(f"Last login: {user['login_last']}")
                user["login_last"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user["failed_attempts"]=0
                save("data.json",data)
                user_menu(username)
                return username
            else:
                user["failed_attempts"]+=1
                if user["failed_attempts"]>=3:
                    user["blocked"]=True
                    user["block_date"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print("Too many failed attempts. Account has been blocked.")
                else:
                    print(f"Invalid password. Attempts left: {3-user['failed_attempts']}")
                save("data.json",data)
                return None

    print("Username was not found.")
    return None

#When user is logged ...
def user_menu(username):
    print("Select an activity: ")
    while True:
        print()
        print("1 - Withdraw")
        print("2 - Deposit")
        print("3 - Show balance")
        print("4 - Show transactions history")
        print("5 - Change password")
        print("6 - Log out")
        print()

        choice=str(input("Choose option: "))

        if choice=="1":
            withdraw(username)
        elif choice=="2":
            deposit(username)
        elif choice=="3":
            balance(username)
        elif choice=="4":
            show_history(username)
        elif choice=="5":
            change_password(username)
        elif choice=="6":
            break
        else:
            print("Select valid option.")

#Withdraw
def withdraw(username):
    data=load("data.json") or []

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

                save("data.json",data)

                print(f"Money withdrawn. Current balance: {user['money']}")
                return
            else:
                print("Not enough money.")
                return

#deposit
def deposit(username):
    data=load("data.json") or []

    while True:
        try:
            money_to_deposit=float(input("Insert a money to deposit: "))
            if money_to_deposit<=0:
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

            save("data.json",data)

            print(f"Money deposited. Current balance: {user['money']}")
            return

#change password
def change_password(username):

    data=load("data.json") or []

    print("Rule of changing password")
    print("1. Password must be longer than 8 characters.")
    print("2. New password should contain at least one: small letter, great letter, digit and special character.")
    print("3. Keep your password in safe place.")
    print()

    changed_password=validate_password()

    for user in data:
        if user["username"]==username:
            hashed,salt=hash_password(changed_password)
            user["password"]=hashed
            user["salt"]=salt
            save("data.json",data)
            print("Password changed successfully.")
            return

#show history of transaction
def show_history(username):
    data=load("data.json") or []

    for user in data:
        if user["username"]==username:
            transactions=user.get("transactions",[])

            if not transactions:
                print("Transactions list is empty.")
                return

            else:
                print("DATE | TYPE | AMOUNT")
                print("----------------------")
                for transaction in transactions:
                    date=transaction["date"]
                    type=transaction["type"]
                    amount=transaction["amount"]
                    print(f"{date} | {type} | {amount}")
                return None

#balance
def balance(username):
    data=load("data.json") or []

    for user in data:
        if user["username"]==username:
            print(f"Balance: {user['money']}")

#create new account
def register():
    small_letters=string.ascii_lowercase
    great_letters=string.ascii_uppercase
    digits="1234567890"
    special="!@#$%^&*()-_+=|,./';[]{}:?><"

    data=load("data.json") or []

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
            if any(user["username"]==new_username for user in data):
                print("Username already exists.")
                continue
            break
        except ValueError:
            print("An error occured. Try again!")

    #password
    new_password=validate_password()

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
    hashed,salt=hash_password(new_password)

    account=User(new_username,hashed,new_money,login_last=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),salt=os.urandom(16).hex())

    data.append(account.to_dict())

    save("data.json",data)

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