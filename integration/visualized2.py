import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def visualize_correlations():
    """
    Create and display a correlation heatmap
    """
    logger.info("Starting correlation visualization")
    
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
    
    # Rebuild the integrated dataset
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
    
    # Create correlation matrix for numeric columns only
    logger.info("Computing correlation matrix...")
    numeric_columns = join_df.select_dtypes(include=[np.number]).columns.tolist()
    logger.info(f"Numeric columns: {numeric_columns}")
    
    correlation_matrix = join_df[numeric_columns].corr()
    logger.info("✓ Correlation matrix computed")
    
    # Print correlation matrix for reference
    print("\nCorrelation Matrix:")
    print("="*50)
    print(correlation_matrix.round(3))
    
    # Create the heatmap
    logger.info("Creating correlation heatmap...")
    
    # Set up the matplotlib figure
    plt.figure(figsize=(10, 8))
    
    # Create heatmap using seaborn
    sns.heatmap(correlation_matrix, 
                annot=True,           # Show correlation values
                cmap='coolwarm',      # Color scheme
                fmt='.2f',           # Format numbers to 2 decimal places
                linewidths=0.5,      # Add lines between cells
                center=0,            # Center colormap at 0
                square=True,         # Make cells square
                cbar_kws={'shrink': 0.8})  # Adjust colorbar size
    
    plt.title('Correlation Matrix Heatmap', fontsize=16, fontweight='bold')
    plt.xlabel('Variables', fontsize=12)
    plt.ylabel('Variables', fontsize=12)
    
    # Rotate labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    logger.info("✓ Heatmap created")
    
    # Display the plot
    plt.show()
    
    # Also save the plot
    plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
    logger.info("✓ Heatmap saved as 'correlation_heatmap.png'")
    
    return correlation_matrix

if __name__ == "__main__":
    correlation_matrix = visualize_correlations()
    logger.info("Correlation visualization complete")
    
    print("\n" + "="*60)
    print("INSTRUCTIONS FOR SUBMISSION:")
    print("="*60)
    print("1. Run this script to generate the heatmap")
    print("2. The heatmap will display on screen")
    print("3. A high-quality PNG file 'correlation_heatmap.png' has been saved")
    print("4. Take a screenshot of the displayed heatmap OR")
    print("5. Use the saved PNG file for your submission")
    print("="*60)