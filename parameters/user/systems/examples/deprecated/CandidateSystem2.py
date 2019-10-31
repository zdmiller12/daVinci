import pandas as pd

class CandidateSystem2:
    def __init__( self, variables ):
        self.variables = variables
        ###
        ##
        #    Variable Values
        self.variables.at['P',    'value'] = 43000 # unit acquisition cost ($)
        self.variables.at['L',    'value'] = 6     # unit design life (years)
        self.variables.at['F',    'value'] = 5000  # unit salvage value at end of design life ($)
        self.variables.at['EC',   'value'] = 800   # energy and fuel cost ($ per year)
        self.variables.at['LC',   'value'] = 700   # operating labor cost ($ per year)
        self.variables.at['PMC',  'value'] = 400   # preventative maintenance cost ($ per year)
        self.variables.at['OAOC', 'value'] = 400   # other annual operating costs ($ per year)
        self.variables.at['Cr',   'value'] = 45000 # annual repair channel cost ($ per repair channel per year)
        self.variables.at['Cs',   'value'] = 73000 # annual shortage cost ($ per unit per year)
        self.variables.at['i',    'value'] = 0.1   # interest rate (0-1)
        self.variables.at['D',    'value'] = 15    # demand (number of units required)
        self.variables.at['N',    'value'] = 19    # number of units in the population
        self.variables.at['M',    'value'] = 3     # number of service (repair) channels
        self.variables.at['n',    'value'] = 4     # number of failed items
        self.variables.at['MTBF_values', 'value']  = [.18, .21, .25, .25, .23, .20] # mean time between failures for age cohorts [0-1, 1-2, 2-3, 3-4, 4-5, 5-6] 
        self.variables.at['MTTR_values', 'value']  = [.04, .04, .05, .05, .06, .06] # mean time to repair for age cohorts        [0-1, 1-2, 2-3, 3-4, 4-5, 5-6]
        #
        ##
        ###
        ##
        #    Optimization Settings
        self.variables['optimize'] = False # default to optimize no variables
        self.variables.at['n', 'optimize'] = True
        self.variables.at['N', 'optimize'] = True
        self.variables.at['M', 'optimize'] = True

        self.variables.at['n', 'sim_increment'] = 1
        self.variables.at['N', 'sim_increment'] = 1
        self.variables.at['M', 'sim_increment'] = 1
        #
        ##
        ###
        ##
        #    Constraint Settings
        self.variables['constrained'] = False 
        self.variables.at['PFC', 'constraint_high']          = 900000
        self.variables.at['P0', 'constraint_low']            = 0.7
        self.variables.at['MTBF_average', 'constraint_low']  = 0.2
        #
        ##
        ###
        ##
        #    Bound Settings
        self.variables.at['n', 'bound_low']  = 3
        self.variables.at['n', 'bound_high'] = 5

        self.variables.at['N', 'bound_low']  = 18
        self.variables.at['N', 'bound_high'] = 20

        self.variables.at['M', 'bound_low']  = 2
        self.variables.at['M', 'bound_high'] = 4
        #
        ##
        ###
        ##
        #    Declare Integers
        self.variables['integer'] = False
        self.variables.at['n', 'integer'] = True
        self.variables.at['N', 'integer'] = True
        self.variables.at['M', 'integer'] = True