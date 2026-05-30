import pandas as pd
import argparse
import os
from shared_utils.erlang_c import ErlangCCalculator

def process_pipeline(input_path, output_path):
    print("\n🚀 Starting WFM Batch Forecasting Pipeline...")
    print(f"📥 Ingesting data from: {input_path}")

    if not os.path.exists(input_path):
        print(f"❌ Error: Input file '{input_path}' not found.")
        return

    # Load data
    df = pd.read_csv(input_path)
    required_cols = ['interval', 'volume', 'aht']
    if not all(col in df.columns for col in required_cols):
        print(f"❌ Error: CSV must contain exactly these columns: {required_cols}")
        return

    print("⚙️ Processing Erlang C calculations via central engine...")
    results = []
    
    for _, row in df.iterrows():
        vol = row['volume']
        aht = row['aht']
        
        # Central Engine Call: Volume, AHT, 30m interval, 80% SL, 20s target
        res = ErlangCCalculator.required_agents(vol, aht, 30, 80, 20)

        # Standard 30% shrinkage buffer for FTE calculation
        base_agents = res['required_agents']
        fte_with_shrinkage = round(base_agents / (1 - 0.30), 1) if base_agents > 0 else 0

        results.append({
            'Interval': row['interval'],
            'Volume': vol,
            'AHT (sec)': aht,
            'Base Agents Required': base_agents,
            'Achieved SL %': res['achieved_sl'],
            'FTE Required (w/ 30% Shrinkage)': fte_with_shrinkage
        })

    out_df = pd.DataFrame(results)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"💾 Saving schedule to: {output_path}")
    out_df.to_excel(output_path, index=False, engine='openpyxl')
    print("✅ Pipeline Complete!\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WFM Batch Forecasting Pipeline")
    parser.add_argument("--input", default="data/sample_intervals.csv", help="Path to input CSV")
    parser.add_argument("--output", default="output/fte_schedule.xlsx", help="Path to output Excel")
    args = parser.parse_args()

    process_pipeline(args.input, args.output)
