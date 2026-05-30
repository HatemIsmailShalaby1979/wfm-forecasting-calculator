import pandas as pd
import argparse
import os

def run_variance(forecast_path, actuals_path, output_path):
    print("\n🔍 Starting WFM Variance Engine...")
    
    if not os.path.exists(forecast_path):
        print(f"❌ Error: Forecast file '{forecast_path}' not found.")
        return
    if not os.path.exists(actuals_path):
        print(f"❌ Error: Actuals file '{actuals_path}' not found.")
        return

    print(f"📊 Loading Forecast: {forecast_path}")
    df_forecast = pd.read_excel(forecast_path)
    
    print(f"📈 Loading Actuals: {actuals_path}")
    df_actuals = pd.read_csv(actuals_path)

    print("⚙️ Calculating Variances...")
    # Merge on the interval string
    df_merged = pd.merge(df_forecast, df_actuals, left_on='Interval', right_on='interval', how='inner')
    
    # Calculate Deltas
    df_merged['Volume Variance'] = df_merged['Actual Volume'] - df_merged['Volume']
    df_merged['Volume Var %'] = (df_merged['Volume Variance'] / df_merged['Volume']).round(4)
    
    df_merged['AHT Variance (sec)'] = df_merged['Actual AHT'] - df_merged['AHT (sec)']
    df_merged['SLA Variance %'] = (df_merged['Actual SLA %'] - df_merged['Achieved SL %']).round(2)

    # Order the columns logically for a WFM report
    cols = [
        'Interval', 
        'Volume', 'Actual Volume', 'Volume Variance', 'Volume Var %',
        'AHT (sec)', 'Actual AHT', 'AHT Variance (sec)',
        'Achieved SL %', 'Actual SLA %', 'SLA Variance %'
    ]
    
    df_report = df_merged[cols].copy()
    
    # Format percentages for Excel readability
    df_report['Volume Var %'] = df_report['Volume Var %'].apply(lambda x: f"{x:.2%}")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"💾 Saving Variance Report to: {output_path}")
    
    df_report.to_excel(output_path, index=False, engine='openpyxl')
    print("✅ Variance Analysis Complete!\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WFM Forecast Variance Engine")
    parser.add_argument("--forecast", default="output/fte_schedule.xlsx", help="Path to forecast output")
    parser.add_argument("--actuals", default="data/actuals.csv", help="Path to actuals CSV")
    parser.add_argument("--output", default="output/variance_report.xlsx", help="Path to output report")
    args = parser.parse_args()

    run_variance(args.forecast, args.actuals, args.output)
