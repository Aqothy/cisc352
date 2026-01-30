# =============================
# Student Names: Anthony, Chloe, Amanda
# Group ID: 88
# Date: 2026-01-23
# =============================
# CISC 352
# heuristics.py
# desc: with these heuristics we want to reduce search space as fast as possible so that we can find failure fastest and backtrack sooner


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

1. ord_dh (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Degree heuristic

2. ord_mv (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Minimum-Remaining-Value heuristic


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    Variables and constraints of the problem. The assigned Variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return next Variable to be assigned according to the Degree Heuristic
    highest degree variable is the one involved in the most constraints with other unassigned variables, like degrees in graphs. again same idea by finding the most influential variable so that we can reduce the search space fastest and find failure fastest so that we can backtrack sooner, often used with mrv when mrv results in ties
    '''
    vars = csp.get_all_unasgn_vars()
    if not vars:
        return None

    best_var = vars[0]
    max_deg = -1

    for v in vars:
        deg = 0
        constraints = csp.get_cons_with_var(v)
        for c in constraints:
            # Check if constraint has other unassigned variables
            # get_n_unasgn() includes v itself. So if > 1, there are others.
            if c.get_n_unasgn() > 1:
                deg += 1

        if deg > max_deg:
            max_deg = deg
            best_var = v

    return best_var


def ord_mrv(csp):
    ''' return Variable to be assigned according to the Minimum Remaining Values heuristic
    we want the smallest domain size so that we can find the failure fastest to backtrack, smallest size has the least options
    '''
    vars = csp.get_all_unasgn_vars()
    if not vars:
        return None

    best_var = vars[0]
    min_size = best_var.cur_domain_size()

    for v in vars[1:]:
        size = v.cur_domain_size()
        if size < min_size:
            min_size = size
            best_var = v

    return best_var
