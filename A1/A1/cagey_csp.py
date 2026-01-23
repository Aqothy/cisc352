# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all Variables in the given csp. If you are returning an entire grid's worth of Variables
they should be arranged linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional Variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 0.5/3 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
| n^2-n | n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '%' for modular addition
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
import itertools
import functools


def binary_ne_grid(cagey_grid):
    n, _ = cagey_grid
    csp = CSP(f"Binary_NE_Grid_{n}")

    # Create variables
    # Format: Cell(row, col) where row, col in 1..n
    vars = []
    # Store in a 2D list for easy constraint creation, flat list for return
    grid = []

    for r in range(1, n + 1):
        row_vars = []
        for c in range(1, n + 1):
            var = Variable(f"Cell({r},{c})", [i for i in range(1, n + 1)])
            csp.add_var(var)
            vars.append(var)
            row_vars.append(var)
        grid.append(row_vars)

    # Add Row Constraints (Binary Not Equal)
    for r in range(n):
        for c1 in range(n):
            for c2 in range(c1 + 1, n):
                con_name = f"Row_{r + 1}_({c1 + 1},{c2 + 1})"
                var1 = grid[r][c1]
                var2 = grid[r][c2]
                con = Constraint(con_name, [var1, var2])

                sat_tuples = []
                for v1 in range(1, n + 1):
                    for v2 in range(1, n + 1):
                        if v1 != v2:
                            sat_tuples.append((v1, v2))

                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)

    # Add Column Constraints (Binary Not Equal)
    for c in range(n):
        for r1 in range(n):
            for r2 in range(r1 + 1, n):
                con_name = f"Col_{c + 1}_({r1 + 1},{r2 + 1})"
                var1 = grid[r1][c]
                var2 = grid[r2][c]
                con = Constraint(con_name, [var1, var2])

                sat_tuples = []
                for v1 in range(1, n + 1):
                    for v2 in range(1, n + 1):
                        if v1 != v2:
                            sat_tuples.append((v1, v2))

                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)

    return csp, vars


def nary_ad_grid(cagey_grid):
    n, _ = cagey_grid
    csp = CSP(f"Nary_AD_Grid_{n}")

    vars = []
    grid = []

    domain = [i for i in range(1, n + 1)]

    for r in range(1, n + 1):
        row_vars = []
        for c in range(1, n + 1):
            var = Variable(f"Cell({r},{c})", domain)
            csp.add_var(var)
            vars.append(var)
            row_vars.append(var)
        grid.append(row_vars)

    # Generate all-different permutations once
    all_diff_tuples = list(itertools.permutations(domain, n))

    # Row Constraints (N-ary All Diff)
    for r in range(n):
        scope = grid[r]
        con = Constraint(f"Row_{r + 1}_AllDiff", scope)
        con.add_satisfying_tuples(all_diff_tuples)
        csp.add_constraint(con)

    # Column Constraints (N-ary All Diff)
    for c in range(n):
        scope = [grid[r][c] for r in range(n)]
        con = Constraint(f"Col_{c + 1}_AllDiff", scope)
        con.add_satisfying_tuples(all_diff_tuples)
        csp.add_constraint(con)

    return csp, vars


def cagey_csp_model(cagey_grid):
    n, cages = cagey_grid

    # We use the binary grid model as the base to save space/time on grid constraints
    # compared to full n-ary on large grids, while adding cage constraints.
    # Note: The prompt allows choice.
    csp, vars_linear = binary_ne_grid(cagey_grid)

    # Create a lookup map for variables
    # vars_linear is [Cell(1,1), Cell(1,2), ..., Cell(n,n)]
    var_map = {}
    idx = 0
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            var_map[(r, c)] = vars_linear[idx]
            idx += 1

    # Add Cage Constraints
    # We also need to add variables for operators

    for cage_idx, (target, cells, op_char) in enumerate(cages):
        cage_vars = [var_map[cell_pos] for cell_pos in cells]

        # Create Operator Variable
        # Domain depends on if op is known or '?'
        if op_char == "?":
            op_domain = ["+", "-", "*", "/", "%"]
        else:
            op_domain = [op_char]

        op_var_name = f"Cage_op({target}:{op_char}:{cage_vars})"
        op_var = Variable(op_var_name, op_domain)
        csp.add_var(op_var)
        vars_linear.append(op_var)

        # Scope includes cage cells and the operator variable
        scope = cage_vars + [op_var]
        con = Constraint(f"Cage_{cage_idx}", scope)

        # Generate satisfying tuples
        # We need to iterate all combinations of values for the cells + op

        sat_tuples = []

        # Pre-calculate cell domains (all are 1..n)
        cell_domains = [range(1, n + 1) for _ in cage_vars]

        # We need to check every permutation of values assigned to cells?
        # Actually, constraint is satisfied if *exists* a permutation that satisfies op.
        # But here we are generating tuples of assignments (v1, v2, ... vn, op).
        # A tuple (v1...vn, op) is satisfying if there is a permutation of (v1...vn)
        # that yields target with op.

        # Optimization: Generate cartesian product of cell values
        # Since n is small (max 9), and cage size usually small, this is feasible.

        for values in itertools.product(*cell_domains):
            # values is a tuple (v1, v2, ... vn)

            valid_ops = []
            for op in op_domain:
                if check_operation(values, op, target):
                    valid_ops.append(op)

            for valid_op in valid_ops:
                # Add (v1, v2, ..., vn, op)
                sat_tuples.append(values + (valid_op,))

        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)

    return csp, vars_linear


def check_operation(values, op, target):
    # 1-cell cage case
    if len(values) == 1:
        return values[0] == target

    perms = itertools.permutations(values)

    for p in perms:
        try:
            res = calculate(p, op)
            if res == target:
                return True
        except:
            continue

    return False


def calculate(values, op):
    if op == "+":
        return sum(values)
    elif op == "*":
        return functools.reduce(lambda x, y: x * y, values)
    elif op == "-":
        # Left associative: ((v1 - v2) - v3) ...
        return functools.reduce(lambda x, y: x - y, values)
    elif op == "/":
        # Division: no fractions allowed. Must be exact integer division at each step.
        def div_op(x, y):
            if y == 0 or x % y != 0:
                raise ValueError("Invalid division")
            return x // y

        return functools.reduce(div_op, values)
    elif op == "%":
        # Modular Addition: sum(others) % first_element
        if values[0] == 0:
            raise ValueError("Modulo by zero")
        return sum(values[1:]) % values[0]
    return None
