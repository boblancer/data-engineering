import pandas as pd

def solve_integration_challenge_2():
    """
    Remove "Statewide Unallocated" records from COVID data
    """
    print("STEP 4: INTEGRATION CHALLENGE #2")
    print("="*50)
    
    # Read the cleaned data from previous step
    cases_df = pd.read_csv('covid_confirmed_usafacts.csv')
    deaths_df = pd.read_csv('covid_deaths_usafacts.csv')
    
    # Trim to needed columns and remove trailing spaces
    cases_df = cases_df[['County Name', 'State', '2023-07-23']].copy()
    deaths_df = deaths_df[['County Name', 'State', '2023-07-23']].copy()
    
    cases_df['County Name'] = cases_df['County Name'].str.rstrip()
    deaths_df['County Name'] = deaths_df['County Name'].str.rstrip()
    
    print(f"BEFORE removing 'Statewide Unallocated':")
    print(f"cases_df: {len(cases_df)} rows")
    print(f"deaths_df: {len(deaths_df)} rows")
    
    # Check how many "Statewide Unallocated" records exist
    statewide_cases = cases_df[cases_df['County Name'] == 'Statewide Unallocated']
    statewide_deaths = deaths_df[deaths_df['County Name'] == 'Statewide Unallocated']
    
    print(f"\n'Statewide Unallocated' records found:")
    print(f"In cases_df: {len(statewide_cases)}")
    print(f"In deaths_df: {len(statewide_deaths)}")
    
    # 1. Remove "Statewide Unallocated" records
    print(f"\n1. Removing 'Statewide Unallocated' records...")
    
    cases_df = cases_df[cases_df['County Name'] != 'Statewide Unallocated']
    deaths_df = deaths_df[deaths_df['County Name'] != 'Statewide Unallocated']
    
    print("✓ Statewide Unallocated records removed")
    
    # 2. Show how many rows remain
    print(f"\n2. AFTER removing 'Statewide Unallocated':")
    print(f"cases_df: {len(cases_df)} rows remain")
    print(f"deaths_df: {len(deaths_df)} rows remain")
    
    # Verify no "Statewide Unallocated" records remain
    remaining_statewide_cases = cases_df[cases_df['County Name'] == 'Statewide Unallocated']
    remaining_statewide_deaths = deaths_df[deaths_df['County Name'] == 'Statewide Unallocated']
    
    print(f"\nVerification - 'Statewide Unallocated' remaining:")
    print(f"In cases_df: {len(remaining_statewide_cases)}")
    print(f"In deaths_df: {len(remaining_statewide_deaths)}")
    
    return cases_df, deaths_df

# Run it
if __name__ == "__main__":
    cases_df, deaths_df = solve_integration_challenge_2()