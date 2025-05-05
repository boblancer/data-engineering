import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

def analyze_salary_distribution(csv_file):
    """
    Analyzes and visualizes the salary distribution in the employee dataset.
    
    Args:
        csv_file (str): Path to the CSV file
    """
    # Read the CSV file
    print(f"Reading file: {csv_file}")
    df = pd.read_csv(csv_file)
    
    # Basic statistics on salary
    salary_stats = df['salary'].describe()
    print("\nSalary Statistics:")
    print(salary_stats)
    
    # Additional statistics
    skewness = df['salary'].skew()
    kurtosis = df['salary'].kurtosis()
    print(f"\nSkewness: {skewness:.4f}")
    print(f"Kurtosis: {kurtosis:.4f}")
    
    # Shapiro-Wilk test for normality
    if len(df) > 5000:
        # Sample for the test due to limitations of Shapiro-Wilk
        sample = df['salary'].sample(5000, random_state=42)
        shapiro_test = stats.shapiro(sample)
    else:
        shapiro_test = stats.shapiro(df['salary'])
    
    print(f"Shapiro-Wilk Test: W={shapiro_test[0]:.4f}, p-value={shapiro_test[1]:.8f}")
    print(f"Distribution {'is' if shapiro_test[1] > 0.05 else 'is not'} normal according to Shapiro-Wilk test")
    
    # Setup the figure with multiple plots
    fig = plt.figure(figsize=(15, 12))
    
    # 1. Main histogram focusing on bulk of the data (up to 200k)
    ax1 = fig.add_subplot(2, 2, 1)
    normal_salaries = df[df['salary'] <= 200000]['salary']
    sns.histplot(normal_salaries, bins=30, kde=True, ax=ax1)
    ax1.set_title('Salary Distribution (≤ $200,000)')
    ax1.set_xlabel('Salary')
    ax1.set_ylabel('Frequency')
    
    # 2. Outlier histogram (salaries above 200k)
    ax2 = fig.add_subplot(2, 2, 2)
    outlier_salaries = df[df['salary'] > 200000]['salary']
    if len(outlier_salaries) > 0:
        sns.histplot(outlier_salaries, bins=20, ax=ax2)
        ax2.set_title(f'Outlier Salaries (> $200,000), n={len(outlier_salaries)}')
        ax2.set_xlabel('Salary')
        ax2.set_ylabel('Frequency')
    else:
        ax2.text(0.5, 0.5, "No outliers found", horizontalalignment='center', 
                 verticalalignment='center', transform=ax2.transAxes)
        ax2.set_title('Outlier Salaries (> $200,000)')
    
    # 3. Log-transformed histogram to see distribution pattern better
    ax3 = fig.add_subplot(2, 2, 3)
    if df['salary'].min() > 0:  # Ensure no zero/negative values for log transform
        sns.histplot(np.log10(df['salary']), bins=30, kde=True, ax=ax3)
        ax3.set_title('Log10-transformed Salary Distribution')
        ax3.set_xlabel('Log10(Salary)')
        ax3.set_ylabel('Frequency')
    else:
        ax3.text(0.5, 0.5, "Cannot log-transform non-positive values", 
                 horizontalalignment='center', verticalalignment='center', 
                 transform=ax3.transAxes)
    
    # 4. Q-Q plot to check for normality
    ax4 = fig.add_subplot(2, 2, 4)
    stats.probplot(df['salary'], dist="norm", plot=ax4)
    ax4.set_title('Q-Q Plot (Normal Distribution Check)')
    
    plt.tight_layout()
    plt.savefig('salary_distribution_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\nSummary of findings:")
    
    # Assess normality and distribution shape
    if skewness > 1:
        print("- The salary distribution is highly positively skewed (right-tailed)")
    elif skewness > 0.5:
        print("- The salary distribution is moderately positively skewed")
    elif skewness < -1:
        print("- The salary distribution is highly negatively skewed (left-tailed)")
    elif skewness < -0.5:
        print("- The salary distribution is moderately negatively skewed")
    else:
        print("- The salary distribution is approximately symmetric")
    
    if kurtosis > 3:
        print("- The distribution has heavy tails (leptokurtic)")
    elif kurtosis < -1:
        print("- The distribution has light tails (platykurtic)")
    else:
        print("- The distribution has tail weight similar to a normal distribution (mesokurtic)")
    
    # Calculate percentage in different salary bands
    below_median = (df['salary'] <= df['salary'].median()).mean() * 100
    above_100k = (df['salary'] > 100000).mean() * 100
    above_200k = (df['salary'] > 200000).mean() * 100
    
    print(f"- {below_median:.1f}% of employees earn at or below the median salary (${df['salary'].median():,.0f})")
    print(f"- {above_100k:.1f}% of employees earn more than $100,000")
    print(f"- {above_200k:.1f}% of employees earn more than $200,000")
    
    if shapiro_test[1] < 0.05:
        print("- The salary distribution does NOT follow a normal distribution")
        if df['salary'].min() > 0:
            # Test log-normality if salaries are positive
            log_salaries = np.log10(df['salary'])
            log_shapiro = stats.shapiro(log_salaries if len(log_salaries) <= 5000 
                                     else log_salaries.sample(5000, random_state=42))
            if log_shapiro[1] > 0.05:
                print("- However, the log-transformed salaries appear to be normally distributed")
                print("  (suggesting a log-normal distribution, which is common for salary data)")
    else:
        print("- The salary distribution appears to follow a normal distribution")
    
    print("\nVisualization saved as 'salary_distribution_analysis.png'")
    return salary_stats, shapiro_test

if __name__ == "__main__":
    csv_file = "employees.csv"
    stats, normality_test = analyze_salary_distribution(csv_file)