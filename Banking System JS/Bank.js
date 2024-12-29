
const readlineSync = require("readline-sync");
const fs = require("fs");
const AcCreation = require("./AcCreation");

function loadAccounts() {
  try {
    return fs.existsSync(AcCreation.accStorage)
      ? JSON.parse(fs.readFileSync(AcCreation.accStorage, "utf8"))
      : [];
  } catch (error) {
    console.error("Error loading accounts:", error.message);
    return [];
  }
}

function findAccount(username, pin, accounts) {
  try {
    return accounts.find((acc) => acc.Username === username && acc.Pin === pin);
  } catch (error) {
    console.error("Error finding account:", error.message);
    return null;
  }
}

function saveAccounts(accounts) {
  try {
    fs.writeFileSync(AcCreation.accStorage, JSON.stringify(accounts, null, 4));
  } catch (error) {
    console.error("Error saving accounts:", error.message);
    throw error;
  }
}

function accountMenu(account, allAccounts) {
  let isRunning = true;
  while (isRunning) {
    try {
      console.log("Account Menu");
      console.log("1. View account details.");
      console.log("2. Transaction history.");
      console.log("3. Deposit money.");
      console.log("4. Withdraw money.");
      console.log("5. Transfer money.");
      console.log("6. Log out.");

      const choice = parseInt(readlineSync.question("Please enter a valid choice: "));
      if (choice === 1) {
        console.log(`Name and Surname: ${account.Name} ${account.Surname}`);
        console.log(`Phone Number: ${account.PhoneNumber}`);
        console.log(`Username: ${account.Username}`);
        console.log(`Balance: ${account.Balance}`);
      } else if (choice === 2) {
        console.log("Transaction history:");
        if (account.Transactions.length) {
          account.Transactions.forEach((tr) => {
            console.log(`${tr.time}: ${tr.type}: ${tr.amount}`);
          });
        } else {
          console.log("No transaction history.");
        }
      } else if (choice === 3) {
        const depAmount = parseFloat(readlineSync.question("Enter amount to deposit: "));
        account.Balance += depAmount;
        account.Transactions.push({
          type: "Deposit",
          amount: depAmount,
          time: new Date().toISOString(),
        });
        saveAccounts(allAccounts);
      } else if (choice === 4) {
        try {
          const witAmount = parseFloat(readlineSync.question("Enter amount to withdraw: "));
          if (witAmount > 0 && witAmount <= account.Balance) {
            account.Balance -= witAmount;
            account.Transactions.push({
              type: "Withdraw",
              amount: witAmount,
              time: new Date().toISOString(),
            });
            saveAccounts(allAccounts);
            console.log(`Successfully withdrew ${witAmount}. New balance: ${account.Balance}`);
          } else if (witAmount > account.Balance) {
            console.log("Insufficient funds to withdraw.");
          } else {
            console.log("The amount must be greater than zero.");
          }
        } catch (error) {
          console.error("Invalid input. Please enter a numeric value.");
        }
      } else if (choice === 5) {
        try {
          const recipient = readlineSync.question("Enter the recipient's username: ");
          const recipientAcc = allAccounts.find((acc) => acc.Username === recipient);

          if (!recipientAcc) {
            console.log("No account found.");
            continue;
          }

          if (recipientAcc.Username === account.Username) {
            console.log("You cannot transfer money to your own account.");
            continue;
          }

          const amount = parseFloat(readlineSync.question(`Enter the amount to transfer to ${recipient}: `));
          if (amount <= 0) {
            console.log("Transfer amount must be greater than zero.");
          } else if (amount > account.Balance) {
            console.log("Insufficient funds for the transfer.");
          } else {
            account.Balance -= amount;
            account.Transactions.push({
              type: "Transfer Out",
              amount: amount,
              time: new Date().toISOString(),
              to: recipientAcc.Username,
            });

            recipientAcc.Balance += amount;
            recipientAcc.Transactions.push({
              type: "Transfer In",
              amount: amount,
              time: new Date().toISOString(),
              from: account.Username,
            });

            saveAccounts(allAccounts);
            console.log(`Successfully transferred ${amount} to ${recipientAcc.Username}`);
          }
        } catch (error) {
          console.error(`Error: ${error.message}`);
        }
      } else if (choice === 6) {
        console.log("Logging out!");
        isRunning = false;
      } else {
        console.log("Please enter a valid choice!");
      }
    } catch (error) {
      console.error("Error in account menu:", error.message);
    }
  }
}

function main() {
  let switcher = true;
  while (switcher) {
    try {
      console.log("Welcome to the bank!");
      console.log("1. Create an account.");
      console.log("2. Login.");
      console.log("3. Exit.");

      const choice = readlineSync.question("Enter your choice: ");
      if (choice === "1") {
        const newAccount = new AcCreation();
        newAccount.saveToJson();
        console.log("Account created successfully!");
      } else if (choice === "2") {
        const accounts = loadAccounts();
        const username = readlineSync.question("Enter username: ");
        const pin = readlineSync.question("Enter pin: ");

        const account = findAccount(username, pin, accounts);

        if (account) {
          console.log(`Welcome, ${account.Name} ${account.Surname}`);
          accountMenu(account, accounts);
        } else {
          console.log("Invalid username or pin.");
        }
      } else if (choice === "3") {
        console.log("Exiting...");
        switcher = false;
      } else {
        console.log("Please enter a valid choice.");
      }
    } catch (error) {
      console.error("Error in main menu:", error.message);
    }
  }
}

main();
