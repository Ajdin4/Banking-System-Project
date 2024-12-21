using System;
using System.collections.Generic;
using system.Linq;




public class BankAccount
{
    public int AccountNumber { get; set; }
    public string AccountHolderName { get; set; }
    public string AccountPassword { get; set; }
    public string accountType { get; set; }
    public double AccountBalance { get; set; }
    public List<string> Transactions { get; set; } = new List<string>();

    
    
    
    public void AddTransaction(string transaction)
    {
        Transactions.Add(transaction);
    }
}


class MainClass
{
    public static void Main(string[] args)
    {
        while (true) {
            Console.WritelLine("\nWelcome to the Banking System Menu");
            Console.WritelLine("1. Create Account");
            Console.WritelLine("2. Login");
            Console.WritelLine("3. Admin");
            Console.WritelLine("4. Exit");
            Console.WritelLine("Enter your choice: ");
            int choice = int.Parse(Console.ReadLine());
        }
}