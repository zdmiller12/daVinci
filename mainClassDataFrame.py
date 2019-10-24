import pdb
import numpy as np
import pandas as pd

import include.basicFunctions as bF
import include.helperFunctions as hF

from parameters.defaults.Problem2 import Problem2 as P2
from parameters.defaults.CandidateSystem1 import CandidateSystem1 as CS1
from parameters.defaults.CandidateSystem2 import CandidateSystem2 as CS2

class mainClassDataFrame:
    def __init__( self, name ):
        self.name = name
        self.load_variables = 'problem-2'
        self.variables_all  = []
        self.variables_per_equation = {}

        for method in dir(bF):
            if method[:5] != 'calc_':
                continue
            else:
                fun   = getattr(bF, method)
                arg_N = fun.__code__.co_argcount
                args  = fun.__code__.co_varnames
                self.variables_all.append(args)
                self.variables_per_equation[fun.__name__] = args[:arg_N]

        self.df_column_names = ['value', 'optimize', 'integer', 'sim_increment', 'bound_low', 'bound_high', 'constraint_low', 'constraint_high', 'constrained', 'weight']
        self.variables_all_list = sorted(set(sum(self.variables_all, ())))
        self.variables = self.setup_variables()
        self.simulated_values = pd.DataFrame(None, index=self.variables_all_list)

    def iterations_completed( self ):
        try:
            return len(self.simulated_values.columns)
        except:
            return 0

    def set_variables_to_optimize( self, variables_to_optimize ):
        self.variables_to_optimize = variables_to_optimize

    def set_simulation_values( self, simulation_values ):
        self.simulation_values = simulation_values

    def set_simulation_array( self, simulation_array ):
        self.simulation_array = simulation_array

    def clear_simulated_values( self ):
        self.simulated_values = pd.DataFrame(None, index=self.variables_all_list)

    def create_new_variable_set( self, column_header ):
        self.variable_set = pd.DataFrame(None, index=self.variables_all_list, columns=[column_header])
        self.variable_set[column_header] = self.variables['value']

    def setup_variables( self ):
        variable_df = pd.DataFrame(None, index=self.variables_all_list, columns=self.df_column_names)
        if self.load_variables == 'problem-2':
            variable_df = P2(variable_df).variables
        elif self.load_variables == 'candidate-1':
            variable_df = CS1(variable_df).variables
        elif self.load_variables == 'candidate-2':
            variable_df = CS2(variable_df).variables
        else:
            print 'bad argument'
            sys.exit(1)
        return variable_df

    def return_constrained_variables( self ):
        # there has to be a better way to do this
        constrained = []
        for index, row in self.variables.iterrows():
            if not np.any(np.isnan(row['constraint_low'])) or not np.any(np.isnan(row['constraint_high'])):
                constrained.append(row.name)
        return constrained

    def process_optimized( self ):
        # retirement age need not be an integer, but that would be a useful option
        integer_variables = ['N', 'M', 'n']
        for var in optimization_variables( variables ):
            if var in integer_variables:
                variables.at[var, 'integer'] = True
            else:
                variables.at[var, 'integer'] = False
        return variables