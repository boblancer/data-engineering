import pandas as pd

def solve_integration_challenge_1():
    """
    Remove trailing spaces from county names and test with Washington County
    """
    print("STEP 3: INTEGRATION CHALLENGE #1")
    print("="*50)
    
    # Read the data
    cases_df = pd.read_csv('covid_confirmed_usafacts.csv')
    deaths_df = pd.read_csv('covid_deaths_usafacts.csv')
    
    # Trim to needed columns
    cases_df = cases_df[['County Name', 'State', '2023-07-23']].copy()
    deaths_df = deaths_df[['County Name', 'State', '2023-07-23']].copy()
    
    print(f"Data loaded: {len(cases_df)} counties")
    
    # Show the problem - county names with trailing spaces
    print(f"\nBEFORE cleaning:")
    print(f"Sample county: '{cases_df['County Name'].iloc[1]}'")
    print(f"Length: {len(cases_df['County Name'].iloc[1])}")
    
    # Test search BEFORE cleaning
    washington_before = cases_df[cases_df['County Name'] == 'Washington County']
    print(f"'Washington County' found: {len(washington_before)} counties")
    
    # 1. Remove trailing spaces
    print(f"\n1. Removing trailing spaces...")
    cases_df['County Name'] = cases_df['County Name'].str.rstrip()
    deaths_df['County Name'] = deaths_df['County Name'].str.rstrip()
    print("✓ Trailing spaces removed")
    
    # Show after cleaning
    print(f"\nAFTER cleaning:")
    print(f"Sample county: '{cases_df['County Name'].iloc[1]}'")
    print(f"Length: {len(cases_df['County Name'].iloc[1])}")
    
    # 2. Test search for "Washington County"
    print(f"\n2. Testing search for 'Washington County'...")
    washington_cases = cases_df[cases_df['County Name'] == 'Washington County']
    washington_deaths = deaths_df[deaths_df['County Name'] == 'Washington County']
    
    print(f"Found in cases_df: {len(washington_cases)} counties")
    print(f"Found in deaths_df: {len(washington_deaths)} counties")
    
    # 3. Answer the question
    num_washington_counties = len(washington_cases)
    print(f"\n3. ANSWER: {num_washington_counties} counties are named 'Washington County'")
    
    # Show which states have Washington County
    if num_washington_counties > 0:
        print("\nWashington Counties by state:")
        for _, row in washington_cases.iterrows():
            print(f"   - {row['County Name']}, {row['State']}")
    
    return cases_df, deaths_df

# Run it
if __name__ == "__main__":
    cases_df, deaths_df = solve_integration_challenge_1()