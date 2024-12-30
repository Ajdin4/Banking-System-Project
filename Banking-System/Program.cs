using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;

public class Program
{
    static List<Account> accounts = new List<Account>();

    public static void Main(string[] args)
    {
        LoadAccountsFromFile();

        while (true)
        {
            Console.WriteLine("Welcome to the Banking System Application");
            Console.WriteLine("1. Create a new account");
            Console.WriteLine("2. Login");
            Console.WriteLine("3. Admin Panel");
            Console.WriteLine("4. Exit");
            Console.Write("Please select an option: ");

            string input = Console.ReadLine();
            if (int.TryParse(input, out int option))
            {
                switch (option)
                {
                    case 1:
                        CreateAccount();

                    case 2:
                        Login();
                        break;
                    case 3:
                        Admin();
                        break;
                    case 4:
                        Console.WriteLine("Thank you for using the Banking System Application.");
                        SaveAccountsToFile();
                        return;
                    default:
                        Console.WriteLine("Invalid option selected. Please try again.");
                        break;
                }
            }
            else
            {
                Console.WriteLine("Invalid input. Please enter a valid number.");
            }
        }
    }

    public static void CreateAccount()
    {
        Console.Clear();
        Console.WriteLine("Enter your name:");
        string? name = Console.ReadLine() ?? string.Empty;

        Console.WriteLine("Enter your password:");
        string? password = Console.ReadLine() ?? string.Empty;

        Console.WriteLine("Enter which account type you want to open (savings/current):");
        string? type = Console.ReadLine()?.ToLower() ?? string.Empty;

        if (type != "savings" && type != "current")
        {
            Console.WriteLine("Invalid account type. Please enter either 'savings' or 'current'.");
            return;
        }

        Console.WriteLine("Enter your initial deposit amount:");
        if (!double.TryParse(Console.ReadLine(), out double balance))
        {
            Console.WriteLine("Invalid input. Please enter a valid number.");
            return;
        }

        var account = new Account
        {
            AccountNumber = accounts.Count + 1,
            Name = name,
            Password = password,
            Type = type,
            Balance = balance,
        };

        accounts.Add(account);
        SaveAccountsToFile();
        Console.WriteLine($"Account created successfully. Your account number is: {account.AccountNumber}");
    }

    public static void Login()
    {
        Console.Clear();
        Console.WriteLine("Enter your account number:");
        string? inputAccountNumber = Console.ReadLine();

        if (inputAccountNumber == null || !int.TryParse(inputAccountNumber, out int accountNumber))
        {
            Console.WriteLine("Invalid account number. Please try again.");
            return;
        }

        Console.WriteLine("Enter your password:");
        string? password = Console.ReadLine() ?? string.Empty;

        var account = accounts.Find(a => a.AccountNumber == accountNumber && a.Password == password);

        if (account != null)
        {
            Console.WriteLine("Login successful!");
            Dashboard(account);
        }
        else
        {
            Console.WriteLine("Invalid account number or password. Please try again.");
        }
    }

    public static void Admin()
    {
        Console.Clear();
        Console.WriteLine("Enter admin password:");
        string? password = Console.ReadLine();

        if (password != null && password == "admin123")
        {
            while (true)
            {
                Console.WriteLine("\nAdmin Panel");
                Console.WriteLine("1. View All Accounts");
                Console.WriteLine("2. View All Transactions");
                Console.WriteLine("3. Delete an Account");
                Console.WriteLine("4. Exit Admin Panel");
                Console.Write("Please select an option: ");

                string? adminChoiceInput = Console.ReadLine();
                if (int.TryParse(adminChoiceInput, out int choice))
                {
                    switch (choice)
                    {
                        case 1:
                            Console.WriteLine("\nAccount List:");
                            foreach (var account in accounts)
                            {
                                Console.WriteLine($"Account {account.AccountNumber}, {account.Name}, Balance: {account.Balance}");
                            }
                            break;

                        case 2:
                            Console.WriteLine("\nTransactions list:");
                            foreach (var account in accounts)
                            {
                                Console.WriteLine($"Transactions for Account {account.AccountNumber}, {account.Name}:");
                                foreach (var transaction in account.Transactions)
                                {
                                    Console.WriteLine(transaction);
                                }
                            }
                            break;

                        case 3:
                            Console.Write("\nEnter the account number to delete: ");
                            string? accountNumberInput = Console.ReadLine();

                            if (int.TryParse(accountNumberInput, out int accountNumber))
                            {
                                var accountToDelete = accounts.Find(a => a.AccountNumber == accountNumber);
                                if (accountToDelete != null)
                                {
                                    accounts.Remove(accountToDelete);
                                    SaveAccountsToFile();
                                    Console.WriteLine($"Account {accountNumber} removed successfully!");
                                }
                                else
                                {
                                    Console.WriteLine("Account not found.");
                                }
                            }
                            else
                            {
                                Console.WriteLine("Invalid account number.");
                            }
                            break;

                        case 4:
                            return;

                        default:
                            Console.WriteLine("Invalid choice. Please try again.");
                            break;
                    }
                }
                else
                {
                    Console.WriteLine("Invalid input. Please enter a valid number.");
                }
            }
        }
        else
        {
            Console.WriteLine("Invalid admin password.");
        }
    }

