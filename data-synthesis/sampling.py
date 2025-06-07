import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from synth2 import generate_synthetic_employee_data

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

def analyze_salary_distribution(emp_df):
    """
    Analyze the original salary distribution to help choose noise parameters
    """
    print("\n" + "="*60)
    print("ORIGINAL SALARY DISTRIBUTION ANALYSIS")
    print("="*60)
    
    salary_stats = emp_df['salary'].describe()
    print("\nOriginal Salary Statistics:")
    print(f"Mean: ${salary_stats['mean']:,.0f}")
    print(f"Std Dev: ${salary_stats['std']:,.0f}")
    print(f"Min: ${salary_stats['min']:,.0f}")
    print(f"Max: ${salary_stats['max']:,.0f}")
    print(f"Range: ${salary_stats['max'] - salary_stats['min']:,.0f}")
    
    # Calculate coefficient of variation
    cv = salary_stats['std'] / salary_stats['mean']
    print(f"Coefficient of Variation: {cv:.3f} ({cv*100:.1f}%)")
    
    return salary_stats

def choose_noise_parameters(emp_df):
    salary_stats = emp_df['salary'].describe()
    mean_salary = salary_stats['mean']
    recommended_std = mean_salary * 0.05  # 5% of mean salary
    return recommended_std

def create_perturbed_dataframe(emp_df, noise_std=None):
    """
    Create perturbed DataFrame with Gaussian noise added to salaries
    """
    if noise_std is None:
        # Use 5% of mean salary as default
        noise_std = emp_df['salary'].mean() * 0.05
    
    print(f"\nCreating perturbed DataFrame with noise std dev: ${noise_std:,.0f}")
    
    # Create a copy of the original DataFrame
    prtrb_df = emp_df.copy()
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate Gaussian noise
    noise = np.random.normal(loc=0, scale=noise_std, size=len(emp_df))
    
    # Add noise to salaries
    prtrb_df['salary'] = emp_df['salary'] + noise
    
    # Ensure salaries remain positive (optional constraint)
    prtrb_df['salary'] = np.maximum(prtrb_df['salary'], 1000)  # Minimum $1,000 salary
    
    # Round to nearest dollar
    prtrb_df['salary'] = prtrb_df['salary'].round().astype(int)
    
    return prtrb_df, noise_std

def analyze_perturbation_effects(emp_df, prtrb_df, noise_std):
    """
    Analyze the effects of perturbation on the data
    """
    print("\n" + "="*60)
    print("PERTURBATION EFFECTS ANALYSIS")
    print("="*60)
    
    # Calculate differences
    salary_diff = prtrb_df['salary'] - emp_df['salary']
    
    print(f"\nNoise Statistics:")
    print(f"Applied noise std dev: ${noise_std:,.0f}")
    print(f"Actual noise std dev: ${salary_diff.std():,.0f}")
    print(f"Mean noise (should be ~0): ${salary_diff.mean():,.0f}")
    print(f"Max positive change: ${salary_diff.max():,.0f}")
    print(f"Max negative change: ${salary_diff.min():,.0f}")
    
    print(f"\nSalary Distribution Comparison:")
    original_stats = emp_df['salary'].describe()
    perturbed_stats = prtrb_df['salary'].describe()
    
    comparison_df = pd.DataFrame({
        'Original': original_stats,
        'Perturbed': perturbed_stats,
        'Change': perturbed_stats - original_stats,
        'Change %': ((perturbed_stats - original_stats) / original_stats * 100).round(2)
    })
    
    print(comparison_df)
    
    # Calculate correlation between original and perturbed salaries
    correlation = emp_df['salary'].corr(prtrb_df['salary'])
    print(f"\nCorrelation between original and perturbed salaries: {correlation:.4f}")
    
    # Privacy-utility tradeoff metrics
    print(f"\nPrivacy-Utility Metrics:")
    relative_error = abs(salary_diff).mean() / emp_df['salary'].mean()
    print(f"Mean Absolute Relative Error: {relative_error:.4f} ({relative_error*100:.2f}%)")
    
    signal_to_noise = emp_df['salary'].std() / noise_std
    print(f"Signal-to-Noise Ratio: {signal_to_noise:.2f}")

def visualize_perturbation(emp_df, prtrb_df):
    """
    Create visualizations to show the effect of perturbation
    """
    plt.figure(figsize=(15, 5))
    
    # Plot 1: Original vs Perturbed scatter plot
    plt.subplot(1, 3, 1)
    plt.scatter(emp_df['salary'], prtrb_df['salary'], alpha=0.5, s=1)
    plt.plot([emp_df['salary'].min(), emp_df['salary'].max()], 
             [emp_df['salary'].min(), emp_df['salary'].max()], 'r--', linewidth=2)
    plt.xlabel('Original Salary')
    plt.ylabel('Perturbed Salary')
    plt.title('Original vs Perturbed Salaries')
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Distribution comparison
    plt.subplot(1, 3, 2)
    plt.hist(emp_df['salary'], bins=50, alpha=0.7, label='Original', density=True)
    plt.hist(prtrb_df['salary'], bins=50, alpha=0.7, label='Perturbed', density=True)
    plt.xlabel('Salary')
    plt.ylabel('Density')
    plt.title('Salary Distribution Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Noise distribution
    plt.subplot(1, 3, 3)
    noise = prtrb_df['salary'] - emp_df['salary']
    plt.hist(noise, bins=50, alpha=0.7, color='green')
    plt.axvline(0, color='red', linestyle='--', linewidth=2)
    plt.xlabel('Added Noise (Salary Change)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Added Noise')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def main():
    """
    Main function to demonstrate salary perturbation
    """
    # Load the employee data
    emp_df = load_or_generate_data()
    
    # Analyze original salary distribution
    analyze_salary_distribution(emp_df)
    
    # Demonstrate how to choose noise parameters
    recommended_std = choose_noise_parameters(emp_df)
    
    # Create perturbed DataFrame
    print("\n" + "="*60)
    print("CREATING PERTURBED DATAFRAME")
    print("="*60)
    
    prtrb_df, noise_std = create_perturbed_dataframe(emp_df, recommended_std)
    
    # Analyze perturbation effects
    analyze_perturbation_effects(emp_df, prtrb_df, noise_std)
    
    # Show required outputs
    print("\n" + "="*60)
    print("REQUIRED OUTPUTS")
    print("="*60)
    
    print("\n2. prtrb_df.describe(include='all'):")
    print("-" * 50)
    print(prtrb_df.describe(include='all'))
    
    print("\n3. prtrb_df.head(10):")
    print("-" * 50)
    print(prtrb_df.head(10))
    
    # Save perturbed data
    prtrb_df.to_csv('perturbed_employee_data.csv', index=False)
    print(f"\nPerturbed data saved to 'perturbed_employee_data.csv'")
    
    # Create visualizations
    print("\nCreating visualizations...")
    visualize_perturbation(emp_df, prtrb_df)
    
    return prtrb_df

if __name__ == "__main__":
    prtrb_df = main()