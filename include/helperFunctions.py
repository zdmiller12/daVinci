import numpy as np
import pandas as pd
import itertools
import pdb

def is_unique(variable_set, simulated_values):
    already_simmed = np.array(len(variable_set))
    for var, col in simulated_values.iteritems():
        if simulated_values.at[var, col] == variable_set.at[var]:
            already_simmed = np.append(already_simmed, True)
        else:
            already_simmed = np.append(already_simmed, False)

    if np.all( already_simmed ):
        return False
    else:
        return True

def create_simulation_array(variables):
    opt_variables = variables.index[variables['optimize']].tolist()
    simulation_values = {}
    for var in opt_variables:
        minimum = variables.at[var, 'bound_low']
        maximum = variables.at[var, 'bound_high']
        increment = variables.at[var, 'sim_increment']
        sim_list = [i for i in range(minimum, maximum+increment, increment)]
        simulation_values[var] = sim_list

    variables_to_optimize = simulation_values.keys()
    simulation_array = list(itertools.product(*simulation_values.values()))
    return (variables_to_optimize, simulation_values, simulation_array)