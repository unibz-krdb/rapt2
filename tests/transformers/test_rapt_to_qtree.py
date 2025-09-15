from rapt2.rapt import Rapt

from rapt2.transformers.qtree.constants import *
from rapt2.treebrd.grammars.extended_grammar import ExtendedGrammar
from rapt2.treebrd.grammars.dependency_grammar import DependencyGrammar
from tests.transformers.test_transfomer import TestTransformer


class TestQTreeTransformer(TestTransformer):
    def setUp(self):
        self.translate = self.translate_func(Rapt(grammar="Extended Grammar").to_qtree)


class TestQTreeDependencyTransformer(TestTransformer):
    def setUp(self):
        self.rapt = Rapt(grammar="Dependency Grammar")
        self.translate = self.translate_func(self.rapt.to_qtree)


class TestRelation(TestQTreeTransformer):
    def test_single_relation(self):
        ra = "alpha;"
        expected = [r"\Tree[.$alpha$ ]"]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)

    def test_multiple_relations(self):
        ra = "alpha; beta;"
        expected = [r"\Tree[.$alpha$ ]", r"\Tree[.$beta$ ]"]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)


class TestSelect(TestQTreeTransformer):
    def test_simple(self):
        ra = r"\select_{a1=a2} alpha;"
        expected = [r"\Tree[.${}_{{(a1 \eq a2)}}$ [.$alpha$ ] ]".format(SELECT_OP)]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)


class TestProject(TestQTreeTransformer):
    def test_simple(self):
        ra = r"\project_{a1, a2, a3} alpha;"
        expected = [r"\Tree[.${}_{{a1, a2, a3}}$ [.$alpha$ ] ]".format(PROJECT_OP)]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)


class TestRename(TestQTreeTransformer):
    def test_rename_relation(self):
        ra = r"\rename_{Apex} alpha;"
        expected = [r"\Tree[.${}_{{apex(a1, a2, a3)}}$ [.$alpha$ ] ]".format(RENAME_OP)]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)

    def test_rename_attributes(self):
        ra = r"\rename_{(a, b, c)} alpha;"
        expected = [r"\Tree[.${}_{{alpha(a, b, c)}}$ [.$alpha$ ] ]".format(RENAME_OP)]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)

    def test_rename_relation_and_attributes(self):
        ra = r"\rename_{apex(a, b, c)} alpha;"
        expected = [r"\Tree[.${}_{{apex(a, b, c)}}$ [.$alpha$ ] ]".format(RENAME_OP)]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)


class TestAssignment(TestQTreeTransformer):
    def test_relation(self):
        ra = "new_alpha := alpha;"
        expected = [r"\Tree[.$new_alpha(a1,a2,a3)$ [.$alpha$ ] ]"]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)

    def test_relation_with_attributes(self):
        ra = "new_alpha(a, b, c) := alpha;"
        expected = [r"\Tree[.$new_alpha(a,b,c)$ [.$alpha$ ] ]"]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)


class TestJoin(TestQTreeTransformer):
    def test_relation(self):
        ra = r"alpha \join beta;"
        expected = [r"\Tree[.${}$ [.$alpha$ ] [.$beta$ ] ]".format(JOIN_OP)]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)


class TestNaturalJoin(TestQTreeTransformer):
    grammar = ExtendedGrammar

    def test_relation(self):
        ra = r"alpha \natural_join beta;"
        expected = [r"\Tree[.${}$ [.$alpha$ ] [.$beta$ ] ]".format(NATURAL_JOIN_OP)]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)


class TestThetaJoin(TestQTreeTransformer):
    grammar = ExtendedGrammar

    def test_relation(self):
        ra = r"alpha \join_{a1 = b1} beta;"
        expected = [
            r"\Tree[.${}_{{(a1 \eq b1)}}$ [.$alpha$ ] [.$beta$ ] ]".format(
                THETA_JOIN_OP
            )
        ]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)


class TestFullOuterJoin(TestQTreeTransformer):
    grammar = ExtendedGrammar

    def test_relation(self):
        ra = r"alpha \full_outer_join_{a1 = b1} beta;"
        expected = [
            r"\Tree[.${}_{{(a1 \eq b1)}}$ [.$alpha$ ] [.$beta$ ] ]".format(
                FULL_OUTER_JOIN_OP
            )
        ]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)

    def test_complex_condition(self):
        ra = r"alpha \full_outer_join_{alpha.a1=beta.b1 and b3>50} beta;"
        expected = [
            r"\Tree[.${}_{{((alpha.a1 \eq beta.b1) \land (b3 \gt 50))}}$ [.$alpha$ ] [.$beta$ ] ]".format(
                FULL_OUTER_JOIN_OP
            )
        ]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)


