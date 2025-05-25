import pandas as pd

def solve_integration_challenge_4():
    """
    Create matching key columns for joining the DataFrames
    """
    print("STEP 6: INTEGRATION CHALLENGE #4")
    print("="*50)
    
    # State abbreviation to full name mapping
    us_state_abbrev = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
        'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
        'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
        'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
        'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
        'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
    }
    
    # Load and clean COVID data
    cases_df = pd.read_csv('covid_confirmed_usafacts.csv')
    deaths_df = pd.read_csv('covid_deaths_usafacts.csv')
    
    # Trim columns
    cases_df = cases_df[['County Name', 'State', '2023-07-23']].copy()
    deaths_df = deaths_df[['County Name', 'State', '2023-07-23']].copy()
    
    # Clean county names and remove unallocated
    cases_df['County Name'] = cases_df['County Name'].str.rstrip()
    deaths_df['County Name'] = deaths_df['County Name'].str.rstrip()
    cases_df = cases_df[cases_df['County Name'] != 'Statewide Unallocated']
    deaths_df = deaths_df[deaths_df['County Name'] != 'Statewide Unallocated']
    
    # Convert state abbreviations to full names
    cases_df['State'] = cases_df['State'].map(us_state_abbrev)
    deaths_df['State'] = deaths_df['State'].map(us_state_abbrev)
    
    # Load census data
    census_df = pd.read_csv('acs2017_county_data.csv')
    census_df = census_df[['County', 'State', 'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']].copy()
    
    print(f"Data loaded:")
    print(f"cases_df: {len(cases_df)} rows")
    print(f"deaths_df: {len(deaths_df)} rows") 
    print(f"census_df: {len(census_df)} rows")
    
    # 1. Create "key" column by concatenating County and State
    print(f"\n1. Creating 'key' column...")
    
    cases_df['key'] = cases_df['County Name'] + ', ' + cases_df['State']
    deaths_df['key'] = deaths_df['County Name'] + ', ' + deaths_df['State']
    census_df['key'] = census_df['County'] + ', ' + census_df['State']
    
    print("✓ Key columns created")
    
    # Show sample keys
    print(f"\nSample keys:")
    print(f"cases_df: {cases_df['key'].head(3).tolist()}")
    print(f"census_df: {census_df['key'].head(3).tolist()}")
    
    # 2. Set "key" as index for each DataFrame
    print(f"\n2. Setting 'key' as index...")
    
    cases_df = cases_df.set_index('key')
    deaths_df = deaths_df.set_index('key')
    census_df = census_df.set_index('key')
    
    print("✓ Index set to 'key' for all DataFrames")
    
    # 3. Show first few rows of census_df
    print(f"\n3. census_df.head():")
    print(census_df.head())
    
    return cases_df, deaths_df, census_df

# Run it
if __name__ == "__main__":
    cases_df, deaths_df, census_df = solve_integration_challenge_4()