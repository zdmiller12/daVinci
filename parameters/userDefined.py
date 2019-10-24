import pandas as pd

class userDefined:
    def __init__( self, variable_list, column_names ):
        self.variables = pd.DataFrame(None, index=variable_list, columns=column_names)
        self.variables['optimize']        = False
        self.variables['constrained']     = False
        self.variables['integer']         = False
        self.variables.at['n', 'integer'] = True
        self.variables.at['N', 'integer'] = True
        self.variables.at['M', 'integer'] = True

        switch_to_zero_value  = ['P', 'L', 'F', 'OC']
        switch_to_zero_values = ['MTBF_values', 'MTTR_values']

        self.variables.loc[switch_to_zero_value,  'value'] =  0
        self.variables.loc[switch_to_zero_values, 'value'] = [0]

    def change_value(self, value_to_change, value_type, new_value):
        self.variables.at[str(value_to_change), str(value_type)] = new_value