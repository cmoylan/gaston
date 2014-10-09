import sys
sys.path += '../'

import unittest
import textwrap

from models.recipe import Recipe


class RecipeTest(unittest.TestCase):

    def test_parse_ingredients(self):
        s = textwrap.dedent("""\
            1 oz cardimom
            2 cup flour
            3 tbsp rice""")

        expected_result = [
            {'name': 'cardimom', 'unit': 'oz', 'quantity': '1'},
            {'name': 'flour', 'unit': 'cup', 'quantity': '2'},
            {'name': 'rice', 'unit': 'tbsp', 'quantity': '3'}]

        result = Recipe.parse_ingredients(s)
        self.assertEqual(result, expected_result)


    def test_parse_incomplete_ingredients(self):
        s = textwrap.dedent("""\
            2 cup
            3 tbsp rice""")

        result = Recipe.parse_ingredients(s)
        self.assertEqual(len(result), 1)


    def test_parse_steps(self):
        s = textwrap.dedent("""\
            Do something
            Do something else
            You are done""")

        expected_result = [
            {'step': 'Do something'},
            {'step': 'Do something else'},
            {'step': 'You are done'}]

        result = Recipe.parse_steps(s)
        self.assertEqual(result, expected_result)





if __name__ == '__main__':
    unittest.main()
