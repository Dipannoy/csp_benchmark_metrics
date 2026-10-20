# import os
# import glob
# import argparse
# import pandas as pd
# from pymatgen.core import Structure
# from pymatgen.analysis.structure_matcher import StructureMatcher
# from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

# def get_spacegroup(struct, symprec=0.1):
#     """Returns the international space group symbol."""
#     try:
#         sga = SpacegroupAnalyzer(struct, symprec=symprec)
#         return sga.get_space_group_symbol()
#     except:
#         return "Unknown"

# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--model_name", type=str, required=True)
#     parser.add_argument("--gt_dir", type=str, required=True)
#     parser.add_argument("--pred_base_dir", type=str, required=True)
#     parser.add_argument("--output_csv", type=str, required=True)
#     args = parser.parse_args()

#     # Standard CSP tolerances
#     matcher = StructureMatcher(ltol=0.2, stol=0.3, angle_tol=5, primitive_cell=True)
    
#     formula_folders = [f.name for f in os.scandir(args.pred_base_dir) if f.is_dir()]
#     results = []
    
#     total_formulas = 0
#     match_success_count = 0
#     sg_success_count = 0
#     consensus_rate = 0

#     print(f"Evaluating {args.model_name}...")

#     for formula in formula_folders:
#         gt_path = os.path.join(args.gt_dir, f"{formula}.cif")
#         if not os.path.exists(gt_path):
#             continue
            
#         total_formulas += 1
#         try:
#             gt_struct = Structure.from_file(gt_path)
#             gt_sg = get_spacegroup(gt_struct)
            
#             formula_dir = os.path.join(args.pred_base_dir, formula)
#             pred_files = glob.glob(os.path.join(formula_dir, "*.cif"))
            
#             formula_matched = False
#             formula_sg_matched = False
#             both_match = False
#             best_pred_sg = "None"

#             for p in pred_files:
#                 pred_struct = Structure.from_file(p)
#                 pred_sg = get_spacegroup(pred_struct)
#                 current_strct_match = False
#                 current_sg_match = False
                
#                 # 1. Check Structure Match (Geometry)
#                 if matcher.fit(gt_struct, pred_struct):
#                     formula_matched = True
#                     current_strct_match = True
                    
                
#                 # 2. Check Space Group Match (Symmetry)
#                 if pred_sg == gt_sg:
#                     formula_sg_matched = True
#                     best_pred_sg = pred_sg
#                     current_sg_match = True
#                 elif best_pred_sg == "None":
#                     best_pred_sg = pred_sg # Track at least one sg found
                    
#                 if current_strct_match and current_sg_match:
#                     both_match = True
                    
                
#             if formula_matched: match_success_count += 1
#             if formula_sg_matched: sg_success_count += 1
#             if both_match: consensus_rate += 1
            
#             results.append({
#                 "model": args.model_name,
#                 "formula": formula,
#                 "gt_spacegroup": gt_sg,
#                 "pred_spacegroup": best_pred_sg,
#                 "sg_match": formula_sg_matched,
#                 "struct_match": formula_matched,
#                 "num_predictions": len(pred_files)
#             })

#         except Exception as e:
#             print(f"Error processing {formula}: {e}")

#     # Calculate Rates
#     match_rate = (match_success_count / total_formulas) * 100 if total_formulas > 0 else 0
#     sg_rate = (sg_success_count / total_formulas) * 100 if total_formulas > 0 else 0
#     consensus_prnctg = (consensus_rate / total_formulas) * 100 if total_formulas > 0 else 0


#     print(f"\n--- Results for {args.model_name} ---")
#     print(f"Total Formulas: {total_formulas}")
#     print(f"Structure Success Rate: {match_rate:.2f}%")
#     print(f"Space Group Success Rate: {sg_rate:.2f}%")
#     print(f"Consensus Rate: {consensus_prnctg:.2f}%")


#     # Save to CSV
#     df = pd.DataFrame(results)
#     df.to_csv(args.output_csv, index=False)
#     print(f"Detailed results saved to {args.output_csv}")

