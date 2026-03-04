from unittest import TestCase

from rapt2.rapt import Rapt
from rapt2.treebrd.errors import RelationReferenceError
from rapt2.treebrd.grammars.core_grammar import CoreGrammar
from rapt2.treebrd.grammars.extended_grammar import ExtendedGrammar
from rapt2.treebrd.grammars.dependency_grammar import DependencyGrammar
from rapt2.treebrd.node import Operator


class TestRaptInit(TestCase):
    def test_default_grammar(self):
        rapt = Rapt()
        self.assertIsInstance(rapt.builder.grammar, ExtendedGrammar)

    def test_core_grammar(self):
        rapt = Rapt(grammar="Core Grammar")
        self.assertIsInstance(rapt.builder.grammar, CoreGrammar)

    def test_extended_grammar(self):
        rapt = Rapt(grammar="Extended Grammar")
        self.assertIsInstance(rapt.builder.grammar, ExtendedGrammar)

    def test_dependency_grammar(self):
        rapt = Rapt(grammar="Dependency Grammar")
        self.assertIsInstance(rapt.builder.grammar, DependencyGrammar)

    def test_unknown_grammar_falls_back_to_core(self):
        rapt = Rapt(grammar="Nonexistent Grammar")
        self.assertIsInstance(rapt.builder.grammar, CoreGrammar)


class TestConfigureGrammar(TestCase):
    def test_default_config(self):
        grammar = Rapt.configure_grammar()
        self.assertIsInstance(grammar, ExtendedGrammar)

    def test_custom_syntax(self):
        grammar = Rapt.configure_grammar(syntax={"select_op": "\\sel"})
        self.assertEqual(grammar.syntax.select_op, "\\sel")

    def test_custom_grammar_and_syntax(self):
        grammar = Rapt.configure_grammar(
            grammar="Core Grammar", syntax={"project_op": "\\proj"}
        )
        self.assertIsInstance(grammar, CoreGrammar)
        self.assertEqual(grammar.syntax.project_op, "\\proj")


class TestToSyntaxTree(TestCase):
    def setUp(self):
        self.rapt = Rapt()
        self.schema = {"alpha": ["a1", "a2"], "beta": ["b1", "b2"]}

    def test_single_relation(self):
        result = self.rapt.to_syntax_tree("alpha;", self.schema)
        self.assertEqual(1, len(result))
        self.assertEqual(Operator.relation, result[0].operator)

    def test_multiple_statements(self):
        result = self.rapt.to_syntax_tree("alpha; beta;", self.schema)
        self.assertEqual(2, len(result))

    def test_returns_list(self):
        result = self.rapt.to_syntax_tree("alpha;", self.schema)
        self.assertIsInstance(result, list)


class TestDefaultSchema(TestCase):
    def setUp(self):
        self.rapt = Rapt(grammar="Core Grammar")

    def test_to_syntax_tree_without_schema_raises(self):
        with self.assertRaises(RelationReferenceError):
            self.rapt.to_syntax_tree("alpha;")

    def test_to_sql_without_schema_raises(self):
        with self.assertRaises(RelationReferenceError):
            self.rapt.to_sql("alpha;")

    def test_to_qtree_without_schema_raises(self):
        with self.assertRaises(RelationReferenceError):
            self.rapt.to_qtree("alpha;")


class TestToSql(TestCase):
    def setUp(self):
        self.rapt = Rapt()
        self.schema = {"alpha": ["a1", "a2"], "beta": ["b1", "b2"]}

    def test_simple_relation(self):
        result = self.rapt.to_sql("alpha;", self.schema)
        self.assertEqual(1, len(result))
        self.assertIn("alpha", result[0])

    def test_bag_semantics(self):
        result = self.rapt.to_sql("alpha;", self.schema, use_bag_semantics=True)
        self.assertIn("SELECT alpha.a1", result[0])
        self.assertNotIn("DISTINCT", result[0])

    def test_set_semantics(self):
        result = self.rapt.to_sql("alpha;", self.schema, use_bag_semantics=False)
        self.assertIn("SELECT DISTINCT", result[0])


class TestToSqlSequence(TestCase):
    def setUp(self):
        self.rapt = Rapt()
        self.schema = {"alpha": ["a1", "a2"], "beta": ["b1", "b2"]}

    def test_single_relation(self):
        result = self.rapt.to_sql_sequence("alpha;", self.schema)
        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], list)

    def test_join_produces_sequence(self):
        result = self.rapt.to_sql_sequence("alpha \\join beta;", self.schema)
        self.assertEqual(1, len(result))
        # post_order traversal of a join: left, right, join node = 3 SQL statements
        self.assertEqual(3, len(result[0]))


class TestToQtree(TestCase):
    def setUp(self):
        self.rapt = Rapt()
        self.schema = {"alpha": ["a1", "a2"]}

    def test_simple_relation(self):
        result = self.rapt.to_qtree("alpha;", self.schema)
        self.assertEqual(1, len(result))
        self.assertIn("alpha", result[0])

    def test_returns_list(self):
        result = self.rapt.to_qtree("alpha;", self.schema)
        self.assertIsInstance(result, list)
