"""
Syntax hierarchy for configurable operator symbols.

Each syntax class pairs with a corresponding grammar class:

    BaseSyntax        → (shared tokens: terminators, delimiters, parentheses)
    ConditionSyntax   → ConditionGrammar  (logical/comparison operators)
    CoreSyntax        → CoreGrammar       (select, project, rename, assign, join, set ops)
    ExtendedSyntax    → ExtendedGrammar   (theta/outer joins, intersect, defined)
    DependencySyntax  → DependencyGrammar (PK, MVD, FD, inclusion constraints)

``Syntax`` is a backward-compatibility alias for ``DependencySyntax``, the
most complete level.  Users can override any token via keyword arguments to
``__init__``, or load overrides from a JSON config file.
"""


class BaseSyntax:
    """
    Base syntax class containing common tokens used by all grammars.
    """

    # General tokens.
    terminator = ";"
    delim = ","
    params_start = "_{"
    params_stop = "}"
    paren_left = "("
    paren_right = ")"

    def __init__(self, **kwargs):
        """
        Override default tokens with user-supplied values.

        :param kwargs: token names and their replacement strings. Only
            attributes already defined on the class are accepted.
        """
        # Set any user defined syntax.
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])


class ConditionSyntax(BaseSyntax):
    """
    Syntax class for condition expressions containing logical and comparison operators.
    """

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


class CoreSyntax(ConditionSyntax):
    """
    Syntax class for core relational algebra containing basic operators.
    """

    # Relational algebra operators.
    project_op = "\\project"
    rename_op = "\\rename"
    select_op = "\\select"
    assign_op = ":="
    join_op = "\\join"
    difference_op = "\\difference"
    union_op = "\\union"


class ExtendedSyntax(CoreSyntax):
    """
    Syntax class for extended relational algebra containing additional join operators.
    """

    # Additional join operators.
    theta_join_op = "\\theta_join"
    natural_join_op = "\\natural_join"
    full_outer_join_op = "\\full_outer_join"
    left_outer_join_op = "\\left_outer_join"
    right_outer_join_op = "\\right_outer_join"
    intersect_op = "\\intersect"

    # Defined operator.
    defined_op = "defined"


class DependencySyntax(ExtendedSyntax):
    """
    Syntax class for dependency grammar containing dependency-specific operators.
    """

    # Dependency operators.
    pk_op = "pk"
    mvd_op = "mvd"
    fd_op = "fd"
    inc_equiv_op = "inc="
    inc_subset_op = "inc⊆"

    _dependency_op_attrs = ("pk_op", "mvd_op", "fd_op", "inc_equiv_op", "inc_subset_op")

    @property
    def dependency_operators(self) -> tuple[str, ...]:
        """Return the resolved dependency operator strings."""
        return tuple(getattr(self, attr) for attr in self._dependency_op_attrs)


# Backward compatibility alias
Syntax = DependencySyntax
