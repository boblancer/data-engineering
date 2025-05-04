import pandas as pd

# Read the CSV file
df = pd.read_csv('bc_trip259172515_230215.csv')

# Count the number of records
num_records = len(df)

# Display the count and the first few records
print(f"Number of breadcrumb records: {num_records}")
print("\nFirst 5 records:")
print(df.head())

# Display column information
print("\nColumn information:")
print(df.info())

import pandas as pd

# Approach 1: Read all data then drop columns
def filter_with_drop():
    # Read the full CSV file
    df = pd.read_csv('bc_trip259172515_230215.csv')
    
    # Print the original column count
    print(f"Original number of columns: {len(df.columns)}")
    
    # Drop the specified columns
    df = df.drop(columns=['EVENT_NO_STOP', 'GPS_SATELLITES', 'GPS_HDOP'])
    
    # Print the new column count
    print(f"Number of columns after dropping: {len(df.columns)}")
    
    return df

# Approach 2: Use usecols parameter to only read needed columns
def filter_with_usecols():
    # First, get all column names
    all_columns = pd.read_csv('bc_trip259172515_230215.csv', nrows=0).columns.tolist()
    
    # Create a list of columns to keep (all except the ones we want to filter)
    columns_to_keep = [col for col in all_columns if col not in ['EVENT_NO_STOP', 'GPS_SATELLITES', 'GPS_HDOP']]
    
    # Read only the columns we want to keep
    df = pd.read_csv('bc_trip259172515_230215.csv', usecols=columns_to_keep)
    
    # Print the column count
    print(f"Number of columns with usecols: {len(df.columns)}")
    
    return df

# Run both approaches
print("APPROACH 1: Using drop() method")
df1 = filter_with_drop()
print("\nAPPROACH 2: Using usecols parameter")
df2 = filter_with_usecols()

# Verify both dataframes have the same columns
print("\nBoth approaches have same columns:", sorted(df1.columns.tolist()) == sorted(df2.columns.tolist()))