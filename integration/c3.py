import pandas as pd

def solve_integration_challenge_3():
    """
    Convert state abbreviations to full state names in COVID data
    """
    print("STEP 5: INTEGRATION CHALLENGE #3")
    print("="*50)
    
    # State abbreviation to full name mapping (public domain)
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
    
    # Load data with previous cleaning applied
    cases_df = pd.read_csv('covid_confirmed_usafacts.csv')
    deaths_df = pd.read_csv('covid_deaths_usafacts.csv')
    
    # Apply previous cleaning steps
    cases_df = cases_df[['County Name', 'State', '2023-07-23']].copy()
    deaths_df = deaths_df[['County Name', 'State', '2023-07-23']].copy()
    
    # Remove trailing spaces
    cases_df['County Name'] = cases_df['County Name'].str.rstrip()
    deaths_df['County Name'] = deaths_df['County Name'].str.rstrip()
    
    # Remove "Statewide Unallocated"
    cases_df = cases_df[cases_df['County Name'] != 'Statewide Unallocated']
    deaths_df = deaths_df[deaths_df['County Name'] != 'Statewide Unallocated']
    
    print(f"Data loaded: {len(cases_df)} counties")
    
    # Show current state format
    print(f"\nBEFORE converting state names:")
    print("Sample states in cases_df:")
    print(cases_df['State'].head().tolist())
    
    # 1. Convert state abbreviations to full names
    print(f"\n1. Converting state abbreviations to full names...")
    
    cases_df['State'] = cases_df['State'].map(us_state_abbrev)
    deaths_df['State'] = deaths_df['State'].map(us_state_abbrev)
    
    print("✓ State names converted")
    
    # Show after conversion
    print(f"\nAFTER converting state names:")
    print("Sample states in cases_df:")
    print(cases_df['State'].head().tolist())
    
    # Show first few rows of cases_df
    print(f"\ncases_df.head():")
    print(cases_df.head())
    
    return cases_df, deaths_df

# Run it
if __name__ == "__main__":
    cases_df, deaths_df = solve_integration_challenge_3()