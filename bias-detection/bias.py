import pandas as pd
from datetime import datetime, timedelta
import re
from scipy.stats import binomtest, ttest_1samp, chi2_contingency

def process_trimet_data(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    stop_events = []
    trip_sections = re.split(r'<h2>Stop events for PDX_TRIP\s+([^<]+)</h2>', html_content)
    
    for i in range(1, len(trip_sections), 2):
        trip_id = trip_sections[i].strip()
        table_content = trip_sections[i + 1] if i + 1 < len(trip_sections) else ""
        
        row_pattern = r'<tr><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td></tr>'
        
        matches = re.findall(row_pattern, table_content)
        
        for match in matches:
            try:
                vehicle_number = int(match[0])
                arrive_time = int(match[8])
                location_id = int(match[10])
                ons = int(match[13])
                offs = int(match[14])
                
                base_date = datetime(2022, 12, 7)
                tstamp = base_date + timedelta(seconds=arrive_time)
                
                stop_events.append({
                    'trip_id': trip_id,
                    'vehicle_number': vehicle_number,
                    'tstamp': tstamp,
                    'location_id': location_id,
                    'ons': ons,
                    'offs': offs
                })
            except (ValueError, IndexError):
                continue
    
    return pd.DataFrame(stop_events)

def basic_analysis(stops_df):
    print("Basic Analysis")
    print("Total events:", len(stops_df))
    print()
    
    # Question 1
    vehicles = stops_df['vehicle_number'].nunique()
    print("1. Vehicles in data:", vehicles)
    
    # Question 2  
    locations = stops_df['location_id'].nunique()
    print("2. Unique locations:", locations)
    
    # Question 3
    min_time = stops_df['tstamp'].min()
    max_time = stops_df['tstamp'].max()
    print("3. Time range:")
    print("   Min:", min_time)
    print("   Max:", max_time)
    
    # Question 4
    boarding_events = (stops_df['ons'] >= 1).sum()
    print("4. Events with boarding:", boarding_events)
    
    # Question 5
    boarding_pct = (boarding_events / len(stops_df)) * 100
    print("5. Boarding percentage:", f"{boarding_pct:.1f}%")
    print()

def validate_cases(stops_df):
    print("Validation")
    
    # Location 6913
    loc_6913 = stops_df[stops_df['location_id'] == 6913]
    print("Location 6913:")
    if len(loc_6913) == 0:
        print("  Not found in data")
        print("  Available locations:", sorted(stops_df['location_id'].unique())[:5], "...")
    else:
        print("  Stops at location:", len(loc_6913))
        print("  Different buses:", loc_6913['vehicle_number'].nunique())
        boarding_at_loc = (loc_6913['ons'] >= 1).sum()
        boarding_pct_loc = (boarding_at_loc / len(loc_6913)) * 100
        print("  Boarding percentage:", f"{boarding_pct_loc:.1f}%")
    print()
    
    # Vehicle 4062
    veh_4062 = stops_df[stops_df['vehicle_number'] == 4062]
    print("Vehicle 4062:")
    if len(veh_4062) == 0:
        print("  Not found in data")
        print("  Available vehicles:", sorted(stops_df['vehicle_number'].unique())[:5], "...")
    else:
        print("  Total stops:", len(veh_4062))
        print("  Total boarded:", veh_4062['ons'].sum())
        print("  Total alighted:", veh_4062['offs'].sum())
        boarding_veh = (veh_4062['ons'] >= 1).sum()
        boarding_pct_veh = (boarding_veh / len(veh_4062)) * 100
        print("  Boarding percentage:", f"{boarding_pct_veh:.1f}%")

def find_biased_vehicles(stops_df):
    print("Bias Detection Analysis")
    print()
    
    # Calculate overall system boarding proportion
    total_events = len(stops_df)
    total_boarding_events = (stops_df['ons'] >= 1).sum()
    system_boarding_rate = total_boarding_events / total_events
    
    print(f"System-wide boarding rate: {system_boarding_rate:.3f} ({total_boarding_events}/{total_events})")
    print()
    
    # Analyze each vehicle
    vehicle_results = []
    
    for vehicle_id in sorted(stops_df['vehicle_number'].unique()):
        vehicle_data = stops_df[stops_df['vehicle_number'] == vehicle_id]
        
        # Count stop events for this vehicle
        n_stops = len(vehicle_data)
        
        # Count stops with boardings
        boarding_stops = (vehicle_data['ons'] >= 1).sum()
        
        # Calculate vehicle boarding percentage
        vehicle_boarding_rate = boarding_stops / n_stops
        
        # Perform binomial test
        # H0: vehicle boarding rate = system boarding rate
        # H1: vehicle boarding rate != system boarding rate
        test_result = binomtest(boarding_stops, n_stops, system_boarding_rate, alternative='two-sided')
        p_value = test_result.pvalue
        
        vehicle_results.append({
            'vehicle_id': vehicle_id,
            'total_stops': n_stops,
            'boarding_stops': boarding_stops,
            'boarding_rate': vehicle_boarding_rate,
            'p_value': p_value
        })
    
    # Create results dataframe
    results_df = pd.DataFrame(vehicle_results)
    
    print("Vehicle Analysis Results:")
    print("Vehicle  Stops  Boarding_Stops  Rate    P_Value")
    for _, row in results_df.iterrows():
        print(f"{row['vehicle_id']:<8} {row['total_stops']:<6} {row['boarding_stops']:<14} {row['boarding_rate']:.3f}   {row['p_value']:.4f}")
    print()
    
    # Find vehicles with significant bias (p < 0.05)
    biased_vehicles = results_df[results_df['p_value'] < 0.05]
    
    print("Vehicles with significant bias (p < 0.05):")
    if len(biased_vehicles) == 0:
        print("None found")
    else:
        print("Vehicle_ID  P_Value")
        for _, row in biased_vehicles.iterrows():
            print(f"{row['vehicle_id']:<10}  {row['p_value']:.4f}")
    print()
    
    return results_df

def process_gps_data(csv_file_path):
    """Process GPS relative position data from CSV file"""
    try:
        # Read the CSV file
        gps_df = pd.read_csv(csv_file_path)
        
        # Convert timestamp to datetime if needed
        gps_df['TIMESTAMP'] = pd.to_datetime(gps_df['TIMESTAMP'])
        
        print(f"GPS data loaded: {len(gps_df)} records")
        print("Columns:", list(gps_df.columns))
        print("Sample data:")
        print(gps_df.head())
        print()
        
        return gps_df
    except FileNotFoundError:
        print("GPS CSV file not found. Skipping GPS bias analysis.")
        return None
    except Exception as e:
        print(f"Error loading GPS data: {e}")
        return None

def find_offs_ons_biased_vehicles(stops_df):
    """Find vehicles with biased offs/ons ratios using chi-square test"""
    print("Offs/Ons Ratio Bias Detection Analysis")
    print()
    
    # 1. Calculate system-wide totals
    total_offs = stops_df['offs'].sum()
    total_ons = stops_df['ons'].sum()
    system_total = total_offs + total_ons
    
    # System proportions
    system_offs_prop = total_offs / system_total
    system_ons_prop = total_ons / system_total
    
    print(f"System-wide statistics:")
    print(f"  Total offs: {total_offs}")
    print(f"  Total ons:  {total_ons}")
    print(f"  Total:      {system_total}")
    print(f"  Offs proportion: {system_offs_prop:.4f}")
    print(f"  Ons proportion:  {system_ons_prop:.4f}")
    print()
    
    # 2. Analyze each vehicle
    vehicle_ratio_results = []
    
    for vehicle_id in sorted(stops_df['vehicle_number'].unique()):
        vehicle_data = stops_df[stops_df['vehicle_number'] == vehicle_id]
        
        # Calculate vehicle totals
        vehicle_offs = vehicle_data['offs'].sum()
        vehicle_ons = vehicle_data['ons'].sum()
        vehicle_total = vehicle_offs + vehicle_ons
        
        # Skip vehicles with no passenger activity
        if vehicle_total == 0:
            continue
        
        # Expected values based on system proportions
        expected_offs = vehicle_total * system_offs_prop
        expected_ons = vehicle_total * system_ons_prop
        
        # Create contingency table for chi-square test
        # Format: [[observed_offs, observed_ons], [expected_offs, expected_ons]]
        observed = [vehicle_offs, vehicle_ons]
        expected = [expected_offs, expected_ons]
        
        # Chi-square test using scipy
        contingency_table = [
            [vehicle_offs, vehicle_ons],
            [total_offs - vehicle_offs, total_ons - vehicle_ons]
        ]
        
        try:
            chi2_stat, p_value, dof, expected_freq = chi2_contingency(contingency_table)
        except:
            # Fallback for cases with insufficient data
            continue
        
        # Calculate vehicle proportions
        vehicle_offs_prop = vehicle_offs / vehicle_total if vehicle_total > 0 else 0
        vehicle_ons_prop = vehicle_ons / vehicle_total if vehicle_total > 0 else 0
        
        vehicle_ratio_results.append({
            'vehicle_id': vehicle_id,
            'vehicle_offs': vehicle_offs,
            'vehicle_ons': vehicle_ons,
            'vehicle_total': vehicle_total,
            'offs_proportion': vehicle_offs_prop,
            'ons_proportion': vehicle_ons_prop,
            'chi2_statistic': chi2_stat,
            'p_value': p_value
        })
    
    # Create results dataframe
    ratio_results_df = pd.DataFrame(vehicle_ratio_results)
    
    print("Vehicle Offs/Ons Analysis Results:")
    print("Vehicle  Offs   Ons    Total  Offs_Prop  Ons_Prop   Chi2_Stat  P_Value")
    for _, row in ratio_results_df.iterrows():
        print(f"{row['vehicle_id']:<8} {row['vehicle_offs']:<6} {row['vehicle_ons']:<6} {row['vehicle_total']:<6} {row['offs_proportion']:.3f}      {row['ons_proportion']:.3f}      {row['chi2_statistic']:.3f}      {row['p_value']:.6f}")
    print()
    
    # Find vehicles with significant offs/ons bias (p < 0.05)
    ratio_biased_vehicles = ratio_results_df[ratio_results_df['p_value'] < 0.05]
    
    print("Vehicles with significant offs/ons bias (p < 0.05):")
    if len(ratio_biased_vehicles) == 0:
        print("None found")
    else:
        print("Vehicle_ID  P_Value     Offs_Prop  Ons_Prop")
        print("-" * 40)
        for _, row in ratio_biased_vehicles.iterrows():
            print(f"{row['vehicle_id']:<10}  {row['p_value']:.6f}  {row['offs_proportion']:.3f}      {row['ons_proportion']:.3f}")
    print()
    
    print(f"Total vehicles with significant offs/ons bias: {len(ratio_biased_vehicles)}")
    
    return ratio_results_df

def find_gps_biased_vehicles(gps_df):
    """Find vehicles with biased GPS data using t-test"""
    if gps_df is None:
        print("No GPS data available for analysis")
        return
    
    print("GPS Bias Detection Analysis")
    print()
    
    # 1. Get all RELPOS values for the entire dataset
    all_relpos = gps_df['RELPOS'].values
    overall_mean = all_relpos.mean()
    
    print(f"Overall RELPOS statistics:")
    print(f"  Mean: {overall_mean:.6f}")
    print(f"  Std:  {all_relpos.std():.6f}")
    print(f"  Min:  {all_relpos.min():.6f}")
    print(f"  Max:  {all_relpos.max():.6f}")
    print(f"  Total measurements: {len(all_relpos)}")
    print()
    
    # 2. Analyze each vehicle
    vehicle_gps_results = []
    
    for vehicle_id in sorted(gps_df['VEHICLE_NUMBER'].unique()):
        vehicle_gps = gps_df[gps_df['VEHICLE_NUMBER'] == vehicle_id]
        vehicle_relpos = vehicle_gps['RELPOS'].values
        
        if len(vehicle_relpos) < 2:  # Need at least 2 values for t-test
            continue
            
        # Calculate vehicle statistics
        vehicle_mean = vehicle_relpos.mean()
        vehicle_std = vehicle_relpos.std()
        n_measurements = len(vehicle_relpos)
        
        # Perform one-sample t-test
        # H0: vehicle mean = overall mean (no bias)
        # H1: vehicle mean != overall mean (bias exists)
        t_stat, p_value = ttest_1samp(vehicle_relpos, overall_mean)
        
        vehicle_gps_results.append({
            'vehicle_id': vehicle_id,
            'n_measurements': n_measurements,
            'vehicle_mean': vehicle_mean,
            'vehicle_std': vehicle_std,
            't_statistic': t_stat,
            'p_value': p_value
        })
    
    # Create results dataframe
    gps_results_df = pd.DataFrame(vehicle_gps_results)
    
    print("GPS Vehicle Analysis Results:")
    print("Vehicle  Measurements  Mean_RELPOS  Std_RELPOS   T_Stat   P_Value")
    for _, row in gps_results_df.iterrows():
        print(f"{row['vehicle_id']:<8} {row['n_measurements']:<12} {row['vehicle_mean']:<11.4f} {row['vehicle_std']:<11.4f} {row['t_statistic']:<8.3f} {row['p_value']:.6f}")
    print()
    
    # Find vehicles with significant GPS bias (p < 0.005)
    gps_biased_vehicles = gps_results_df[gps_results_df['p_value'] < 0.005]
    
    print("Vehicles with significant GPS bias (p < 0.005):")
    if len(gps_biased_vehicles) == 0:
        print("None found")
    else:
        print("Vehicle_ID  P_Value     Mean_RELPOS")
        print("-" * 35)
        for _, row in gps_biased_vehicles.iterrows():
            print(f"{row['vehicle_id']:<10}  {row['p_value']:.6f}  {row['vehicle_mean']:.6f}")
    print()
    
    print(f"Total vehicles with significant GPS bias: {len(gps_biased_vehicles)}")
    print()
    
    return gps_results_df

def show_sample(stops_df):
    print("Sample data:")
    print(stops_df.head())
    print()
    print("Random sample:")
    print(stops_df.sample(3))
    print()

if __name__ == "__main__":
    stops_df = process_trimet_data('trimet_stopevents_2022-12-07.html')
    
    show_sample(stops_df)
    basic_analysis(stops_df)
    validate_cases(stops_df)
    
    # Bias detection analysis
    bias_results = find_biased_vehicles(stops_df)
    
    # Offs/Ons ratio bias detection
    ratio_bias_results = find_offs_ons_biased_vehicles(stops_df)
    
    # GPS bias detection analysis
    gps_df = process_gps_data('trimet_gps_data.csv')  # Adjust filename as needed
    if gps_df is not None:
        gps_bias_results = find_gps_biased_vehicles(gps_df)