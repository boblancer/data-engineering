import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
from scipy import stats

def validate_name_not_null(csv_file):
    """
    Validates the assertion that every record has a non-null name field.
    
    Args:
        csv_file (str): Path to the CSV file
        
    Returns:
        int: Number of records that violate the assertion
    """
    # Read the CSV file
    print(f"Reading file: {csv_file}")
    df = pd.read_csv(csv_file)
    
    # Count records with null names
    # This checks for various null representations: None, np.nan, empty strings, whitespace-only strings
    null_names = df[df['name'].isna() | (df['name'].astype(str).str.strip() == '')].shape[0]
    
    # Print the results
    print("\n--- Existence Assertion: Non-null Name Field ---")
    print(f"Total records: {len(df)}")
    print(f"Records with null names: {null_names}")
    print(f"Assertion {'PASSED' if null_names == 0 else 'FAILED'}")
    
    return null_names

def validate_hire_date_after_2015(csv_file):
    """
    Validates the assertion that every employee was hired no earlier than 2015.
    
    Args:
        csv_file (str): Path to the CSV file
        
    Returns:
        int: Number of records that violate the assertion
    """
    # Read the CSV file if not already loaded
    df = pd.read_csv(csv_file)
    
    # Convert hire_date column to datetime
    # Assuming the format is YYYY-MM-DD; adjust as needed
    df['hire_date'] = pd.to_datetime(df['hire_date'], errors='coerce')
    
    # Find records with hire_date before 2015-01-01
    early_hires = df[df['hire_date'] < '2015-01-01'].shape[0]
    
    # Print the results
    print("\n--- Limit Assertion: Hire Date No Earlier Than 2015 ---")
    print(f"Total records: {len(df)}")
    print(f"Records with hire_date before 2015: {early_hires}")
    print(f"Assertion {'PASSED' if early_hires == 0 else 'FAILED'}")
    
    return early_hires

def validate_birth_before_hire(csv_file):
    """
    Validates the assertion that each employee was born before they were hired.
    
    Args:
        csv_file (str): Path to the CSV file
        
    Returns:
        int: Number of records that violate the assertion
    """
    # Read the CSV file if not already loaded
    df = pd.read_csv(csv_file)
    
    # Convert date columns to datetime
    df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
    df['hire_date'] = pd.to_datetime(df['hire_date'], errors='coerce')
    
    # Find records where birth_date is not before hire_date
    # This includes records where birth_date >= hire_date or where either date is null
    invalid_records = df[~((df['birth_date'].notna() & df['hire_date'].notna()) & 
                          (df['birth_date'] < df['hire_date']))].shape[0]
    
    # Find records where both dates exist but birth_date is not before hire_date
    impossible_records = df[(df['birth_date'].notna() & df['hire_date'].notna()) & 
                           (df['birth_date'] >= df['hire_date'])].shape[0]
    
    # Print the results
    print("\n--- Intra-record Assertion: Birth Before Hire ---")
    print(f"Total records: {len(df)}")
    print(f"Records with missing date fields: {invalid_records - impossible_records}")
    print(f"Records where birth_date is not before hire_date: {impossible_records}")
    print(f"Total violation count: {impossible_records}")  # We only count impossible cases as violations
    print(f"Assertion {'PASSED' if impossible_records == 0 else 'FAILED'}")
    
    return impossible_records

def validate_manager_exists(csv_file):
    """
    Validates the assertion that each employee has a manager who is a known employee.
    
    Args:
        csv_file (str): Path to the CSV file
        
    Returns:
        int: Number of records that violate the assertion
    """
    # Read the CSV file if not already loaded
    df = pd.read_csv(csv_file)
    
    # Get unique set of valid employee IDs
    valid_eids = set(df['eid'].unique())
    
    # Count employees with reports_to values that are not null and not valid employee IDs
    # First, filter out NaN values from reports_to
    invalid_managers = df[
        (df['reports_to'].notna()) &  # reports_to is not null
        (~df['reports_to'].isin(valid_eids))  # reports_to is not a valid eid
    ].shape[0]
    
    # Print the results
    print("\n--- Inter-record Assertion: Manager Exists ---")
    print(f"Total records: {len(df)}")
    print(f"Employees with non-existent managers: {invalid_managers}")
    print(f"Assertion {'PASSED' if invalid_managers == 0 else 'FAILED'}")
    
    return invalid_managers

