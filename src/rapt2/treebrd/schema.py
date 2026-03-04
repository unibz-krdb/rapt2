import copy

from rapt2.treebrd.attributes import AttributeList

from .errors import RelationReferenceError


class Schema:
    """
    A Schema is a description of relational data.
    """

    def __init__(self, definition: dict[str, list[str]] | None = None) -> None:
        """
        :param definition: a mapping of relation names to their attribute
            lists. Names and attributes are lowercased on storage.
        """
        self._data: dict[str, list[str]] = {}
        if definition is None:
            return
        for name, attributes in definition.items():
            self._data[name.lower()] = [attr.lower() for attr in attributes]

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        if self.to_dict() != other.to_dict():  # type: ignore[union-attr]
            return False
        return True

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def contains(self, name: str) -> bool:
        """
        Return true if the Schema contains a relation with the specified name.
        :param name: A name of a relation.
        :return: True if the Schema contains a relation with the specified name.
        """
        return name in self._data

    def to_dict(self) -> dict[str, list[str]]:
        """
        Return a dictionary containing the name-attribute pairs in this Schema.
        :return: A dictionary of name-attribute pairs.
        """
        return copy.deepcopy(self._data)

    def get_attributes(self, name: str) -> list[str]:
        """
        Return the list of attributes associated with the specified relation.
        :param name: A name of a relation in the Schema.
        :return: A list of attributes.
        :raise RelationReferenceError: Raised if the name does not exist.
        """
        attributes = self._data.get(name, None)
        if not attributes:
            raise RelationReferenceError(
                "Relation '{name}' does not exist.".format(name=name)
            )
        return attributes[:]

    def add(self, name: str, attributes: list[str] | AttributeList) -> None:
        """
        Add the relation to the Schema.
        :param name: The name of a relation.
        :param attributes: A list of attributes for the relation.
        :raise RelationReferenceError: Raised if the name already exists.
        """
        if name in self._data:
            raise RelationReferenceError(
                "Relation '{name}' already exists.".format(name=name)
            )
        if isinstance(attributes, AttributeList):
            self._data[name.lower()] = attributes.to_list()
        else:
            self._data[name.lower()] = [attribute.lower() for attribute in attributes]
