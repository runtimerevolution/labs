
import unittest

from code_examples.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(10, 5), 15)

    def test_add_negative_with_positive(self):
        self.assertEqual(self.calc.add(-1, 1), 0)

    def test_add_negative_with_negative(self):
        self.assertEqual(self.calc.add(-1, -1), -2)

    def test_add_zeros(self):
        self.assertEqual(self.calc.add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 5), 5)

    def test_subtract_negative_with_positive(self):
        self.assertEqual(self.calc.subtract(-1, 1), -2)

    def test_subtract_negative_with_negative(self):
        self.assertEqual(self.calc.subtract(-1, -1), 0)

    def test_subtract_zeros(self):
        self.assertEqual(self.calc.subtract(0, 0), 0)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(10, 10), 100)

    def test_multiply_negative(self):
        self.assertEqual(self.calc.multiply(-1, 5), -5)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

if __name__ == "__main__":
    unittest.main()