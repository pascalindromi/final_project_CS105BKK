from datetime import datetime
import json
import os


class Storage:

    def __init__(self, filename="data/results.json"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.filename = os.path.join(base_dir, filename)

        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def load_results(self):
        """Load previously saved typing test results."""

        try:
            with open(self.filename, "r") as file:
                return json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_results(self, results):
        """Save all typing test results to JSON."""

        with open(self.filename, "w") as file:
            json.dump(results, file, indent=4)

    def add_result(self, result):

        results = self.load_results()

        test_number = len(results) + 1

        timestamp = datetime.now()

        result["test_name"] = f"test{test_number}"
        result["date"] = timestamp.strftime("%Y-%m-%d")
        result["time"] = timestamp.strftime("%H:%M:%S")

        results.append(result)

        self.save_results(results)

    def clear_results(self):
        """Delete all stored typing test results."""

        self.save_results([])

