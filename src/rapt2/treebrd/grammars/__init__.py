from .core_grammar import CoreGrammar
from .extended_grammar import ExtendedGrammar
from .dependency_grammar import DependencyGrammar

GRAMMARS = {
    "Core Grammar": CoreGrammar,
    "Extended Grammar": ExtendedGrammar,
    "Dependency Grammar": DependencyGrammar,
}
