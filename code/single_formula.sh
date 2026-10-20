#!/bin/sh
#SBATCH --job-name=single_formula
#SBATCH -N 1
#SBATCH -n 14
#SBATCH --gres=gpu:1 ## Run on 1 GPU
#SBATCH --output single_formula.out
#SBATCH --error single_formula.err
#SBATCH -p dgx_aic
##Load your modules and run code here
hostname
date
##module load cuda/11.0
##module load python3/anaconda/2021.11
##source activate version

module purge

# 2. Load the base python/anaconda module
module load python3/anaconda/2023.9

ENV_PATH=$(conda info --envs | grep 'metrics_2' | awk '{print $NF}')

echo "Using Python from: $ENV_PATH/bin/python"

$ENV_PATH/bin/python distance_single.py --ground_truth ../data/Ba2BiSbO6.cif --predicted ../data/Ba2BiSbO6_pmg.cif\
