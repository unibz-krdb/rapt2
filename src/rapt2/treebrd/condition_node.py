from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto

from pyparsing import ParseBaseException

from .grammars.condition_grammar import ConditionGrammar
from .grammars.syntax import Syntax


class UnaryConditionalOperator(Enum):
    """Operators for unary condition expressions (NOT, DEFINED)."""

    NOT = auto()
    DEFINED = auto()

    @classmethod
    def from_syntax(cls, syntax: Syntax, instring: str) -> "UnaryConditionalOperator":
        """
        Map a syntax token string to the corresponding enum member.

        :param syntax: the active syntax defining operator tokens.
        :param instring: the parsed operator string.
        :return: the matching UnaryConditionalOperator.
        :raises ValueError: if the string doesn't match any known operator.
        """
        match instring:
            case syntax.not_op:
                return cls.NOT
            case syntax.defined_op:
                return cls.DEFINED
            case _:
                raise ValueError(f"Unknown unary conditional operator: {instring}")


class BinaryConditionalOperator(Enum):
    """Operators for binary condition expressions (AND, OR, comparisons)."""

    AND = auto()
    OR = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    LESS_THAN_EQUAL = auto()
    GREATER_THAN = auto()
    GREATER_THAN_EQUAL = auto()

    @classmethod
    def from_syntax(cls, syntax: Syntax, instring: str) -> "BinaryConditionalOperator":
        """
        Map a syntax token string to the corresponding enum member.

        :param syntax: the active syntax defining operator tokens.
        :param instring: the parsed operator string.
        :return: the matching BinaryConditionalOperator.
        :raises ValueError: if the string doesn't match any known operator.
        """
        match instring:
            case syntax.and_op:
                return cls.AND
            case syntax.or_op:
                return cls.OR
            case syntax.equal_op:
                return cls.EQUAL
            case syntax.not_equal_op | syntax.not_equal_alt_op:
                return cls.NOT_EQUAL
            case syntax.less_than_op:
                return cls.LESS_THAN
            case syntax.less_than_equal_op:
                return cls.LESS_THAN_EQUAL
            case syntax.greater_than_op:
                return cls.GREATER_THAN
            case syntax.greater_than_equal_op:
                return cls.GREATER_THAN_EQUAL
            case _:
                raise ValueError(f"Unknown binary conditional operator: {instring}")


@dataclass(frozen=True)
class ConditionNode(ABC):
    """Abstract base for nodes in a condition expression tree."""

    @abstractmethod
    def attribute_references(self) -> list[str]:
        """
        Return a list of attribute references in this condition node.
        """
        raise NotImplementedError()


@dataclass(frozen=True)
class IdentityConditionNode(ConditionNode):
    """A leaf condition node holding a single identifier (attribute reference,
    literal, or number)."""

    ident: str

    def attribute_references(self) -> list[str]:
        try:
            ConditionGrammar().attribute_reference.parse_string(self.ident)
            return [self.ident]
        except ParseBaseException:
            return []


@dataclass(frozen=True)
class UnaryConditionNode(ConditionNode):
    """A condition node applying a unary operator (NOT, DEFINED) to a child."""

    op: UnaryConditionalOperator
    child: ConditionNode

    def attribute_references(self) -> list[str]:
        return self.child.attribute_references()


@dataclass(frozen=True)
class BinaryConditionNode(ConditionNode):
    """A condition node applying a binary operator (AND, OR, comparison) to
    left and right children."""

    op: BinaryConditionalOperator
    left: ConditionNode
    right: ConditionNode

    def attribute_references(self) -> list[str]:
        return list(
            self.left.attribute_references() + self.right.attribute_references()
        )
