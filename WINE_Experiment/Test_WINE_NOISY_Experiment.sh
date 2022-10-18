#!/bin/env bash
#SBATCH --array=0-199
#SBATCH --job-name=WINE_Experiment
#SBATCH --output=outputWINE/output%A%a.txt
#SBATCH --error=outputWINE/error%A%a.txt
#SBATCH --mem=16GB
#SBATCH --time=0-24:0:0
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mail-type=ALL
#SBATCH --mail-user=17tna@queensu.ca
#SBATCH --account=def-bshastri
input$SLURM_ARRAY_TASK_ID.dat

activation_values=( TanH )
classical_size_values=( 20 )
cutoff_dimension_values=( 5 )
encoding_method_values=( Amplitude_Phase )
ff_activation_values=( relu )
max_initial_weight_values=( None )
n_circuits_values=( 1 )
n_classes_values=( 10 )
n_qumodes_values=( 2 )
norm_threshold_values=( 0.99 )
num_classical_values=( 4 )
num_layers_values=( 1 )
regularizer_string_values=( L1=0.1 )
seed_values=( 809275366 )
shots_values=( 1 2 4 8 16 32 64 128 256 512 )
sigma_values=( 1e-10 3.3598182862837877e-10 1.1288378916846883e-09 3.792690190732254e-09 1.274274985703132e-08 4.281332398719396e-08 1.438449888287663e-07 4.832930238571752e-07 1.6237767391887209e-06 5.455594781168514e-06 1.8329807108324338e-05 6.158482110660255e-05 0.00020691380811147902 0.0006951927961775605 0.002335721469090121 0.007847599703514606 0.026366508987303555 0.08858667904100832 0.2976351441631313 1.0 )
precision_values=( 65536 )
max_epoch_values=( 31 )
exp_train_values=( 224 )
trial=${SLURM_ARRAY_TASK_ID}
activation=${activation_values[$(( trial % ${#activation_values[@]} ))]}
trial=$(( trial / ${#activation_values[@]} ))
classical_size=${classical_size_values[$(( trial % ${#classical_size_values[@]} ))]}
trial=$(( trial / ${#classical_size_values[@]} ))
cutoff_dimension=${cutoff_dimension_values[$(( trial % ${#cutoff_dimension_values[@]} ))]}
trial=$(( trial / ${#cutoff_dimension_values[@]} ))
encoding_method=${encoding_method_values[$(( trial % ${#encoding_method_values[@]} ))]}
trial=$(( trial / ${#encoding_method_values[@]} ))
ff_activation=${ff_activation_values[$(( trial % ${#ff_activation_values[@]} ))]}
trial=$(( trial / ${#ff_activation_values[@]} ))
max_initial_weight=${max_initial_weight_values[$(( trial % ${#max_initial_weight_values[@]} ))]}
trial=$(( trial / ${#max_initial_weight_values[@]} ))
n_circuits=${n_circuits_values[$(( trial % ${#n_circuits_values[@]} ))]}
trial=$(( trial / ${#n_circuits_values[@]} ))
n_classes=${n_classes_values[$(( trial % ${#n_classes_values[@]} ))]}
trial=$(( trial / ${#n_classes_values[@]} ))
n_qumodes=${n_qumodes_values[$(( trial % ${#n_qumodes_values[@]} ))]}
trial=$(( trial / ${#n_qumodes_values[@]} ))
norm_threshold=${norm_threshold_values[$(( trial % ${#norm_threshold_values[@]} ))]}
trial=$(( trial / ${#norm_threshold_values[@]} ))
num_classical=${num_classical_values[$(( trial % ${#num_classical_values[@]} ))]}
trial=$(( trial / ${#num_classical_values[@]} ))
num_layers=${num_layers_values[$(( trial % ${#num_layers_values[@]} ))]}
trial=$(( trial / ${#num_layers_values[@]} ))
regularizer_string=${regularizer_string_values[$(( trial % ${#regularizer_string_values[@]} ))]}
trial=$(( trial / ${#regularizer_string_values[@]} ))
seed=${seed_values[$(( trial % ${#seed_values[@]} ))]}
trial=$(( trial / ${#seed_values[@]} ))
shots=${shots_values[$(( trial % ${#shots_values[@]} ))]}
trial=$(( trial / ${#shots_values[@]} ))
sigma=${sigma_values[$(( trial % ${#sigma_values[@]} ))]}
trial=$(( trial / ${#sigma_values[@]} ))
precision=${precision_values[$(( trial % ${#precision_values[@]} ))]}
trial=$(( trial / ${#precision_values[@]} ))
max_epoch=${max_epoch_values[$(( trial % ${#max_epoch_values[@]} ))]}
trial=$(( trial / ${#max_epoch_values[@]} ))
exp_train=${exp_train_values[$(( trial % ${#exp_train_values[@]} ))]}

python WINE_NoisyTest_Experiment.py with activation=${activation} classical_size=${classical_size} cutoff_dimension=${cutoff_dimension} encoding_method=${encoding_method} ff_activation=${ff_activation} max_initial_weight=${max_initial_weight} n_circuits=${n_circuits} n_classes=${n_classes} n_qumodes=${n_qumodes} norm_threshold=${norm_threshold} num_classical=${num_classical} num_layers=${num_layers} regularizer_string=${regularizer_string} seed=${seed} shots=${shots} sigma=${sigma} precision=${precision} max_epoch=${max_epoch} exp_train=${exp_train} 