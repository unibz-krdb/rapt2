import unittest

from pyparsing import ParseException

from rapt2.treebrd.grammars.core_grammar import CoreGrammar


class TestDifference(unittest.TestCase):
    def setUp(self):
        self.parser = CoreGrammar()

    def test_simple(self):
        expression = "astronauts \\difference cosmonauts;"
        expected = [[["astronauts"], "\\difference", ["cosmonauts"]]]
        actual = self.parser.statements.parseString(expression).asList()
        self.assertEqual(expected, actual)

    def test_multiple(self):
        expression = "a \\difference b \\difference c;"
        expected = [[["a"], "\\difference", ["b"], "\\difference", ["c"]]]
        actual = self.parser.statements.parseString(expression).asList()
        self.assertEqual(expected, actual)

    def test_precedence_with_join(self):
        expression = "a \\difference b \\join c;"
        expected = [[["a"], "\\difference", [["b"], "\\join", ["c"]]]]
        actual = self.parser.statements.parseString(expression).asList()
        self.assertEqual(expected, actual)

    def test_precedence_join_before_difference(self):
        expression = "a \\join b \\difference c;"
        expected = [[[["a"], "\\join", ["b"]], "\\difference", ["c"]]]
        actual = self.parser.statements.parseString(expression).asList()
        self.assertEqual(expected, actual)

    def test_with_unary(self):
        expression = "\\project_{x} a \\difference \\project_{x} b;"
        expected = [
            [
                ["\\project", ["x"], ["a"]],
                "\\difference",
                ["\\project", ["x"], ["b"]],
            ]
        ]
        actual = self.parser.statements.parseString(expression).asList()
        self.assertEqual(expected, actual)

    def test_with_parentheses(self):
        expression = "a \\difference (b \\difference c);"
        expected = [[["a"], "\\difference", [["b"], "\\difference", ["c"]]]]
        actual = self.parser.statements.parseString(expression).asList()
        self.assertEqual(expected, actual)

    # Exceptions

    def test_exp_no_relations(self):
        expression = "\\difference;"
        self.assertRaises(
            ParseException, self.parser.statements.parseString, expression
        )

    def test_exp_left_only(self):
        expression = "astronauts \\difference;"
        self.assertRaises(
            ParseException, self.parser.statements.parseString, expression
        )

    def test_exp_right_only(self):
        expression = "\\difference cosmonauts;"
        self.assertRaises(
            ParseException, self.parser.statements.parseString, expression
        )
