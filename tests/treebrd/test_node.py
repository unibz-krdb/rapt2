from unittest import TestCase

from rapt2.treebrd.attributes import AttributeList
from rapt2.treebrd.condition_node import (
    BinaryConditionalOperator,
    BinaryConditionNode,
    IdentityConditionNode,
)
from rapt2.treebrd.errors import RelationReferenceError
from rapt2.treebrd.node import (
    CONDITIONAL_JOIN_OPERATORS,
    JOIN_OPERATORS,
    CrossJoinNode,
    Node,
    Operator,
    ProjectNode,
    RelationNode,
    SelectNode,
)
from rapt2.treebrd.schema import Schema


class NodeTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # logging.basicConfig(level=logging.NOTSET)
        pass

    def setUp(self):
        self.schema = Schema(
            {
                "alpha": ["a1"],
                "beta": ["b1", "b2"],
                "gamma": ["c1", "c2", "c3"],
                "twin": ["t1", "t2", "t3"],
                "twin_prime": ["t1", "t2", "t3"],
                "ambiguous": ["d1", "d1"],
            }
        )
        self.alpha = RelationNode("alpha", self.schema)
        self.beta = RelationNode("beta", self.schema)
        self.gamma = RelationNode("gamma", self.schema)
        self.twin = RelationNode("twin", self.schema)
        self.twin_prime = RelationNode("twin_prime", self.schema)
        self.ambiguous = RelationNode("ambiguous", self.schema)


class TestNode(TestCase):
    def test_operator_from_init(self):
        expected = Operator.relation
        actual = Node(Operator.relation, None).operator
        self.assertEqual(expected, actual)

    def test_name_when_init_has_none(self):
        node = Node(Operator.relation, None)
        self.assertIsNone(node.name)

    def test_name_when_init_has_name(self):
        expected = "alpha"
        actual = Node(Operator.relation, "alpha").name
        self.assertEqual(expected, actual)

    def test_attributes_from_init_when_none(self):
        actual = Node(Operator.relation, None).attributes
        self.assertIsNone(actual)


class TestNodeEquality(TestCase):
    def test_equality_when_identical(self):
        node = Node(Operator.relation, "borg")
        same = node
        self.assertTrue(node == same)

    def test_equality_when_same_operator_and_name(self):
        node = Node(Operator.relation, "borg")
        twin = Node(Operator.relation, "borg")
        self.assertTrue(node == twin)

    def test_non_equality_when_different_operator_and_name(self):
        node = Node(Operator.relation, "borg")
        other = Node(Operator.project, "other")
        self.assertTrue(node != other)

    def test_non_equality_when_different_operator(self):
        node = Node(Operator.relation, "borg")
        other = Node(Operator.project, "borg")
        self.assertTrue(node != other)

    def test_non_equality_when_different_name(self):
        node = Node(Operator.relation, "borg")
        other = Node(Operator.relation, "other")
        self.assertTrue(node != other)


class TestRelationNode(NodeTestCase):
    def test_operator_from_init(self):
        expected = Operator.relation
        actual = RelationNode("alpha", self.schema).operator
        self.assertEqual(expected, actual)

    def test_exception_raised_when_name_not_in_schema(self):
        self.assertRaises(RelationReferenceError, RelationNode, "unknown", self.schema)

    def test_attributes_when_name_is_in_schema(self):
        expected = AttributeList(self.schema.get_attributes("alpha"), "alpha").to_list()
        node = RelationNode("alpha", self.schema)
        self.assertEqual(expected, node.attributes.to_list())


class TestPostOrder(NodeTestCase):
    def test_relation_node_returns_self(self):
        result = self.alpha.post_order()
        self.assertEqual([self.alpha], result)

    def test_unary_project_returns_child_then_self(self):
        project = ProjectNode(self.beta, ["b1"])
        result = project.post_order()
        self.assertEqual(2, len(result))
        self.assertEqual(self.beta, result[0])
        self.assertEqual(project, result[1])

    def test_unary_select_returns_child_then_self(self):
        condition = BinaryConditionNode(
            BinaryConditionalOperator.EQUAL,
            IdentityConditionNode("a1"),
            IdentityConditionNode("a1"),
        )
        select = SelectNode(self.alpha, condition)
        result = select.post_order()
        self.assertEqual(2, len(result))
        self.assertEqual(self.alpha, result[0])
        self.assertEqual(select, result[1])

    def test_binary_join_returns_left_right_self(self):
        join = CrossJoinNode(self.alpha, self.beta)
        result = join.post_order()
        self.assertEqual(3, len(result))
        self.assertEqual(self.alpha, result[0])
        self.assertEqual(self.beta, result[1])
        self.assertEqual(join, result[2])

    def test_nested_unary_over_binary(self):
        join = CrossJoinNode(self.alpha, self.beta)
        project = ProjectNode(join, ["a1"])
        result = project.post_order()
        self.assertEqual(4, len(result))
        self.assertEqual(self.alpha, result[0])
        self.assertEqual(self.beta, result[1])
        self.assertEqual(join, result[2])
        self.assertEqual(project, result[3])

    def test_chained_binary_joins(self):
        left_join = CrossJoinNode(self.alpha, self.beta)
        outer_join = CrossJoinNode(left_join, self.gamma)
        result = outer_join.post_order()
        self.assertEqual(5, len(result))
        self.assertEqual(self.alpha, result[0])
        self.assertEqual(self.beta, result[1])
        self.assertEqual(left_join, result[2])
        self.assertEqual(self.gamma, result[3])
        self.assertEqual(outer_join, result[4])


class TestOperatorSets(TestCase):
    def test_join_operators_contains_all_join_types(self):
        expected = {
            Operator.cross_join,
            Operator.natural_join,
            Operator.theta_join,
            Operator.full_outer_join,
            Operator.left_outer_join,
            Operator.right_outer_join,
        }
        self.assertEqual(JOIN_OPERATORS, expected)

    def test_conditional_join_operators_subset_of_join_operators(self):
        self.assertTrue(CONDITIONAL_JOIN_OPERATORS < JOIN_OPERATORS)

    def test_conditional_join_operators_contains_theta_and_outer_joins(self):
        expected = {
            Operator.theta_join,
            Operator.full_outer_join,
            Operator.left_outer_join,
            Operator.right_outer_join,
        }
        self.assertEqual(CONDITIONAL_JOIN_OPERATORS, expected)

    def test_cross_and_natural_join_not_conditional(self):
        self.assertNotIn(Operator.cross_join, CONDITIONAL_JOIN_OPERATORS)
        self.assertNotIn(Operator.natural_join, CONDITIONAL_JOIN_OPERATORS)
