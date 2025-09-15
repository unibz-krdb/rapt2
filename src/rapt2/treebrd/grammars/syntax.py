class Syntax:
    # General tokens.
    terminator = ";"
    delim = ","
    params_start = "_{"
    params_stop = "}"
    paren_left = "("
    paren_right = ")"

    # Logical tokens.
    not_op = "not"
    and_op = "and"
    or_op = "or"

    # Comparison operators.
    equal_op = "="
    not_equal_op = "!="
    not_equal_alt_op = "<>"
    less_than_op = "<"
    less_than_equal_op = "<="
    greater_than_op = ">"
    greater_than_equal_op = ">="

    # Relational algebra operators.
    project_op = "\\project"
    rename_op = "\\rename"
    select_op = "\\select"
    assign_op = ":="
    join_op = "\\join"
    theta_join_op = "\\theta_join"
    natural_join_op = "\\natural_join"
    full_outer_join_op = "\\full_outer_join"
    left_outer_join_op = "\\left_outer_join"
    right_outer_join_op = "\\right_outer_join"
    difference_op = "\\difference"
    union_op = "\\union"
    intersect_op = "\\intersect"

    # Defined operator.
    defined_op = "defined"

    # Dependency operators.
    pk_op = "pk"
    mvd_op = "mvd"
    fd_op = "fd"
    inc_equiv_op = "inc="
    inc_subset_op = "inc⊆"

    def __init__(self, **kwargs):
        # Set any user defined syntax.
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
