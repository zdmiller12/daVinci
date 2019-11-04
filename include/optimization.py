import itertools
import numpy as np
import pandas as pd

from include import basicFunctions as bF
   
class Optimization:
    def __init__(self, system_current):
        self.system = system_current
        self.setup_optimizer()

    def setup_optimizer(self):
        self.system.clear_simulated_values()
        self.create_simulation_array()
        for sim_vals in self.system.simulation_array:
            self.column_header = 'iter_' + str(self.system.iterations_completed() + 1)
            self.system.create_new_variable_set(self.column_header)
            self.system.variable_set.loc[self.system.variables_to_optimize, self.column_header] = sim_vals
            total_cost = self.calculate_total_cost()
            print total_cost
            within_constraints = self.check_constraints()
            if within_constraints:
                self.system.simulated_values = self.system.simulated_values.join(self.system.variable_set)
            else:
                continue
        
    def create_simulation_array(self):
        # should get rid of this column
        # opt_variables = self.system.variables.index[self.system.variables['optimize']].tolist()
        opt_variables = ['n','N','M']
        simulation_values = {}
        for var in opt_variables:
            if self.system.variables.at[var, 'sim_vals_def_type'] == 'bound':
                simulation_values[var] = self.define_simulation_values_bounded(var)
            else:
                simulation_values[var] = self.define_simulation_values_explicit(var)

        variables_to_optimize = simulation_values.keys()
        simulation_array = list(itertools.product(*simulation_values.values()))
        self.system.variables_to_optimize = variables_to_optimize
        self.system.simulation_values = simulation_values
        self.system.simulation_array = simulation_array

    def define_simulation_values_bounded(self, var):
        minimum = self.system.variables.at[var, 'bound_low']
        maximum = self.system.variables.at[var, 'bound_high']
        increment = self.system.variables.at[var, 'sim_increment']
        return [i for i in range(minimum, maximum+increment, increment)]

    def define_simulation_values_explicit(self, var):
        return self.system.variables.at[var, 'value']

    def calculate_total_cost(self):
        self.counter = 0
        while np.isnan(self.system.variable_set.at['TC', self.column_header]) and self.counter < 5:
            self.calculate_new_variables()
            self.counter += 1

    def calculate_new_variables(self):
        for equation_name, equation_variables in self.system.variables_per_equation.items():
            have_NaN = False
            send_variables = []
            var = equation_name[5:]
            check_variables = self.system.variable_set.loc[equation_variables, self.column_header].values
            for variable in check_variables:
                if np.any(np.isnan(variable)): 
                    have_NaN = True
                    break
                else: 
                    send_variables.append(variable)
            if have_NaN: 
                continue
            if np.any(np.isnan(self.system.variable_set.at[var, self.column_header])):
                fun = getattr(bF, equation_name)
                new_var = fun(*send_variables)
                try:
                    if np.isnan(new_var):
                        continue
                except ValueError:
                    if np.any(np.isnan(new_var)):
                        continue                    
                else:
                    # log this
                    # print('CALCULATED {} as {}'.format(var, self.system.variable_set.at[var, self.column_header]))
                    self.system.variable_set.at[var, self.column_header] = new_var
                    self.counter = 0

    def check_constraints(self):
        within_constraints = True
        for con in self.system.return_constrained_variables():
            if not np.any(np.isnan(self.system.variables.at[con, 'constraint_low'])) and (self.system.variable_set.at[con, self.column_header] < self.system.variables.at[con, 'constraint_low']):
                within_constraints = False
                print self.system.variable_set[self.column_header]
                print 'variable {} breaks low constraint at {}'.format(con, self.system.variable_set.at[con, self.column_header])
                break
            if not np.any(np.isnan(self.system.variables.at[con, 'constraint_high'])) and (self.system.variable_set.at[con, self.column_header] > self.system.variables.at[con, 'constraint_high']):
                within_constraints = False
                print self.system.variable_set[self.column_header]
                print 'variable {} breaks high constraint at {}'.format(con, self.system.variable_set.at[con, self.column_header])
                break

        if within_constraints:
            return True
        else:
            return False