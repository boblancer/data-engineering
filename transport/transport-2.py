import pandas as pd
from datetime import datetime, timedelta

def load_and_decode_timestamps():
    # Get all column names
    all_columns = pd.read_csv('bc_trip259172515_230215.csv', nrows=0).columns.tolist()
    
    # Create a list of columns to keep (all except the ones we want to filter)
    columns_to_keep = [col for col in all_columns if col not in ['EVENT_NO_STOP', 'GPS_SATELLITES', 'GPS_HDOP']]
    
    # Read only the columns we want to keep
    df = pd.read_csv('bc_trip259172515_230215.csv', usecols=columns_to_keep)
    
    # Print the shape of the dataframe
    print(f"DataFrame shape: {df.shape}")
    
    # Define a function to convert OPD_DATE and ACT_TIME to a timestamp
    def create_timestamp(row):
        # Create datetime from OPD_DATE
        base_date = pd.to_datetime(row['OPD_DATE'], format='%d%b%Y:%H:%M:%S')
        
        # Create timedelta from ACT_TIME (seconds)
        time_offset = timedelta(seconds=int(row['ACT_TIME']))
        
        # Add timedelta to datetime
        return base_date + time_offset
    
    # Apply the function to create the TIMESTAMP column
    df['TIMESTAMP'] = df.apply(create_timestamp, axis=1)
    
    # Print the first few rows to verify timestamps were created correctly
    print("\nFirst few rows with TIMESTAMP:")
    print(df[['OPD_DATE', 'ACT_TIME', 'TIMESTAMP']].head())
    
    # Now drop the OPD_DATE and ACT_TIME columns
    df = df.drop(columns=['OPD_DATE', 'ACT_TIME'])
    
    # Print the remaining columns
    print("\nRemaining columns after dropping OPD_DATE and ACT_TIME:")
    print(df.columns.tolist())
    
    return df

# Execute the function
decoded_df = load_and_decode_timestamps()