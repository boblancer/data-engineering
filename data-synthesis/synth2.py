import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

def generate_synthetic_employee_data():
    """
    Generate 10,000 synthetic employees following the specified constraints
    """
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Initialize Faker instances for different locales
    fakers = {
        'USA': Faker('en_US'),
        'India': Faker('en_IN'), 
        'China': Faker('zh_CN'),
        'Mexico': Faker('es_MX'),
        'Canada': Faker('en_CA'),
        'Philippines': Faker('fil_PH'),
        'Taiwan': Faker('zh_TW'),
        'South Korea': Faker('ko_KR')
    }
    
    # Country distributions: 60% USA, others based on 2019 H1B percentages
    country_weights = {
        'USA': 0.60,
        'India': 0.25,      # ~74% of non-USA H1B petitions
        'China': 0.08,      # ~11% of non-USA H1B petitions
        'Mexico': 0.02,     # ~2.5% of non-USA H1B petitions
        'Canada': 0.02,     # ~2.5% of non-USA H1B petitions
        'Philippines': 0.015, # ~1.9% of non-USA H1B petitions
        'Taiwan': 0.01,     # ~1.3% of non-USA H1B petitions
        'South Korea': 0.005 # ~0.6% of non-USA H1B petitions
    }
    
    # Estimated department structure (since spreadsheet not provided)
    departments = {
        'Engineering': 0.35,
        'Sales': 0.15,
        'Marketing': 0.10,
        'Operations': 0.12,
        'Finance': 0.08,
        'Human Resources': 0.05,
        'Customer Support': 0.10,
        'Legal': 0.03,
        'Executive': 0.02
    }
    
    # Role hierarchies with salary ranges (estimated structure)
    role_salary_data = {
        'Engineering': {
            'Software Engineer': {'avg': 110000, 'range': (90000, 140000), 'weight': 0.40},
            'Senior Software Engineer': {'avg': 140000, 'range': (120000, 180000), 'weight': 0.25},
            'Principal Engineer': {'avg': 180000, 'range': (160000, 220000), 'weight': 0.15},
            'Engineering Manager': {'avg': 160000, 'range': (140000, 200000), 'weight': 0.15},
            'VP Engineering': {'avg': 250000, 'range': (200000, 300000), 'weight': 0.05}
        },
        'Sales': {
            'Sales Representative': {'avg': 75000, 'range': (60000, 95000), 'weight': 0.50},
            'Senior Sales Representative': {'avg': 95000, 'range': (80000, 120000), 'weight': 0.25},
            'Sales Manager': {'avg': 130000, 'range': (110000, 160000), 'weight': 0.15},
            'Sales Director': {'avg': 180000, 'range': (150000, 220000), 'weight': 0.08},
            'VP Sales': {'avg': 250000, 'range': (200000, 300000), 'weight': 0.02}
        },
        'Marketing': {
            'Marketing Specialist': {'avg': 65000, 'range': (55000, 80000), 'weight': 0.40},
            'Marketing Manager': {'avg': 90000, 'range': (75000, 110000), 'weight': 0.30},
            'Senior Marketing Manager': {'avg': 120000, 'range': (100000, 145000), 'weight': 0.20},
            'Marketing Director': {'avg': 150000, 'range': (130000, 180000), 'weight': 0.08},
            'VP Marketing': {'avg': 220000, 'range': (180000, 260000), 'weight': 0.02}
        },
        'Operations': {
            'Operations Analyst': {'avg': 70000, 'range': (60000, 85000), 'weight': 0.35},
            'Operations Manager': {'avg': 95000, 'range': (80000, 115000), 'weight': 0.30},
            'Senior Operations Manager': {'avg': 125000, 'range': (105000, 150000), 'weight': 0.20},
            'Operations Director': {'avg': 160000, 'range': (140000, 190000), 'weight': 0.12},
            'VP Operations': {'avg': 200000, 'range': (170000, 240000), 'weight': 0.03}
        },
        'Finance': {
            'Financial Analyst': {'avg': 75000, 'range': (65000, 90000), 'weight': 0.40},
            'Senior Financial Analyst': {'avg': 95000, 'range': (80000, 115000), 'weight': 0.25},
            'Finance Manager': {'avg': 120000, 'range': (100000, 145000), 'weight': 0.20},
            'Finance Director': {'avg': 160000, 'range': (140000, 190000), 'weight': 0.12},
            'CFO': {'avg': 280000, 'range': (230000, 350000), 'weight': 0.03}
        },
        'Human Resources': {
            'HR Specialist': {'avg': 60000, 'range': (50000, 75000), 'weight': 0.40},
            'HR Manager': {'avg': 85000, 'range': (70000, 105000), 'weight': 0.35},
            'Senior HR Manager': {'avg': 110000, 'range': (95000, 130000), 'weight': 0.15},
            'HR Director': {'avg': 140000, 'range': (120000, 170000), 'weight': 0.08},
            'CHRO': {'avg': 220000, 'range': (180000, 270000), 'weight': 0.02}
        },
        'Customer Support': {
            'Support Representative': {'avg': 45000, 'range': (38000, 55000), 'weight': 0.50},
            'Senior Support Representative': {'avg': 60000, 'range': (50000, 72000), 'weight': 0.25},
            'Support Manager': {'avg': 80000, 'range': (65000, 95000), 'weight': 0.20},
            'Support Director': {'avg': 120000, 'range': (100000, 145000), 'weight': 0.05}
        },
        'Legal': {
            'Legal Assistant': {'avg': 65000, 'range': (55000, 78000), 'weight': 0.30},
            'Corporate Counsel': {'avg': 150000, 'range': (130000, 180000), 'weight': 0.40},
            'Senior Counsel': {'avg': 200000, 'range': (170000, 240000), 'weight': 0.20},
            'General Counsel': {'avg': 280000, 'range': (240000, 340000), 'weight': 0.10}
        },
        'Executive': {
            'VP': {'avg': 250000, 'range': (200000, 320000), 'weight': 0.60},
            'SVP': {'avg': 350000, 'range': (280000, 420000), 'weight': 0.25},
            'CEO': {'avg': 500000, 'range': (400000, 700000), 'weight': 0.15}
        }
    }
    
    n_employees = 10000
    employees = []
    used_ids = set()
    used_ssns = set()
    
    # Company started in 2010
    company_start = datetime(2010, 1, 1)
    current_date = datetime.now()
    
    print("Generating 10,000 synthetic employees...")
    
    for i in range(n_employees):
        # Progress indicator
        if (i + 1) % 1000 == 0:
            print(f"Generated {i + 1} employees...")
        
        # Generate unique 9-digit employee ID
        while True:
            employee_id = random.randint(100000000, 999999999)
            if employee_id not in used_ids:
                used_ids.add(employee_id)
                break
        
        # Select country based on weights
        country = np.random.choice(list(country_weights.keys()), p=list(country_weights.values()))
        faker = fakers[country]
        
        # Generate gender (49% female, 49% male, 2% nonbinary)
        gender = np.random.choice(['female', 'male', 'nonbinary'], p=[0.49, 0.49, 0.02])
        
        # Generate name based on gender and country
        if gender == 'female':
            first_name = faker.first_name_female()
        elif gender == 'male':
            first_name = faker.first_name_male()
        else:  # nonbinary
            first_name = faker.first_name()
        
        name = f"{first_name} {faker.last_name()}"
        
        # Generate phone (US format) and email
        phone = fakers['USA'].phone_number()
        email = fakers['USA'].email()
        
        # Generate birthdate (age 20-65)
        min_birth = (current_date - timedelta(days=65*365)).date()
        max_birth = (current_date - timedelta(days=20*365)).date()
        birthdate = faker.date_between(start_date=min_birth, end_date=max_birth)
        
        # Generate hire date (after age 20, after company start)
        earliest_hire_datetime = datetime.combine(birthdate, datetime.min.time()) + timedelta(days=20*365)
        earliest_hire = max(company_start, earliest_hire_datetime).date()
        hiredate = faker.date_between(start_date=earliest_hire, end_date=current_date.date())
        
        # Select department and role
        department = np.random.choice(list(departments.keys()), p=list(departments.values()))
        dept_roles = role_salary_data[department]
        roles = list(dept_roles.keys())
        role_weights = [dept_roles[role]['weight'] for role in roles]
        role = np.random.choice(roles, p=role_weights)
        
        # Generate salary based on role
        salary_info = dept_roles[role]
        salary = random.randint(salary_info['range'][0], salary_info['range'][1])
        
        # Generate unique SSN
        while True:
            ssn = fakers['USA'].ssn()
            if ssn not in used_ssns:
                used_ssns.add(ssn)
                break
        
        employee = {
            'employeeID': employee_id,
            'CountryOfBirth': country,
            'name': name,
            'phone': phone,
            'email': email,
            'gender': gender,
            'birthdate': birthdate,
            'hiredate': hiredate,
            'department': department,
            'role': role,
            'salary': salary,
            'SSID': ssn
        }
        
        employees.append(employee)
    
    return pd.DataFrame(employees)

