const fs = require("fs");
const readlineSync = require("readline-sync");

class AcCreation {
  static accStorage = "acc.json";

  constructor() {
    try {
      this.name = this.setName();
      this.surname = this.setSurname();
      this.username = this.setUsername();
      this.pin = this.setPin();
      this.phoneNumber = this.setPhoneNumber();
      this.initDeposit = this.setInitDeposit();
      this.Balance = parseInt(this.initDeposit);
      this.transactions = [];
    } catch (error) {
      console.error("Error during account creation:", error.message);
      throw error;
    }
  }

  setName() {
    while (true) {
      try {
        const name = readlineSync.question("Please enter your name: ");
        if (/^[a-zA-Z]+$/.test(name)) return name;
        throw new Error("Invalid name format");
      } catch (error) {
        console.error(error.message);
      }
    }
  }

  setSurname() {
    while (true) {
      try {
        const surname = readlineSync.question("Please enter your surname: ");
        if (/^[a-zA-Z]+$/.test(surname)) return surname;
        throw new Error("Invalid surname format");
      } catch (error) {
        console.error(error.message);
      }
    }
  }

  setUsername() {
    while (true) {
      try {
        const username = readlineSync.question("Please enter your username: ");
        if (this.isUsernameUnique(username) && username.length < 12) return username;
        throw new Error("Username taken or too long");
      } catch (error) {
        console.error(error.message);
      }
    }
  }

  setPin() {
    while (true) {
      try {
        const pin = readlineSync.question("Please enter your pin (at least 4 digits): ");
        if (pin.length >= 4 && /^\d+$/.test(pin)) return pin;
        throw new Error("Invalid PIN format");
      } catch (error) {
        console.error(error.message);
      }
    }
  }

  setPhoneNumber() {
    while (true) {
      try {
        const phoneNumber = readlineSync.question("Please enter your phone number: ");
        if (/^\d{7,}$/.test(phoneNumber)) return phoneNumber;
        throw new Error("Invalid phone number format");
      } catch (error) {
        console.error(error.message);
      }
    }
  }

  setInitDeposit() {
    while (true) {
      try {
        const initDeposit = readlineSync.question("Please enter your initial deposit: ");
        if (/^\d+$/.test(initDeposit)) return parseInt(initDeposit);
        throw new Error("Invalid initial deposit format");
      } catch (error) {
        console.error(error.message);
      }
    }
  }

  toJson() {
    try {
      return {
        Name: this.name,
        Surname: this.surname,
        Username: this.username,
        Pin: this.pin,
        PhoneNumber: this.phoneNumber,
        Balance: this.Balance,
        Transactions: this.transactions,
      };
    } catch (error) {
      console.error("Error creating JSON representation:", error.message);
      throw error;
    }
  }

  saveToJson() {
    try {
      let accounts = [];
      
      
      if (fs.existsSync(AcCreation.accStorage)) {
        const fileContent = fs.readFileSync(AcCreation.accStorage, "utf8");
        if (fileContent.trim() !== "") {
          try {
            accounts = JSON.parse(fileContent);
          } catch (parseError) {
            console.error("Error parsing JSON:", parseError.message);
            accounts = [];  
          }
        }
      }

      accounts.push(this.toJson());
      fs.writeFileSync(AcCreation.accStorage, JSON.stringify(accounts, null, 4));
    } catch (error) {
      console.error("Error saving account to JSON file:", error.message);
      throw error;
    }
  }

  isUsernameUnique(username) {
    try {
      if (fs.existsSync(AcCreation.accStorage)) {
        const fileContent = fs.readFileSync(AcCreation.accStorage, "utf8");
        if (fileContent.trim() === "") return true;
        const accounts = JSON.parse(fileContent);
        return !accounts.some((acc) => acc.Username === username);
      }
      return true;
    } catch (error) {
      console.error("Error checking username uniqueness:", error.message);
      return true;
    }
  }

  addTransaction(transactionType, amount) {
    try {
      const transaction = {
        type: transactionType,
        amount,
        time: new Date().toISOString(),
      };
      this.transactions.push(transaction);
    } catch (error) {
      console.error("Error adding transaction:", error.message);
      throw error;
    }
  }
}

module.exports = AcCreation;