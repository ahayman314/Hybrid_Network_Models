#%% Sweep Hyperparameters Sequentially
from Iris_Experiment import ex
from sklearn.model_selection import ParameterGrid
from SLURM_Script_Factory import save_script
import sys

if __name__ == "__main__":
    args = sys.argv[1:]

    parameters = {'initial_weight_amplitudes': [0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0],
                  'initial_input_amplitude': [0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0],
                  'loss_coefficient': [0.01],
                  'cutoff_management':[None, "L1", "L2", "Loss"],
                  'cutoff_dimension':[10,20,30]
    }

    fields = {
        'memory': 16,
        'job_name': 'test_sweep',
        'time_h': 8,
        'num_cpus': 11
    }

    parameter_combinations = list(ParameterGrid(parameters))

    if(args[0]=='run'):
        for parameter_combo in parameter_combinations:
             ex.run(config_updates=parameter_combo)

    elif(args[0]=='build_slurm'):
        save_script('Iris.sh', 'Iris_Experiment.py', fields, parameters)

    else:
        print("please enter 'run' or 'build_slurm'")