    static void Dashboard(Account account)
    {
        
        while (true)
        {
            
            Console.WriteLine("\nAccount Dashboard");
            Console.WriteLine("1. Deposit Funds");
            Console.WriteLine("2. Withdraw Funds");
            Console.WriteLine("3. Make Transaction");
            Console.WriteLine("4. Check Account Balance");
            Console.WriteLine("5. View Transaction History");
            Console.WriteLine("6. Sign Out");
            Console.Write("Please choose an option: ");

            string? input = Console.ReadLine();

            if (!int.TryParse(input, out int choice))
            {
                Console.WriteLine("Invalid input. Please try again.");
                continue;
            }

            switch (choice)
            {
                case 1:
                    Deposit(account);
                    break;
                case 2:
                    Withdraw(account);
                    break;
                case 3:
                    Transaction(account);
                    break;
                case 4:
                    Console.WriteLine($"Current Balance: {account.Balance}");
                    break;
                case 5:
                    ViewTransactionHistory(account);
                    break;
                case 6:
                    Console.WriteLine("Signing out...");
                    return;
                default:
                    Console.WriteLine("Invalid choice. Please try again.");
                    break;
            }
        }
    }

    static void Deposit(Account account)
    {
        Console.Write("Enter deposit amount: ");
        string? input = Console.ReadLine();

        if (input != null && double.TryParse(input, out double amount) && amount > 0)
        {
            account.Balance += amount;
            account.AddTransaction($"[{DateTime.Now}] Deposited {amount}");
            SaveAccountsToFile();
            Console.WriteLine("Deposit successful!");
        }
        else
        {
            Console.WriteLine("Invalid amount. Deposit failed.");
        }
    }

    static void Withdraw(Account account)
    {
        Console.Write("Enter withdrawal amount: ");
        string? input = Console.ReadLine();

        if (input != null && double.TryParse(input, out double amount) && amount > 0)
        {
            if (amount > account.Balance)
            {
                Console.WriteLine("Insufficient balance.");
            }
            else
            {
                account.Balance -= amount;
                account.AddTransaction($"[{DateTime.Now}] Withdrew {amount}");
                SaveAccountsToFile();
                Console.WriteLine("Withdrawal successful!");
            }
        }
        else
        {
            Console.WriteLine("Invalid amount. Withdrawal failed.");
        }
    }

    static void Transaction(Account sender)
    {
        Console.Write("Enter recipient account number: ");
        string? input = Console.ReadLine();

        if (input == null || !int.TryParse(input, out int recipientAccountNumber))
        {
            Console.WriteLine("Invalid account number.");
            return;
        }

        var recipient = accounts.Find(a => a.AccountNumber == recipientAccountNumber);
        if (recipient == null)
        {
            Console.WriteLine("Recipient account not found.");
            return;
        }

        Console.Write("Enter amount to transfer: ");
        string? amountInput = Console.ReadLine();

        if (amountInput != null && double.TryParse(amountInput, out double amount) && amount > 0)
        {
            if (amount > sender.Balance)
            {
                Console.WriteLine("Insufficient balance.");
            }
            else
            {
                sender.Balance -= amount;
                recipient.Balance += amount;

                string time = DateTime.Now.ToString();
                sender.AddTransaction($"[{time}] Sent {amount} to account {recipient.AccountNumber}");
                recipient.AddTransaction($"[{time}] Received {amount} from account {sender.AccountNumber}");

                SaveAccountsToFile();
                Console.WriteLine("Transaction successful!");
            }
        }
        else
        {
            Console.WriteLine("Invalid amount. Transaction failed.");
        }
    }

    static void ViewTransactionHistory(Account account)
    {
        Console.WriteLine("\nTransaction History:");
        if (account.Transactions.Count == 0)
        {
            Console.WriteLine("No transactions found.");
        }
        else
        {
            foreach (var transaction in account.Transactions)
            {
                Console.WriteLine(transaction);
            }
        }
    }

    public static void SaveAccountsToFile()
    {
        try
        {
            File.WriteAllText("accounts.json", JsonConvert.SerializeObject(accounts, Formatting.Indented));
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error saving accounts: {ex.Message}");
        }
    }

    public static void LoadAccountsFromFile()
    {
        try
        {
            if (File.Exists("accounts.json"))
            {
                accounts = JsonConvert.DeserializeObject<List<Account>>(File.ReadAllText("accounts.json")) ?? new List<Account>();
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error loading accounts: {ex.Message}");
        }
    }
}

public class Account
{
    public int AccountNumber { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
    public string Type { get; set; } = string.Empty;
    public double Balance { get; set; }
    public List<string> Transactions { get; set; } = new List<string>();

    public void AddTransaction(string transaction)
    {
        Transactions.Add(transaction);
    }
}
