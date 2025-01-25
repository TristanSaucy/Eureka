import unittest
from src.main import CalculatorApp
import tkinter as tk

class TestMain(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = CalculatorApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_basic_functionality(self):
        """Test basic calculator functionality"""
        # Test initial state
        self.assertEqual(self.app.total, 0)
        self.assertEqual(self.app.press_count, 0)

        # Test orderly phase (first 5 presses)
        self.app.press_count = 1
        value = self.app.calculate_next_value()
        self.assertEqual(value, 1)

    def test_initial_state(self):
        """Test initial state of calculator"""
        self.assertEqual(self.app.total, 0)
        self.assertEqual(self.app.press_count, 0)
        self.assertEqual(len(self.app.totals), 0)
        self.assertTrue(self.app.chaos_enabled.get())  # Default should be True

    def test_calculate_next_value_orderly_phase(self):
        """Test the orderly phase (first 5 presses)"""
        self.app.press_count = 1
        self.assertEqual(self.app.calculate_next_value(), 1)  # First press should add 1
        
        self.app.press_count = 2
        self.assertEqual(self.app.calculate_next_value(), -1)  # Second press should subtract 1

    def test_calculate_next_value_standard_chaos(self):
        """Test the standard chaos phase (presses 6-100)"""
        self.app.press_count = 50
        value = self.app.calculate_next_value()
        self.assertTrue(value in [1, -1, 2, -2])  # Should return one of these values

    def test_chaos_level_calculation(self):
        """Test chaos level calculation"""
        # Before press 100
        self.app.press_count = 50
        self.app.calculate_next_value()
        self.assertEqual(self.app.chaos_level, 0)

        # After press 100
        self.app.press_count = 300
        self.app.calculate_next_value()
        self.assertTrue(0 < self.app.chaos_level <= 1)

    def test_chaos_toggle(self):
        """Test chaos toggle functionality"""
        self.app.chaos_enabled.set(False)
        self.app.press_count = 300
        self.app.calculate_next_value()
        self.assertEqual(self.app.chaos_level, 0)

if __name__ == '__main__':
    unittest.main()