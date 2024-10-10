#!/usr/bin/env python3
# Simple single-entry cash accounting script.

import os
import pandas as pd

DB_PATH = './data'

# Ensure the data directory exists
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

# Function to get account names from existing CSV files
def get_account_names():
    account_files = os.listdir(DB_PATH)
    accounts = []
    for filename in account_files:
        if filename.endswith('_single_entry.csv'):
            account_name = filename.split('_single_entry.csv')[0]
            accounts.append(account_name)
    return accounts

accounts = get_account_names()

# Prompt user for account name
if not accounts:
    account = input('No accounts found. Please create a new account name: ')
else:
    account = input(f"Available accounts: {', '.join(accounts)}\nSelect account name or enter a new one: ")

file_path = os.path.join(DB_PATH, f'{account}_single_entry.csv')

# Check if the account exists; if not, offer to create it
if account not in accounts:
    create_new = input(f"Account '{account}' does not exist. Would you like to create it? (y/n): ").lower()
    if create_new == 'y':
        # Create new account with empty DataFrame
        df = pd.DataFrame(columns=['Date', 'Amount', 'Description'])
        df.to_csv(file_path, index=False)
        print(f"Account '{account}' created.")
    else:
        print('Exiting program.')
        exit()

# Read the account CSV file
try:
    db = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: The file {file_path} does not exist.")
    exit()

# Display existing entries
if db.empty:
    print('No entries in the account.')
else:
    print('Existing entries:')
    print(db)

# Function to get new transaction input with validation
def get_transaction_input():
    while True:
        date_ = input('Date (YYYY-MM-DD): ')
        try:
            pd.to_datetime(date_)
            break
        except ValueError:
            print('Invalid date format. Please enter in YYYY-MM-DD format.')
    while True:
        amount_ = input('Amount: ')
        try:
            amount_ = float(amount_)
            break
        except ValueError:
            print('Invalid amount. Please enter a numeric value.')
    desc_ = input('Description: ')
    return {'Date': date_, 'Amount': amount_, 'Description': desc_}

# Get new transaction and append to DataFrame
transaction = get_transaction_input()
new_entry = pd.DataFrame([transaction], columns=['Date', 'Amount', 'Description'])
new_entry['Date'] = pd.to_datetime(new_entry['Date'])
new_entry['Amount'] = pd.to_numeric(new_entry['Amount'])
new_entry['Description'] = new_entry['Description'].astype(str)

# Ensure db has the same dtypes as new_entry
db['Date'] = pd.to_datetime(db['Date'])
db['Amount'] = pd.to_numeric(db['Amount'])
db['Description'] = db['Description'].astype(str)

# Concatenate the DataFrames
db = pd.concat([db, new_entry], ignore_index=True)

# Convert 'Date' column to datetime and sort
db.sort_values('Date', inplace=True)

# Save the DataFrame back to CSV
db.to_csv(file_path, index=False)
print('Transaction saved successfully.')
