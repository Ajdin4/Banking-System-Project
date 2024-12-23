import json
import os
import hashlib
from datetime import datetime
class AcCreation:
    acc_storage = "acc.json"
    
    def __init__(self):
        self.setName()
        self.setSurname()
        self.setUsername()
        self.setPin()
        self.setPhoneNum()
        self.setInitDeposit()
        self.__transactions = []
        
        
    def setName(self):
        hold = True
        while(hold):
            name = input("please enter a valid name: ")
            if name.isalpha():
                hold = False
        self.__name = name
        
    def setSurname(self):
        hold = True
        while(hold):
            surname = input("please enter a valid surname: ")
            if surname.isalpha():
                hold = False
        self.__surname = surname
        
    def setUsername(self):
        hold = True 
        while hold:
            username = input("enter your desired username: ")
            if self.isUsernameUnique(username):
                choice = input("are you sure you want to proceed with this username? (enter 'yes' or 'no') ")
                if choice.lower() =="yes":
                    self.__username = username
                    hold = False
            else:
                print("username taken, choose another one")

    def setPin(self):
        hold = True
        while hold:
            pin = input("enter your desired pin, atleast 4 digits: ")
            if pin.isdigit() and len(pin)>=4:
                self.__pin = pin
                hold = False
                         
    def setPhoneNum(self):
        hold = True
        while(hold):
            phoneNum = input("Please enter a valid phone number: ")
            if phoneNum.startswith('0') and phoneNum.isdigit() and '-' not in phoneNum:
                hold = False
            elif phoneNum.isdigit() and '-' not in phoneNum:
                hold = False
                
        self.__phoneNum = phoneNum
        
    def setInitDeposit(self):
        self.__balance = 0
        hold = True
        while(hold):
            balance = input("Please enter your initial deposit if there is any: ")
            if balance.isdigit() and '-' not in balance:
                hold = False
        self.__balance = int(balance)
    
    def addTransaction(self,transaction_type,amount):
        transaction={
            "type": transaction_type,
            "amount": amount,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.__transactions.append(transaction)
        
        
    def getNameAndSurname(self):
        return self.__name +" "+self.__surname
    
    def getPhoneNum(self):
        return self.__phoneNum
    
    def getBalance(self):
        return self.__balance
    
    def getUsername(self):
        return self.__username
    
    def getPin(self):
        return self.__pin
    '''
    def AccInformations(self):
        hold = True
        while hold:
            if self.verifyPin():
                print(f"Name and Surname: {self.getNameAndSurname()}")
                print(f"Phone number: {self.getPhoneNum()}")
                print(f"Balance: {self.getBalance()}")
                print(f"Username: {self.getUsername()}")
                print(f"pin: {self.getPin()}")
                hold = False
            else:
                print("Failed to verify PIN")
    '''
    def isUsernameUnique(self, username):
        if os.path.exists(self.acc_storage):
            with open(self.acc_storage, "r") as fl:
                try:
                    accounts = json.load(fl)
                    return all(acc["Username"] != username for acc in accounts)
                except json.JSONDecodeError:
                    return True
        return True
    '''
    def verifyPin(self):
        for i in range(3): #3 attempts
            check = input("Enter your PIN: ")
            if check == self.getPin():
                return True
            print("incorrect PIN. Try again.")
        print("Too many incorrect attempts. Exiting.")
        return False
    '''
        
    def getDict(self):
        #convert the object to a python to a dictionary suitable for JSON storage
        return {
            "Name": self.__name,
            "Surname": self.__surname,
            "Phone number": self.__phoneNum,
            "Balance": self.__balance,
            "Username": self.__username,
            "Pin": self.__pin,
            "Transactions": self.__transactions    
            }
        
    def saveToJson(self):
        try:
            if os.path.exists(self.acc_storage):
                with open(self.acc_storage, "r") as fl:
                    try:
                        accounts = json.load(fl)
                    except json.JSONDecodeError:
                        accounts = []
            else:
                accounts = []
                
            accounts.append(self.getDict())
            
            with open(self.acc_storage,"w") as fl:
                json.dump(accounts,fl,indent = 3)
        except Exception as e:
            print(f"error occured: {e}")
        


        
        
    
                
                

    
    