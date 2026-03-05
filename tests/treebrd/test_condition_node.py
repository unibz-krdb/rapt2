from unittest import TestCase

from rapt2.treebrd.condition_node import (
    BinaryConditionalOperator,
    BinaryConditionNode,
    IdentityConditionNode,
    UnaryConditionalOperator,
    UnaryConditionNode,
)
from rapt2.treebrd.grammars.syntax import Syntax
from rapt2.treebrd.schema import Schema
from rapt2.transformers.qtree.qtree_translator import QTreeTranslator as QTreeTranslator
from rapt2.transformers.sql.sql_translator import SQLTranslator as SQLTranslator


class ConditionNodeTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.schema = Schema(
            {
                "alpha": ["a1"],
                "beta": ["b1", "b2"],
                "gamma": ["c1", "c2", "c3"],
            }
        )
        self.qtree_translator = QTreeTranslator()
        self.sql_translator = SQLTranslator()


class TestUnaryConditionalOperatorFromSyntax(ConditionNodeTestCase):
    def setUp(self):
        super().setUp()
        self.syntax = Syntax()

    def test_not_operator(self):
        result = UnaryConditionalOperator.from_syntax(self.syntax, self.syntax.not_op)
        self.assertEqual(result, UnaryConditionalOperator.NOT)

    def test_defined_operator(self):
        result = UnaryConditionalOperator.from_syntax(
            self.syntax, self.syntax.defined_op
        )
        self.assertEqual(result, UnaryConditionalOperator.DEFINED)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            UnaryConditionalOperator.from_syntax(self.syntax, "invalid")


class TestBinaryConditionalOperatorFromSyntax(ConditionNodeTestCase):
    def setUp(self):
        super().setUp()
        self.syntax = Syntax()

    def test_and_operator(self):
        result = BinaryConditionalOperator.from_syntax(self.syntax, self.syntax.and_op)
        self.assertEqual(result, BinaryConditionalOperator.AND)

    def test_or_operator(self):
        result = BinaryConditionalOperator.from_syntax(self.syntax, self.syntax.or_op)
        self.assertEqual(result, BinaryConditionalOperator.OR)

    def test_equal_operator(self):
        result = BinaryConditionalOperator.from_syntax(
            self.syntax, self.syntax.equal_op
        )
        self.assertEqual(result, BinaryConditionalOperator.EQUAL)

    def test_not_equal_operator(self):
        result = BinaryConditionalOperator.from_syntax(
            self.syntax, self.syntax.not_equal_op
        )
        self.assertEqual(result, BinaryConditionalOperator.NOT_EQUAL)

    def test_not_equal_alt_operator(self):
        result = BinaryConditionalOperator.from_syntax(
            self.syntax, self.syntax.not_equal_alt_op
        )
        self.assertEqual(result, BinaryConditionalOperator.NOT_EQUAL)

    def test_less_than_operator(self):
        result = BinaryConditionalOperator.from_syntax(
            self.syntax, self.syntax.less_than_op
        )
        self.assertEqual(result, BinaryConditionalOperator.LESS_THAN)

    def test_less_than_equal_operator(self):
        result = BinaryConditionalOperator.from_syntax(
            self.syntax, self.syntax.less_than_equal_op
        )
        self.assertEqual(result, BinaryConditionalOperator.LESS_THAN_EQUAL)

    def test_greater_than_operator(self):
        result = BinaryConditionalOperator.from_syntax(
            self.syntax, self.syntax.greater_than_op
        )
        self.assertEqual(result, BinaryConditionalOperator.GREATER_THAN)

    def test_greater_than_equal_operator(self):
        result = BinaryConditionalOperator.from_syntax(
            self.syntax, self.syntax.greater_than_equal_op
        )
        self.assertEqual(result, BinaryConditionalOperator.GREATER_THAN_EQUAL)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            BinaryConditionalOperator.from_syntax(self.syntax, "invalid")


class TestIdentityConditionNodeAttributeReferences(ConditionNodeTestCase):
    def test_simple_identifier(self):
        self.assertEqual(IdentityConditionNode("a1").attribute_references(), ["a1"])

    def test_prefixed_identifier(self):
        self.assertEqual(
            IdentityConditionNode("alpha.a1").attribute_references(), ["alpha.a1"]
        )

    def test_underscore_identifier(self):
        self.assertEqual(IdentityConditionNode("_foo").attribute_references(), ["_foo"])

    def test_numeric_literal(self):
        self.assertEqual(IdentityConditionNode("42").attribute_references(), [])

    def test_decimal_literal(self):
        self.assertEqual(IdentityConditionNode("3.14").attribute_references(), [])

    def test_quoted_string(self):
        self.assertEqual(IdentityConditionNode("'hello'").attribute_references(), [])

    def test_double_quoted_string(self):
        self.assertEqual(IdentityConditionNode('"world"').attribute_references(), [])

    def test_empty_string(self):
        self.assertEqual(IdentityConditionNode("").attribute_references(), [])


class TestConditionNode(ConditionNodeTestCase):
    def test_identity_condition_node(self):
        node = IdentityConditionNode("alpha.a1")
        self.assertEqual(self.qtree_translator.translate_condition(node), "alpha.a1")
        self.assertEqual(self.sql_translator.translate_condition(node), "alpha.a1")
        self.assertEqual(node.attribute_references(), ["alpha.a1"])

    def test_unary_condition_node(self):
        child = IdentityConditionNode("alpha.a1")
        node = UnaryConditionNode(UnaryConditionalOperator.NOT, child)
        self.assertEqual(
            self.qtree_translator.translate_condition(node), "\\neg alpha.a1"
        )
        self.assertEqual(self.sql_translator.translate_condition(node), "NOT alpha.a1")
        self.assertEqual(node.attribute_references(), ["alpha.a1"])

    def test_binary_condition_node(self):
        left = IdentityConditionNode("alpha.a1")
        right = IdentityConditionNode("beta.b1")
        node = BinaryConditionNode(BinaryConditionalOperator.AND, left, right)
        self.assertEqual(
            self.qtree_translator.translate_condition(node), "(alpha.a1 \\land beta.b1)"
        )
        self.assertEqual(
            self.sql_translator.translate_condition(node), "(alpha.a1 AND beta.b1)"
        )
        self.assertEqual(node.attribute_references(), ["alpha.a1", "beta.b1"])
