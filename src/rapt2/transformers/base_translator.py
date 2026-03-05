from ..treebrd.condition_node import (
    BinaryConditionNode,
    ConditionNode,
    IdentityConditionNode,
    UnaryConditionNode,
)
from ..treebrd.grammars.syntax import Syntax
from ..treebrd.node import Operator


class BaseTranslator:
    """
    A Translator defining the operations for translating a relational algebra
    statement into some output format.
    """

    def __init__(self, syntax: Syntax | None = None):
        self.syntax = syntax or Syntax()
        self._condition_translate_functions: dict = {
            IdentityConditionNode: self.identity_condition,
            UnaryConditionNode: self.unary_condition,
            BinaryConditionNode: self.binary_condition,
        }
        self._translate_functions = {
            Operator.relation: self.relation,
            Operator.select: self.select,
            Operator.project: self.project,
            Operator.rename: self.rename,
            Operator.assign: self.assign,
            Operator.cross_join: self.cross_join,
            Operator.natural_join: self.natural_join,
            Operator.theta_join: self.theta_join,
            Operator.full_outer_join: self.full_outer_join,
            Operator.left_outer_join: self.left_outer_join,
            Operator.right_outer_join: self.right_outer_join,
            Operator.union: self.union,
            Operator.difference: self.difference,
            Operator.intersect: self.intersect,
            Operator.primary_key: self.primary_key,
            Operator.multivalued_dependency: self.multivalued_dependency,
            Operator.functional_dependency: self.functional_dependency,
            Operator.inclusion_equivalence: self.inclusion_equivalence,
            Operator.inclusion_subsumption: self.inclusion_subsumption,
        }

    def translate(self, node):
        """
        Translate a node into some output format.
        :param node: a treebrd node
        :return: a node's translation to some format
        """
        _translate = self._translate_functions.get(node.operator)
        if _translate is None:
            raise NotImplementedError(f"No translator for operator: {node.operator}")
        return _translate(node)

    def relation(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def select(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def project(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def rename(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def assign(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def cross_join(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def natural_join(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def theta_join(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def full_outer_join(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def left_outer_join(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def right_outer_join(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def union(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def difference(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def intersect(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def primary_key(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def multivalued_dependency(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def functional_dependency(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def inclusion_equivalence(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def inclusion_subsumption(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def identity_condition(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def unary_condition(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def binary_condition(self, node):
        raise NotImplementedError("Must be implemented by translation modules.")

    def translate_condition(self, condition: ConditionNode):
        """
        Dispatch a condition node to the appropriate condition translator method.

        :param condition: a condition node
        :return: translated representation of the condition
        """
        _translate = self._condition_translate_functions.get(type(condition))
        if _translate is None:
            raise ValueError(f"Unknown condition node type: {type(condition)}")
        return _translate(condition)


def translate(roots):
    """
    Translate a list of relational algebra trees into some output format.
    :param roots: a list of tree roots
    :return:  a list of translations
    """
    raise NotImplementedError("Must be implemented by translation modules.")
