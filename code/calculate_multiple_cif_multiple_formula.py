import sys
import os
import glob
import argparse
import pandas as pd
from distance_mul import main as run_analysis

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True)
parser.add_argument("--gt_dir", type=str, required=True)
parser.add_argument("--pred_base_dir", type=str, required=True)
# parser.add_argument("--output_csv", type=str, required=True)
args = parser.parse_args()
model_name = args.model

if not os.path.exists("../results"):
    os.mkdir("../results")

if os.path.exists(f"../results/distance_table_{args.model}.csv"):
    os.remove(f"../results/distance_table_{args.model}.csv")
# 1. Get all subdirectories in the prediction base path
# Each subdirectory is a formula (e.g., Ba2BiSbO6)
formula_folders = [f.name for f in os.scandir(args.pred_base_dir) if f.is_dir()]

if not formula_folders:
    print(f"!!! ERROR: No subfolders found in: {args.pred_base_dir}")
    sys.exit(1)

print(f"Found {len(formula_folders)} formulas to process for model: {args.model}")

# Ensure results directory exists
# os.makedirs(os.path.dirname(args.output_csv), exist_ok=True)

for formula in formula_folders:
    groundtruth_cif = os.path.join(args.gt_dir, f'{formula}.cif')
    
    # Check if ground truth exists for this formula before starting
    if not os.path.exists(groundtruth_cif):
        print(f"Skipping {formula}: Ground truth file not found at {groundtruth_cif}")
        continue

    formula_dir = os.path.join(args.pred_base_dir, formula)
    predicted_files = glob.glob(os.path.join(formula_dir, "*.cif"))
    
    if not predicted_files:
        print(f"No CIF files found inside folder: {formula_dir}")
        continue

    print(f"\n>>> Processing Formula: {formula} ({len(predicted_files)} structures)")

    for p in predicted_files:
        # Inject arguments into sys.argv for distance_mul
        sys.argv = [
            'distance_mul.py',
            '--ground_truth', groundtruth_cif,
            '--predicted', p,
            '--formula', formula,
            '--model', model_name,
        ]
        
        try:
            # Run the imported main function from distance_mul.py
            run_analysis()
            
            # distance_mul saves a temp file: ../results/distance_table_{formula}.csv
            # temp_csv = f"../results/distance_table_{formula}.csv"
            
            # if os.path.exists(temp_csv):
            #     df = pd.read_csv(temp_csv)
            #     df.insert(0, 'model_name', args.model_name)
            #     df.insert(1, 'formula_name', formula) # Added for clarity
                
            #     write_header = not os.path.exists(args.output_csv)
            #     df.to_csv(args.output_csv, mode='a', index=False, header=write_header)
                
            #     os.remove(temp_csv)
        except Exception as e:
            print(f"Error processing {p}: {e}")

# print(f"\nALL DONE. Results saved to {args.output_csv}")
