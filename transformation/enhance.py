import pandas as pd
from datetime import datetime, timedelta
import os

def load_and_enhance_data(file_path='bc_trip259172515_230215.csv'):
    # Verify the file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found!")
        print(f"Current working directory: {os.getcwd()}")
        print("Please provide the correct file path.")
        return None
    
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Filter out unwanted columns
        df = df.drop(columns=['EVENT_NO_STOP', 'GPS_SATELLITES', 'GPS_HDOP'], errors='ignore')
        
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
        
        # Drop the OPD_DATE and ACT_TIME columns
        df = df.drop(columns=['OPD_DATE', 'ACT_TIME'])
        
        # Sort by TIMESTAMP to ensure records are in chronological order
        df = df.sort_values(by='TIMESTAMP')
        
        # Calculate differences in METERS and TIMESTAMP
        df['dMETERS'] = df['METERS'].diff()
        
        # Convert TIMESTAMP differences to seconds
        df['dTIMESTAMP'] = df['TIMESTAMP'].diff().dt.total_seconds()
        
        # Calculate SPEED (meters per second)
        # Use a lambda function to avoid division by zero
        df['SPEED'] = df.apply(
            lambda row: row['dMETERS'] / row['dTIMESTAMP'] if row['dTIMESTAMP'] > 0 else 0, 
            axis=1
        )
        
        # Drop the temporary columns used for calculation
        df = df.drop(columns=['dMETERS', 'dTIMESTAMP'])
        
        # Calculate speed statistics
        min_speed = df['SPEED'].min()
        max_speed = df['SPEED'].max()
        avg_speed = df['SPEED'].mean()
        
        print(f"\nSpeed Statistics (meters per second):")
        print(f"Minimum speed: {min_speed:.2f} m/s")
        print(f"Maximum speed: {max_speed:.2f} m/s")
        print(f"Average speed: {avg_speed:.2f} m/s")
        
        # Convert to km/h for easier interpretation
        print(f"\nSpeed Statistics (kilometers per hour):")
        print(f"Minimum speed: {min_speed * 3.6:.2f} km/h")
        print(f"Maximum speed: {max_speed * 3.6:.2f} km/h")
        print(f"Average speed: {avg_speed * 3.6:.2f} km/h")
        
        # Print remaining columns
        print("\nFinal columns in DataFrame:")
        print(df.columns.tolist())
        
        return df
    
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

# Execute the function with the file path
file_path = 'bc_trip259172515_230215.csv'  # Update this path as needed
enhanced_df = load_and_enhance_data(file_path)