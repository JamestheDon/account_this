#!/usr/bin/env python3
# Fix Accounting.
# Simple single entry cash accounting.
import os.path as path
import pandas as pd
# Init sequence
print('Pandas version:', pd.__version__)
# database path
file = r'data/single_entry.csv'
# Check that the csv file exists.
pathExists = path.exists(file)
if pathExists == True:
    print('CSV Ready:', pathExists)
    db = pd.read_csv(file)
    pass
else:
# If file doesnt exist we must make one.
#  set column values  with pandas.
    df = pd.DataFrame(columns=['Date', 'Amount', 'Description'])
    # write columns to csv.
    df.to_csv(file, index=False)
    # Read csv into state
    db = pd.read_csv(file) 
    print('Database ready')

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
    date_ = input('Date: ') 
    amount_ = input('Amount: ')
    desc_ = input('Description: ')
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