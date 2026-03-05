from unittest import TestCase

from rapt2.treebrd.attributes import Attribute, AttributeList

__author__ = "Noel"


class TestAttribute(TestCase):
    def test_name_after_init(self):
        attribute = Attribute("Name", "Prefix")
        self.assertEqual("Name", attribute.name)

    def test_prefix_after_init(self):
        attribute = Attribute("Name", "Prefix")
        self.assertEqual("Prefix", attribute.prefix)

    def test_prefixed_after_init(self):
        attribute = Attribute("Name", "Prefix")
        self.assertEqual("Prefix.Name", attribute.prefixed)

    def test_equality_when_name_and_attribute_are_equal(self):
        attribute_a = Attribute("Name", "Prefix")
        attribute_b = Attribute("Name", "Prefix")
        self.assertEqual(attribute_a, attribute_b)

    def test_equality_when_name_and_attribute_are_different(self):
        attribute_a = Attribute("Name", "Prefix")
        attribute_b = Attribute("Other", "Other")
        self.assertNotEqual(attribute_a, attribute_b)

    def test_equality_when_name_is_different(self):
        attribute_a = Attribute("Name", "Prefix")
        attribute_b = Attribute("Other", "Prefix")
        self.assertNotEqual(attribute_a, attribute_b)

    def test_equality_when_attribute_is_different(self):
        attribute_a = Attribute("Name", "Prefix")
        attribute_b = Attribute("Name", "Other")
        self.assertNotEqual(attribute_a, attribute_b)

    def test_hash_when_name_and_attribute_are_equal(self):
        attribute_a = Attribute("Name", "Prefix")
        attribute_b = Attribute("Name", "Prefix")
        self.assertEqual(hash(attribute_a), hash(attribute_b))


class TestAttributeList(TestCase):
    def test_trim_when_restriction_is_empty(self):
        a_list = AttributeList(["A", "B", "C"], "prefix")
        a_list.trim([])
        self.assertEqual([], a_list.to_list())

    def test_trim_when_restriction_contains_all_with_no_prefix(self):
        expected = ["prefix.A", "prefix.B", "prefix.C"]
        a_list = AttributeList(["A", "B", "C"], "prefix")
        a_list.trim(["A", "B", "C"])
        self.assertEqual(expected, a_list.to_list())

    def test_trim_when_restriction_contains_all_with_prefix(self):
        expected = ["prefix.A", "prefix.B", "prefix.C"]
        a_list = AttributeList(["A", "B", "C"], "prefix")
        a_list.trim(["prefix.A", "prefix.B", "prefix.C"])
        self.assertEqual(expected, a_list.to_list())

    def test_trim_when_restriction_excludes_first(self):
        expected = ["prefix.B", "prefix.C"]
        a_list = AttributeList(["A", "B", "C"], "prefix")
        a_list.trim(["B", "C"])
        self.assertEqual(expected, a_list.to_list())

    def test_trim_when_restriction_excludes_last(self):
        expected = ["prefix.A", "prefix.B"]
        a_list = AttributeList(["A", "B", "C"], "prefix")
        a_list.trim(["A", "B"])
        self.assertEqual(expected, a_list.to_list())

    def test_trim_when_restriction_excludes_middle(self):
        expected = ["prefix.A", "prefix.C"]
        a_list = AttributeList(["A", "B", "C"], "prefix")
        a_list.trim(["A", "C"])
        self.assertEqual(expected, a_list.to_list())

    def test_trim_when_restriction_leaves_first(self):
        expected = ["prefix.A"]
        a_list = AttributeList(["A", "B", "C"], "prefix")
        a_list.trim(["A"])
        self.assertEqual(expected, a_list.to_list())

    def test_trim_when_restriction_leaves_last(self):
        expected = ["prefix.C"]
        a_list = AttributeList(["A", "B", "C"], "prefix")
        a_list.trim(["C"])
        self.assertEqual(expected, a_list.to_list())

    def test_trim_when_restriction_leaves_middle(self):
        expected = ["prefix.B"]
        a_list = AttributeList(["A", "B", "C"], "prefix")
        a_list.trim(["B"])
        self.assertEqual(expected, a_list.to_list())

    def test_trim_when_reorder(self):
        expected = ["prefix.B", "prefix.C", "prefix.A"]
        a_list = AttributeList(["B", "C", "A"], "prefix")
        a_list.trim(["B", "C", "A"])
        self.assertEqual(expected, a_list.to_list())

    def test_trim_when_reorder_and_restrict(self):
        expected = ["prefix.C", "prefix.A"]
        a_list = AttributeList(["B", "C", "A"], "prefix")
        a_list.trim(["C", "A"])
        self.assertEqual(expected, a_list.to_list())

    def test_rename_prefix(self):
        expected = ["prefix.A", "prefix.B", "prefix.C"]
        a_list = AttributeList(["A", "B", "C"], "old")
        a_list.rename([], "prefix")
        self.assertEqual(expected, a_list.to_list())

    def test_rename_attribute_names(self):
        expected = ["prefix.A", "prefix.B", "prefix.C"]
        a_list = AttributeList(["a", "b", "c"], "prefix")
        a_list.rename(["A", "B", "C"], None)
        self.assertEqual(expected, a_list.to_list())

    def test_rename_attribute_name_and_prefix(self):
        expected = ["prefix.A", "prefix.B", "prefix.C"]
        a_list = AttributeList(["a", "b", "c"], "old")
        a_list.rename(["A", "B", "C"], "prefix")
        self.assertEqual(expected, a_list.to_list())


