from typing import Union, List
from ..base_translator import BaseTranslator
from .operators import latex_operator
from ...treebrd.node import (
    Node,
    RelationNode,
    SelectNode,
    ProjectNode,
    RenameNode,
    AssignNode,
    ThetaJoinNode,
    CrossJoinNode,
    NaturalJoinNode,
    FullOuterJoinNode,
    LeftOuterJoinNode,
    RightOuterJoinNode,
    UnionNode,
    DifferenceNode,
    IntersectNode,
    PrimaryKeyNode,
    MultivaluedDependencyNode,
    FunctionalDependencyNode,
    InclusionEquivalenceNode,
    InclusionSubsumptionNode,
)


class Translator(BaseTranslator):
    """
    A Translator defining the operations for translating a relational algebra
    statement into a latex tree output.
    """

    def _get_latex_operator(self, operator):
        """
        Get the LaTeX operator for a given operator.
        For now, we use the hardcoded mapping, but this could be extended
        to use syntax-based mappings in the future.
        """
        return latex_operator[operator]

    def relation(self, node: RelationNode) -> str:
        """
        Translate a relation node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return "[.${}$ ]".format(node.name)

    def select(self, node: SelectNode) -> str:
        """
        Translate a select node into a latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        child = self.translate(node.child)
        return "[.${op}_{{{conditions}}}$ {child} ]".format(
            op=self._get_latex_operator(node.operator),
            conditions=node.conditions.to_latex(),
            child=child,
        )

    def project(self, node: ProjectNode) -> str:
        """
        Translate a project node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        child = self.translate(node.child)
        return "[.${op}_{{{attributes}}}$ {child} ]".format(
            op=self._get_latex_operator(node.operator),
            attributes=", ".join(node.attributes.names),
            child=child,
        )

    def rename(self, node: RenameNode) -> str:
        """
        Translate a rename node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        child = self.translate(node.child)
        attributes = ""
        if node.attributes:
            attributes = "({})".format(", ".join(node.attributes.names))
        return "[.${op}_{{{name}{attributes}}}$ {child} ]".format(
            op=self._get_latex_operator(node.operator),
            name=node.name,
            attributes=attributes,
            child=child,
        )

    def assign(self, node: AssignNode) -> str:
        """
        Translate an assign node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        child = self.translate(node.child)
        attributes = ""
        if node.attributes:
            attributes = "({})".format(",".join(node.attributes.names))
        return "[.${name}{attributes}$ {child} ]".format(
            name=node.name, attributes=attributes, child=child
        )

    def theta_join(self, node: ThetaJoinNode) -> str:
        """
        Translate a join node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return "[.${op}_{{{conditions}}}$ {left} {right} ]".format(
            op=self._get_latex_operator(node.operator),
            conditions=node.conditions.to_latex(),
            left=self.translate(node.left),
            right=self.translate(node.right),
        )

    def cross_join(self, node: CrossJoinNode) -> str:
        """
        Translate a cross node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return self._binary(node)

    def natural_join(self, node: NaturalJoinNode) -> str:
        """
        Translate a natural join node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return self._binary(node)

    def full_outer_join(self, node: FullOuterJoinNode) -> str:
        """
        Translate a full outer join node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return "[.${op}_{{{conditions}}}$ {left} {right} ]".format(
            op=self._get_latex_operator(node.operator),
            conditions=node.conditions.to_latex(),
            left=self.translate(node.left),
            right=self.translate(node.right),
        )

    def left_outer_join(self, node: LeftOuterJoinNode) -> str:
        """
        Translate a left outer join node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return "[.${op}_{{{conditions}}}$ {left} {right} ]".format(
            op=self._get_latex_operator(node.operator),
            conditions=node.conditions.to_latex(),
            left=self.translate(node.left),
            right=self.translate(node.right),
        )

    def right_outer_join(self, node: RightOuterJoinNode) -> str:
        """
        Translate a right outer join node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return "[.${op}_{{{conditions}}}$ {left} {right} ]".format(
            op=self._get_latex_operator(node.operator),
            conditions=node.conditions.to_latex(),
            left=self.translate(node.left),
            right=self.translate(node.right),
        )

    def union(self, node: UnionNode) -> str:
        """
        Translate a union node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return self._binary(node)

    def difference(self, node: DifferenceNode) -> str:
        """
        Translate a difference node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return self._binary(node)

    def intersect(self, node: IntersectNode) -> str:
        """
        Translate an intersect node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return self._binary(node)

    def _binary(self, node: Union[CrossJoinNode, NaturalJoinNode, UnionNode, DifferenceNode, IntersectNode]) -> str:
        """
        Translate a binary node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return "[.${op}$ {left} {right} ]".format(
            op=self._get_latex_operator(node.operator),
            left=self.translate(node.left),
            right=self.translate(node.right),
        )

    def primary_key(self, node: PrimaryKeyNode) -> str:
        """
        Translate a primary key dependency node into a latex qtree node.
        :param node: a dependency node
        :return: a qtree subtree rooted at the node
        """
        attributes = ", ".join(node.attributes)
        return "[.${op}_{{{attributes}}}({relation})$ ]".format(
            op=self._get_latex_operator(node.operator),
            attributes=attributes,
            relation=node.relation_name,
        )

    def multivalued_dependency(self, node: MultivaluedDependencyNode) -> str:
        """
        Translate a multivalued dependency node into a latex qtree node.
        :param node: a dependency node
        :return: a qtree subtree rooted at the node
        """
        attributes = ", ".join(node.attributes)
        return "[.${op}_{{{attributes}}}({relation})$ ]".format(
            op=self._get_latex_operator(node.operator),
            attributes=attributes,
            relation=node.relation_name,
        )

    def functional_dependency(self, node: FunctionalDependencyNode) -> str:
        """
        Translate a functional dependency node into a latex qtree node.
        :param node: a dependency node
        :return: a qtree subtree rooted at the node
        """
        left_attr, right_attr = node.attributes
        op = self._get_latex_operator(node.operator)
        child = self.translate(node.child)
        return f"[.${left_attr} {op} {right_attr}$ {child} ]"

    def inclusion_equivalence(self, node: InclusionEquivalenceNode) -> str:
        """
        Translate an inclusion equivalence dependency node into a latex qtree node.
        :param node: a dependency node
        :return: a qtree subtree rooted at the node
        """
        rel1, rel2 = node.relation_names
        attr1, attr2 = node.attributes
        op = self._get_latex_operator(node.operator)

        return f"[.${rel1}[{attr1}] {op} {rel2}[{attr2}]$ ]"

    def inclusion_subsumption(self, node: InclusionSubsumptionNode) -> str:
        """
        Translate an inclusion subsumption dependency node into a latex qtree node.
        :param node: a dependency node
        :return: a qtree subtree rooted at the node
        """

        rel1, rel2 = node.relation_names
        attr1, attr2 = node.attributes
        op = self._get_latex_operator(node.operator)

        return f"[.${rel1}[{attr1}] {op} {rel2}[{attr2}]$ ]"


def translate(roots: List[Node], syntax=None) -> List[str]:
    """
    Translate a treebrd tree rooted at root into latex tree.
    :param roots: a list of treebrd nodes
    :param syntax: syntax instance for custom operators
    :return:  a string representing a latex qtree rooted at root
    """
    return [
        "\\Tree{root}".format(root=Translator(syntax).translate(root)) for root in roots
    ]
