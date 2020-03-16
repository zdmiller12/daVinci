import numpy as np

# Equation references are from Systems Engineering and Analysis (5th edition)
# by Fabrycky and Blanchard


def calc_AELCC(PC, OC, RC, SC):
    """
    Equation 17.10
    AELCC = annual equivalent life-cycle cost
       PC = annual equivalent population cost
       OC = annual operating cost
       RC = annual repair facility cost
       SC = annual shortage penalty cost
    """
    AELCC = PC + OC + RC + SC
    return AELCC

def calc_PFC(P, N):
    """
    PFC = population first cost
    P   = unit acquisition cost
    N   = number of units in population
    """
    if type(N) == list:
        N = N[0]
    N = np.int64(N)
    PFC = P * N
    return PFC

def calc_PC(Ci, N):
    """
    Equation 17.11
    PC = annual equivalent population cost
    Ci = annual equivalent cost per unit
     N = number of units in the population
    """
    if type(N) == list:
        N = N[0]
    N = np.int64(N)
    PC = Ci * N
    return PC
    # or return equivalent form given by eq 8.18

def calc_Ci(P, B, i, n):
    """
    Equation 17.11
    Ci = annual equivalent cost per unit
     P = first or acquisition cost of a unit
     B = book value of a unit at the end of year n
    """
    if type(n) == list:
        n = n[0]
    n = np.int64(n)
    P_eq = P - B
    Ci = find_A_given_P(P_eq, i, n) + (B * i)
    return Ci

def calc_B(P, n, F, L):
    """
    Equation 17.12 (straight line method)
    B = book value of a unit at the end of year n
    P = first or acquisition cost of a unit
    F = estimated salvage value of a unit
    n = retirement age of units (n>1)
    L = estimated design life of the unit
    """
    if type(n) == list:
        n = n[0]
    n = np.int64(n)
    numerator = P - F
    B = P - n * np.true_divide(numerator, L)
    return B

def calc_OC(EC, LC, PMC, N, OAOC):
    """
    Equation 17.13
     OC = annual operating cost
     EC = annual cost of energy consumed
     LC = annual cost of operating labor
    PMC = annual cost of preventative maintenance
      N = number of units in population
    """
    if type(N) == list:
        N = N[0]
    N = np.int64(N)
    OC = (EC + LC + PMC + OAOC) * N
    return OC

def calc_RC(Cr, M):
    """
    Equation 17.14
    RC = annual repair facility cost
    Cr = annual fixed and variable repair cost per repair channel
     M = number of repair channels
    """
    if type(M) == list:
        M = M[0]
    M = np.int64(M)
    RC = Cr * M
    return RC

def calc_SC(Cs, E_S_):
    """
    Equation 17.15
      SC = annual shortage penalty cost
      Cs = annual shortage cost
    E_S_ = expected number of units short
    """
    SC = Cs * E_S_
    return SC

def calc_MTBF_average(n, MTBF_values):
    """
    Page 637
    MTBF = mean time between failures
    if units are homogenous, aggregate MTBF for the population is just the average
    """
    if type(n) == list:
        n = n[0]
    n = np.int64(n)
    MTBF_average = np.average(MTBF_values[:n])
    return MTBF_average

def calc_MTTR_average(n, MTTR_values):
    """
    Page 637
    MTTR = mean time to repair
    if units are homogenous, aggregate MTBF for the population is just the average
    """
    if type(n) == list:
        n = n[0]
    n = np.int64(n)
    MTTR_average = np.average(MTTR_values[:n])
    return MTTR_average

def calc_LAMBDA(MTBF_average):
    """
    Pages 325 and 637
    MTBF = mean time between failures
    """
    LAMBDA = np.true_divide(1, MTBF_average)
    return LAMBDA

def calc_MU(MTTR_average):
    """
    Pages 325 and 637
    MTTR = mean time to repair
    """
    MU = np.true_divide(1, MTTR_average)
    return MU

def calc_Cn_array(N, n, LAMBDA, MU, M):
    """
    Equation 10.39
         Cn = 
          N = number of units in the population
          n = number of failed items
     LAMBDA = failure rate of an item
         MU = repair rate of a repair channel
          M = number of service (repair) channels
    """
    if type(M) == list:
        M = M[0]
    if type(N) == list:
        N = N[0]
    if type(n) == list:
        n = n[0]
    M = np.int64(M)
    N = np.int64(N)
    n = np.int64(n)
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

