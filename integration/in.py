import pandas as pd
import numpy as np

def read_and_trim_data():
    """
    Read the three CSV files and trim them to required columns
    """
    print("="*60)
    print("STEP 2: READ AND TRIM DATA")
    print("="*60)
    
    # 1. Read the three CSV files into individual DataFrames
    print("1. Reading CSV files...")
    
    try:
        # Read COVID cases data
        cases_df = pd.read_csv('covid_confirmed_usafacts.csv')
        print(f"   ✓ COVID cases data loaded: {cases_df.shape}")
        
        # Read COVID deaths data  
        deaths_df = pd.read_csv('covid_deaths_usafacts.csv')
        print(f"   ✓ COVID deaths data loaded: {deaths_df.shape}")
        
        # Read Census data
        census_df = pd.read_csv('acs2017_county_data.csv')
        print(f"   ✓ Census data loaded: {census_df.shape}")
        
    except FileNotFoundError as e:
        print(f"   ❌ Error reading files: {e}")
        return None, None, None
    
    print(f"\nOriginal column counts:")
    print(f"   - cases_df: {len(cases_df.columns)} columns")
    print(f"   - deaths_df: {len(deaths_df.columns)} columns") 
    print(f"   - census_df: {len(census_df.columns)} columns")
    # 2. Trim cases_df and deaths_df to needed columns
    print(f"\n2. Trimming COVID data to required columns...")
    
    # Required columns for COVID data
    required_covid_cols = ['County Name', 'State', '2023-07-23']
    print(f"   Looking for columns: {required_covid_cols}")
    
    # Trim cases_df
    if all(col in cases_df.columns for col in required_covid_cols):
        cases_df = cases_df[required_covid_cols].copy()
        print(f"   ✓ cases_df trimmed to: {list(cases_df.columns)}")
    else:
        missing_cols = [col for col in required_covid_cols if col not in cases_df.columns]
        print(f"   ❌ Missing columns in cases_df: {missing_cols}")
        print(f"   Available columns: {list(cases_df.columns[:10])}...{list(cases_df.columns[-5:])}")
    
    # Trim deaths_df  
    if all(col in deaths_df.columns for col in required_covid_cols):
        deaths_df = deaths_df[required_covid_cols].copy()
        print(f"   ✓ deaths_df trimmed to: {list(deaths_df.columns)}")
    else:
        missing_cols = [col for col in required_covid_cols if col not in deaths_df.columns]
        print(f"   ❌ Missing columns in deaths_df: {missing_cols}")
        print(f"   Available columns: {list(deaths_df.columns[:10])}...{list(deaths_df.columns[-5:])}")
    
    # 3. Trim census_df to required columns
    print(f"\n3. Trimming census data to required columns...")
    
    required_census_cols = ['County', 'State', 'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']
    print(f"   Looking for columns: {required_census_cols}")
    print(f"   Available census columns: {list(census_df.columns)}")
    
    if all(col in census_df.columns for col in required_census_cols):
        census_df = census_df[required_census_cols].copy()
        print(f"   ✓ census_df trimmed to: {list(census_df.columns)}")
    else:
        missing_cols = [col for col in required_census_cols if col not in census_df.columns]
        print(f"   ❌ Missing columns in census_df: {missing_cols}")
        print(f"   Available columns: {list(census_df.columns)}")
    
    # 4. Show the list of column headers for each DataFrame
    print(f"\n" + "="*60)
    print("4. FINAL COLUMN HEADERS:")
    print("="*60)
    
    print(f"\ncases_df columns ({len(cases_df.columns)}):")
    for i, col in enumerate(cases_df.columns, 1):
        print(f"   {i}. {col}")
    
    print(f"\ndeaths_df columns ({len(deaths_df.columns)}):")
    for i, col in enumerate(deaths_df.columns, 1):
        print(f"   {i}. {col}")
    
    print(f"\ncensus_df columns ({len(census_df.columns)}):")
    for i, col in enumerate(census_df.columns, 1):
        print(f"   {i}. {col}")
    
    # Show sample data from each DataFrame
    print(f"\n" + "="*60)
    print("SAMPLE DATA PREVIEW:")
    print("="*60)
    
    print(f"\ncases_df sample:")
    print(cases_df.head())
    
    print(f"\ndeaths_df sample:")
    print(deaths_df.head())
    
    print(f"\ncensus_df sample:")
    print(census_df.head())
    
    # Show data types
    print(f"\n" + "="*60)
    print("DATA TYPES:")
    print("="*60)
    
    print(f"\ncases_df data types:")
    print(cases_df.dtypes)
    
    print(f"\ndeaths_df data types:")
    print(deaths_df.dtypes)
    
    print(f"\ncensus_df data types:")
    print(census_df.dtypes)
    
    return cases_df, deaths_df, census_df

# Run the function
if __name__ == "__main__":
    cases_df, deaths_df, census_df = read_and_trim_data()
    
    if cases_df is not None:
        print(f"\n" + "="*60)
        print("✅ DATA SUCCESSFULLY READ AND TRIMMED")
        print("="*60)
        print(f"Ready for next step: Join the DataFrames")
        
        # Additional validation
        print(f"\nDataFrame shapes after trimming:")
        print(f"   - cases_df: {cases_df.shape}")
        print(f"   - deaths_df: {deaths_df.shape}")
        print(f"   - census_df: {census_df.shape}")
        
        # Show actual data samples
        print(f"\n" + "="*60)
        print("SAMPLE DATA FROM EACH DATAFRAME:")
        print("="*60)
        
        print(f"\nFirst 3 rows of cases_df:")
        print(cases_df.head(3))
        
        print(f"\nFirst 3 rows of deaths_df:")
        print(deaths_df.head(3))
        
        print(f"\nFirst 3 rows of census_df:")
        print(census_df.head(3))
        
    else:
        print(f"\n❌ Error occurred during data processing")
        
    # Save the trimmed dataframes for next steps
    if 'cases_df' in locals() and cases_df is not None:
        cases_df.to_csv('trimmed_cases.csv', index=False)
        deaths_df.to_csv('trimmed_deaths.csv', index=False)
        census_df.to_csv('trimmed_census.csv', index=False)
        print(f"\n💾 Trimmed data saved to CSV files for next steps")