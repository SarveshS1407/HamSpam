"""
Mathematical Probability and Statistical Analysis Module for HamSpam.

Implements:
1. Prior class probabilities P(Spam) and P(Ham).
2. Word-based conditional probability calculations using direct counting and Bayes' Theorem.
3. Bernoulli random variable modeling: P(Y=1), P(Y=0), E(Y), Var(Y), and StdDev(Y).
4. Verification of Bayes' Theorem equivalence within floating-point tolerance.
5. Publication-quality chart generation for distributions and conditional probabilities.
"""

import math
import os
import re
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DEFAULT_WORDS = ["free", "prize", "win", "urgent", "offer"]
DEFAULT_OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs"
)


def calculate_class_probabilities(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate empirical prior probabilities of the spam and ham classes.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset containing 'label' and 'label_num'.

    Returns
    -------
    Dict[str, float]
        Dictionary with total, ham, and spam counts and probabilities.
    """
    total = len(df)
    if total == 0:
        raise ValueError("Dataset cannot be empty when computing class probabilities.")

    ham_count = int((df["label_num"] == 0).sum())
    spam_count = int((df["label_num"] == 1).sum())

    p_ham = ham_count / total
    p_spam = spam_count / total

    return {
        "total_messages": total,
        "ham_count": ham_count,
        "spam_count": spam_count,
        "p_ham": p_ham,
        "p_spam": p_spam,
    }


def calculate_word_probabilities(
    df: pd.DataFrame,
    words: Optional[List[str]] = None,
    matching: str = "whole_word",
    tolerance: float = 1e-9,
) -> pd.DataFrame:
    """
    Analyze suspicious words using direct counting and Bayes' Theorem.

    For each word:
        P(Word | Spam) = Count(Spam with Word) / Count(Spam)
        P(Word | Ham)  = Count(Ham with Word)  / Count(Ham)
        P(Word)        = Count(Total with Word) / Total
        P(Spam | Word)_direct = Count(Spam with Word) / Count(Total with Word)
        P(Spam | Word)_bayes  = [P(Word | Spam) * P(Spam)] / P(Word)
        P(Ham | Word)         = Count(Ham with Word)  / Count(Total with Word)

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset with 'message', 'label', and 'label_num'.
    words : List[str], optional
        List of words to evaluate. Defaults to ['free', 'prize', 'win', 'urgent', 'offer'].
    matching : str, optional
        'whole_word' uses regex \\bword\\b; 'substring' uses simple substring matching.
    tolerance : float
        Allowable floating-point difference between direct and Bayes calculations.

    Returns
    -------
    pd.DataFrame
        Comprehensive table of counts, conditional probabilities, and verification.
    """
    if words is None:
        words = DEFAULT_WORDS

    class_stats = calculate_class_probabilities(df)
    total_messages = class_stats["total_messages"]
    total_spam = class_stats["spam_count"]
    total_ham = class_stats["ham_count"]
    p_spam = class_stats["p_spam"]
    p_ham = class_stats["p_ham"]

    records = []

    for word in words:
        clean_word = word.strip().lower()
        if matching == "whole_word":
            # Match word with word boundaries to avoid false collisions (e.g., 'winter' for 'win')
            pattern = rf"\b{re.escape(clean_word)}\b"
            mask_has_word = df["message"].str.contains(pattern, case=False, regex=True)
        elif matching == "substring":
            mask_has_word = df["message"].str.lower().str.contains(clean_word, regex=False)
        else:
            raise ValueError(f"Unknown matching mode: {matching}. Choose 'whole_word' or 'substring'.")

        spam_with_word = int((mask_has_word & (df["label_num"] == 1)).sum())
        ham_with_word = int((mask_has_word & (df["label_num"] == 0)).sum())
        total_with_word = int(mask_has_word.sum())

        # Likelihoods: P(Word | Spam) and P(Word | Ham)
        p_word_given_spam = spam_with_word / total_spam if total_spam > 0 else 0.0
        p_word_given_ham = ham_with_word / total_ham if total_ham > 0 else 0.0

        # Marginal probability: P(Word)
        p_word = total_with_word / total_messages if total_messages > 0 else 0.0

        # Direct posterior: P(Spam | Word) = Count(Spam & Word) / Count(Word)
        if total_with_word > 0:
            p_spam_given_word_direct = spam_with_word / total_with_word
            p_ham_given_word = ham_with_word / total_with_word
        else:
            p_spam_given_word_direct = 0.0
            p_ham_given_word = 0.0

        # Bayes' Theorem posterior: [P(Word | Spam) * P(Spam)] / P(Word)
        if p_word > 0:
            p_spam_given_word_bayes = (p_word_given_spam * p_spam) / p_word
        else:
            p_spam_given_word_bayes = 0.0

        diff = abs(p_spam_given_word_direct - p_spam_given_word_bayes)
        verified = diff <= tolerance

        records.append({
            "word": clean_word,
            "spam_messages": spam_with_word,
            "ham_messages": ham_with_word,
            "total_messages_with_word": total_with_word,
            "p_word_given_spam": p_word_given_spam,
            "p_word_given_ham": p_word_given_ham,
            "p_word": p_word,
            "p_spam_given_word_direct": p_spam_given_word_direct,
            "p_spam_given_word_bayes": p_spam_given_word_bayes,
            "p_ham_given_word": p_ham_given_word,
            "bayes_direct_diff": diff,
            "bayes_verified": verified,
        })

    return pd.DataFrame(records)


def calculate_bernoulli_statistics(p_spam: float) -> Dict[str, float]:
    """
    Model the spam indicator as a Bernoulli random variable Y ~ Bernoulli(p).

    Definitions:
        Y = 1 if message is Spam
        Y = 0 if message is Ham
        p = P(Spam)

    Statistical Properties:
        P(Y = 1) = p
        P(Y = 0) = 1 - p
        E(Y)     = 1 * p + 0 * (1 - p) = p
        Var(Y)   = E(Y^2) - [E(Y)]^2 = p - p^2 = p(1 - p)
        StdDev(Y)= sqrt(Var(Y))

    Parameters
    ----------
    p_spam : float
        Prior probability of spam in the dataset.

    Returns
    -------
    Dict[str, float]
        Dictionary with all theoretical parameters.
    """
    if not (0.0 <= p_spam <= 1.0):
        raise ValueError(f"Probability p must be in [0, 1], received: {p_spam}")

    p = p_spam
    q = 1.0 - p
    expectation = p
    variance = p * q
    std_dev = math.sqrt(variance)

    return {
        "p": p,
        "q": q,
        "p_y_1": p,
        "p_y_0": q,
        "expectation_E_Y": expectation,
        "variance_Var_Y": variance,
        "std_dev_sigma_Y": std_dev,
    }


def plot_class_distribution(
    df: pd.DataFrame,
    save_path: Optional[str] = None,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> str:
    """
    Generate and save a publication-quality bar chart of the class distribution.
    """
    os.makedirs(output_dir, exist_ok=True)
    if save_path is None:
        save_path = os.path.join(output_dir, "class_distribution.png")

    class_stats = calculate_class_probabilities(df)
    labels = ["Ham (Legitimate)", "Spam"]
    counts = [class_stats["ham_count"], class_stats["spam_count"]]
    proportions = [class_stats["p_ham"], class_stats["p_spam"]]
    colors = ["#2b5c8f", "#d9534f"]

    plt.figure(figsize=(8, 6), dpi=300)
    bars = plt.bar(labels, counts, color=colors, width=0.5, edgecolor="black", linewidth=1.2)

    # Annotate bars with count and percentage
    for bar, count, prop in zip(bars, counts, proportions):
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            yval + max(counts) * 0.02,
            f"{count:,}\n({prop:.2%})",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    plt.title("SMS Spam Collection — Cleaned Class Distribution\n(BAMAT207 Probability & Statistics)", fontsize=13, fontweight="bold", pad=15)
    plt.xlabel("Message Class", fontsize=11, fontweight="semibold", labelpad=8)
    plt.ylabel("Number of Messages", fontsize=11, fontweight="semibold", labelpad=8)
    plt.ylim(0, max(counts) * 1.15)
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    # Note annotation
    note_text = f"Total messages: {class_stats['total_messages']:,}\nP(Ham) = {class_stats['p_ham']:.4f}\nP(Spam) = {class_stats['p_spam']:.4f}"
    plt.annotate(
        note_text,
        xy=(0.70, 0.75),
        xycoords="axes fraction",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#f8f9fa", edgecolor="#ced4da"),
    )

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[ProbabilityAnalysis] Saved class distribution chart to {save_path}")
    return save_path


def plot_word_probabilities(
    word_df: pd.DataFrame,
    save_path: Optional[str] = None,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> str:
    """
    Generate and save a publication-quality chart comparing P(Spam | Word).
    """
    os.makedirs(output_dir, exist_ok=True)
    if save_path is None:
        save_path = os.path.join(output_dir, "word_probability_chart.png")

    words = word_df["word"].str.upper().tolist()
    p_spam_word = word_df["p_spam_given_word_direct"].tolist()
    total_occurrences = word_df["total_messages_with_word"].tolist()

    plt.figure(figsize=(9, 6), dpi=300)
    bars = plt.bar(
        words,
        p_spam_word,
        color="#e06666",
        edgecolor="#990000",
        linewidth=1.2,
        width=0.55,
    )

    # Add reference baseline line for prior P(Spam)
    baseline_p_spam = 653 / 5171  # ~0.1263
    plt.axhline(
        y=baseline_p_spam,
        color="#333333",
        linestyle="--",
        linewidth=1.5,
        label=f"Overall Prior P(Spam) = {baseline_p_spam:.3f}",
    )

    # Annotate bars
    for bar, prob, occ in zip(bars, p_spam_word, total_occurrences):
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            yval + 0.02,
            f"{prob:.1%}\n(n={occ})",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    plt.title(
        "Posterior Probability P(Spam | Word) for Suspicious Keywords\nBayes' Theorem & Direct Empirical Calculation",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )
    plt.xlabel("Keyword Analyzed (Case-Insensitive, Whole-Word)", fontsize=11, fontweight="semibold", labelpad=8)
    plt.ylabel("P(Spam | Word)", fontsize=11, fontweight="semibold", labelpad=8)
    plt.ylim(0, 1.15)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.legend(loc="upper left", framealpha=0.9)

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[ProbabilityAnalysis] Saved word probability chart to {save_path}")
    return save_path


def run_full_probability_analysis(
    df_clean: pd.DataFrame,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Tuple[Dict[str, float], pd.DataFrame, Dict[str, float]]:
    """
    Execute full statistical and probability pipeline, saving CSVs and charts.
    """
    os.makedirs(output_dir, exist_ok=True)

    # 1. Class probabilities
    class_stats = calculate_class_probabilities(df_clean)

    # 2. Word probabilities
    word_df = calculate_word_probabilities(df_clean, matching="whole_word")

    # 3. Bernoulli statistics
    bernoulli_stats = calculate_bernoulli_statistics(class_stats["p_spam"])

    # 4. Save CSV outputs
    summary_df = pd.DataFrame([
        {"Metric": "Cleaned Total Messages", "Value": class_stats["total_messages"]},
        {"Metric": "Ham Messages", "Value": class_stats["ham_count"]},
        {"Metric": "Spam Messages", "Value": class_stats["spam_count"]},
        {"Metric": "P(Ham)", "Value": f"{class_stats['p_ham']:.6f}"},
        {"Metric": "P(Spam)", "Value": f"{class_stats['p_spam']:.6f}"},
        {"Metric": "Expectation E(Y)", "Value": f"{bernoulli_stats['expectation_E_Y']:.6f}"},
        {"Metric": "Variance Var(Y)", "Value": f"{bernoulli_stats['variance_Var_Y']:.6f}"},
        {"Metric": "Std Dev Sigma(Y)", "Value": f"{bernoulli_stats['std_dev_sigma_Y']:.6f}"},
    ])
    summary_path = os.path.join(output_dir, "dataset_summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"[ProbabilityAnalysis] Saved dataset summary to {summary_path}")

    word_csv_path = os.path.join(output_dir, "word_probability_analysis.csv")
    word_df.to_csv(word_csv_path, index=False)
    print(f"[ProbabilityAnalysis] Saved word probability analysis to {word_csv_path}")

    # 5. Charts
    plot_class_distribution(df_clean, output_dir=output_dir)
    plot_word_probabilities(word_df, output_dir=output_dir)

    return class_stats, word_df, bernoulli_stats


if __name__ == "__main__":
    from data_loader import load_and_preprocess

    _, clean_df, _ = load_and_preprocess()
    class_stats, word_df, bern_stats = run_full_probability_analysis(clean_df)

    print("\n--- Class Distribution & Bernoulli Parameters ---")
    for k, v in class_stats.items():
        print(f"  {k:20}: {v}")
    for k, v in bern_stats.items():
        print(f"  {k:20}: {v:.6f}")

    print("\n--- Word-Based Conditional Probability Analysis ---")
    print(
        word_df[[
            "word",
            "total_messages_with_word",
            "spam_messages",
            "ham_messages",
            "p_spam_given_word_direct",
            "p_spam_given_word_bayes",
            "bayes_verified",
        ]].to_string(index=False)
    )
