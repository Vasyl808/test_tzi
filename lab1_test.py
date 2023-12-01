import unittest
import json
from generator import NumberGenerator, GeneratorPeriod


class TestNumberGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = NumberGenerator(m=10, a=2, c=3, X0=1, n=5)

    def test_generate(self):
        expected_sequence = [5, 3, 9, 1, 5]  # Expected sequence based on given parameters
        self.assertEqual(self.generator.generate(), expected_sequence)


class TestNumberGeneratorFromConfig(unittest.TestCase):

    def test_valid_config(self):
        # Create a mock config file with valid settings
        valid_config = {"m": 10, "a": 2, "c": 3, "X0": 1}
        with open("valid_config.json", "w") as file:
            json.dump(valid_config, file)

        generator = NumberGenerator.from_config_file("valid_config.json", x0=1, n=5)
        self.assertEqual(generator.generate(), [5, 3, 9, 1, 5])

    def test_invalid_config(self):
        # Create a mock config file with invalid settings
        invalid_config = {"m": -10, "a": -2, "c": -3, "X0": -1}
        with open("invalid_config.json", "w") as file:
            json.dump(invalid_config, file)

        generator = NumberGenerator.from_config_file("invalid_config.json", x0=1, n=5)
        self.assertNotEqual(generator.m, -10)  # Asserts that default values are used

    def test_missing_config(self):
        generator = NumberGenerator.from_config_file("non_existing_file.json", x0=1, n=5)
        self.assertIsNotNone(generator)  # Asserts that a generator is still created


class TestGeneratorPeriod(unittest.TestCase):

    def setUp(self):
        self.period_generator = GeneratorPeriod(m=10, a=2, c=3, X0=1)

    def test_get_period(self):
        expected_period = 4 # Expected period based on given parameters
        self.assertEqual(self.period_generator.get_period(), expected_period)


if __name__ == '__main__':
    unittest.main()
