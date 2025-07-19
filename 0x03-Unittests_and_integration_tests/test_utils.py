#!/usr/bin/env python3

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


###############################################################################
class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for access_nested_map"""

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand(
        [
            ({}, ("a",)),
            ({"a": 1}, ("a", "b")),
        ]
    )
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that KeyError is raised for invalid path"""
        with self.assertRaises(KeyError) as ctx:
            access_nested_map(nested_map, path)

        self.assertEqual(ctx.exception.args[0], path[-1])


###############################################################################


class TestGetJson(unittest.TestCase):
    """Unit tests for get_json"""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        # Configure the mock to return a response with our test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function under test
        result = get_json(test_url)

        # Assert requests.get was called once with the correct URL
        mock_get.assert_called_once_with(test_url)

        # Assert the function returned the mocked JSON data
        self.assertEqual(result, test_payload)


###############################################################################


class TestMemoize(unittest.TestCase):
    """Unit test for the memoize decorator"""

    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_m:
            obj = TestClass()

            # Call the memoized property twice
            result1 = obj.a_property
            result2 = obj.a_property
            # Both calls return the same value
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # The method was only called once (memoized)
            mock_m.assert_called_once()


###############################################################################
# pip install parameterized
# python -m unittest test_utils.py
# python -m unittest test_utils.py
###############################################################################
