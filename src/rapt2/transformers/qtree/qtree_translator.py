from typing import List, Union

from ...treebrd.node import (
    AssignNode,
    CrossJoinNode,
    DifferenceNode,
    FullOuterJoinNode,
    FunctionalDependencyNode,
    InclusionEquivalenceNode,
    InclusionSubsumptionNode,
    IntersectNode,
    LeftOuterJoinNode,
    MultivaluedDependencyNode,
    NaturalJoinNode,
    Node,
    PrimaryKeyNode,
    ProjectNode,
    RelationNode,
    RenameNode,
    RightOuterJoinNode,
    SelectNode,
    ThetaJoinNode,
    UnionNode,
)
from ...treebrd.condition_node import (
    BinaryConditionNode,
    IdentityConditionNode,
    UnaryConditionNode,
    UnaryConditionalOperator,
)
from ..base_translator import BaseTranslator
from .operators import latex_operator, conditional_latex_operator


class QTreeTranslator(BaseTranslator):
    """
    A Translator defining the operations for translating a relational algebra
    statement into a latex tree output.
    """

    @staticmethod
    def _escape_latex(name: str) -> str:
        """Escape underscores in a name for LaTeX."""
        return name.replace("_", r"\_") if name else ""

    def _get_latex_operator(self, operator):
        """
        Get the LaTeX operator for a given operator.
        For now, we use the hardcoded mapping, but this could be extended
        to use syntax-based mappings in the future.
        """
        return latex_operator[operator]

    def _get_conditional_latex_operator(self, operator):
        """
        Get the LaTeX operator for a given conditional operator.
        """
        return conditional_latex_operator[operator]

    def relation(self, node: RelationNode) -> str:
        """
        Translate a relation node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return "[.${}$ ]".format(self._escape_latex(node.name))

    def select(self, node: SelectNode) -> str:
        """
        Translate a select node into a latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        child = self.translate(node.child)
        return "[.${op}_{{{conditions}}}$ {child} ]".format(
            op=self._get_latex_operator(node.operator),
            conditions=self.translate_condition(node.conditions),
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
            attributes=r",\,".join(node.attributes.names),
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
            attributes = "({})".format(r",\,".join(node.attributes.names))
        return "[.${op}_{{{name}{attributes}}}$ {child} ]".format(
            op=self._get_latex_operator(node.operator),
            name=self._escape_latex(node.name),
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
            attributes = "({})".format(r",\,".join(node.attributes.names))
        return "[.${name}{attributes}$ {child} ]".format(
            name=self._escape_latex(node.name),
            attributes=attributes,
            child=child,
        )

    def _conditioned_binary(
        self,
        node: Union[
            ThetaJoinNode, FullOuterJoinNode, LeftOuterJoinNode, RightOuterJoinNode
        ],
    ) -> str:
        """Translate a binary node with conditions into a LaTeX qtree node."""
        return "[.${op}_{{{conditions}}}$ {left} {right} ]".format(
            op=self._get_latex_operator(node.operator),
            conditions=self.translate_condition(node.conditions),
            left=self.translate(node.left),
            right=self.translate(node.right),
        )

    def theta_join(self, node: ThetaJoinNode) -> str:
        """
        Translate a join node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return self._conditioned_binary(node)

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
        return self._conditioned_binary(node)

    def left_outer_join(self, node: LeftOuterJoinNode) -> str:
        """
        Translate a left outer join node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return self._conditioned_binary(node)

    def right_outer_join(self, node: RightOuterJoinNode) -> str:
        """
        Translate a right outer join node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return self._conditioned_binary(node)

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

    def _binary(
        self,
        node: Union[
            CrossJoinNode, NaturalJoinNode, UnionNode, DifferenceNode, IntersectNode
        ],
    ) -> str:
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
        attributes = r",\,".join(node.attributes)
        return f"[.${self._get_latex_operator(node.operator)}({node.relation_name}) \\eq {{{attributes}}}$ ]"

    def _latex_child_str(self, child: Union[SelectNode, RelationNode]) -> str:
        """Format a dependency child node as a LaTeX string."""
        if isinstance(child, SelectNode):
            return f"{self._get_latex_operator(child.operator)}_{{{self.translate_condition(child.conditions)}}} ({child.name})"
        return child.name

    def _unary_dependency(
        self, node: Union[MultivaluedDependencyNode, FunctionalDependencyNode]
    ) -> str:
        """Translate a unary dependency node (MVD or FD) into a latex qtree node."""
        left_attr, right_attr = node.attributes
        op = self._get_latex_operator(node.operator)
        child_str = self._latex_child_str(node.child)
        return f"[.${child_str} : {left_attr} {op} {right_attr}$ ]"

    def multivalued_dependency(self, node: MultivaluedDependencyNode) -> str:
        return self._unary_dependency(node)

    def functional_dependency(self, node: FunctionalDependencyNode) -> str:
        return self._unary_dependency(node)

    def _inclusion_dependency(
        self, node: Union[InclusionEquivalenceNode, InclusionSubsumptionNode]
    ) -> str:
        """Translate an inclusion dependency node into a latex qtree node."""
        attr1, attr2 = node.attributes
        op = self._get_latex_operator(node.operator)
        left_str = self._latex_child_str(node.left_child)
        right_str = self._latex_child_str(node.right_child)
        return f"[.${left_str}[{attr1}] {op} {right_str}[{attr2}]$ ]"

    def inclusion_equivalence(self, node: InclusionEquivalenceNode) -> str:
        return self._inclusion_dependency(node)

    def inclusion_subsumption(self, node: InclusionSubsumptionNode) -> str:
        return self._inclusion_dependency(node)

    def identity_condition(self, node: IdentityConditionNode) -> str:
        """
        Translate an identity condition node into LaTeX.
        :param node: an identity condition node
        :return: LaTeX representation of the condition
        """
        return node.ident

    def unary_condition(self, node: UnaryConditionNode) -> str:
        """
        Translate a unary condition node into LaTeX.
        :param node: a unary condition node
        :return: LaTeX representation of the condition
        """
        op = self._get_conditional_latex_operator(node.op)
        if node.op == UnaryConditionalOperator.DEFINED:
            return f"{op}({self.translate_condition(node.child)})"
        else:
            return f"{op} {self.translate_condition(node.child)}"

    def binary_condition(self, node: BinaryConditionNode) -> str:
        """
        Translate a binary condition node into LaTeX.
        :param node: a binary condition node
        :return: LaTeX representation of the condition
        """
        op = self._get_conditional_latex_operator(node.op)
        return f"({self.translate_condition(node.left)} {op} {self.translate_condition(node.right)})"


def translate(roots: List[Node], syntax=None) -> List[str]:
    """
    Translate a treebrd tree rooted at root into latex tree.
    :param roots: a list of treebrd nodes
    :param syntax: syntax instance for custom operators
    :return:  a string representing a latex qtree rooted at root
    """
    return [
        "\\Tree{root}".format(root=QTreeTranslator(syntax).translate(root))
        for root in roots
    ]
