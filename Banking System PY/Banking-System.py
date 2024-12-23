from AcCreation import AcCreation
import json
import os
from datetime import datetime

accounts = {}

def save_acc(accounts):
    with open(AcCreation.acc_storage,"w") as fl:
        json.dump(accounts,fl,indent=4)

def load_acc():
    if os.path.exists(AcCreation.acc_storage):
        with open(AcCreation.acc_storage,"r") as fl:
            try:
                return json.load(fl)
            except json.JSONDecodeError:
                return []
    return []
def find_acc(username,pin,accounts):
    for account in accounts:
        if account["Username"] == username and account["Pin"]==pin:
            return account
    return None

def account_menu(account_data, all_accounts):
    hold = True
    while hold:
        print("\nAccount Menu")
        print("1. View account details")
        print("2. Transaction history")
        print("3. Deposit money")
        print("4. Withdraw money")
        print("5. Log out")
        
        choice = int(input("enter a valid choice: "))
        
        if choice == 1:
            print("\nAccount Details:")
            print(f"Name and Surname: {account_data['Name']} {account_data['Surname']}")
            print(f"Phone Number: {account_data['Phone number']}")
            print(f"Balance: {account_data['Balance']}")
            print(f"Username: {account_data['Username']}")
            print(f"Pin: {account_data['Pin']}")
        
        elif choice == 2:
            print("\nTransaction history:")
            if account_data["Transactions"]:
                for tr in account_data["Transactions"]:
                    print(f"{tr['timestamp']}: {tr['type']} of {tr['amount']}")
            else:
                print("no transactions yet.")
        elif choice == 3:
            amount  = int(input("Enter the amount to deposit: "))
            account_data["Balance"]+=amount
            account_data["Transactions"].append({
                "type": "Deposit",
                "amount": amount,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_acc(all_accounts)
            print(f"Successfully deposited {amount}. New balance: {account_data['Balance']}")
            
        elif choice == 4:
            amount  = int(input("Enter the amount to withdraw: "))
            if amount <= account_data['Balance']:
                account_data["Balance"]-=amount
                account_data["Transactions"].append({
                    "type": "withdrawal",
                    "amount": amount,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                save_acc(all_accounts)
                print(f"Successfully withdrew {amount}. New balance: {account_data['Balance']}")                    

            else:
                print("insufficient funds to withdraw!")
                
        elif choice == 5:
            print("logging out...")
            print("heading back to the main menu")
            hold = False
        else:
            print("invalid choice. try again!")
def main():
    toggle = True
    while toggle:
        print("\n\nwelcome to The Bank of Ilidza\n\n")
        print("1. create an account")
        # when 1 pressed entered account creation and then operations over the made acc
        print("2. log in into an existing account")
        # when 2 is pressed user is prompted for a username and password
        print("3. exit the bank")
        # quits the program
        choice = int(input("enter a valid choice:"))
        if choice == 1:
            print("\nCreating a new account...")
            newAccount = AcCreation()
            newAccount.saveToJson()
            accounts = load_acc()
            print("\nAccount successfully created!")
        elif choice == 2:
            accounts = load_acc()
            username = input("Enter your username: ")
            pin = input("enter your pin: ")
            account = find_acc(username,pin,accounts)
            if account:
                account_menu(account,accounts)
            else:
                print("invalid credentials, Please try again.")
        elif choice == 3:
            print("Thank you for using the Bank of Ilidza")
            toggle = False
        else:
            print("Please only enter a number 1,2 or 3!")
            
if __name__ == "__main__":
    main()
    
        
