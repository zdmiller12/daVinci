import pdb
import os
import numpy as np
import pandas as pd

import basicFunctions as bF


class mainClassDataFrame:
    def __init__(self, name):
        self.name = name
        self.variables_all  = []
        self.variables_per_equation = {}

        self.default_system_filePath = os.path.join(os.getcwd(), 'parameters', 'user', 'systems', 'examples', 'default.pkl')

        for method in dir(bF):
            if method[:5] != 'calc_':
                continue
            else:
                fun   = getattr(bF, method)
                arg_N = fun.__code__.co_argcount
                args  = fun.__code__.co_varnames
                self.variables_all.append(args)
                self.variables_per_equation[fun.__name__] = args[:arg_N]

        self.df_column_names = ['value', 'optimize', 'integer', 'sim_vals_def_type', 'sim_increment', 'bound_low', 'bound_high', 'constraint_low', 'constraint_high', 'constrained', 'weight']
        self.variables_all_list = sorted(set(sum(self.variables_all, ())))
        self.variables = self.setup_variables()
        self.simulated_values = pd.DataFrame(None, index=self.variables_all_list)

    def iterations_completed(self):
        try:
            return len(self.simulated_values.columns)
        except:
            return 0

    def clear_simulated_values(self):
        self.simulated_values = pd.DataFrame(None, index=self.variables_all_list)

    def create_new_variable_set(self, column_header):
        self.variable_set = pd.DataFrame(None, index=self.variables_all_list, columns=[column_header])
        self.variable_set[column_header] = self.variables['value']

    def setup_variables(self):
        # df = pd.DataFrame(None, index=self.variables_all_list, columns=self.df_column_names)
        return pd.read_pickle(self.default_system_filePath)

    def update_variables(self, fileName):
        try:
            df_loaded = pd.read_pickle(fileName)
            self.variables = df_loaded
        except Exception as e:
            print e
            raise

    def return_constrained_variables(self):
        # there has to be a better way to do this
        constrained = []
        for index, row in self.variables.iterrows():
            if not np.any(np.isnan(row['constraint_low'])) or not np.any(np.isnan(row['constraint_high'])):
                constrained.append(row.name)
        return constrained

    def process_optimized(self):
        # retirement age need not be an integer, but that would be a useful option
        integer_variables = ['N', 'M', 'n']
        for var in optimization_variables( variables ):
            if var in integer_variables:
                variables.at[var, 'integer'] = True
            else:
                variables.at[var, 'integer'] = False
        return variables

    def save_dataFrame(self, fileName):
        self.variables.to_pickle(fileName)