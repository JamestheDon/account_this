#!/usr/bin/env python3
# Fix Accounting.
# Simple single entry cash accounting.
import os
# import numpy.crypto
import pandas as pd

#print('Pandas version:', pd.__version__)
# Init sequence
# database path
dbpath = r'./data'
# list database items
accounts = os.listdir(dbpath)

if accounts != []:
    account = input('Account name? -->')
    
## This tyipically will only run once, upon first use.                   
if accounts == []: 
    # Create first account.
    account = input('Account name? -->')
    #  set column values  with pandas.
    df = pd.DataFrame(columns=['Date', 'Amount', 'Description'])
    # write columns to csv.
    df.to_csv(f'data/{account}_single_entry.csv', index=False)
    # list database items
    accounts = os.listdir(dbpath)
""""
Commenting out blocks.
"""""
def all_account_names():
    lc = 0 
    all = []
    #entries = {'name': '', 'path': ''} # create dic for each accout?
    for i in accounts:
        if i == 0:
            print('ooops!', i)
        lc += 1
        # items in list
        acc_name = i.split('_')
        all.append(acc_name[0])
    print('finally: got all -->', lc, all)
    return all

all = all_account_names()

# @TODO new account?
def gen_acc(account):
    lc = 0
    for i in all:
        if i == account:
            print('Match', i)
            return f'data/{i}_single_entry.csv'
        if i != account:
            lc += 1
            if i == account:
                print('found:', account)
                gen_acc(account)
            if len(all) == lc:
                print('NO MATCH.\nCreating csv now...')
                #  set column values  with pandas.
                df = pd.DataFrame(columns=['Date', 'Amount', 'Description'])
                # write columns to csv.
                df.to_csv(f'data/{account}_single_entry.csv', index=False)
                return f'data/{account}_single_entry.csv'
"""""
# create new account
# database account file path 
def create_new(acc_name):
    print('No Match...\nCreating file now:')
    #  set column values  with pandas.
    df = pd.DataFrame(columns=['Date', 'Amount', 'Description'])
    # write columns to csv.
    df.to_csv(f'data/{account}_single_entry.csv', index=False)
    return f'data/{account}_single_entry.csv'
#                 
"""
file = gen_acc(account)
print('Selected Account --->', file)
# Read csv into state
db = pd.read_csv(file) 
print('Database ready', db.shape)
## ================================= ##
# Check that the csv file exists.
pathExists = os.path.exists(file)
if pathExists == True:
    print('CSV Ready:', pathExists)
    db = pd.read_csv(file)
    pass
else:
    # account name:
    account = input('Account name? -->')
# If file doesnt exist we must make one.
#  set column values  with pandas.
    df = pd.DataFrame(columns=['Date', 'Amount', 'Description'])
    # write columns to csv.
    df.to_csv(f'data/{account}_single_entry.csv', index=False)
    # Read csv into state
    db = pd.read_csv(file) 
    print('Database ready')

#####

#####

# continue prg
print('**Columns**\n', db['Date'], db['Amount'], db['Description']) 
# Check csv file entires.
# shape at index [0] checks for rows.
if db.shape[0] == 0:
    print('ZeroSHape?',db.shape )
if db.shape[0] > 0:
    print('Entires ready:', db)

# user input questions.
def qs(): 
    # TODO add format hints.  
    # %m/%d/%y
    date_ = input('Date? --> ') 
    amount_ = input('Amount? --> ')
    desc_ = input('Description? --> ')
    # TODO input formatting.
    # set answers data to tx2
    tx = [date_] + [amount_] + [desc_]
    return tx

## most important code:
def findLoc():
    # TODO Find locations for saving: save by date.
    return

def editLoc():
    # TODO Find entires for editing.
    return

print('Database rows:', db.shape[0])
# sort index by date.
index = db.shape[0] 
db.loc[index] = qs()

print('\n \n',db)
db.to_csv(file, index=False)
# Save to csv