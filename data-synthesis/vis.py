import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from synth2 import generate_synthetic_employee_data
import numpy as np

def load_or_generate_data():
    """
    Load data from CSV if exists, otherwise generate new data
    """
    try:
        print("Loading existing employee data...")
        emp_df = pd.read_csv('employee_data.csv')
        # Convert date columns back to datetime
        emp_df['birthdate'] = pd.to_datetime(emp_df['birthdate'])
        emp_df['hiredate'] = pd.to_datetime(emp_df['hiredate'])
        print(f"Loaded {len(emp_df)} employees from CSV")
        return emp_df
    except FileNotFoundError:
        print("CSV not found. Generating new data...")
        emp_df = generate_synthetic_employee_data()
        emp_df.to_csv('employee_data.csv', index=False)
        print("Data saved to employee_data.csv")
        return emp_df

def viz1_country_births(emp_df):
    """
    1. Bar chart displaying counts of each CountryOfBirth 
    Order the bars from most frequent country to least frequent
    """
    plt.figure(figsize=(12, 8))
    country_counts = emp_df['CountryOfBirth'].value_counts()
    
    bars = plt.bar(range(len(country_counts)), country_counts.values, 
                   color='steelblue', edgecolor='navy', linewidth=0.5)
    
    plt.title('Employee Counts by Country of Birth', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Country of Birth', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Employees', fontsize=14, fontweight='bold')
    plt.xticks(range(len(country_counts)), country_counts.index, rotation=45, ha='right')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 50,
                f'{int(height):,}', ha='center', va='bottom', fontweight='bold')
    
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()

def viz2_department_counts(emp_df):
    """
    2. Bar chart displaying employee counts for each Department
    Order the bars from largest department to smallest
    """
    plt.figure(figsize=(12, 8))
    dept_counts = emp_df['department'].value_counts()
    
    bars = plt.bar(range(len(dept_counts)), dept_counts.values, 
                   color='forestgreen', edgecolor='darkgreen', linewidth=0.5)
    
    plt.title('Employee Counts by Department', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Department', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Employees', fontsize=14, fontweight='bold')
    plt.xticks(range(len(dept_counts)), dept_counts.index, rotation=45, ha='right')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 20,
                f'{int(height):,}', ha='center', va='bottom', fontweight='bold')
    
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()

def viz3_hire_day_of_week(emp_df):
    """
    3. Bar chart with X axis of "day of the week" showing all seven days of the week
    Y axis represents the number of employees hired on each day of the week
    """
    plt.figure(figsize=(10, 6))
    
    # Convert hiredate to datetime if it's not already
    emp_df['hiredate'] = pd.to_datetime(emp_df['hiredate'])
    emp_df['hire_day_of_week'] = emp_df['hiredate'].dt.day_name()
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = emp_df['hire_day_of_week'].value_counts().reindex(day_order, fill_value=0)
    
    bars = plt.bar(day_order, day_counts.values, 
                   color='orange', edgecolor='darkorange', linewidth=0.5)
    
    plt.title('Employee Hires by Day of Week', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Day of Week', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Employees Hired', fontsize=14, fontweight='bold')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 10,
                f'{int(height):,}', ha='center', va='bottom', fontweight='bold')
    
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()

def viz4_salary_kde(emp_df):
    """
    4. A KDE plot of salaries
    """
    plt.figure(figsize=(12, 6))
    
    sns.kdeplot(data=emp_df['salary'], fill=True, color='purple', alpha=0.7, linewidth=2)
    
    plt.title('Salary Distribution (KDE)', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Annual Salary ($)', fontsize=14, fontweight='bold')
    plt.ylabel('Density', fontsize=14, fontweight='bold')
    
    # Format x-axis to show currency
    ax = plt.gca()
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # Add statistics text box
    mean_salary = emp_df['salary'].mean()
    median_salary = emp_df['salary'].median()
    textstr = f'Mean: ${mean_salary:,.0f}\nMedian: ${median_salary:,.0f}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(0.75, 0.95, textstr, transform=ax.transAxes, fontsize=12,
             verticalalignment='top', bbox=props)
    
    plt.grid(alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()

def viz5_birthdates_over_time(emp_df):
    """
    5. Line plot showing number of birthdates over time
    X axis shows the years from earliest birth year to most recent
    Y axis represents the number of employees born in each year
    """
    plt.figure(figsize=(14, 6))
    
    # Convert birthdate to datetime if it's not already
    emp_df['birthdate'] = pd.to_datetime(emp_df['birthdate'])
    emp_df['birth_year'] = emp_df['birthdate'].dt.year
    
    birth_year_counts = emp_df['birth_year'].value_counts().sort_index()
    
    plt.plot(birth_year_counts.index, birth_year_counts.values, 
             marker='o', linewidth=3, markersize=6, color='red', 
             markerfacecolor='darkred', markeredgecolor='white', markeredgewidth=1)
    
    plt.title('Employee Birth Years Over Time', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Birth Year', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Employees Born', fontsize=14, fontweight='bold')
    
    # Set reasonable axis limits
    plt.xlim(birth_year_counts.index.min() - 1, birth_year_counts.index.max() + 1)
    plt.ylim(0, birth_year_counts.values.max() * 1.1)
    
    plt.grid(alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()

def viz6_salary_kde_by_department(emp_df):
    """
    6. Single diagram with KDE plots of salaries for each Department
    """
    plt.figure(figsize=(16, 8))
    
    # Get unique departments
    departments = emp_df['department'].unique()
    
    # Create color palette
    colors = sns.color_palette("husl", len(departments))
    
    for i, dept in enumerate(departments):
        dept_salaries = emp_df[emp_df['department'] == dept]['salary']
        sns.kdeplot(data=dept_salaries, label=dept, alpha=0.7, linewidth=2, color=colors[i])
    
    plt.title('Salary Distribution by Department (KDE)', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Annual Salary ($)', fontsize=14, fontweight='bold')
    plt.ylabel('Density', fontsize=14, fontweight='bold')
    
    # Format x-axis to show currency
    ax = plt.gca()
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    plt.legend(title='Department', bbox_to_anchor=(1.05, 1), loc='upper left', 
               title_fontsize=12, fontsize=10)
    plt.grid(alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()

def create_all_visualizations():
    """
    Create all 6 visualizations
    """
    # Load data
    emp_df = load_or_generate_data()
    
    print("\n" + "="*60)
    print("CREATING VISUALIZATIONS")
    print("="*60)
    
    print("\nVisualization 1: Country of Birth Counts")
    viz1_country_births(emp_df)
    
    print("\nVisualization 2: Department Counts")
    viz2_department_counts(emp_df)
    
    print("\nVisualization 3: Hires by Day of Week")
    viz3_hire_day_of_week(emp_df)
    
    print("\nVisualization 4: Salary Distribution (KDE)")
    viz4_salary_kde(emp_df)
    
    print("\nVisualization 5: Birth Years Over Time")
    viz5_birthdates_over_time(emp_df)
    
    print("\nVisualization 6: Salary KDE by Department")
    viz6_salary_kde_by_department(emp_df)
    
    print("\nAll visualizations complete!")

if __name__ == "__main__":
    create_all_visualizations()