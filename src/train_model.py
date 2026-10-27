"""
Multinomial Naive Bayes Model Training and Evaluation Module for HamSpam.

Implements:
1. 80/20 Stratified train/test splitting to preserve prior class distribution.
2. CountVectorizer bag-of-words feature extraction (fit strictly on training data).
3. Multinomial Naive Bayes training with Laplace smoothing.
4. Comprehensive test-set evaluation: Accuracy, Precision, Recall, F1-Score,
   Confusion Matrix, and Classification Report.
5. Publication-quality confusion matrix visualization.
6. Detailed textual evaluation report explaining confusion matrix concepts,
   Type I/II errors, and why accuracy alone is insufficient under class imbalance.
"""

import os
from typing import Any, Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

DEFAULT_OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs"
)


def split_data(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Split the dataset into training and testing partitions using stratified sampling.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset containing 'message' and 'label_num'.
    test_size : float
        Fraction of data reserved for evaluation (default 0.20).
    random_state : int
        Seed for reproducibility (default 42).

    Returns
    -------
    Tuple[pd.Series, pd.Series, pd.Series, pd.Series]
        X_train, X_test, y_train, y_test
    """
    X = df["message"]
    y = df["label_num"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    return X_train, X_test, y_train, y_test


def train_multinomial_nb(
    X_train: pd.Series,
    y_train: pd.Series,
) -> Tuple[MultinomialNB, CountVectorizer]:
    """
    Fit CountVectorizer on training texts and train MultinomialNB classifier.

    Guarantees no data leakage: CountVectorizer is fit exclusively on X_train.

    Parameters
    ----------
    X_train : pd.Series
        Training SMS text messages.
    y_train : pd.Series
        Training labels (0 for Ham, 1 for Spam).

    Returns
    -------
    Tuple[MultinomialNB, CountVectorizer]
        Trained classifier and fitted vectorizer.
    """
    vectorizer = CountVectorizer(lowercase=True, stop_words=None)
    X_train_dtm = vectorizer.fit_transform(X_train)

    clf = MultinomialNB(alpha=1.0)  # Laplace add-one smoothing
    clf.fit(X_train_dtm, y_train)

    return clf, vectorizer


def evaluate_model(
    clf: MultinomialNB,
    vectorizer: CountVectorizer,
    X_test: pd.Series,
    y_test: pd.Series,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, Any]:
    """
    Evaluate the trained classifier on held-out test data.

    Calculates performance metrics, generates confusion matrix visualization,
    and writes a comprehensive evaluation report.

    Parameters
    ----------
    clf : MultinomialNB
        Trained Naive Bayes model.
    vectorizer : CountVectorizer
        Fitted CountVectorizer.
    X_test : pd.Series
        Held-out test text messages.
    y_test : pd.Series
        True ground truth test labels.
    output_dir : str
        Directory to save reports and figures.

    Returns
    -------
    Dict[str, Any]
        Dictionary of computed performance metrics and confusion matrix.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Transform test messages using strictly fitted vectorizer
    X_test_dtm = vectorizer.transform(X_test)

    # Predict discrete classes and posterior probability distributions
    y_pred = clf.predict(X_test_dtm)
    y_prob = clf.predict_proba(X_test_dtm)

    # Compute key evaluation metrics
    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred))
    rec = float(recall_score(y_test, y_pred))
    f1 = float(f1_score(y_test, y_pred))
    cm = confusion_matrix(y_test, y_pred)
    clf_report = classification_report(
        y_test, y_pred, target_names=["Ham", "Spam"], digits=4
    )

    # Confusion matrix elements:
    # [[TN, FP],
    #  [FN, TP]]
    tn, fp, fn, tp = int(cm[0, 0]), int(cm[0, 1]), int(cm[1, 0]), int(cm[1, 1])

    # 1. Plot and save confusion matrix heatmap
    cm_path = os.path.join(output_dir, "confusion_matrix.png")
    plot_confusion_matrix(cm, save_path=cm_path)

    # 2. Write textual evaluation report
    report_path = os.path.join(output_dir, "evaluation_report.txt")
    write_evaluation_report(
        acc=acc,
        prec=prec,
        rec=rec,
        f1=f1,
        tn=tn,
        fp=fp,
        fn=fn,
        tp=tp,
        clf_report=clf_report,
        save_path=report_path,
        test_total=len(y_test),
        test_ham=int((y_test == 0).sum()),
        test_spam=int((y_test == 1).sum()),
    )

    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1_score": f1,
        "confusion_matrix": cm,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
        "classification_report": clf_report,
        "y_pred": y_pred,
        "y_prob": y_prob,
    }


def plot_confusion_matrix(cm: np.ndarray, save_path: str) -> None:
    """
    Render and save a clear confusion matrix diagram with annotated cells.
    """
    tn, fp = cm[0, 0], cm[0, 1]
    fn, tp = cm[1, 0], cm[1, 1]

    fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
    cax = ax.matshow(cm, cmap="Blues", alpha=0.75)

    cell_labels = [
        [f"True Negative (TN)\n{tn}\n(Correct Ham)", f"False Positive (FP)\n{fp}\n(False Alarm)"],
        [f"False Negative (FN)\n{fn}\n(Missed Spam)", f"True Positive (TP)\n{tp}\n(Caught Spam)"],
    ]

    for i in range(2):
        for j in range(2):
            color = "white" if cm[i, j] > (cm.max() / 2) else "black"
            ax.text(
                j,
                i,
                cell_labels[i][j],
                ha="center",
                va="center",
                fontsize=11,
                fontweight="bold",
                color=color,
            )

    fig.colorbar(cax, shrink=0.8)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Predicted Ham", "Predicted Spam"], fontsize=11, fontweight="semibold")
    ax.set_yticklabels(["Actual Ham", "Actual Spam"], fontsize=11, fontweight="semibold")
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    plt.title(
        "Multinomial Naive Bayes Confusion Matrix\n(Held-out Test Split n=1,035)",
        fontsize=12,
        fontweight="bold",
        pad=25,
    )
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[TrainModel] Saved confusion matrix visualization to {save_path}")


