import pandas as pd

def solve_integration_challenge_5():
    """
    Rename the confusing date columns to Cases and Deaths
    """
    print("STEP 7: INTEGRATION CHALLENGE #5")
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
    
    # Load and clean all data (applying all previous steps)
    cases_df = pd.read_csv('covid_confirmed_usafacts.csv')
    deaths_df = pd.read_csv('covid_deaths_usafacts.csv')
    census_df = pd.read_csv('acs2017_county_data.csv')
    
    # Trim columns
    cases_df = cases_df[['County Name', 'State', '2023-07-23']].copy()
    deaths_df = deaths_df[['County Name', 'State', '2023-07-23']].copy()
    census_df = census_df[['County', 'State', 'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']].copy()
    
    # Clean county names and remove unallocated
    cases_df['County Name'] = cases_df['County Name'].str.rstrip()
    deaths_df['County Name'] = deaths_df['County Name'].str.rstrip()
    cases_df = cases_df[cases_df['County Name'] != 'Statewide Unallocated']
    deaths_df = deaths_df[deaths_df['County Name'] != 'Statewide Unallocated']
    
    # Convert state abbreviations to full names
    cases_df['State'] = cases_df['State'].map(us_state_abbrev)
    deaths_df['State'] = deaths_df['State'].map(us_state_abbrev)
    
    # Create key columns and set as index
    cases_df['key'] = cases_df['County Name'] + ', ' + cases_df['State']
    deaths_df['key'] = deaths_df['County Name'] + ', ' + deaths_df['State']
    census_df['key'] = census_df['County'] + ', ' + census_df['State']
    
    cases_df = cases_df.set_index('key')
    deaths_df = deaths_df.set_index('key')
    census_df = census_df.set_index('key')
    
    print("Data prepared with all previous cleaning steps")
    
    # Show current confusing column names
    print(f"\nBEFORE renaming columns:")
    print(f"cases_df columns: {cases_df.columns.values.tolist()}")
    print(f"deaths_df columns: {deaths_df.columns.values.tolist()}")
    
    # 1. Rename the confusing date columns
    print(f"\n1. Renaming '2023-07-23' columns...")
    
    cases_df = cases_df.rename(columns={'2023-07-23': 'Cases'})
    deaths_df = deaths_df.rename(columns={'2023-07-23': 'Deaths'})
    
    print("✓ Columns renamed")
    
    # 2. Show the resulting column headers
    print(f"\n2. AFTER renaming columns:")
    print(f"cases_df.columns.values.tolist(): {cases_df.columns.values.tolist()}")
    print(f"deaths_df.columns.values.tolist(): {deaths_df.columns.values.tolist()}")
    
    return cases_df, deaths_df, census_df

# Run it
if __name__ == "__main__":
    cases_df, deaths_df, census_df = solve_integration_challenge_5()