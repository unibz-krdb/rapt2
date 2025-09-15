from ..base_translator import BaseTranslator
from .operators import latex_operator


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

    def relation(self, node):
        """
        Translate a relation node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return "[.${}$ ]".format(node.name)

    def select(self, node):
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

    def project(self, node):
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

    def rename(self, node):
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

    def assign(self, node):
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

    def theta_join(self, node):
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

    def cross_join(self, node):
        """
        Translate a cross node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return self._binary(node)

    def natural_join(self, node):
        """
        Translate a natural join node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return self._binary(node)

    def full_outer_join(self, node):
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

    def left_outer_join(self, node):
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

    def right_outer_join(self, node):
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

    def union(self, node):
        """
        Translate a union node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return self._binary(node)

    def difference(self, node):
        """
        Translate a difference node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return self._binary(node)

    def intersect(self, node):
        """
        Translate an intersect node into latex qtree node.
        :param node: a treebrd node
        :return: a qtree subtree rooted at the node
        """
        return self._binary(node)

    def _binary(self, node):
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

    def primary_key(self, node):
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

    def multivalued_dependency(self, node):
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

    def functional_dependency(self, node):
        """
        Translate a functional dependency node into a latex qtree node.
        :param node: a dependency node
        :return: a qtree subtree rooted at the node
        """
        left_attr, right_attr = node.attributes
        conditions = node.conditions.to_latex()
        relation = node.relation_name
        op = self._get_latex_operator(node.operator)
        return f"[.${relation} : {left_attr} {op} {right_attr}$ ]"

    def inclusion_equivalence(self, node):
        """
        Translate an inclusion equivalence dependency node into a latex qtree node.
        :param node: a dependency node
        :return: a qtree subtree rooted at the node
        """
        rel1, rel2 = node.relation_names
        attr1, attr2 = node.attributes
        op = self._get_latex_operator(node.operator)

        return f"[.${rel1}[{attr1}] {op} {rel2}[{attr2}]$ ]"

    def inclusion_subsumption(self, node):
        """
        Translate an inclusion subsumption dependency node into a latex qtree node.
        :param node: a dependency node
        :return: a qtree subtree rooted at the node
        """

        rel1, rel2 = node.relation_names
        attr1, attr2 = node.attributes
        op = self._get_latex_operator(node.operator)

        return f"[.${rel1}[{attr1}] {op} {rel2}[{attr2}]$ ]"


def translate(roots, syntax=None):
    """
    Translate a treebrd tree rooted at root into latex tree.
    :param roots: a list of treebrd nodes
    :param syntax: syntax instance for custom operators
    :return:  a string representing a latex qtree rooted at root
    """
    return ["\\Tree{root}".format(root=Translator(syntax).translate(root)) for root in roots]  # type: ignore
