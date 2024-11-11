
class AcCreation:
    
    def __init__(self):
        self.setName()
        self.setSurname()
        self.setPhoneNum()
        self.setInitDeposit()
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
        
    #random generated pin function
        
    def getNameAndSurname(self):
        return self.__name +" "+self.__surname
    
    def getPhoneNum(self):
        return self.__phoneNum
    
    def getBalance(self):
        return self.__balance
    
    def AccInformations(self):
        print(f"Name and Surname: {self.getNameAndSurname()}")
        print(f"Phone number: {self.getPhoneNum()}")
        print(f"Balance: {self.getBalance()}")


        
        
    
                
                

    
    