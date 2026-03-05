from unittest import TestCase

from rapt2.treebrd.grammars.syntax import DependencySyntax, Syntax


class TestSyntax(TestCase):
    def test___init__when_operator_is_changed(self):
        new_op = "test_op"
        self.assertEqual(new_op, Syntax(and_op=new_op).and_op)

    def test___init__cannot_set_unknown_attributes(self):
        self.assertFalse(hasattr(Syntax(foo="bar"), "foo"))


class TestDependencyOperators(TestCase):
    def test_dependency_operators_returns_all_five_defaults(self):
        syntax = DependencySyntax()
        ops = syntax.dependency_operators
        self.assertEqual(ops, ("pk", "mvd", "fd", "inc=", "inc⊆"))

    def test_dependency_operators_reflects_overrides(self):
        syntax = DependencySyntax(pk_op="PK", fd_op="FD")
        ops = syntax.dependency_operators
        self.assertEqual(ops, ("PK", "mvd", "FD", "inc=", "inc⊆"))

    def test_dependency_operators_returns_tuple(self):
        syntax = DependencySyntax()
        self.assertIsInstance(syntax.dependency_operators, tuple)
