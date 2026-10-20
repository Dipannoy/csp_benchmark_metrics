#!/bin/sh
#SBATCH --job-name=materium_baseline_loss_mp20_success_rate_0.5
#SBATCH -N 1
#SBATCH -n 14
#SBATCH --gres=gpu:1 ## Run on 1 GPU
#SBATCH --output materium_baseline_loss_mp20_success_rate_0.5.out
#SBATCH --error materium_baseline_loss_mp20_success_rate_0.5.err
#SBATCH -p v100-16gb-hiprio
##Load your modules and run code here
hostname
date

# Force environment paths
export CONDA_ENV_PATH=/home/dg47/.conda/envs/metrics_2
export PATH=$CONDA_ENV_PATH/bin:$PATH
export LD_LIBRARY_PATH=$CONDA_ENV_PATH/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$CONDA_ENV_PATH/lib/python3.10/site-packages

GT="/work/dg47/MLEG/CSPBenchMetrics/data/180-primitive-groundtruth"

PRED_BASE="/work/dg47/MLEG/CSPBenchMetrics/data/materium_structures_pmg/csp_benchmark_mp20_baseline_guess_ox_primitive_formula_free_2/relaxed_results_step_200_top_0.5"


python -u calculate_success_rate.py \
    --model "materium_baseline_loss_mp20" \
    --gt_dir "$GT" \
    --pred_base_dir "$PRED_BASE" \
    --output_csv "../results/match_results_materium_baeline_loss_mp20_step_500_0.5.csv"
