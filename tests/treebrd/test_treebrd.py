import functools
from unittest import TestCase

from rapt2.treebrd.condition_node import (
    BinaryConditionalOperator,
    BinaryConditionNode,
    IdentityConditionNode,
)
from rapt2.treebrd.errors import RelationReferenceError
from rapt2.treebrd.grammars import DependencyGrammar
from rapt2.treebrd.node import (
    CrossJoinNode,
    FunctionalDependencyNode,
    InclusionEquivalenceNode,
    InclusionSubsumptionNode,
    MultivaluedDependencyNode,
    NaturalJoinNode,
    PrimaryKeyNode,
    ProjectNode,
    RelationNode,
    SelectNode,
    ThetaJoinNode,
)
from rapt2.treebrd.schema import Schema
from rapt2.treebrd.treebrd import TreeBRD


class TreeBRDTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = None

    @classmethod
    def create_build_function(cls, schema):
        builder = TreeBRD(DependencyGrammar())
        return functools.partial(builder.build, schema=schema)


class TestRelation(TreeBRDTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.definition = {
            "letters": ["position", "value"],
            "numbers": ["value", "prime"],
        }
        cls.schema = Schema(cls.definition)
        cls.build = staticmethod(cls.create_build_function(cls.definition))

    def test_build_when_instring_is_single_relation(self):
        forest = self.build("letters;")
        self.assertEqual(1, len(forest))
        expected = RelationNode("letters", self.schema)
        self.assertEqual(expected, forest[0])

    def test_build_when_instring_has_multiple_relations(self):
        instring = "numbers; letters;"
        forest = self.build(instring)
        self.assertEqual(2, len(forest))
        first = RelationNode("numbers", self.schema)
        second = RelationNode("letters", self.schema)
        self.assertEqual(first, forest[0])
        self.assertEqual(second, forest[1])


class TestProject(TreeBRDTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.definition = {
            "magic_wand": [
                "owner",
                "manufacturer",
                "wood",
                "core",
                "length",
                "rigidity",
            ]
        }
        cls.schema = Schema(cls.definition)
        cls.build = staticmethod(cls.create_build_function(cls.definition))

    def test_project_with_single_attr(self):
        instring = r"\project_{owner} magic_wand;"
        forest = self.build(instring)
        child = RelationNode("magic_wand", self.schema)
        expected = ProjectNode(child, ["owner"])
        self.assertEqual(expected, forest[0])

    def test_project_with_two_attr(self):
        instring = r"\project_{owner, wood} magic_wand;"
        forest = self.build(instring)
        child = RelationNode("magic_wand", self.schema)
        expected = ProjectNode(child, ["owner", "wood"])
        self.assertEqual(expected, forest[0])

    def test_project_with_all_but_one_attr(self):
        attr = self.schema.get_attributes("magic_wand")
        attr.remove("rigidity")
        instring = r"\project_{" + ", ".join(attr) + r"} magic_wand;"
        forest = self.build(instring)
        child = RelationNode("magic_wand", self.schema)
        expected = ProjectNode(child, attr)
        self.assertEqual(expected, forest[0])

    def test_project_with_all_attr(self):
        attr = self.schema.get_attributes("magic_wand")
        instring = r"\project_{" + ", ".join(attr) + r"} magic_wand;"
        forest = self.build(instring)
        child = RelationNode("magic_wand", self.schema)
        expected = ProjectNode(child, attr)
        self.assertEqual(expected, forest[0])

    def test_project_with_all_attr_shuffled(self):
        attr = self.schema.get_attributes("magic_wand")
        attr.sort()
        instring = r"\project_{" + ", ".join(attr) + r"} magic_wand;"
        forest = self.build(instring)
        child = RelationNode("magic_wand", self.schema)
        expected = ProjectNode(child, attr)
        self.assertEqual(expected, forest[0])


class JoinTestCase(TreeBRDTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.definition = {
            "alpha": ["a1"],
            "beta": ["b1", "b2"],
            "gamma": ["c1", "c2", "c3"],
        }
        cls.schema = Schema(cls.definition)
        cls.build = staticmethod(cls.create_build_function(cls.definition))


class TestJoins(JoinTestCase):
    def test_join_with_natural_join(self):
        instring = "alpha \\join beta \\natural_join gamma;"
        forest = self.build(instring)
        left = RelationNode("alpha", self.schema)
        middle = RelationNode("beta", self.schema)
        right = RelationNode("gamma", self.schema)
        intermediate = CrossJoinNode(left, middle)
        expected = NaturalJoinNode(intermediate, right)
        self.assertEqual(expected, forest[0])

    def test_natural_join_with_join(self):
        instring = "alpha \\natural_join beta \\join gamma;"
        forest = self.build(instring)
        left = RelationNode("alpha", self.schema)
        middle = RelationNode("beta", self.schema)
        right = RelationNode("gamma", self.schema)
        intermediate = NaturalJoinNode(left, middle)
        expected = CrossJoinNode(intermediate, right)
        self.assertEqual(expected, forest[0])

    def test_join_with_theta_join(self):
        instring = "alpha \\join beta \\theta_join_{a1 = c1} gamma;"
        forest = self.build(instring)
        left = RelationNode("alpha", self.schema)
        middle = RelationNode("beta", self.schema)
        right = RelationNode("gamma", self.schema)
        intermediate = CrossJoinNode(left, middle)
        condition = BinaryConditionNode(
            BinaryConditionalOperator.EQUAL,
            IdentityConditionNode("a1"),
            IdentityConditionNode("c1"),
        )
        expected = ThetaJoinNode(intermediate, right, condition)
        self.assertEqual(expected, forest[0])

    def test_theta_join_with_join(self):
        instring = "alpha \\theta_join_{a1 = b1} beta \\join gamma;"
        forest = self.build(instring)
        left = RelationNode("alpha", self.schema)
        middle = RelationNode("beta", self.schema)
        right = RelationNode("gamma", self.schema)
        condition = BinaryConditionNode(
            BinaryConditionalOperator.EQUAL,
            IdentityConditionNode("a1"),
            IdentityConditionNode("b1"),
        )
        intermediate = ThetaJoinNode(left, middle, condition)
        expected = CrossJoinNode(intermediate, right)
        self.assertEqual(expected, forest[0])


class TestCrossJoin(JoinTestCase):
    def test_join_two_separate_relations(self):
        instring = "alpha \\join beta;"
        forest = self.build(instring)
        left = RelationNode("alpha", self.schema)
        right = RelationNode("beta", self.schema)
        expected = CrossJoinNode(left, right)
        self.assertEqual(expected, forest[0])

    def test_join_three_separate_relations(self):
        instring = "alpha \\join beta \\join gamma;"
        forest = self.build(instring)
        left = RelationNode("alpha", self.schema)
        middle = RelationNode("beta", self.schema)
        right = RelationNode("gamma", self.schema)
        intermediate = CrossJoinNode(left, middle)
        expected = CrossJoinNode(intermediate, right)
        self.assertEqual(expected, forest[0])

    def test_exception_when_join_two_identical_relations(self):
        left = RelationNode("alpha", self.schema)
        right = RelationNode("alpha", self.schema)
        self.assertRaises(RelationReferenceError, CrossJoinNode, left, right)


class TestThetaJoin(JoinTestCase):
    def test_join_two_separate_relations(self):
        instring = "alpha \\theta_join_{a1 = b1} beta;"
        forest = self.build(instring)
        left = RelationNode("alpha", self.schema)
        right = RelationNode("beta", self.schema)
        condition = BinaryConditionNode(
            BinaryConditionalOperator.EQUAL,
            IdentityConditionNode("a1"),
            IdentityConditionNode("b1"),
        )
        expected = ThetaJoinNode(left, right, condition)
        self.assertEqual(expected, forest[0])

    def test_join_three_separate_relations(self):
        instring = "alpha \\theta_join_{a1 = b1} beta \\theta_join_{a1 = b1} gamma;"
        forest = self.build(instring)
        left = RelationNode("alpha", self.schema)
        middle = RelationNode("beta", self.schema)
        right = RelationNode("gamma", self.schema)
        condition = BinaryConditionNode(
            BinaryConditionalOperator.EQUAL,
            IdentityConditionNode("a1"),
            IdentityConditionNode("b1"),
        )
        intermediate = ThetaJoinNode(left, middle, condition)
        expected = ThetaJoinNode(intermediate, right, condition)
        self.assertEqual(expected, forest[0])

    def test_exception_when_join_two_identical_relations(self):
        left = RelationNode("alpha", self.schema)
        right = RelationNode("alpha", self.schema)
        self.assertRaises(RelationReferenceError, ThetaJoinNode, left, right, "a1=5")


class TestNaturalJoin(JoinTestCase):
    def test_join_two_separate_relations(self):
        instring = "alpha \\natural_join beta;"
        forest = self.build(instring)
        left = RelationNode("alpha", self.schema)
        right = RelationNode("beta", self.schema)
        expected = NaturalJoinNode(left, right)
        self.assertEqual(expected, forest[0])

    def test_join_three_separate_relations(self):
        instring = "alpha \\natural_join beta \\natural_join gamma;"
        forest = self.build(instring)
        left = RelationNode("alpha", self.schema)
        middle = RelationNode("beta", self.schema)
        right = RelationNode("gamma", self.schema)
        intermediate = NaturalJoinNode(left, middle)
        expected = NaturalJoinNode(intermediate, right)
        self.assertEqual(expected, forest[0])

    def test_exception_when_join_two_identical_relations(self):
        left = RelationNode("alpha", self.schema)
        right = RelationNode("alpha", self.schema)
        self.assertRaises(RelationReferenceError, NaturalJoinNode, left, right)


class DependencyTestCase(TreeBRDTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.definition = {
            "alpha": ["a1"],
            "beta": ["b1", "b2"],
        }
        cls.schema = Schema(cls.definition)
        cls.build = staticmethod(cls.create_build_function(cls.definition))


class TestIsDependencyStatement(DependencyTestCase):
    def setUp(self):
        self.builder = TreeBRD(DependencyGrammar())

    def test_pk_is_dependency(self):
        ra = self.builder.grammar.parse("pk_{a1} alpha;")
        self.assertTrue(self.builder.is_dependency_statement(ra[0]))

    def test_mvd_is_dependency(self):
        ra = self.builder.grammar.parse("mvd_{a1, a1} alpha;")
        self.assertTrue(self.builder.is_dependency_statement(ra[0]))

    def test_fd_is_dependency(self):
        ra = self.builder.grammar.parse("fd_{a1, a1} alpha;")
        self.assertTrue(self.builder.is_dependency_statement(ra[0]))

    def test_relation_is_not_dependency(self):
        ra = self.builder.grammar.parse("alpha;")
        self.assertFalse(self.builder.is_dependency_statement(ra[0]))

    def test_empty_is_not_dependency(self):
        from pyparsing import ParseResults

        self.assertFalse(self.builder.is_dependency_statement(ParseResults([])))

    def test_single_element_is_not_dependency(self):
        from pyparsing import ParseResults

        self.assertFalse(self.builder.is_dependency_statement(ParseResults(["x"])))


class TestCreateDependencyNode(DependencyTestCase):
    def test_pk_node(self):
        forest = self.build("pk_{a1} alpha;")
        self.assertEqual(1, len(forest))
        node = forest[0]
        self.assertIsInstance(node, PrimaryKeyNode)
        self.assertEqual(node.relation_name, "alpha")

    def test_mvd_node(self):
        forest = self.build("mvd_{a1, a1} alpha;")
        self.assertEqual(1, len(forest))
        node = forest[0]
        self.assertIsInstance(node, MultivaluedDependencyNode)
        self.assertEqual(node.relation_name, "alpha")
        self.assertIsInstance(node.child, RelationNode)

    def test_fd_node(self):
        forest = self.build("fd_{a1, a1} alpha;")
        self.assertEqual(1, len(forest))
        node = forest[0]
        self.assertIsInstance(node, FunctionalDependencyNode)
        self.assertEqual(node.relation_name, "alpha")
        self.assertIsInstance(node.child, RelationNode)

    def test_mvd_with_select(self):
        forest = self.build("mvd_{a1, a1} \\select_{a1 = a1} alpha;")
        self.assertEqual(1, len(forest))
        node = forest[0]
        self.assertIsInstance(node, MultivaluedDependencyNode)
        self.assertEqual(node.relation_name, "alpha")
        self.assertIsInstance(node.child, SelectNode)

    def test_fd_with_select(self):
        forest = self.build("fd_{a1, a1} \\select_{a1 = a1} alpha;")
        self.assertEqual(1, len(forest))
        node = forest[0]
        self.assertIsInstance(node, FunctionalDependencyNode)
        self.assertEqual(node.relation_name, "alpha")
        self.assertIsInstance(node.child, SelectNode)

    def test_inc_equiv_simple(self):
        forest = self.build("inc=_{a1, b1} (alpha, beta);")
        self.assertEqual(1, len(forest))
        node = forest[0]
        self.assertIsInstance(node, InclusionEquivalenceNode)

    def test_inc_subset_simple(self):
        forest = self.build("inc⊆_{a1, b1} (alpha, beta);")
        self.assertEqual(1, len(forest))
        node = forest[0]
        self.assertIsInstance(node, InclusionSubsumptionNode)

    def test_dependency_mixed_with_ra(self):
        forest = self.build("pk_{a1} alpha; alpha;")
        self.assertEqual(2, len(forest))
        self.assertIsInstance(forest[0], PrimaryKeyNode)
        self.assertIsInstance(forest[1], RelationNode)


class TestAssignmentSchemaUpdate(TreeBRDTestCase):
    """Verify that assignment through TreeBRD.build() updates the schema."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.definition = {
            "alpha": ["a1"],
            "beta": ["b1", "b2"],
        }

    def test_schema_updated_after_assign(self):
        builder = TreeBRD(DependencyGrammar())
        forest = builder.build("omega := beta;", dict(self.definition))
        node = forest[0]
        self.assertEqual(node.name, "omega")
        self.assertEqual(node.attributes.names, ["b1", "b2"])

    def test_schema_updated_with_renamed_attributes(self):
        builder = TreeBRD(DependencyGrammar())
        forest = builder.build("omega(x, y) := beta;", dict(self.definition))
        node = forest[0]
        self.assertEqual(node.name, "omega")
        self.assertEqual(node.attributes.names, ["x", "y"])

    def test_assigned_relation_usable_in_subsequent_statement(self):
        builder = TreeBRD(DependencyGrammar())
        schema = dict(self.definition)
        forest = builder.build("omega := alpha; omega;", schema)
        self.assertEqual(2, len(forest))
        self.assertIsInstance(forest[1], RelationNode)
        self.assertEqual(forest[1].name, "omega")


class TestExtractBinaryParts(TestCase):
    """Tests for TreeBRD._extract_binary_parts static method."""

    @classmethod
    def setUpClass(cls):
        from pyparsing import ParseResults

        cls.ParseResults = ParseResults

    def _make_pr(self, items):
        """Create a ParseResults from a list of items."""
        return self.ParseResults(items)

    def test_without_params(self):
        # [..., operator, right] → op at -2, no param
        exp = self._make_pr(["A", "\\join", "B"])
        parts = TreeBRD._extract_binary_parts(exp)
        self.assertEqual(parts.operator, "\\join")
        self.assertIsNone(parts.operator_params)
        self.assertEqual(list(parts.right), ["B"])

    def test_with_params(self):
        # [..., operator, param, right] → op at -3
        param = self._make_pr(["cond"])
        exp = self._make_pr(["A", "\\theta_join", param, "B"])
        parts = TreeBRD._extract_binary_parts(exp)
        self.assertEqual(parts.operator, "\\theta_join")
        self.assertEqual(list(parts.operator_params), ["cond"])
        self.assertEqual(list(parts.right), ["B"])

    def test_left_captures_everything_before_operator(self):
        exp = self._make_pr(["A", "\\join", "B", "\\union", "C"])
        parts = TreeBRD._extract_binary_parts(exp)
        # Rightmost operator is \union at -2
        self.assertEqual(parts.operator, "\\union")
        self.assertEqual(list(parts.left), ["A", "\\join", "B"])
        self.assertEqual(list(parts.right), ["C"])
