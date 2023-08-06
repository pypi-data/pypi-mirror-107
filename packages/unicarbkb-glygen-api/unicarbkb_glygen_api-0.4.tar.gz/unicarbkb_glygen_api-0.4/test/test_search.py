from unicarbkb_glygen_api import mymath
import unittest

class TestAdd(unittest.TestCase):
    """
    Test the add function from the mymath library
    """

    def test_add_integer(self):
        """
        Test that the addition of two integers returns the correct total
        """
        result = mymath.add(1, 2)
        self.assertEqual(result, 3)


    def test_add_integer2(self):
        """
        Test that the addition of two integers returns the correct total
        """
        result = mymath.add(2, 2)
        self.assertEqual(result, 4)

    def test_add_floats(self):
        """
        Test that the addition of two integers returns the correct total
        """
        result = mymath.add(10.5, 2)
        self.assertEqual(result, 12.5)

    def test_add_strings(self):
        """
        Test that the addition of two strings returns the two strings as one
        concatenated string
        """
        result = mymath.add('abc', 'def')
        self.assertEqual(result, 'abcdef')

if __name__ == '__main__':
    unittest.main()
