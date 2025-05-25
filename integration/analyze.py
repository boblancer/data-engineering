import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def analyze_correlations():
    """
    Create and analyze correlation matrix for the integrated dataset
    """
    logger.info("Starting correlation analysis")
    
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
    
    # Rebuild the integrated dataset (same as previous step)
    logger.info("Rebuilding integrated dataset...")
    
    # Load and prepare data
    cases_df = pd.read_csv('covid_confirmed_usafacts.csv')
    deaths_df = pd.read_csv('covid_deaths_usafacts.csv')
    census_df = pd.read_csv('acs2017_county_data.csv')
    
    # Apply all cleaning steps
    cases_df = cases_df[['County Name', 'State', '2023-07-23']].copy()
    deaths_df = deaths_df[['County Name', 'State', '2023-07-23']].copy()
    census_df = census_df[['County', 'State', 'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']].copy()
    
    cases_df['County Name'] = cases_df['County Name'].str.rstrip()
    deaths_df['County Name'] = deaths_df['County Name'].str.rstrip()
    cases_df = cases_df[cases_df['County Name'] != 'Statewide Unallocated']
    deaths_df = deaths_df[deaths_df['County Name'] != 'Statewide Unallocated']
    
    cases_df['State'] = cases_df['State'].map(us_state_abbrev)
    deaths_df['State'] = deaths_df['State'].map(us_state_abbrev)
    
    cases_df['key'] = cases_df['County Name'] + ', ' + cases_df['State']
    deaths_df['key'] = deaths_df['County Name'] + ', ' + deaths_df['State']
    census_df['key'] = census_df['County'] + ', ' + census_df['State']
    
    cases_df = cases_df.set_index('key')
    deaths_df = deaths_df.set_index('key')
    census_df = census_df.set_index('key')
    
    cases_df = cases_df.rename(columns={'2023-07-23': 'Cases'})
    deaths_df = deaths_df.rename(columns={'2023-07-23': 'Deaths'})
    
    # Join the dataframes
    covid_df = cases_df.join(deaths_df['Deaths'])
    census_cols_to_join = ['County', 'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']
    join_df = covid_df.join(census_df[census_cols_to_join])
    
    # Add per capita columns
    join_df['CasesPerCap'] = join_df['Cases'] / join_df['TotalPop']
    join_df['DeathsPerCap'] = join_df['Deaths'] / join_df['TotalPop']
    
    logger.info(f"✓ Dataset rebuilt: {len(join_df):,} rows")
    
    # Identify numeric columns
    logger.info("Identifying numeric columns...")
    numeric_columns = join_df.select_dtypes(include=[np.number]).columns.tolist()
    logger.info(f"Numeric columns found: {numeric_columns}")
    
    # Create correlation matrix
    logger.info("Computing correlation matrix...")
    correlation_matrix = join_df[numeric_columns].corr()
    logger.info("✓ Correlation matrix computed")
    
    # Display the correlation matrix
    print("\n" + "="*60)
    print("CORRELATION MATRIX")
    print("="*60)
    print(correlation_matrix)
    
    # Round for better readability
    print("\n" + "="*60)
    print("CORRELATION MATRIX (rounded to 3 decimal places)")
    print("="*60)
    correlation_rounded = correlation_matrix.round(3)
    print(correlation_rounded)
    
    # Analyze strongest correlations
    logger.info("Analyzing strongest correlations...")
    
    # Get correlation pairs (excluding diagonal)
    correlations = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            var1 = correlation_matrix.columns[i]
            var2 = correlation_matrix.columns[j]
            corr_value = correlation_matrix.iloc[i, j]
            correlations.append((var1, var2, corr_value))
    
    # Sort by absolute correlation strength
    correlations.sort(key=lambda x: abs(x[2]), reverse=True)
    
    print("\n" + "="*60)
    print("STRONGEST CORRELATIONS (sorted by strength)")
    print("="*60)
    
    for var1, var2, corr in correlations:
        direction = "positive" if corr > 0 else "negative"
        strength = "very strong" if abs(corr) >= 0.8 else "strong" if abs(corr) >= 0.6 else "moderate" if abs(corr) >= 0.4 else "weak"
        print(f"{var1} ↔ {var2}: {corr:.3f} ({strength} {direction})")
    
    return correlation_matrix

if __name__ == "__main__":
    correlation_matrix = analyze_correlations()
    logger.info("Correlation analysis complete")