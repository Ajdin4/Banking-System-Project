from AcCreation import AcCreation
import json
import os
from datetime import datetime

accounts = {}
currency = "BAM"

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

def admin_panel(accounts):
    admin_password = "admin123"
    password = input("Enter admin password: ")
    if password != admin_password:
        print("Incorrect password. Access denied.")
        return
    toggle = True
    while toggle:
        try:
            print("\nAdmin Panel")
            print("1. View all accounts")
            print("2. View all transaction history")
            print("3. Delete an account")
            print("4. Exit Admin Panel")
            
            choice = int(input("Enter a valid choice: "))
            
            if choice == 1:
                print("\nAll accounts: ")
                if accounts:
                    for a in accounts:
                        print(f"Name: {a['Name']} {a['Surname']}\nUsername: {a['Username']}\nBalance: {a['Balance']} {currency}")
                else:
                    print("No accounts available.")
            
            elif choice == 2:
                print("\nAll accounts: ")
                if accounts:
                    for a in accounts:
                        print(f"\nTransactions for {a['Username']}: ")
                        if a['Transactions']:
                            for tr in a['Transactions']:
                                    if tr.get("to") or tr.get("from"):
                                        print(f"{tr['timestamp']}: {tr['type']} of {tr['amount']} {currency} (To: {tr.get('to', 'N/A')} From: {tr.get('from', 'N/A')})")
                                    else:
                                        print(f"{tr['timestamp']}: {tr['type']} of {tr['amount']} {currency}")
                        else:
                            print("No transactions yet.")
                else:
                    print("No accounts available.")
            elif choice == 3:
                username = input("Enter the username of the account to delete")
                account_to_delete = next((acc for acc in accounts if acc["Username"] == username), None)
                
                if account_to_delete:
                    confirm = input("Are you sure you want to delete this account?(yes for confirmation, anything else for cancellation)")
                    if confirm.lower() == "yes":
                        accounts.remove(account_to_delete)
                        save_acc(accounts)
                        print("Account successfully deleted!")
                    else:
                        print("Account deletion cancelled")
                else:
                    print("Account not found.")
            elif choice == 4:
                print("Exiting admin panel...")
                toggle = False
                
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
           
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            
    

def account_menu(account_data, all_accounts):
    hold = True
    while hold:
        try:
            print("\nAccount Menu")
            print("1. View account details")
            print("2. Transaction history")
            print("3. Deposit money")
            print("4. Withdraw money")
            print("5. Transfer money")
            print("6. Log out")
            
            choice = int(input("enter a valid choice: "))
            
            if choice == 1:
                print("\nAccount Details:")
                print(f"Name and Surname: {account_data['Name']} {account_data['Surname']}")
                print(f"Phone Number: {account_data['Phone number']}")
                print(f"Balance: {account_data['Balance']} {currency}")
                print(f"Username: {account_data['Username']}")
                print(f"Pin: {account_data['Pin']}")
            
            elif choice == 2:
                print("\nTransaction history:")
                if account_data["Transactions"]:
                    for tr in account_data["Transactions"]:
                        print(f"{tr['timestamp']}: {tr['type']} of {tr['amount']} {currency}")
                else:
                    print("no transactions yet.")
            elif choice == 3:
                try:
                    amount  = int(input("Enter the amount to deposit in BAM: "))
                    if amount>0:
                        account_data["Balance"]+=amount
                        account_data["Transactions"].append({
                            "type": "Deposit",
                            "amount": amount,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        save_acc(all_accounts)
                        print(f"Successfully deposited {amount} {currency}. New balance: {account_data['Balance']} {currency}")
                    else:
                        print("Deposit amount must be grater than 0.")
                except ValueError:
                    print("Invalid input. Please enter a numeric value")
                
            elif choice == 4:
                try:
                    amount  = int(input("Enter the amount to withdraw in BAM: "))
                    if amount>0 and amount <= account_data['Balance']:
                        account_data["Balance"]-=amount
                        account_data["Transactions"].append({
                            "type": "withdrawal",
                            "amount": amount,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                            
                        save_acc(all_accounts)
                        print(f"Successfully withdrew {amount}. New balance: {account_data['Balance']} {currency}")
                    elif amount>account_data['Balance']:
                        print("insufficient funds to withdraw")                   
                    else:
                        print("the amount must be greater than zero")
                except ValueError:
                    print("Invalid input. Please enter a numeric value")
            elif choice == 5:
                try:
                    recipient = input("Enter the recipient's username: ")
                    recipient_acc = next((acc for acc in all_accounts if acc["Username"]==recipient),None) 
                    
                    if recipient_acc is None:
                        print("no account found")
                        continue
                    if recipient_acc["Username"] == account_data["Username"]:
                        raise ValueError("You cannot transfer money to your own account")
                    amount = int(input(f"Enter the amount to transfer to {recipient} in BAM "))
                    
                    if amount <=0:
                        raise ValueError("Transfer amount must be greater than zero")
                    if amount > account_data["Balance"]:
                        raise ValueError("Insufficient funds for the transfer. ")
                    
                    account_data["Balance"]-=amount
                    account_data["Transactions"].append({
                        "type":"Transfer Out",
                        "amount":amount,
                        "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "to":recipient_acc["Username"]
                    })
                    
                    recipient_acc["Balance"]+=amount
                    recipient_acc["Transactions"].append({
                        "type":"Transfer In",
                        "amount":amount,
                        "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "from":account_data["Username"]
                    })
                    print(f"sucessfully transferred {amount} {currency} to {recipient_acc["Username"]} ")
                    save_acc(all_accounts)
                      
                except ValueError as e:
                    print(f"Error: {e}")    
                    
            elif choice == 6:
                print("logging out...")
                print("heading back to the main menu")
                hold = False
            else:
                print("invalid choice. try again!")
        except ValueError:
            print("Invalid input. please enter a numeric value.")
            
def main():
    toggle = True
    while toggle:
        try:
            print("\n\nwelcome to The Bank of Ilidza\n\n")
            print("1. create an account")
            # when 1 pressed entered account creation and then operations over the made acc
            print("2. log in into an existing account")
            # when 2 is pressed user is prompted for a username and password
            print("3. Admin panel")
            print("4. exit the bank")
            # quits the program
            choice = int(input("enter a valid choice: "))
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
                accounts =load_acc()
                admin_panel(accounts)
                
            elif choice == 4:
                print("\nThank you for using the Bank of Ilidza\n")
                toggle = False
            else:
                print("Please only enter a number 1,2 or 3!")
        except ValueError:
            print("Invalid input. Please enter a numeric value")
if __name__ == "__main__":
    main()
    
        