# Generate the dataset
emp_df = generate_synthetic_employee_data()

print("\n" + "="*50)
print("DATASET GENERATION COMPLETE")
print("="*50)

# 1. Show emp_df.describe(include='all')
print("\n1. emp_df.describe(include='all'):")
print("-" * 40)
print(emp_df.describe(include='all'))

# 2. Show emp_df.head(10)
print("\n2. emp_df.head(10):")
print("-" * 40)
print(emp_df.head(10))

# 3. Calculate total yearly payroll
total_payroll = emp_df['salary'].sum()
print(f"\n3. Total Yearly Payroll:")
print("-" * 40)
print(f"${total_payroll:,}")
print(f"${total_payroll/1000000:.1f} million")

# Additional statistics
print(f"\nAdditional Statistics:")
print("-" * 40)
print(f"Average salary: ${emp_df['salary'].mean():,.0f}")
print(f"Median salary: ${emp_df['salary'].median():,.0f}")
print(f"Salary range: ${emp_df['salary'].min():,} - ${emp_df['salary'].max():,}")

print(f"\nCountry distribution:")
print(emp_df['CountryOfBirth'].value_counts(normalize=True).sort_values(ascending=False))

print(f"\nGender distribution:")
print(emp_df['gender'].value_counts(normalize=True))

print(f"\nDepartment distribution:")
print(emp_df['department'].value_counts(normalize=True).sort_values(ascending=False))