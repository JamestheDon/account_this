#!/usr/bin/env python3
import os
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint
import questionary
from questionary import Choice
from datetime import date
from cryptography.fernet import Fernet
import bcrypt

DB_PATH = './data'
console = Console()

def get_account_names():
    account_files = [f.split('_single_entry.csv')[0] for f in os.listdir(DB_PATH) if f.endswith('_single_entry.csv')]
    return account_files

def select_account():
    accounts = get_account_names()
    choices = [Choice(acc, acc) for acc in accounts] + [Choice("Create new account", "new")]
    selected = questionary.select("Select an account or create a new one:", choices=choices).ask()
    
    if selected == "new":
        account = Prompt.ask("Enter new account name")
        create_account(account)
    else:
        account = selected
    
    return account

def create_account(account):
    file_path = os.path.join(DB_PATH, f'{account}_single_entry.csv')
    df = pd.DataFrame(columns=['Date', 'Amount', 'Description'])
    df.to_csv(file_path, index=False)
    rprint(f"[green]Account '[cyan]{account}[/cyan]' created.[/green]")

def load_account_data(account):
    file_path = os.path.join(DB_PATH, f'{account}_single_entry.csv')
    try:
        db = pd.read_csv(file_path)
        db['Date'] = pd.to_datetime(db['Date'], errors='coerce')
        # Don't convert to float here, keep as string
        db['Amount'] = db['Amount'].apply(decrypt_data)
        db['Description'] = db['Description'].apply(decrypt_data)
        return db
    except FileNotFoundError:
        rprint(f"[red]Error: The file {file_path} does not exist.[/red]")
        exit()

def save_account_data(account, db):
    file_path = os.path.join(DB_PATH, f'{account}_single_entry.csv')
    # Encrypt data before saving
    db['Amount'] = db['Amount'].astype(str).apply(encrypt_data)
    db['Description'] = db['Description'].apply(encrypt_data)
    db.to_csv(file_path, index=False)

def view_transactions(account, db):
    if db.empty:
        rprint("[yellow]No transactions to display.[/yellow]")
        return

    table = Table(title=f"Transactions for {account}")
    table.add_column("Index", style="cyan")
    table.add_column("Date", style="magenta")
    table.add_column("Amount", style="green")
    table.add_column("Description", style="yellow")

    total_balance = 0.0
    for idx, row in db.iterrows():
        try:
            amount = float(row['Amount'])
        except ValueError:
            amount = float(decrypt_data(row['Amount']))
        
        description = decrypt_data(row['Description'])
        
        total_balance += amount
        table.add_row(str(idx), str(row['Date']), f"${amount:.2f}", description)

    rprint(table)
    
    console.print(Panel(f"Current Balance: [green]${total_balance:.2f}[/green]", title="Account Summary", border_style="blue"))

def create_transaction(account, db):
    date_input = Prompt.ask("Enter date (YYYY-MM-DD)", default=str(date.today()))
    amount = float(Prompt.ask("Enter amount"))
    description = Prompt.ask("Enter description")
    
    new_entry = pd.DataFrame([[date_input, amount, description]], columns=['Date', 'Amount', 'Description'])
    new_entry['Date'] = pd.to_datetime(new_entry['Date'])
    
    db = pd.concat([db, new_entry], ignore_index=True)
    db.sort_values('Date', inplace=True)
    
    save_account_data(account, db)
    rprint("[green]Transaction saved successfully.[/green]")
    return db

def edit_transaction(account, db):
    view_transactions(account, db)
    index = int(Prompt.ask("Enter the index of the transaction to edit"))
    
    if 0 <= index < len(db):
        date_input = Prompt.ask("Enter new date (YYYY-MM-DD)", default=str(db.loc[index, 'Date'].date()))
        amount = float(Prompt.ask("Enter new amount", default=str(db.loc[index, 'Amount'])))
        description = Prompt.ask("Enter new description", default=db.loc[index, 'Description'])
        
        db.loc[index] = [date_input, amount, description]
        db['Date'] = pd.to_datetime(db['Date'])
        db.sort_values('Date', inplace=True)
        
        save_account_data(account, db)
        rprint("[green]Transaction updated successfully.[/green]")
    else:
        rprint("[red]Invalid index. No transaction edited.[/red]")
    
    return db

def delete_transaction(account, db):
    if db.empty:
        rprint("[yellow]No transactions to delete.[/yellow]")
    else:
        view_transactions(account, db)
        to_delete = int(Prompt.ask("Enter the index of the transaction to delete"))
        
        if 0 <= to_delete < len(db):
            db = db.drop(to_delete).reset_index(drop=True)
            save_account_data(account, db)
            rprint("[green]Transaction deleted successfully.[/green]")
        else:
            rprint("[red]Invalid index. No transaction deleted.[/red]")
    
    return db

def display_ascii_art():
    ascii_art ="""
                  ,@@@@@@@,
           ,,,.  /@@@@@@/@@,
        ,&%%&%&&%@@@@/@@@@@@,
       ,%&\%&&%&&%@@@@\@@@/@@@
       %&&%&%&/%&&%@@@\@@/ /@@@
       %&&%/ %&%%&&@@@\ V /@@'
       `&%\ ` /%&'    ) ('
           |o|        /\_
           |.|       /  \
    """
    console.print(ascii_art, style="bold green")

def get_or_create_key():
    key_file = os.path.join(DB_PATH, '.key')
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        return key

def encrypt_data(data):
    return fernet.encrypt(str(data).encode()).decode()

def decrypt_data(data):
    try:
        return fernet.decrypt(data.encode()).decode()
    except:
        # If decryption fails, return the original data
        return data

def create_user():
    username = Prompt.ask("Enter a username")
    password = Prompt.ask("Enter a password", password=True)
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with open(os.path.join(DB_PATH, '.users'), 'a') as f:
        f.write(f"{username}:{hashed.decode()}\n")
    return username

def authenticate():
    if not os.path.exists(os.path.join(DB_PATH, '.users')):
        return create_user()
    
    username = Prompt.ask("Username")
    password = Prompt.ask("Password", password=True)
    
    with open(os.path.join(DB_PATH, '.users'), 'r') as f:
        for line in f:
            stored_username, stored_hash = line.strip().split(':')
            if username == stored_username and bcrypt.checkpw(password.encode(), stored_hash.encode()):
                return username
    
    rprint("[red]Authentication failed.[/red]")
    return None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    
    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)

    global fernet
    key = get_or_create_key()
    fernet = Fernet(key)

    display_ascii_art()

    if not authenticate():
        return

    while True:
        clear_screen()
        account = select_account()
        db = load_account_data(account)
        
        # Display transactions initially
        view_transactions(account, db)

        while True:
            action = questionary.select(
                "What would you like to do?",
                choices=[
                    Choice("View transactions", "view"),
                    Choice("Create new transaction", "new"),
                    Choice("Edit existing transaction", "edit"),
                    Choice("Delete transaction", "delete"),
                    Choice("Go back to main accounts page", "back"),
                    Choice("Exit", "exit")
                ]
            ).ask()

            if action == "back":
                break
            elif action == "exit":
                return

            if action == "view":
                view_transactions(account, db)
            elif action == "new":
                db = create_transaction(account, db)
                view_transactions(account, db)
            elif action == "edit":
                db = edit_transaction(account, db)
                view_transactions(account, db)
            elif action == "delete":
                db = delete_transaction(account, db)
                view_transactions(account, db)

if __name__ == "__main__":
    main()