# if __name__ == "__main__":
#     main()

import os
import glob
import argparse
import pandas as pd
from pymatgen.core import Structure
from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

def get_spacegroup(struct, symprec=0.1):
    """Returns the international space group symbol."""
    try:
        sga = SpacegroupAnalyzer(struct, symprec=symprec)
        return sga.get_space_group_symbol()
    except Exception:
        return "Unknown"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--gt_dir", type=str, required=True)
    parser.add_argument("--pred_base_dir", type=str, required=True)
    parser.add_argument("--output_csv", type=str, required=True)
    args = parser.parse_args()

    # Standard CSP tolerances
    matcher = StructureMatcher(ltol=0.2, stol=0.3, angle_tol=5, primitive_cell=True)
    
    formula_folders = [f.name for f in os.scandir(args.pred_base_dir) if f.is_dir()]
    results = []
    
    total_formulas = 0
    match_success_count = 0
    sg_success_count = 0
    consensus_rate = 0

    print(f"Evaluating {args.model_name}...")

    for formula in formula_folders:
        gt_path = os.path.join(args.gt_dir, f"{formula}.cif")
        if not os.path.exists(gt_path):
            print(formula)
            continue
            
        total_formulas += 1
        
        # Try to load the ground truth first
        try:
            gt_struct = Structure.from_file(gt_path)
            gt_sg = get_spacegroup(gt_struct)
        except Exception as e:
            print(f"Error processing ground truth for {formula}: {e}")
            continue # Skip to next formula if GT is broken
            
        formula_dir = os.path.join(args.pred_base_dir, formula)
        pred_files = glob.glob(os.path.join(formula_dir, "*.cif"))
        
        formula_matched = False
        formula_sg_matched = False
        both_match = False
        best_pred_sg = "None"

        for p in pred_files:
            # Safely attempt to parse each generative prediction
            try:
                pred_struct = Structure.from_file(p)
                pred_sg = get_spacegroup(pred_struct)
            except Exception:
                continue # Skip malformed predicted CIFs seamlessly
                
            current_strct_match = False
            current_sg_match = False
            
            # 1. Check Structure Match (Geometry)
            if matcher.fit(gt_struct, pred_struct):
                formula_matched = True
                current_strct_match = True
                
            # 2. Check Space Group Match (Symmetry)
            if pred_sg == gt_sg:
                formula_sg_matched = True
                best_pred_sg = pred_sg
                current_sg_match = True
            elif best_pred_sg in ["None", "Unknown"]:
                best_pred_sg = pred_sg # Track a valid sg if we haven't found an exact match yet
                
            # 3. Check Consensus
            if current_strct_match and current_sg_match:
                both_match = True
                break # Optimization: Perfect match found, stop evaluating remaining candidates
                
        if formula_matched: match_success_count += 1
        if formula_sg_matched: sg_success_count += 1
        if both_match: consensus_rate += 1
        
        results.append({
            "model": args.model_name,
            "formula": formula,
            "gt_spacegroup": gt_sg,
            "pred_spacegroup": best_pred_sg,
            "sg_match": formula_sg_matched,
            "struct_match": formula_matched,
            "num_predictions": len(pred_files)
        })
        
    total_formulas=180

    # Calculate Rates
    match_rate = (match_success_count / total_formulas) * 100 if total_formulas > 0 else 0
    sg_rate = (sg_success_count / total_formulas) * 100 if total_formulas > 0 else 0
    consensus_prnctg = (consensus_rate / total_formulas) * 100 if total_formulas > 0 else 0

    print(f"\n--- Results for {args.model_name} ---")
    print(f"Total Formulas: {total_formulas}")
    print(f"Structure Success Rate: {match_rate:.2f}%")
    print(f"Space Group Success Rate: {sg_rate:.2f}%")
    print(f"Consensus Rate: {consensus_prnctg:.2f}%")

    # Save to CSV
    df = pd.DataFrame(results)
    df.to_csv(args.output_csv, index=False)
    print(f"Detailed results saved to {args.output_csv}")

if __name__ == "__main__":
    main()
