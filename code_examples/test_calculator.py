import unittest

from calculator import Calculator


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


if __name__ == "__main__":
    unittest.main()
