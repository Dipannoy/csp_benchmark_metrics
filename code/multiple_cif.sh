#!/bin/sh
#SBATCH --job-name=multiple_cif
#SBATCH -N 1
#SBATCH -n 14
#SBATCH --gres=gpu:1 ## Run on 1 GPU
#SBATCH --output multiple_cif.out
#SBATCH --error multiple_cif.err
#SBATCH -p gpu
##Load your modules and run code here
hostname
date
##module load cuda/11.0
##module load python3/anaconda/2021.11
##source activate version

module purge

module load python3/anaconda/2023.9
export CONDA_ENV_PATH=/home/dg47/.conda/envs/metrics_2
export PATH=$CONDA_ENV_PATH/bin:$PATH
export LD_LIBRARY_PATH=$CONDA_ENV_PATH/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$CONDA_ENV_PATH/lib/python3.10/site-packages

# 2. Verify exactly which python we are using
echo "CHECKING PYTHON PATH:"
which python
python -c "import torch; print('Torch found at:', torch.__file__)"

# 3. Run the script
python calculate_multiple_cif.py --formula Li3Ti3Se6O3
