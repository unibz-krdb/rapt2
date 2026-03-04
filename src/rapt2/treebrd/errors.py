class TreeBRDError(Exception):
    """
    Base class for exceptions in this module.
    """

    pass


class InputError(TreeBRDError):
    """Raised when the input expression is malformed or violates constraints."""

    pass


class InputReferenceError(InputError):
    """Raised when a reference within the input cannot be resolved."""

    pass


class RelationReferenceError(InputReferenceError):
    """Raised when a relation name cannot be found or already exists in the schema."""

    pass


class AttributeReferenceError(InputReferenceError):
    """Raised when an attribute reference is missing or ambiguous."""

    pass
