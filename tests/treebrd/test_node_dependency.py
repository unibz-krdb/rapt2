from unittest import TestCase

from rapt2.treebrd.node import (
    DependencyNode,
    FunctionalDependencyNode,
    InclusionEquivalenceNode,
    InclusionSubsumptionNode,
    MultivaluedDependencyNode,
    Operator,
    PrimaryKeyNode,
    RelationNode,
)
from rapt2.treebrd.schema import Schema


class DependencyNodeTestCase(TestCase):
    def setUp(self):
        self.schema = Schema(
            {
                "alpha": ["a1"],
                "beta": ["b1", "b2"],
                "gamma": ["c1", "c2", "c3"],
            }
        )
        self.alpha = RelationNode("alpha", self.schema)
        self.beta = RelationNode("beta", self.schema)


class TestDependencyNode(DependencyNodeTestCase):
    def test_operator(self):
        node = DependencyNode(Operator.primary_key, "alpha", ["a1"])
        self.assertEqual(node.operator, Operator.primary_key)

    def test_relation_name(self):
        node = DependencyNode(Operator.primary_key, "alpha", ["a1"])
        self.assertEqual(node.relation_name, "alpha")

    def test_attributes(self):
        node = DependencyNode(Operator.primary_key, "alpha", ["a1"])
        self.assertEqual(node.attributes, ["a1"])

    def test_post_order(self):
        node = DependencyNode(Operator.primary_key, "alpha", ["a1"])
        self.assertEqual(node.post_order(), [node])

    def test_equality_identical(self):
        node = DependencyNode(Operator.primary_key, "alpha", ["a1"])
        other = DependencyNode(Operator.primary_key, "alpha", ["a1"])
        self.assertEqual(node, other)

    def test_inequality_different_relation(self):
        node = DependencyNode(Operator.primary_key, "alpha", ["a1"])
        other = DependencyNode(Operator.primary_key, "beta", ["a1"])
        self.assertNotEqual(node, other)

    def test_inequality_different_attributes(self):
        node = DependencyNode(Operator.primary_key, "alpha", ["a1"])
        other = DependencyNode(Operator.primary_key, "alpha", ["a2"])
        self.assertNotEqual(node, other)

    def test_inequality_different_operator(self):
        node = DependencyNode(Operator.primary_key, "alpha", ["a1"])
        other = DependencyNode(Operator.functional_dependency, "alpha", ["a1"])
        self.assertNotEqual(node, other)


class TestPrimaryKeyNode(DependencyNodeTestCase):
    def test_operator(self):
        node = PrimaryKeyNode("alpha", ["a1"])
        self.assertEqual(node.operator, Operator.primary_key)

    def test_relation_name(self):
        node = PrimaryKeyNode("alpha", ["a1"])
        self.assertEqual(node.relation_name, "alpha")

    def test_attributes(self):
        node = PrimaryKeyNode("beta", ["b1", "b2"])
        self.assertEqual(node.attributes, ["b1", "b2"])

    def test_post_order(self):
        node = PrimaryKeyNode("alpha", ["a1"])
        self.assertEqual(node.post_order(), [node])

    def test_equality(self):
        node = PrimaryKeyNode("alpha", ["a1"])
        other = PrimaryKeyNode("alpha", ["a1"])
        self.assertEqual(node, other)

    def test_inequality(self):
        node = PrimaryKeyNode("alpha", ["a1"])
        other = PrimaryKeyNode("beta", ["b1"])
        self.assertNotEqual(node, other)


class TestMultivaluedDependencyNode(DependencyNodeTestCase):
    def test_operator(self):
        node = MultivaluedDependencyNode("alpha", ["a1"], self.alpha)
        self.assertEqual(node.operator, Operator.multivalued_dependency)

    def test_relation_name(self):
        node = MultivaluedDependencyNode("alpha", ["a1"], self.alpha)
        self.assertEqual(node.relation_name, "alpha")

    def test_attributes(self):
        node = MultivaluedDependencyNode("alpha", ["a1"], self.alpha)
        self.assertEqual(node.attributes, ["a1"])

    def test_child(self):
        node = MultivaluedDependencyNode("alpha", ["a1"], self.alpha)
        self.assertEqual(node.child, self.alpha)

    def test_equality(self):
        node = MultivaluedDependencyNode("alpha", ["a1"], self.alpha)
        other = MultivaluedDependencyNode("alpha", ["a1"], self.alpha)
        self.assertEqual(node, other)

    def test_inequality_different_child(self):
        node = MultivaluedDependencyNode("alpha", ["a1"], self.alpha)
        other = MultivaluedDependencyNode("alpha", ["a1"], self.beta)
        self.assertNotEqual(node, other)