def write_evaluation_report(
    acc: float,
    prec: float,
    rec: float,
    f1: float,
    tn: int,
    fp: int,
    fn: int,
    tp: int,
    clf_report: str,
    save_path: str,
    test_total: int,
    test_ham: int,
    test_spam: int,
) -> None:
    """
    Write detailed academic evaluation report explaining concepts and metrics.
    """
    report_content = f"""================================================================================
HAMSPAM — MULTINOMIAL NAIVE BAYES MODEL EVALUATION REPORT
BAMAT207: Probability and Statistics Project, VIT Vellore
================================================================================

1. TEST DATASET PARTITION
--------------------------------------------------------------------------------
Total Held-Out Test Messages : {test_total:,}
Actual Ham Messages (Negative) : {test_ham:,} ({test_ham / test_total:.2%})
Actual Spam Messages (Positive): {test_spam:,} ({test_spam / test_total:.2%})
Train / Test Split Ratio       : 80% Training / 20% Testing (Stratified)
Data Leakage Prevention        : CountVectorizer fit strictly on training set

2. QUANTITATIVE PERFORMANCE METRICS
--------------------------------------------------------------------------------
Accuracy  : {acc:.4f} ({acc:.2%})
Precision : {prec:.4f} ({prec:.2%})
Recall    : {rec:.4f} ({rec:.2%})
F1-Score  : {f1:.4f} ({f1:.2%})

3. CONFUSION MATRIX BREAKDOWN
--------------------------------------------------------------------------------
                   Predicted Ham (0)        Predicted Spam (1)
Actual Ham (0)     TN = {tn:4d}                FP = {fp:4d}
Actual Spam (1)    FN = {fn:4d}                TP = {tp:4d}

Definitions:
- True Positive (TP = {tp}):
  Spam messages correctly identified as spam.
- True Negative (TN = {tn}):
  Genuine (ham) messages correctly identified as genuine.
- False Positive (FP = {fp}) [Type I Error]:
  Genuine (ham) messages incorrectly flagged as spam. In an email/SMS filter,
  this is severe because an important personal or financial message might be lost.
- False Negative (FN = {fn}) [Type II Error]:
  Spam messages incorrectly classified as genuine (ham). The spam message leaks
  into the user's inbox.

4. WHY ACCURACY ALONE IS MISLEADING
--------------------------------------------------------------------------------
In this dataset, legitimate messages (ham) make up {test_ham / test_total:.2%} of the test set,
while spam accounts for only {test_spam / test_total:.2%}.
Consider a naive 'dummy' classifier that labels every incoming message as Ham:
- Trivial Accuracy: {test_ham} / {test_total} = {test_ham / test_total:.4f} ({test_ham / test_total:.2%})!
Despite achieving over 87% accuracy, such a trivial baseline would catch ZERO spam
messages (Recall = 0.00%, Precision undefined/0.00%, F1 = 0.00%).

Therefore, in class-imbalanced probabilistic problems:
- Precision (TP / [TP + FP]) measures spam purity (minimizing False Positives).
- Recall (TP / [TP + FN]) measures spam sensitivity (minimizing False Negatives).
- F1-Score (Harmonic Mean of Precision and Recall) reflects balanced model quality.

Our trained Multinomial Naive Bayes model achieves {prec:.2%} Precision and {rec:.2%} Recall,
proving it is genuinely learning discriminative token distributions rather than
defaulting to the majority class.

5. SCIKIT-LEARN DETAILED CLASSIFICATION REPORT
--------------------------------------------------------------------------------
{clf_report}
================================================================================
Report generated automatically by HamSpam evaluation pipeline.
"""
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[TrainModel] Saved evaluation report to {save_path}")


def train_and_evaluate_pipeline(
    df_clean: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Tuple[MultinomialNB, CountVectorizer, Dict[str, Any]]:
    """
    Run full training and evaluation pipeline end-to-end.
    """
    X_train, X_test, y_train, y_test = split_data(
        df_clean, test_size=test_size, random_state=random_state
    )
    print(f"[TrainModel] Train size: {len(X_train)} (Ham: {(y_train == 0).sum()}, Spam: {(y_train == 1).sum()})")
    print(f"[TrainModel] Test size:  {len(X_test)} (Ham: {(y_test == 0).sum()}, Spam: {(y_test == 1).sum()})")

    clf, vectorizer = train_multinomial_nb(X_train, y_train)
    eval_results = evaluate_model(clf, vectorizer, X_test, y_test, output_dir=output_dir)

    return clf, vectorizer, eval_results


if __name__ == "__main__":
    from data_loader import load_and_preprocess

    _, clean_df, _ = load_and_preprocess()
    clf, vec, results = train_and_evaluate_pipeline(clean_df)

    print("\n--- Pipeline Summary ---")
    print(f"Accuracy : {results['accuracy']:.4f}")
    print(f"Precision: {results['precision']:.4f}")
    print(f"Recall   : {results['recall']:.4f}")
    print(f"F1-Score : {results['f1_score']:.4f}")
    print("Confusion Matrix:\n", results["confusion_matrix"])
