from enum import Enum, auto
from abc import ABC, abstractmethod
from dataclasses import dataclass

from rapt2.treebrd.grammars.syntax import Syntax

class UnaryConditionalOperator(Enum):
    NOT = auto()
    DEFINED = auto()

    @classmethod
    def from_syntax(cls, syntax: Syntax, instring: str) -> "UnaryConditionalOperator":
        match instring:
            case syntax.not_op:
                return cls.NOT
            case syntax.defined_op:
                return cls.DEFINED
            case _:
                raise ValueError

class BinaryConditionalOperator(Enum):
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
        match instring:
            case syntax.and_op:
                return cls.AND
            case syntax.or_op:
                return cls.OR
            case syntax.equal_op:
                return cls.EQUAL
            case syntax.not_equal_op:
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
                raise ValueError

@dataclass(frozen=True)
class ConditionNode(ABC):

    @abstractmethod
    def latex(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def sql(self) -> str:
        raise NotImplementedError()

@dataclass(frozen=True)
class IdentityConditionNode(ConditionNode):
    ident: str

    def latex(self) -> str:
        return self.ident

    def sql(self) -> str:
        return self.ident

@dataclass(frozen=True)
class UnaryConditionNode(ConditionNode):
    op: UnaryConditionalOperator
    child: ConditionNode

    def latex(self) -> str:
        match self.op:
            case UnaryConditionalOperator.NOT:
                return f"\\neg {self.child.latex()}"
            case UnaryConditionalOperator.DEFINED:
                return f"\\text{{defined}}({self.child.latex()})"
            case _:
                raise ValueError

    def sql(self) -> str:
        match self.op:
            case UnaryConditionalOperator.NOT:
                return f"NOT {self.child.sql()}"
            case UnaryConditionalOperator.DEFINED:
                return f"{self.child.sql()} IS NOT NULL"
            case _:
                raise ValueError

@dataclass(frozen=True)
class BinaryConditionNode(ConditionNode):
    op: BinaryConditionalOperator
    left: ConditionNode
    right: ConditionNode

    def latex(self) -> str:
        match self.op:
            case BinaryConditionalOperator.AND:
                return f"({self.left.latex()} \\land {self.right.latex()})"
            case BinaryConditionalOperator.OR:
                return f"({self.left.latex()} \\lor {self.right.latex()})"
            case BinaryConditionalOperator.EQUAL:
                return f"({self.left.latex()} \\eq {self.right.latex()})"
            case BinaryConditionalOperator.NOT_EQUAL:
                return f"({self.left.latex()} \\neq {self.right.latex()})"
            case BinaryConditionalOperator.LESS_THAN:
                return f"({self.left.latex()} \\lt {self.right.latex()})"
            case BinaryConditionalOperator.LESS_THAN_EQUAL:
                return f"({self.left.latex()} \\leq {self.right.latex()})"
            case BinaryConditionalOperator.GREATER_THAN:
                return f"({self.left.latex()} \\gt {self.right.latex()})"
            case BinaryConditionalOperator.GREATER_THAN_EQUAL:
                return f"({self.left.latex()} \\geq {self.right.latex()})"
            case _:
                raise ValueError

    def sql(self) -> str:
        match self.op:
            case BinaryConditionalOperator.AND:
                return f"({self.left.sql()} AND {self.right.sql()})"
            case BinaryConditionalOperator.OR:
                return f"({self.left.sql()} OR {self.right.sql()})"
            case BinaryConditionalOperator.EQUAL:
                return f"({self.left.sql()} = {self.right.sql()})"
            case BinaryConditionalOperator.NOT_EQUAL:
                return f"({self.left.sql()} != {self.right.sql()})"
            case BinaryConditionalOperator.LESS_THAN:
                return f"({self.left.sql()} < {self.right.sql()})"
            case BinaryConditionalOperator.LESS_THAN_EQUAL:
                return f"({self.left.sql()} <= {self.right.sql()})"
            case BinaryConditionalOperator.GREATER_THAN:
                return f"({self.left.sql()} > {self.right.sql()})"
            case BinaryConditionalOperator.GREATER_THAN_EQUAL:
                return f"({self.left.sql()} >= {self.right.sql()})"
            case _:
                raise ValueError