import numpy as np
import pandas as pd
from userDefined import userDefined as uD
from defaults.Problem2 import Problem2 as P2
from defaults.CandidateSystem1 import CandidateSystem1 as CS1
from defaults.CandidateSystem2 import CandidateSystem2 as CS2


def setup_variables( load_variables, variable_list, column_names ):
    variable_df = pd.DataFrame(None, index=variable_list, columns=column_names)
    if load_variables == 'problem-2':
        variable_df = P2(variable_df).variables
    elif load_variables == 'candidate-1':
        variable_df = CS1(variable_df).variables
    elif load_variables == 'candidate-2':
        variable_df = CS2(variable_df).variables
    else:
        print 'bad argument'
        sys.exit(1)
    return variable_df


def process_constraints( variables ):
    for index, row in variables.iterrows():
        if not np.any(np.isnan(row['constraint_low'])) or not np.any(np.isnan(row['constraint_high'])):
            row['constrained'] = True
    constrained_variables = variables.index[variables['constrained']].tolist()
    return (variables, constrained_variables)


def process_optimized( variables ):
    # retirement age need not be an integer, but that would be a useful option
    integer_variables = ['N', 'M', 'n']
    for var in optimization_variables( variables ):
        if var in integer_variables:
            variables.at[var, 'integer'] = True
        else:
            variables.at[var, 'integer'] = False
    return variables