class TestAttributeListMerge(TestCase):
    def test_merge_two_lists(self):
        first = AttributeList(["a1"], "alpha")
        second = AttributeList(["b1", "b2"], "beta")
        merged = AttributeList.merge(first, second)
        self.assertEqual(["alpha.a1", "beta.b1", "beta.b2"], merged.to_list())

    def test_merge_preserves_originals(self):
        first = AttributeList(["a1"], "alpha")
        second = AttributeList(["b1"], "beta")
        AttributeList.merge(first, second)
        self.assertEqual(["alpha.a1"], first.to_list())
        self.assertEqual(["beta.b1"], second.to_list())

    def test_merge_empty_lists(self):
        first = AttributeList([], None)
        second = AttributeList([], None)
        merged = AttributeList.merge(first, second)
        self.assertEqual([], merged.to_list())

    def test_merge_one_empty(self):
        first = AttributeList(["a1"], "alpha")
        second = AttributeList([], None)
        merged = AttributeList.merge(first, second)
        self.assertEqual(["alpha.a1"], merged.to_list())

    def test_merge_rejects_non_attribute_list_first(self):
        with self.assertRaises(TypeError):
            AttributeList.merge("not_a_list", AttributeList([], None))

    def test_merge_rejects_non_attribute_list_second(self):
        with self.assertRaises(TypeError):
            AttributeList.merge(AttributeList([], None), "not_a_list")


class TestAttributeListValidate(TestCase):
    def test_validate_existing_attributes(self):
        a_list = AttributeList(["a1", "a2"], "alpha")
        a_list.validate(["a1", "a2"])

    def test_validate_with_prefix(self):
        a_list = AttributeList(["a1", "a2"], "alpha")
        a_list.validate(["alpha.a1"])

    def test_validate_nonexistent_raises(self):
        from rapt2.treebrd.errors import AttributeReferenceError

        a_list = AttributeList(["a1", "a2"], "alpha")
        self.assertRaises(AttributeReferenceError, a_list.validate, ["nonexistent"])

    def test_validate_empty_references(self):
        a_list = AttributeList(["a1"], "alpha")
        a_list.validate([])


class TestAttributeListGetAttribute(TestCase):
    def test_get_by_name(self):
        a_list = AttributeList(["a1", "a2"], "alpha")
        result = a_list.get_attribute("a1")
        self.assertEqual(Attribute("a1", "alpha"), result)

    def test_get_by_prefixed_name(self):
        a_list = AttributeList(["a1", "a2"], "alpha")
        result = a_list.get_attribute("alpha.a1")
        self.assertEqual(Attribute("a1", "alpha"), result)

    def test_get_nonexistent_raises(self):
        from rapt2.treebrd.errors import AttributeReferenceError

        a_list = AttributeList(["a1"], "alpha")
        self.assertRaises(AttributeReferenceError, a_list.get_attribute, "b1")

    def test_get_ambiguous_raises(self):
        from rapt2.treebrd.errors import AttributeReferenceError

        a_list = AttributeList(["a1"], "alpha")
        a_list.extend(["a1"], "beta")
        self.assertRaises(AttributeReferenceError, a_list.get_attribute, "a1")

    def test_get_ambiguous_with_prefix_succeeds(self):
        a_list = AttributeList(["a1"], "alpha")
        a_list.extend(["a1"], "beta")
        result = a_list.get_attribute("alpha.a1")
        self.assertEqual(Attribute("a1", "alpha"), result)


class TestAttributeListHasDuplicates(TestCase):
    def test_no_duplicates(self):
        self.assertFalse(AttributeList.has_duplicates([1, 2, 3]))

    def test_with_duplicates(self):
        self.assertTrue(AttributeList.has_duplicates([1, 2, 2]))

    def test_empty_list(self):
        self.assertFalse(AttributeList.has_duplicates([]))

    def test_single_element(self):
        self.assertFalse(AttributeList.has_duplicates([1]))


class TestAttributeListDunderMethods(TestCase):
    def test_str(self):
        a_list = AttributeList(["a1", "a2"], "alpha")
        self.assertEqual("alpha.a1, alpha.a2", str(a_list))

    def test_str_no_prefix(self):
        a_list = AttributeList(["a1", "a2"], None)
        self.assertEqual("a1, a2", str(a_list))

    def test_len(self):
        a_list = AttributeList(["a1", "a2", "a3"], "alpha")
        self.assertEqual(3, len(a_list))

    def test_len_empty(self):
        a_list = AttributeList([], None)
        self.assertEqual(0, len(a_list))

    def test_eq_same(self):
        a = AttributeList(["a1", "a2"], "alpha")
        b = AttributeList(["a1", "a2"], "alpha")
        self.assertEqual(a, b)

    def test_eq_different(self):
        a = AttributeList(["a1", "a2"], "alpha")
        b = AttributeList(["b1", "b2"], "beta")
        self.assertNotEqual(a, b)

    def test_eq_different_type(self):
        a = AttributeList(["a1"], "alpha")
        self.assertNotEqual(a, "not an attribute list")

    def test_ne(self):
        a = AttributeList(["a1"], "alpha")
        b = AttributeList(["b1"], "beta")
        self.assertTrue(a != b)

    def test_iter(self):
        a_list = AttributeList(["a1", "a2"], "alpha")
        items = list(a_list)
        self.assertEqual([Attribute("a1", "alpha"), Attribute("a2", "alpha")], items)
