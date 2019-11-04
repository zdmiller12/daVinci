import numpy as np

# equation 17.10
# AELCC = annual equivalent life-cycle cost
#    PC = annual equivalent population cost
#    OC = annual operating cost
#    RC = annual repair facility cost
#    SC = annual shortage penalty cost
def calc_AELCC(PC, OC, RC, SC):
    AELCC = PC + OC + RC + SC
    return AELCC

# population first cost
# P = unit acquisition cost
# N = number of units in population
def calc_PFC(P, N):
    if type(N) == list:
        N = int(N[0])
    PFC = P * N
    return PFC

# equation 17.11
# PC = annual equivalent population cost
# Ci = annual equivalent cost per unit
#  N = number of units in the population
def calc_PC(Ci, N):
    if type(N) == list:
        N = int(N[0])
    PC = Ci * N
    return PC
    # or return equivalent form given by eq 8.18

# equation 17.11
# Ci = annual equivalent cost per unit
#  P = first or acquisition cost of a unit
#  B = book value of a unit at the end of year n
def calc_Ci(P, B, i, n):
    if type(n) == list:
        n = int(n[0])
    P_eq = P - B
    Ci = find_A_given_P(P_eq, i, n) + (B * i)
    return Ci

# straight-line method
# equation 17.12
# B = book value of a unit at the end of year n
# P = first or acquisition cost of a unit
# F = estimated salvage value of a unit
# n = retirement age of units (n>1)
# L = estimated design life of the unit
def calc_B(P, n, F, L):
    if type(n) == list:
        n = int(n[0])
    numerator = P - F
    B = P - n * np.true_divide(numerator, L)
    return B

# equation 17.13
#  EC = annual cost of energy consumed
#  LC = annual cost of operating labor
# PMC = annual cost of preventative maintenance
#   N = number of units in population
def calc_OC(EC, LC, PMC, N, OAOC):
    if type(N) == list:
        N = int(N[0])
    OC = (EC + LC + PMC + OAOC) * N
    return OC

# equation 17.14
# RC = annual repair facility cost
# Cr = annual fixed and variable repair cost per repair channel
#  M = number of repair channels
def calc_RC(Cr, M):
    if type(M) == list:
        M = int(M[0])
    RC = Cr * M
    return RC

# equation 17.15
#   SC = annual shortage penalty cost
#   Cs = annual shortage cost
# E_S_ = expected number of units short
def calc_SC(Cs, E_S_):
    SC = Cs * E_S_
    return SC

# page 637
# MTBF = mean time between failures
# if units are homogenous, aggregate MTBF for the population is just the average
def calc_MTBF_average(n, MTBF_values):
    if type(n) == list:
        n = int(n[0])
    MTBF_average = np.average(MTBF_values[:n])
    return MTBF_average

# page 637
# MTTR = mean time to repair
# if units are homogenous, aggregate MTBF for the population is just the average
def calc_MTTR_average(n, MTTR_values):
    if type(n) == list:
        n = int(n[0])
    MTTR_average = np.average(MTTR_values[:n])
    return MTTR_average

# pages 325 and 637
# MTBF = mean time between failures
def calc_LAMBDA(MTBF_average):
    LAMBDA = np.true_divide(1, MTBF_average)
    return LAMBDA

# pages 325 and 637
# MTTR = mean time to repair
def calc_MU(MTTR_average):
    MU = np.true_divide(1, MTTR_average)
    return MU

# equation 10.39
#      Cn = 
#       N = number of units in the population
#       n = number of failed items
#  LAMBDA = failure rate of an item
#      MU = repair rate of a repair channel
#       M = number of service (repair) channels
def calc_Cn_array(N, n, LAMBDA, MU, M):
    if type(M) == list:
        M = int(M[0])
    if type(N) == list:
        N = int(N[0])
    if type(n) == list:
        n = int(n[0])
    numerator   = np.math.factorial(N)
    parentheses = np.true_divide(LAMBDA, MU)
    Cn_array    = np.array([])
    for n in range(N+1):
        if n in range(M+1): 
            denominator = np.math.factorial(N-n) * np.math.factorial(n)
        else:
            denominator = np.math.factorial(N-n) * np.math.factorial(M) * np.power(M, n-M)
        Cn = np.true_divide(numerator, denominator) * np.power(parentheses, n)  
        Cn_array = np.append(Cn_array, Cn)
    return Cn_array

