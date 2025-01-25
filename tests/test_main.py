import unittest
from src.main import CalculatorApp
import tkinter as tk
import sys

class TestCalculatorApp(unittest.TestCase):
    def setUp(self):
        print("\n=== Starting New Test ===")
        self.root = tk.Tk()
        self.app = CalculatorApp(self.root)

    def tearDown(self):
        print("=== Test Complete ===")
        self.root.destroy()

    def test_initial_values(self):
        """Test initial values are set correctly"""
        print(f"\nTesting initial values:")
        initial_value = self.app.presses_var.get()
        print(f"Expected: 500")
        print(f"Actual: {initial_value}")
        self.assertEqual(initial_value, "500")

    def test_invalid_input(self):
        """Test handling of invalid input"""
        print(f"\nTesting invalid input:")
        test_value = "-100"
        print(f"Testing with invalid input: {test_value}")
        self.app.presses_var.set(test_value)
        self.app.run_simulation()
        output = self.app.output_text.get("1.0", tk.END)
        print(f"Output received: {output.strip()}")
        self.assertIn("Error", output)

    def test_valid_input(self):
        """Test handling of valid input"""
        print(f"\nTesting valid input:")
        test_value = "10"
        print(f"Testing with valid input: {test_value}")
        self.app.presses_var.set(test_value)
        self.app.run_simulation()
        output = self.app.output_text.get("1.0", tk.END)
        print(f"Output contains 'Final Results': {('Final Results' in output)}")
        self.assertIn("Final Results", output)

def run_tests():
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculatorApp)
    
    # Run the tests
    print("\n=== Running Calculator App Tests ===")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"\nTest Summary:")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(not success)  # Exit with 0 if successful, 1 if failed