class TestFunctionalDependencyNode(DependencyNodeTestCase):
    def test_operator(self):
        node = FunctionalDependencyNode("alpha", ["a1"], self.alpha)
        self.assertEqual(node.operator, Operator.functional_dependency)

    def test_relation_name(self):
        node = FunctionalDependencyNode("alpha", ["a1"], self.alpha)
        self.assertEqual(node.relation_name, "alpha")

    def test_attributes(self):
        node = FunctionalDependencyNode("alpha", ["a1"], self.alpha)
        self.assertEqual(node.attributes, ["a1"])

    def test_child(self):
        node = FunctionalDependencyNode("alpha", ["a1"], self.alpha)
        self.assertEqual(node.child, self.alpha)

    def test_equality(self):
        node = FunctionalDependencyNode("alpha", ["a1"], self.alpha)
        other = FunctionalDependencyNode("alpha", ["a1"], self.alpha)
        self.assertEqual(node, other)

    def test_inequality_different_child(self):
        node = FunctionalDependencyNode("alpha", ["a1"], self.alpha)
        other = FunctionalDependencyNode("alpha", ["a1"], self.beta)
        self.assertNotEqual(node, other)


class TestInclusionEquivalenceNode(DependencyNodeTestCase):
    def test_operator(self):
        node = InclusionEquivalenceNode(
            ["alpha", "beta"], ["a1", "b1"], self.alpha, self.beta
        )
        self.assertEqual(node.operator, Operator.inclusion_equivalence)

    def test_relation_names(self):
        node = InclusionEquivalenceNode(
            ["alpha", "beta"], ["a1", "b1"], self.alpha, self.beta
        )
        self.assertEqual(node.relation_names, ["alpha", "beta"])

    def test_attributes(self):
        node = InclusionEquivalenceNode(
            ["alpha", "beta"], ["a1", "b1"], self.alpha, self.beta
        )
        self.assertEqual(node.attributes, ["a1", "b1"])

    def test_children(self):
        node = InclusionEquivalenceNode(
            ["alpha", "beta"], ["a1", "b1"], self.alpha, self.beta
        )
        self.assertEqual(node.left_child, self.alpha)
        self.assertEqual(node.right_child, self.beta)

    def test_equality(self):
        node = InclusionEquivalenceNode(
            ["alpha", "beta"], ["a1", "b1"], self.alpha, self.beta
        )
        other = InclusionEquivalenceNode(
            ["alpha", "beta"], ["a1", "b1"], self.alpha, self.beta
        )
        self.assertEqual(node, other)

    def test_inequality_different_children(self):
        node = InclusionEquivalenceNode(
            ["alpha", "beta"], ["a1", "b1"], self.alpha, self.beta
        )
        other = InclusionEquivalenceNode(
            ["alpha", "beta"], ["a1", "b1"], self.beta, self.alpha
        )
        self.assertNotEqual(node, other)

    def test_inequality_different_relation_names(self):
        node = InclusionEquivalenceNode(
            ["alpha", "beta"], ["a1", "b1"], self.alpha, self.beta
        )
        other = InclusionEquivalenceNode(
            ["beta", "alpha"], ["a1", "b1"], self.alpha, self.beta
        )
        self.assertNotEqual(node, other)


class TestInclusionSubsumptionNode(DependencyNodeTestCase):
    def test_operator(self):
        node = InclusionSubsumptionNode(
            ["alpha", "beta"], ["a1", "b1"], self.alpha, self.beta
        )
        self.assertEqual(node.operator, Operator.inclusion_subsumption)

    def test_relation_names(self):
        node = InclusionSubsumptionNode(
            ["alpha", "beta"], ["a1", "b1"], self.alpha, self.beta
        )
        self.assertEqual(node.relation_names, ["alpha", "beta"])

    def test_attributes(self):
        node = InclusionSubsumptionNode(
            ["alpha", "beta"], ["a1", "b1"], self.alpha, self.beta
        )
        self.assertEqual(node.attributes, ["a1", "b1"])

    def test_children(self):
        node = InclusionSubsumptionNode(
            ["alpha", "beta"], ["a1", "b1"], self.alpha, self.beta
        )
        self.assertEqual(node.left_child, self.alpha)
        self.assertEqual(node.right_child, self.beta)

    def test_equality(self):
        node = InclusionSubsumptionNode(
            ["alpha", "beta"], ["a1", "b1"], self.alpha, self.beta
        )
        other = InclusionSubsumptionNode(
            ["alpha", "beta"], ["a1", "b1"], self.alpha, self.beta
        )
        self.assertEqual(node, other)

    def test_inequality_different_children(self):
        node = InclusionSubsumptionNode(
            ["alpha", "beta"], ["a1", "b1"], self.alpha, self.beta
        )
        other = InclusionSubsumptionNode(
            ["alpha", "beta"], ["a1", "b1"], self.beta, self.alpha
        )
        self.assertNotEqual(node, other)
