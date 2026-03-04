from rapt2.treebrd.grammars.core_grammar import CoreGrammar
from tests.treebrd.grammars.grammar_test_case import GrammarTestCase


class TestCoreGrammarIsUnary(GrammarTestCase):
    def setUp(self):
        self.grammar = CoreGrammar()

    def test_select_is_unary(self):
        self.assertTrue(self.grammar.is_unary(self.grammar.syntax.select_op))

    def test_project_is_unary(self):
        self.assertTrue(self.grammar.is_unary(self.grammar.syntax.project_op))

    def test_rename_is_unary(self):
        self.assertTrue(self.grammar.is_unary(self.grammar.syntax.rename_op))

    def test_join_is_not_unary(self):
        self.assertFalse(self.grammar.is_unary(self.grammar.syntax.join_op))

    def test_union_is_not_unary(self):
        self.assertFalse(self.grammar.is_unary(self.grammar.syntax.union_op))

    def test_difference_is_not_unary(self):
        self.assertFalse(self.grammar.is_unary(self.grammar.syntax.difference_op))

    def test_unknown_is_not_unary(self):
        self.assertFalse(self.grammar.is_unary("\\unknown"))


class TestCoreGrammarIsBinary(GrammarTestCase):
    def setUp(self):
        self.grammar = CoreGrammar()

    def test_join_is_binary(self):
        self.assertTrue(self.grammar.is_binary(self.grammar.syntax.join_op))

    def test_union_is_binary(self):
        self.assertTrue(self.grammar.is_binary(self.grammar.syntax.union_op))

    def test_difference_is_binary(self):
        self.assertTrue(self.grammar.is_binary(self.grammar.syntax.difference_op))

    def test_select_is_not_binary(self):
        self.assertFalse(self.grammar.is_binary(self.grammar.syntax.select_op))

    def test_project_is_not_binary(self):
        self.assertFalse(self.grammar.is_binary(self.grammar.syntax.project_op))

    def test_rename_is_not_binary(self):
        self.assertFalse(self.grammar.is_binary(self.grammar.syntax.rename_op))

    def test_unknown_is_not_binary(self):
        self.assertFalse(self.grammar.is_binary("\\unknown"))