class TestLeftOuterJoin(TestQTreeTransformer):
    grammar = ExtendedGrammar

    def test_relation(self):
        ra = r"alpha \left_outer_join_{a1 = b1} beta;"
        expected = [
            r"\Tree[.${}_{{(a1 \eq b1)}}$ [.$alpha$ ] [.$beta$ ] ]".format(
                LEFT_OUTER_JOIN_OP
            )
        ]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)

    def test_complex_condition(self):
        ra = r"alpha \left_outer_join_{alpha.a1=beta.b1 and b3>50} beta;"
        expected = [
            r"\Tree[.${}_{{((alpha.a1 \eq beta.b1) \land (b3 \gt 50))}}$ [.$alpha$ ] [.$beta$ ] ]".format(
                LEFT_OUTER_JOIN_OP
            )
        ]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)


class TestRightOuterJoin(TestQTreeTransformer):
    grammar = ExtendedGrammar

    def test_relation(self):
        ra = r"alpha \right_outer_join_{a1 = b1} beta;"
        expected = [
            r"\Tree[.${}_{{(a1 \eq b1)}}$ [.$alpha$ ] [.$beta$ ] ]".format(
                RIGHT_OUTER_JOIN_OP
            )
        ]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)

    def test_complex_condition(self):
        ra = r"alpha \right_outer_join_{alpha.a1=beta.b1 and b3>50} beta;"
        expected = [
            r"\Tree[.${}_{{((alpha.a1 \eq beta.b1) \land (b3 \gt 50))}}$ [.$alpha$ ] [.$beta$ ] ]".format(
                RIGHT_OUTER_JOIN_OP
            )
        ]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)


class TestUnion(TestQTreeTransformer):
    def test_simple(self):
        ra = r"gamma \union gammatwin;"
        expected = [r"\Tree[.${}$ [.$gamma$ ] [.$gammatwin$ ] ]".format(UNION_OP)]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)


class TestIntersect(TestQTreeTransformer):
    grammar = ExtendedGrammar

    def test_simple(self):
        ra = r"gamma \intersect gammatwin;"
        expected = [r"\Tree[.${}$ [.$gamma$ ] [.$gammatwin$ ] ]".format(INTERSECT_OP)]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)


class TestDifference(TestQTreeTransformer):
    def test_simple(self):
        ra = r"gamma \difference gammatwin;"
        expected = [r"\Tree[.${}$ [.$gamma$ ] [.$gammatwin$ ] ]".format(DIFFERENCE_OP)]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)


class TestFunctionalDependency(TestQTreeDependencyTransformer):
    def setUp(self):
        """Set up test fixtures with proper schema."""
        super().setUp()
        # Override the schema to include the attributes we need for functional dependencies
        self.schema = {"alpha": ["a", "b", "c"], "beta": ["c", "d", "e"], "gamma": ["id", "name", "value"]}
        # Update the translate function to use our custom schema
        self.translate = self.translate_func(self.rapt.to_qtree, schema=self.schema)

    def test_simple_functional_dependency(self):
        """Test simple functional dependency without select condition."""
        ra = "fd_{a, b} alpha;"
        expected = [r"\Tree[.$alpha : a \rightarrow b$ ]"]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)

    def test_functional_dependency_with_simple_select(self):
        """Test functional dependency with simple select condition."""
        ra = "fd_{a, b} \\select_{a = 1} alpha;"
        expected = [r"\Tree[.$\sigma_{(a \eq 1)} (alpha) : a \rightarrow b$ ]"]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)

    def test_functional_dependency_with_complex_select(self):
        """Test functional dependency with complex select condition."""
        ra = "fd_{a, b} \\select_{a = 1 and b > 0} alpha;"
        expected = [r"\Tree[.$\sigma_{((a \eq 1) \land (b \gt 0))} (alpha) : a \rightarrow b$ ]"]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)

    def test_functional_dependency_with_different_attributes(self):
        """Test functional dependency with different attribute names."""
        ra = "fd_{id, name} \\select_{id > 0} gamma;"
        expected = [r"\Tree[.$\sigma_{(id \gt 0)} (gamma) : id \rightarrow name$ ]"]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)

    def test_functional_dependency_with_or_condition(self):
        """Test functional dependency with OR condition in select."""
        ra = "fd_{a, b} \\select_{a = 1 or a = 2} alpha;"
        expected = [r"\Tree[.$\sigma_{((a \eq 1) \lor (a \eq 2))} (alpha) : a \rightarrow b$ ]"]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)

    def test_functional_dependency_with_not_condition(self):
        """Test functional dependency with NOT condition in select."""
        ra = "fd_{a, b} \\select_{not(a = 1)} alpha;"
        expected = [r"\Tree[.$\sigma_{\neg (a \eq 1)} (alpha) : a \rightarrow b$ ]"]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)

    def test_multiple_functional_dependencies(self):
        """Test multiple functional dependencies in one statement."""
        ra = "fd_{a, b} \\select_{a = 1} alpha; fd_{c, d} \\select_{c > 0} beta;"
        expected = [
            r"\Tree[.$\sigma_{(a \eq 1)} (alpha) : a \rightarrow b$ ]",
            r"\Tree[.$\sigma_{(c \gt 0)} (beta) : c \rightarrow d$ ]"
        ]
        actual = self.translate(ra)
        self.assertEqual(expected, actual)
