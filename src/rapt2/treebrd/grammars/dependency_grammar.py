from typing import TypeVar
from pyparsing import (
    Group,
    Suppress,
    OneOrMore,
    Literal,
)

from .extended_grammar import ExtendedGrammar
from .syntax import DependencySyntax

TDependencySyntax = TypeVar('TDependencySyntax', bound=DependencySyntax)


class DependencyGrammar(ExtendedGrammar[TDependencySyntax]):
    """
    A parser that recognizes database dependency grammar rules.

    The rules are annotated with their BNF equivalents. For a complete
    specification refer to the associated grammar file.
    """
    syntax: TDependencySyntax

    def __init__(self, syntax: TDependencySyntax = DependencySyntax()):
        """
        Initializes a DependencyGrammar. Uses the default syntax if none
        is provided.

        :param syntax: a syntax for this grammar.
        """
        super().__init__(syntax)

    def parse(self, instring):
        instring = r"" + instring
        return self.statements.parseString(instring, parseAll=True)

    @property
    def pk(self):
        """
        pk ::= "pk"
        """
        return Literal(self.syntax.pk_op)

    @property
    def pk_dep(self):
        """
        pk_dep ::= pk param_start attribute_list param_stop relation_name
        """
        return Group(self.pk + self.parameter(self.attribute_list) + self.relation_name)

    @property
    def mvd(self):
        """
        mvd ::= "mvd"
        """
        return Literal(self.syntax.mvd_op)

    @property
    def mvd_dep(self):
        """
        mvd_dep ::= mvd param_start attribute_name delim attribute_name param_stop relation_name
        """
        return Group(
            self.mvd
            + self.parameter(
                self.attribute_name + Suppress(self.syntax.delim) + self.attribute_name
            )
            + self.relation_name
        )

    @property
    def fd(self):
        """
        fd ::= "fd"
        """
        return Literal(self.syntax.fd_op)

    @property
    def fd_dep(self):
        """
        fd_dep ::= fd param_start attribute_name delim attribute_name param_stop ((select param_start conditions param_stop relation_name) | relation_name)
        """
        return Group(
            self.fd
            + self.parameter(
                self.attribute_name + Suppress(self.syntax.delim) + self.attribute_name
            )
            + (
                (Literal(self.syntax.select_op) + self.parameter(self.conditions) + self.relation_name)
                | self.relation_name
            )
        )

    @property
    def inc_eq(self):
        """
        inc_eq ::= "inc="
        """
        return Literal(self.syntax.inc_equiv_op)

    @property
    def inc_eq_dep(self):
        """
        inc_eq_dep ::= inc_eq param_start attribute_name delim attribute_name param_stop paren_left relation_name delim relation_name paren_right
        """
        return Group(
            self.inc_eq
            + self.parameter(
                self.attribute_name + Suppress(self.syntax.delim) + self.attribute_name
            )
            + self.parenthesize(
                self.relation_name + Suppress(self.syntax.delim) + self.relation_name
            )
        )

    @property
    def inc_subs(self):
        """
        inc_subs ::= "inc⊆"
        """
        return Literal(self.syntax.inc_subset_op)

    @property
    def inc_subs_dep(self):
        """
        inc_subs_dep ::= inc_subs param_start attribute_name delim attribute_name param_stop paren_left relation_name delim relation_name paren_right
        """
        return Group(
            self.inc_subs
            + self.parameter(
                self.attribute_name + Suppress(self.syntax.delim) + self.attribute_name
            )
            + self.parenthesize(
                self.relation_name + Suppress(self.syntax.delim) + self.relation_name
            )
        )

    @property
    def dep(self):
        """
        dep ::= pk_dep | mvd_dep | fd_dep | inc_eq_dep | inc_subs_dep
        """
        return (
            self.pk_dep
            | self.mvd_dep
            | self.fd_dep
            | self.inc_eq_dep
            | self.inc_subs_dep
        )

    @property
    def statement(self):
        """
        statement ::= dep terminate | statement
        """
        return self.dep + Suppress(self.syntax.terminator)

    @property
    def statements(self):
        """
        An ordered collection of dependency statements.
        """
        return OneOrMore(self.statement)
