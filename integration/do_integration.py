import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def do_integration():
    """
    Integrate all three DataFrames and add per capita columns
    """
    logger.info("Starting data integration process")
    
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
    
    # Load raw data
    logger.info("Loading CSV files...")
    try:
        cases_df = pd.read_csv('covid_confirmed_usafacts.csv')
        deaths_df = pd.read_csv('covid_deaths_usafacts.csv')
        census_df = pd.read_csv('acs2017_county_data.csv')
        logger.info("✓ All CSV files loaded successfully")
    except FileNotFoundError as e:
        logger.error(f"Failed to load CSV files: {e}")
        return None
    
    # Data preparation pipeline
    logger.info("Starting data preparation pipeline...")
    
    # Step 1: Trim columns
    logger.info("Trimming columns to required fields...")
    cases_df = cases_df[['County Name', 'State', '2023-07-23']].copy()
    deaths_df = deaths_df[['County Name', 'State', '2023-07-23']].copy()
    census_df = census_df[['County', 'State', 'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']].copy()
    logger.info("✓ Columns trimmed")
    
    # Step 2: Clean county names
    logger.info("Removing trailing spaces from county names...")
    cases_df['County Name'] = cases_df['County Name'].str.rstrip()
    deaths_df['County Name'] = deaths_df['County Name'].str.rstrip()
    logger.info("✓ Trailing spaces removed")
    
    # Step 3: Remove unallocated records
    logger.info("Removing 'Statewide Unallocated' records...")
    before_cases = len(cases_df)
    before_deaths = len(deaths_df)
    cases_df = cases_df[cases_df['County Name'] != 'Statewide Unallocated']
    deaths_df = deaths_df[deaths_df['County Name'] != 'Statewide Unallocated']
    logger.info(f"✓ Removed {before_cases - len(cases_df)} cases records, {before_deaths - len(deaths_df)} deaths records")
    
    # Step 4: Convert state abbreviations
    logger.info("Converting state abbreviations to full names...")
    cases_df['State'] = cases_df['State'].map(us_state_abbrev)
    deaths_df['State'] = deaths_df['State'].map(us_state_abbrev)
    logger.info("✓ State names converted")
    
    # Step 5: Create key columns
    logger.info("Creating key columns for joining...")
    cases_df['key'] = cases_df['County Name'] + ', ' + cases_df['State']
    deaths_df['key'] = deaths_df['County Name'] + ', ' + deaths_df['State']
    census_df['key'] = census_df['County'] + ', ' + census_df['State']
    logger.info("✓ Key columns created")
    
    # Step 6: Set index
    logger.info("Setting key as index...")
    cases_df = cases_df.set_index('key')
    deaths_df = deaths_df.set_index('key')
    census_df = census_df.set_index('key')
    logger.info("✓ Index set to key")
    
    # Step 7: Rename columns
    logger.info("Renaming date columns to meaningful names...")
    cases_df = cases_df.rename(columns={'2023-07-23': 'Cases'})
    deaths_df = deaths_df.rename(columns={'2023-07-23': 'Deaths'})
    logger.info("✓ Columns renamed")
    
    # Log preparation summary
    logger.info("Data preparation complete")
    logger.info(f"  cases_df: {len(cases_df):,} rows")
    logger.info(f"  deaths_df: {len(deaths_df):,} rows")
    logger.info(f"  census_df: {len(census_df):,} rows")
    
    # Integration phase
    logger.info("Starting DataFrame integration...")
    
    # First join: cases + deaths
    logger.info("Performing first join: cases + deaths...")
    covid_df = cases_df.join(deaths_df['Deaths'])
    logger.info(f"✓ First join complete: {len(covid_df):,} rows")
    
    # Second join: covid + census
    logger.info("Performing second join: covid + census...")
    census_cols_to_join = ['County', 'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']
    join_df = covid_df.join(census_df[census_cols_to_join])
    logger.info(f"✓ Second join complete: {len(join_df):,} rows")
    
    # Calculate per capita metrics
    logger.info("Calculating per capita metrics...")
    join_df['CasesPerCap'] = join_df['Cases'] / join_df['TotalPop']
    join_df['DeathsPerCap'] = join_df['Deaths'] / join_df['TotalPop']
    logger.info("✓ Per capita columns added")
    
    # Final summary
    logger.info("Integration complete!")
    logger.info(f"Final DataFrame contains {len(join_df):,} rows")
    logger.info(f"Columns: {list(join_df.columns)}")
    
    # Data quality check
    logger.info("Performing data quality check...")
    missing_data = join_df.isnull().sum()
    if missing_data.sum() > 0:
        logger.warning("Missing data detected:")
        for col, count in missing_data[missing_data > 0].items():
            logger.warning(f"  {col}: {count:,} missing values")
    else:
        logger.info("✓ No missing data detected")
    
    logger.info("Sample of integrated data:")
    print(join_df.head())
    
    return join_df

if __name__ == "__main__":
    join_df = do_integration()
    if join_df is not None:
        logger.info(f"SUCCESS: Integrated dataset created with {len(join_df):,} rows")
    else:
        logger.error("FAILED: Integration process failed")