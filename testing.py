import unittest
from Calculator_project import CalculatorEngine

class TestCalculatorEngine(unittest.TestCase):

    def setUp(self):
        # Create an engine instance without GUI for testing
        self.engine = CalculatorEngine(None)

    def test_addition(self):
        self.assertEqual(self.engine.evaluate_expression("2+3"), 5)

    def test_multiplication(self):
        self.assertEqual(self.engine.evaluate_expression("4×5"), 20)

    def test_power(self):
        self.assertEqual(self.engine.evaluate_expression("2^3"), 8)

    def test_square_root(self):
        self.assertEqual(self.engine.evaluate_expression("√25"), 5)

    def test_sin(self):
        self.assertAlmostEqual(
            self.engine.evaluate_expression("sin(30)"),
            0.5,
            places=5
        )

if __name__ == "__main__":
    unittest.main()
