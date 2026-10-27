"""
Automated Integration and API Tests for HamSpam Backend.

Verifies:
1. /health endpoint reports healthy status and model readiness.
2. /api/stats returns accurate dataset counts matching cleaned UCI corpus (5,171 rows).
3. /api/probabilities returns all 5 required keywords and Bayes verification flags.
4. /api/evaluation returns real test-set accuracy, precision, recall, and confusion matrix.
5. /api/predict handles canonical spam messages with high spam probability.
6. /api/predict handles canonical ham messages with high ham probability.
7. /api/predict safely handles whitespace and empty input with is_valid=False.
8. Probability sums P(Ham) + P(Spam) == 1.0 for predictions.
9. Static file serving at '/' returns 200 with HTML content.
"""

import os
import sys
import unittest
from fastapi.testclient import TestClient

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from api import app


class TestHamSpamAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create test client once for all integration tests."""
        cls.client = TestClient(app)

    def test_01_health_endpoint(self):
        """Verify /health returns 200 with healthy status and model_loaded=True."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertTrue(data["model_loaded"])
        self.assertTrue(data["dataset_loaded"])
        self.assertEqual(data["version"], "1.0.0")

    def test_02_stats_endpoint(self):
        """Verify /api/stats returns actual UCI dataset cleaning metrics."""
        response = self.client.get("/api/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["raw_total"], 5574)
        self.assertEqual(data["cleaned_total"], 5171)
        self.assertEqual(data["duplicates_removed"], 403)
        self.assertEqual(data["ham_count"], 4518)
        self.assertEqual(data["spam_count"], 653)
        self.assertAlmostEqual(data["p_ham"] + data["p_spam"], 1.0, places=4)

        # Bernoulli moments
        bern = data["bernoulli"]
        self.assertAlmostEqual(bern["p"], data["p_spam"], places=5)
        self.assertAlmostEqual(bern["expectation_E_Y"], data["p_spam"], places=5)
        self.assertAlmostEqual(bern["variance_Var_Y"], data["p_spam"] * (1.0 - data["p_spam"]), places=5)

    def test_03_probabilities_endpoint(self):
        """Verify /api/probabilities analyzes the 5 designated suspicious words."""
        response = self.client.get("/api/probabilities")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        words = data["words"]
        self.assertEqual(len(words), 5)
        word_names = {w["word"] for w in words}
        self.assertEqual(word_names, {"free", "prize", "win", "urgent", "offer"})

        for item in words:
            self.assertTrue(item["bayes_verified"])
            self.assertLessEqual(item["bayes_direct_diff"], 1e-9)
            self.assertAlmostEqual(
                item["p_spam_given_word_direct"], item["p_spam_given_word_bayes"], places=7
            )

    def test_04_evaluation_endpoint(self):
        """Verify /api/evaluation returns held-out test split metrics."""
        response = self.client.get("/api/evaluation")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["test_size"], 1035)
        self.assertEqual(data["train_size"], 4136)

        metrics = data["metrics"]
        self.assertGreater(metrics["accuracy"], 0.95)
        self.assertGreater(metrics["precision"], 0.90)
        self.assertGreater(metrics["recall"], 0.85)
        self.assertGreater(metrics["f1_score"], 0.90)

        # Confusion matrix checks
        cm = data["confusion_matrix"]
        self.assertEqual(cm["tn"] + cm["fp"] + cm["fn"] + cm["tp"], 1035)
        self.assertEqual(cm["tn"], 898)
        self.assertEqual(cm["fp"], 6)
        self.assertEqual(cm["fn"], 14)
        self.assertEqual(cm["tp"], 117)

    def test_05_predict_canonical_spam(self):
        """Verify /api/predict correctly classifies promotional message."""
        payload = {"message": "Congratulations! You have won a free prize. Claim now."}
        response = self.client.post("/api/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertTrue(data["is_valid"])
        self.assertEqual(data["predicted_label"], "Spam")
        self.assertEqual(data["predicted_class"], 1)
        self.assertGreater(data["p_spam"], 0.90)
        self.assertAlmostEqual(data["p_ham"] + data["p_spam"], 1.0, places=3)
        self.assertIn("SPAM ALERT", data["visual_indicator"])

    def test_06_predict_canonical_ham(self):
        """Verify /api/predict correctly classifies standard lunch message."""
        payload = {"message": "Hey, are we meeting for lunch today?"}
        response = self.client.post("/api/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertTrue(data["is_valid"])
        self.assertEqual(data["predicted_label"], "Ham")
        self.assertEqual(data["predicted_class"], 0)
        self.assertGreater(data["p_ham"], 0.90)
        self.assertAlmostEqual(data["p_ham"] + data["p_spam"], 1.0, places=3)
        self.assertIn("LEGITIMATE HAM", data["visual_indicator"])

    def test_07_predict_empty_and_whitespace(self):
        """Verify /api/predict handles empty or whitespace input safely."""
        for empty_text in ["", "   ", "\t\n"]:
            response = self.client.post("/api/predict", json={"message": empty_text})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertFalse(data["is_valid"])
            self.assertEqual(data["predicted_label"], "Empty / Invalid")
            self.assertIsNone(data["p_ham"])
            self.assertIsNone(data["p_spam"])

    def test_08_root_serves_static_frontend(self):
        """Verify GET / returns 200 and serves frontend index.html."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers.get("content-type", ""))
        self.assertIn("HamSpam", response.text)


if __name__ == "__main__":
    unittest.main()
