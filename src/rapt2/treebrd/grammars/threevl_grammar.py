from pyparsing import CaselessKeyword, Keyword, Literal, one_of
from .core_grammar import CoreGrammar


class ThreeVLGrammar(CoreGrammar):
    """
    A parser that recognizes a three-valued logic relational algebra grammar.

    The rules are annotated with their BNF equivalents. For a complete
    specification refer to the associated grammar file.
    """

    @property
    def defined_op(self):
        return self.syntax.defined_op

    @property
    def defined_condition(self):
        """
        defined_condition ::= defined_op "(" identifier ")"
        """
        return (
            Keyword(self.defined_op)
            + Literal(self.syntax.paren_left).suppress()
            + self.attribute_reference("attribute_reference*")
            + Literal(self.syntax.paren_right).suppress()
        )
