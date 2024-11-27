import pymysql
import random
import smtplib
from email.message import EmailMessage
import datetime
import ssl


def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",  # Your MySQL username
        password="Akash@12345",  # Your MySQL password
        database="banking"
    )


def register_customer(name, email, phone_number, address):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO customers (name, email, phone_number, address) VALUES (%s, %s, %s, %s)", 
                   (name, email, phone_number, address))
    db.commit()
    db.close()
    print("Customer registration successful!")


def create_account(customer_id, password, pin, balance=0.00):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO accounts (customer_id, password, pin, balance) VALUES (%s, %s, %s, %s)", 
                   (customer_id, password, pin, balance))
    db.commit()
    db.close()
    print("Account created successfully!")


def login_customer(email, password):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT customers.id, accounts.id FROM customers INNER JOIN accounts ON customers.id = accounts.customer_id WHERE customers.email = %s AND accounts.password = %s", 
                   (email, password))
    user = cursor.fetchone()
    db.close()
    return user


def deposit(account_id, amount):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, account_id))
    cursor.execute("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'Deposit', %s)", 
                   (account_id, amount))
    db.commit()
    db.close()
    print(f"Deposited Rs. {amount}.")


def withdraw(account_id, amount):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    balance = cursor.fetchone()[0]
    if balance >= amount:
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, account_id))
        cursor.execute("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'Withdraw', %s)", 
                       (account_id, amount))
        db.commit()
        db.close()
        print(f"Withdrew Rs. {amount}.")
    else:
        db.close()
        print("Insufficient balance!")


def view_transactions(account_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT transaction_type, amount, timestamp FROM transactions WHERE account_id = %s", (account_id,))
    transactions = cursor.fetchall()
    db.close()
    if transactions:
        for txn in transactions:
            print(f"Transaction: {txn[0]}, Amount: Rs. {txn[1]}, Date: {txn[2]}")
    else:
        print("No transactions found.")


def view_balance(account_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    balance = cursor.fetchone()[0]
    db.close()
    print(f"Your balance is: Rs. {balance}")


def main_menu(account_id):
    while True:
        print("\nBank Menu:")
        print("1. View Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transaction History")
        print("5. Logout")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            view_balance(account_id)
        elif choice == '2':
            amount = float(input("Enter amount to deposit: "))
            deposit(account_id, amount)
        elif choice == '3':
            amount = float(input("Enter amount to withdraw: "))
            withdraw(account_id, amount)
        elif choice == '4':
            view_transactions(account_id)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")


def login():
    email = input("Enter email: ")
    password = input("Enter password: ")
    user = login_customer(email, password)
    if user:
        account_id = user[1]
        print(f"Welcome!")
        main_menu(account_id)
    else:
        print("Invalid credentials.")


def register():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone_number = input("Enter your phone number: ")
    address = input("Enter your address: ")
    register_customer(name, email, phone_number, address)
    
    password = input("Enter password for your account: ")
    pin = input("Enter 6-digit PIN for your account: ")
    
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM customers WHERE email = %s", (email,))
    customer_id = cursor.fetchone()[0]
    create_account(customer_id, password, pin)
    db.close()


if __name__ == "__main__":
    print("Welcome to the Online Bank System!")
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            login()
        elif choice == '2':
            register()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