def calc_P0(N, Cn_array):
    """
    Equation 10.38
    P0 = probability that no items failed
    N = number of units in the population
    """
    if type(N) == list:
        N = N[0]
    N = np.int64(N)
    summation = np.sum(Cn_array)
    P0 = np.true_divide(1, summation)
    return P0

def calc_Pn_array(P0, Cn_array):
    """
    Pages 327 and 638
    Pn = steady-state probability of n failed items
    P0 = probability that no items failed
    """
    Pn_array = P0 * Cn_array
    return Pn_array

def calc_Pr_array(N, D, Pn_array):
    """
    Shortage distribution
        N = number of units in the population
        D = demand ( number of required  units )
        S = number of units short
    Pr(S) = probability of being s units short
    """ 
    if type(D) == list:
        D = D[0]
    if type(N) == list:
        N = N[0]
    D = np.int64(D)
    N = np.int64(N)
    index = N - D
    Pr_array = Pn_array[index:]
    return Pr_array

def calc_P_naught(N, D, Pn_array):
    """
    Probability of being no units short
    """
    if type(D) == list:
        D = D[0]
    if type(N) == list:
        N = N[0]
    D = np.int64(D)
    N = np.int64(N)
    index = N - D + 1 
    P_naught = sum(Pn_array[:index])
    return P_naught

def calc_E_S_(D, N, Pn_array):
    """
    Equation 17.16
    E_S_ = expected number of units short
       D = demand ( number of required  units )
       N = supply ( number of available units )
    """
    if type(D) == list:
        D = D[0]
    if type(N) == list:
        N = N[0]
    D = np.int64(D)
    N = np.int64(N)
    summation = 0
    # D changed to array during transition to tables for user edit
    for j in range(1, D+1):
        summation += j * Pn_array[N-D+j]
    return summation

def calc_TC(PC, OC, RC, SC):
    """
    Page 639
    TC = total system annual equivalent cost
    OC = annual operating cost
    RC = annual repair facility cost
    SC = annual shortage penalty cost
    """
    TC = PC + OC + RC + SC
    return TC

### ## ## ## ## ## ## ##
##
#    Summary of Interest Formulas
#    page 222

#    for find_A_given_B
# format A=B(^{A/B,i,n})

def find_F_given_P(P, i, n):
    """
    Single-payment, compound-amount
    """
    if type(n) == list:
        n = n[0]
    n = np.int64(n)
    base = 1 + i
    F = P * np.power(base, n)
    return F

def find_P_given_F(F, i, n):
    """
    Single-payment, present-amount
    """
    if type(n) == list:
        n = n[0]
    n = np.int64(n)
    base = 1 + i
    denominator = np.power(base, n)
    P = np.true_divide(F, denominator)
    return P

def find_F_given_A(A, i, n):
    """
    Equal-payment series, compound-amount
    """
    if type(n) == list:
        n = n[0]
    n = np.int64(n)
    base = 1 + i
    numerator = np.power(base, n) - 1
    F = np.true_divide( (A*numerator), i)
    return F

def find_A_given_F(F, i, n):
    """
    Equal-payment series, sinking-fund
    """
    if type(n) == list:
        n = n[0]
    n = np.int64(n)
    base = 1 + i
    denominator = np.power(base, n) - 1
    A = np.true_divide( (F*i), denominator)
    return A

def find_P_given_A(A, i, n):
    """
    Equal-payment series, present-amount
    """
    if type(n) == list:
        n = n[0]
    n = np.int64(n)
    base = 1 + i
    numerator = np.power(base, n) - 1
    denominator = i * np.power(base, n)
    P = np.true_divide( (A*numerator), denominator)
    return P

def find_A_given_P(P, i, n):
    """
    Equal-payment series, capital-recovery
    """
    if type(n) == list:
        n = n[0]
    n = np.int64(n)
    base = 1 + i
    numerator = i * np.power(base, n)
    denominator = np.power(base, n) - 1
    A = np.true_divide((P*numerator), denominator)
    return A
#
##
### ## ## ## ## ## ## ##