# equation 10.38
# P0 = probability that no items failed
# N = number of units in the population
def calc_P0(N, Cn_array):
    if type(N) == list:
        N = int(N[0])
    summation = np.sum(Cn_array)
    P0 = np.true_divide(1, summation)
    return P0

# pages 327 and 638
# Pn = steady-state probability of n failed items
# P0 = probability that no items failed
def calc_Pn_array(P0, Cn_array):
    Pn_array = P0 * Cn_array
    return Pn_array

# shortage distribution
#     N = number of units in the population
#     D = demand ( number of required  units )
#     S = number of units short
# Pr(S) = probability of being s units short 
def calc_Pr_array(N, D, Pn_array):
    if type(D) == list:
        D = int(D[0])
    if type(N) == list:
        N = int(N[0])
    index = N - D
    Pr_array = Pn_array[index:]
    return Pr_array

# probability of being no units short
def calc_P_naught(N, D, Pn_array):
    if type(D) == list:
        D = int(D[0])
    if type(N) == list:
        N = int(N[0])
    index = N - D + 1 
    P_naught = sum(Pn_array[:index])
    return P_naught

# equation 17.16
# E_S_ = expected number of units short
#    D = demand ( number of required  units )
#    N = supply ( number of available units )
def calc_E_S_(D, N, Pn_array):
    if type(D) == list:
        D = int(D[0])
    if type(N) == list:
        N = int(N[0])
    summation = 0
    # D changed to array during transition to tables for user edit
    for j in range(1, D+1):
        summation += j * Pn_array[N-D+j]
    return summation

# page 639
# TC = total system annual equivalent cost
# OC = annual operating cost
# RC = annual repair facility cost
# SC = annual shortage penalty cost
def calc_TC(PC, OC, RC, SC):
    TC = PC + OC + RC + SC
    return TC

### ## ## ## ## ## ## ##
##
#    Summary of Interest Formulas
#    page 222

#    for find_A_given_B
# format A=B(^{A/B,i,n})

# single-payment, compound-amount
def find_F_given_P(P, i, n):
    if type(n) == list:
        n = int(n[0])
    base = 1 + i
    F = P * np.power(base, n)
    return F

# single-payment, present-amount
def find_P_given_F(F, i, n):
    # n = int(n[0])
    base = 1 + i
    denominator = np.power(base, n)
    P = np.true_divide(F, denominator)
    return P

# equal-payment series, compound-amount
def find_F_given_A(A, i, n):
    if type(n) == list:
        n = int(n[0])
    base = 1 + i
    numerator = np.power(base, n) - 1
    F = np.true_divide( (A*numerator), i)
    return F

# equal-payment series, sinking-fund
def find_A_given_F(F, i, n):
    if type(n) == list:
        n = int(n[0])
    base = 1 + i
    denominator = np.power(base, n) - 1
    A = np.true_divide( (F*i), denominator)
    return A

# equal-payment series, present-amount
def find_P_given_A(A, i, n):
    if type(n) == list:
        n = int(n[0])
    base = 1 + i
    numerator = np.power(base, n) - 1
    denominator = i * np.power(base, n)
    P = np.true_divide( (A*numerator), denominator)
    return P

# equal-payment series, capital-recovery
def find_A_given_P(P, i, n):
    if type(n) == list:
        n = int(n[0])
    base = 1 + i
    numerator = i * np.power(base, n)
    denominator = np.power(base, n) - 1
    A = np.true_divide( (P*numerator), denominator)
    return A
#
##
### ## ## ## ## ## ## ##