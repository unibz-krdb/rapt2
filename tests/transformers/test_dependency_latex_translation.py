import pytest
from src.rapt2.rapt import Rapt
from src.rapt2.treebrd.grammars.dependency_grammar import DependencyGrammar
from src.rapt2.treebrd.treebrd import TreeBRD


class TestDependencyLatexTranslation:
    """Test cases for LaTeX translation of dependency grammar statements."""

    def setup_method(self):
        """Set up test fixtures."""
        self.rapt = Rapt(grammar="Dependency Grammar")
        self.schema = {"R": ["a", "b", "c"], "S": ["x", "y"], "T": ["id", "name"]}

    def test_primary_key_latex_translation(self):
        """Test LaTeX translation of primary key dependencies."""
        # Test single attribute primary key
        latex = self.rapt.to_qtree("pk_{a} R;", self.schema)
        assert len(latex) == 1
        assert "\\text{pk}_{a}(r)" in latex[0]
        assert "\\Tree" in latex[0]

        # Test multiple attributes primary key
        latex = self.rapt.to_qtree("pk_{a, b} R;", self.schema)
        assert len(latex) == 1
        assert "\\text{pk}_{a, b}(r)" in latex[0]

    def test_multivalued_dependency_latex_translation(self):
        """Test LaTeX translation of multivalued dependencies."""
        latex = self.rapt.to_qtree("mvd_{a, b} R;", self.schema)
        assert len(latex) == 1
        assert "\\text{mvd}_{a, b}(r)" in latex[0]
        assert "\\Tree" in latex[0]

    def test_functional_dependency_latex_translation(self):
        """Test LaTeX translation of functional dependencies."""
        # Test simple functional dependency
        latex = self.rapt.to_qtree("fd_{a, b} \\select_{a = 1} R;", self.schema)
        assert len(latex) == 1
        assert "a \\rightarrow b" in latex[0]
        assert "\\Tree" in latex[0]

        # Test complex functional dependency
        latex = self.rapt.to_qtree(
            "fd_{a, b} \\select_{a = 1 and b > 0} R;", self.schema
        )
        assert len(latex) == 1
        assert "a \\rightarrow b" in latex[0]

    def test_inclusion_equivalence_latex_translation(self):
        """Test LaTeX translation of inclusion equivalence dependencies."""
        latex = self.rapt.to_qtree("inc=_{a, b} (R, S);", self.schema)
        assert len(latex) == 1
        assert "r[a] \\equiv s[b]" in latex[0]
        assert "\\Tree" in latex[0]

    def test_inclusion_subsumption_latex_translation(self):
        """Test LaTeX translation of inclusion subsumption dependencies."""
        latex = self.rapt.to_qtree("inc⊆_{a, b} (R, S);", self.schema)
        assert len(latex) == 1
        assert "r[a] \\subseteq s[b]" in latex[0]
        assert "\\Tree" in latex[0]

    def test_multiple_dependency_statements_latex_translation(self):
        """Test LaTeX translation of multiple dependency statements."""
        latex = self.rapt.to_qtree(
            "pk_{a} R; mvd_{x, y} S; fd_{id, name} \\select_{id > 0} T; inc=_{a, b} (R, S); inc⊆_{x, y} (S, T);",
            self.schema,
        )
        assert len(latex) == 5

        # Check first statement (primary key)
        assert "\\text{pk}_{a}(r)" in latex[0]

        # Check second statement (multivalued dependency)
        assert "\\text{mvd}_{x, y}(s)" in latex[1]

        # Check third statement (functional dependency)
        assert "id \\rightarrow name" in latex[2]

        # Check fourth statement (inclusion equivalence)
        assert "r[a] \\equiv s[b]" in latex[3]

        # Check fifth statement (inclusion subsumption)
        assert "s[x] \\subseteq t[y]" in latex[4]

    def test_latex_structure_consistency(self):
        """Test that LaTeX output has consistent structure."""
        test_cases = [
            "pk_{a, b} R;",
            "mvd_{x, y} S;",
            "fd_{id, name} \\select_{id > 0} T;",
            "inc=_{a, b} (R, S);",
            "inc⊆_{x, y} (S, T);",
        ]

        for test_case in test_cases:
            latex = self.rapt.to_qtree(test_case, self.schema)
            assert len(latex) == 1
            assert latex[0].startswith("\\Tree")
            assert latex[0].endswith(" ]")
            # Most dependency operators use \\text{}, but inclusion and functional dependencies use mathematical symbols
            if "inc=" in test_case or "inc⊆" in test_case:
                assert "\\equiv" in latex[0] or "\\subseteq" in latex[0]
            elif "fd_" in test_case:
                assert "\\rightarrow" in latex[0]
            else:
                assert "\\text{" in latex[0]

    def test_latex_operators_mapping(self):
        """Test that correct LaTeX operators are used for each dependency type."""
        test_mappings = [
            ("pk_{a} R;", "\\text{pk}"),
            ("mvd_{a, b} R;", "\\text{mvd}"),
            ("fd_{a, b} \\select_{a = 1} R;", "\\rightarrow"),
            ("inc=_{a, b} (R, S);", "\\equiv"),
            ("inc⊆_{a, b} (R, S);", "\\subseteq"),
        ]

        for test_case, expected_operator in test_mappings:
            latex = self.rapt.to_qtree(test_case, self.schema)
            assert expected_operator in latex[0]

    def test_latex_attributes_formatting(self):
        """Test that attributes are properly formatted in LaTeX output."""
        # Test single attribute
        latex = self.rapt.to_qtree("pk_{a} R;", self.schema)
        assert "_{a}" in latex[0]

        # Test multiple attributes
        latex = self.rapt.to_qtree("pk_{a, b, c} R;", self.schema)
        assert "_{a, b, c}" in latex[0]

    def test_latex_relation_names_formatting(self):
        """Test that relation names are properly formatted in LaTeX output."""
        # Test single relation
        latex = self.rapt.to_qtree("pk_{a} R;", self.schema)
        assert "(r)" in latex[0]

        # Test inclusion dependencies with new format
        latex = self.rapt.to_qtree("inc=_{a, b} (R, S);", self.schema)
        assert "r[a]" in latex[0] and "s[b]" in latex[0]

        latex = self.rapt.to_qtree("inc⊆_{x, y} (S, T);", self.schema)
        assert "s[x]" in latex[0] and "t[y]" in latex[0]

    def test_latex_conditions_formatting(self):
        """Test that conditions are properly formatted in LaTeX output."""
        latex = self.rapt.to_qtree(
            "fd_{a, b} \\select_{a = 1 and b > 0} R;", self.schema
        )
        assert "a \\rightarrow b" in latex[0]
        # Note: Conditions are now included as child nodes in the new functional dependency format

    def test_latex_translation_with_different_schemas(self):
        """Test LaTeX translation with different schema configurations."""
        schema1 = {"Users": ["id", "name", "email"]}
        schema2 = {
            "Products": ["product_id", "name", "price"],
            "Orders": ["order_id", "customer_id"],
        }

        # Test with schema1
        latex1 = self.rapt.to_qtree("pk_{id} Users;", schema1)
        assert "\\text{pk}_{id}(users)" in latex1[0]

        # Test with schema2
        latex2 = self.rapt.to_qtree("inc=_{id, name} (Products, Orders);", schema2)
        assert "products[id] \\equiv orders[name]" in latex2[0]

    def test_latex_translation_error_handling(self):
        """Test LaTeX translation error handling."""
        # Test with invalid syntax
        with pytest.raises(Exception):
            self.rapt.to_qtree("invalid syntax", self.schema)

        # Test with empty input
        with pytest.raises(Exception):
            self.rapt.to_qtree("", self.schema)

    def test_latex_translation_consistency_across_runs(self):
        """Test that LaTeX translation is consistent across multiple runs."""
        test_case = "pk_{a, b} R; mvd_{x, y} S;"

        # Run multiple times
        latex1 = self.rapt.to_qtree(test_case, self.schema)
        latex2 = self.rapt.to_qtree(test_case, self.schema)

        assert latex1 == latex2
        assert len(latex1) == 2
        assert len(latex2) == 2


