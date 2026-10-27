"""
Automated Unit Tests for HamSpam Probability and Statistics Modules.

Verifies:
1. Label encoding (spam=1, ham=0).
2. Class prior probabilities sum to 1.0.
3. Bernoulli random variable properties: E(Y) = p, Var(Y) = p(1-p).
4. Direct conditional probabilities agree with Bayes' Theorem within float tolerance.
5. Zero index overlap between stratified training and testing sets.
6. Multinomial Naive Bayes model returns valid discrete predictions (0 or 1).
7. Predicted posterior class probabilities sum to 1.0 for arbitrary messages.
8. Safe and graceful handling of empty or whitespace-only inputs.
9. Word absent from category division-by-zero resilience.
"""

import math
import os
import sys
import unittest
import numpy as np
import pandas as pd

# Add src to python path for testing
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from data_loader import clean_dataset, load_and_preprocess
from probability_analysis import (
    calculate_bernoulli_statistics,
    calculate_class_probabilities,
    calculate_word_probabilities,
)
from train_model import split_data, train_multinomial_nb
from predict import predict_message


class TestProbabilityAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Load dataset once for all unit tests."""
        cls.raw_df, cls.clean_df, cls.stats = load_and_preprocess()

    def test_01_label_encoding(self):
        """Verify labels are strictly mapped: ham -> 0, spam -> 1."""
        unique_labels = set(self.clean_df["label"].unique())
        self.assertEqual(unique_labels, {"ham", "spam"})

        unique_nums = set(self.clean_df["label_num"].unique())
        self.assertEqual(unique_nums, {0, 1})

        ham_match = (self.clean_df[self.clean_df["label"] == "ham"]["label_num"] == 0).all()
        spam_match = (self.clean_df[self.clean_df["label"] == "spam"]["label_num"] == 1).all()
        self.assertTrue(ham_match, "All ham labels must encode to 0.")
        self.assertTrue(spam_match, "All spam labels must encode to 1.")

    def test_02_class_probabilities_sum_to_one(self):
        """Verify empirical class priors sum to 1.0."""
        class_stats = calculate_class_probabilities(self.clean_df)
        p_ham = class_stats["p_ham"]
        p_spam = class_stats["p_spam"]

        self.assertGreater(p_ham, 0.0)
        self.assertGreater(p_spam, 0.0)
        self.assertAlmostEqual(p_ham + p_spam, 1.0, places=9)

    def test_03_bernoulli_expectation_and_variance(self):
        """Verify E(Y) = p, Var(Y) = p(1-p), and sigma(Y) = sqrt(Var(Y))."""
        class_stats = calculate_class_probabilities(self.clean_df)
        p = class_stats["p_spam"]
        bern = calculate_bernoulli_statistics(p)

        self.assertEqual(bern["expectation_E_Y"], p)
        expected_var = p * (1.0 - p)
        self.assertAlmostEqual(bern["variance_Var_Y"], expected_var, places=9)
        self.assertAlmostEqual(bern["std_dev_sigma_Y"], math.sqrt(expected_var), places=9)
        self.assertAlmostEqual(bern["p_y_1"] + bern["p_y_0"], 1.0, places=9)

    def test_04_bayes_theorem_agrees_with_direct_calculation(self):
        """Verify P(Spam | Word)_direct == P(Spam | Word)_bayes within tolerance."""
        words = ["free", "prize", "win", "urgent", "offer"]
        word_df = calculate_word_probabilities(self.clean_df, words=words, matching="whole_word")

        for _, row in word_df.iterrows():
            word = row["word"]
            p_direct = row["p_spam_given_word_direct"]
            p_bayes = row["p_spam_given_word_bayes"]
            diff = row["bayes_direct_diff"]
            verified = row["bayes_verified"]

            self.assertTrue(
                verified,
                f"Word '{word}' direct ({p_direct:.6f}) and Bayes ({p_bayes:.6f}) differ by {diff}",
            )
            self.assertLessEqual(diff, 1e-9)

    def test_05_train_test_split_no_overlap(self):
        """Verify 80/20 train/test split has zero overlapping indices and maintains stratification."""
        X_train, X_test, y_train, y_test = split_data(
            self.clean_df, test_size=0.2, random_state=42
        )

        train_indices = set(X_train.index)
        test_indices = set(X_test.index)
        intersection = train_indices.intersection(test_indices)
        self.assertEqual(len(intersection), 0, "Train and test splits must not share indices.")

        total_records = len(self.clean_df)
        self.assertEqual(len(X_train) + len(X_test), total_records)
        self.assertAlmostEqual(len(X_test) / total_records, 0.20, delta=0.01)

        # Stratification check
        overall_spam_ratio = self.clean_df["label_num"].mean()
        train_spam_ratio = y_train.mean()
        test_spam_ratio = y_test.mean()

        self.assertAlmostEqual(train_spam_ratio, overall_spam_ratio, places=3)
        self.assertAlmostEqual(test_spam_ratio, overall_spam_ratio, places=3)

    def test_06_model_returns_valid_class_predictions(self):
        """Verify MultinomialNB outputs valid classes {0, 1}."""
        X_train, X_test, y_train, y_test = split_data(self.clean_df, random_state=42)
        clf, vectorizer = train_multinomial_nb(X_train, y_train)

        X_test_dtm = vectorizer.transform(X_test)
        preds = clf.predict(X_test_dtm)

        unique_preds = set(np.unique(preds))
        self.assertTrue(unique_preds.issubset({0, 1}))

    def test_07_predicted_probabilities_sum_to_one(self):
        """Verify model's predicted class probabilities sum to 1.0 for sample inputs."""
        X_train, _, y_train, _ = split_data(self.clean_df, random_state=42)
        clf, vectorizer = train_multinomial_nb(X_train, y_train)

        sample_messages = [
            "Congratulations! You have won a free prize. Claim now.",
            "Hey, are we meeting for lunch today?",
            "Call me when you are free.",
            "Urgent: your account requires password verification.",
            "Normal conversation with no suspicious words at all.",
        ]

        for msg in sample_messages:
            res = predict_message(msg, clf, vectorizer)
            self.assertTrue(res["is_valid"])
            self.assertIn(res["predicted_label"], ["Spam", "Ham"])
            self.assertAlmostEqual(res["p_ham"] + res["p_spam"], 1.0, places=6)

    def test_08_empty_and_whitespace_input_handling(self):
        """Verify empty and whitespace inputs are handled safely without exceptions."""
        X_train, _, y_train, _ = split_data(self.clean_df, random_state=42)
        clf, vectorizer = train_multinomial_nb(X_train, y_train)

        for empty_val in ["", "   ", "\t\n", None]:
            res = predict_message(empty_val, clf, vectorizer)
            self.assertFalse(res["is_valid"])
            self.assertEqual(res["predicted_label"], "Empty / Invalid")
            self.assertIsNone(res["p_ham"])
            self.assertIsNone(res["p_spam"])

    def test_09_absent_word_zero_division_safety(self):
        """Verify words not present in the corpus return safe zero probabilities."""
        absent_word = "xyznonexistentword12345"
        word_df = calculate_word_probabilities(self.clean_df, words=[absent_word])

        self.assertEqual(len(word_df), 1)
        row = word_df.iloc[0]
        self.assertEqual(row["total_messages_with_word"], 0)
        self.assertEqual(row["p_spam_given_word_direct"], 0.0)
        self.assertEqual(row["p_spam_given_word_bayes"], 0.0)
        self.assertTrue(row["bayes_verified"])


if __name__ == "__main__":
    unittest.main()
