#!/bin/sh
#SBATCH --job-name=toss_bertos_ft_full_model_ckpt_success_rate
#SBATCH -N 1
#SBATCH -n 14
#SBATCH --gres=gpu:1 ## Run on 1 GPU
#SBATCH --output toss_bertos_ft_full_model_ckpt_success_rate.out
#SBATCH --error toss_bertos_ft_full_model_ckpt_success_rate.err
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

PRED_BASE="/work/dg47/MLEG/CSPBenchMetrics/data/materium_structures_pmg/csp_benchmark_toss_model_bertos_ox_primitive_formula_ft_full_model_checkpoint/relaxed_results_pmg"


python -u calculate_success_rate.py \
    --model "toss" \
    --gt_dir "$GT" \
    --pred_base_dir "$PRED_BASE" \
    --output_csv "../results/match_results_toss_model_bertos_ox_ft_full_model_checkpoint.csv"