def validate_multiple_employees_per_city(csv_file):
    """
    Validates the assertion that each city has more than one employee.
    
    Args:
        csv_file (str): Path to the CSV file
        
    Returns:
        int: Number of cities that violate the assertion
    """
    # Read the CSV file if not already loaded
    df = pd.read_csv(csv_file)
    
    # Count employees per city
    city_counts = df['city'].value_counts()
    
    # Find cities with only one employee
    single_employee_cities = city_counts[city_counts == 1]
    
    # Print the results
    print("\n--- Summary Assertion: Multiple Employees Per City ---")
    print(f"Total cities: {len(city_counts)}")
    print(f"Cities with only one employee: {len(single_employee_cities)}")
    
    if len(single_employee_cities) > 0:
        print("Examples of cities with only one employee:")
        for city, count in single_employee_cities.head(5).items():
            print(f"  - {city}: {count} employee")
    
    print(f"Assertion {'PASSED' if len(single_employee_cities) == 0 else 'FAILED'}")
    
    return len(single_employee_cities)

def validate_normal_salary_distribution(csv_file):
    """
    Validates the assertion that salaries are normally distributed.
    
    Args:
        csv_file (str): Path to the CSV file
        
    Returns:
        tuple: (is_normal, p_value, statistics)
    """
    # Read the CSV file if not already loaded
    df = pd.read_csv(csv_file)
    
    # Basic statistics on salary
    salary_stats = df['salary'].describe()
    
    # Normality test (Shapiro-Wilk)
    # Due to the limitations of the test, for large datasets we might need to sample
    if len(df) > 5000:
        # Sample 5000 records for the test
        sample = df['salary'].sample(5000, random_state=42)
        shapiro_test = stats.shapiro(sample)
    else:
        shapiro_test = stats.shapiro(df['salary'])
    
    # Prepare visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Histogram
    ax1.hist(df['salary'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    ax1.set_title('Salary Distribution')
    ax1.set_xlabel('Salary')
    ax1.set_ylabel('Frequency')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Q-Q plot
    stats.probplot(df['salary'], dist="norm", plot=ax2)
    ax2.set_title('Q-Q Plot')
    
    # Save the figure for review
    plt.tight_layout()
    plt.savefig('salary_distribution.png')
    plt.close()
    
    # Print the results
    print("\n--- Statistical Assertion: Normal Salary Distribution ---")
    print(f"Salary Statistics:\n{salary_stats}")
    print(f"Shapiro-Wilk Test: W={shapiro_test[0]:.4f}, p-value={shapiro_test[1]:.8f}")
    
    # For a normal distribution, p-value should be > 0.05
    is_normal = shapiro_test[1] > 0.05
    
    print(f"According to Shapiro-Wilk test, the distribution {'is' if is_normal else 'is not'} normal")
    print(f"Assertion {'PASSED' if is_normal else 'FAILED'}")
    print("Visualization saved as 'salary_distribution.png'")
    
    return (is_normal, shapiro_test[1], salary_stats)

if __name__ == "__main__":
    csv_file = "employees.csv"
    
    # Validate existence assertion
    null_name_count = validate_name_not_null(csv_file)
    print("\nExistence Assertion Result: ", end="")
    if null_name_count == 0:
        print("Every record has a non-null name field.")
    else:
        print(f"{null_name_count} records have null name fields.")
    
    # Validate limit assertion
    early_hire_count = validate_hire_date_after_2015(csv_file)
    print("\nLimit Assertion Result: ", end="")
    if early_hire_count == 0:
        print("Every employee was hired in 2015 or later.")
    else:
        print(f"{early_hire_count} employees were hired before 2015.")
        
    # Validate intra-record assertion
    impossible_date_count = validate_birth_before_hire(csv_file)
    print("\nIntra-record Assertion Result: ", end="")
    if impossible_date_count == 0:
        print("Every employee was born before they were hired.")
    else:
        print(f"{impossible_date_count} employees have birth dates that are not before their hire dates.")
        
    # Validate inter-record assertion
    invalid_manager_count = validate_manager_exists(csv_file)
    print("\nInter-record Assertion Result: ", end="")
    if invalid_manager_count == 0:
        print("Every employee has a manager who is a known employee.")
    else:
        print(f"{invalid_manager_count} employees have managers who are not known employees.")
        
    # Validate summary assertion
    single_employee_city_count = validate_multiple_employees_per_city(csv_file)
    print("\nSummary Assertion Result: ", end="")
    if single_employee_city_count == 0:
        print("Every city has more than one employee.")
    else:
        print(f"{single_employee_city_count} cities have only one employee.")
        
    # Validate statistical assertion
    is_normal, p_value, salary_stats = validate_normal_salary_distribution(csv_file)
    print("\nStatistical Assertion Result: ", end="")
    if is_normal:
        print("Salaries are normally distributed.")
    else:
        print("Salaries are not normally distributed (p-value: {:.8f}).".format(p_value))