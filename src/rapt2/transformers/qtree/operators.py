from ...treebrd.node import Operator
from ...treebrd.condition_node import BinaryConditionalOperator, UnaryConditionalOperator
from .constants import *

latex_operator = {
    Operator.select: SELECT_OP,
    Operator.project: PROJECT_OP,
    Operator.rename: RENAME_OP,
    Operator.assign: ASSIGN_OP,
    Operator.cross_join: JOIN_OP,
    Operator.natural_join: NATURAL_JOIN_OP,
    Operator.theta_join: THETA_JOIN_OP,
    Operator.full_outer_join: FULL_OUTER_JOIN_OP,
    Operator.left_outer_join: LEFT_OUTER_JOIN_OP,
    Operator.right_outer_join: RIGHT_OUTER_JOIN_OP,
    Operator.union: UNION_OP,
    Operator.difference: DIFFERENCE_OP,
    Operator.intersect: INTERSECT_OP,
    Operator.primary_key: PRIMARY_KEY_OP,
    Operator.multivalued_dependency: MULTIVALUED_DEPENDENCY_OP,
    Operator.functional_dependency: FUNCTIONAL_DEPENDENCY_OP,
    Operator.inclusion_equivalence: INCLUSION_EQUIVALENCE_OP,
    Operator.inclusion_subsumption: INCLUSION_SUBSUMPTION_OP,
}

# Conditional operator mappings
conditional_latex_operator = {
    # Binary operators
    BinaryConditionalOperator.AND: AND_OP,
    BinaryConditionalOperator.OR: OR_OP,
    BinaryConditionalOperator.EQUAL: EQUAL_OP,
    BinaryConditionalOperator.NOT_EQUAL: NOT_EQUAL_OP,
    BinaryConditionalOperator.LESS_THAN: LESS_THAN_OP,
    BinaryConditionalOperator.LESS_THAN_EQUAL: LESS_THAN_EQUAL_OP,
    BinaryConditionalOperator.GREATER_THAN: GREATER_THAN_OP,
    BinaryConditionalOperator.GREATER_THAN_EQUAL: GREATER_THAN_EQUAL_OP,
    # Unary operators
    UnaryConditionalOperator.NOT: NOT_OP,
    UnaryConditionalOperator.DEFINED: DEFINED_OP,
}