class TestDependencyLatexTranslationIntegration:
    """Integration tests for dependency LaTeX translation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.grammar = DependencyGrammar()
        self.schema = {"R": ["a", "b", "c"], "S": ["x", "y"], "T": ["id", "name"]}
        self.builder = TreeBRD(self.grammar)

    def test_direct_grammar_latex_translation(self):
        """Test LaTeX translation using grammar directly."""
        from src.rapt2.transformers.qtree import qtree_translator

        # Parse dependency statements
        trees = self.builder.build("pk_{a, b} R;", self.schema)
        assert len(trees) == 1

        # Translate to LaTeX
        latex = qtree_translator.translate(trees)
        assert len(latex) == 1
        assert "\\text{pk}_{a, b}(r)" in latex[0]

    def test_multiple_dependency_types_latex_translation(self):
        """Test LaTeX translation of all dependency types in one go."""
        from src.rapt2.transformers.qtree import qtree_translator

        test_input = "pk_{a} R; mvd_{x, y} S; fd_{id, name} \\select_{id > 0} T; inc=_{a, b} (R, S); inc⊆_{x, y} (S, T);"
        trees = self.builder.build(test_input, self.schema)
        assert len(trees) == 5

        latex = qtree_translator.translate(trees)
        assert len(latex) == 5

        # Check each dependency type is properly translated
        expected_operators = [
            "\\text{pk}",
            "\\text{mvd}",
            "\\rightarrow",
            "\\equiv",
            "\\subseteq",
        ]
        for i, expected_op in enumerate(expected_operators):
            assert expected_op in latex[i]
