"""
Script to generate and execute the HamSpam Jupyter Notebook.
"""

import os
import nbformat as nbf

def generate_notebook():
    nb = nbf.v4.new_notebook()
    cells = []

    # Title & Metadata
    cells.append(nbf.v4.new_markdown_cell(
        "# HamSpam — Probabilistic SMS Spam Detection Using Bayes' Theorem and Naive Bayes\n\n"
        "**Course**: BAMAT207 — Probability and Statistics  \n"
        "**Institution**: Vellore Institute of Technology (VIT), Vellore  \n\n"
        "---\n\n"
        "### Project Overview\n"
        "In probabilistic text classification, determining whether an incoming SMS is legitimate (**Ham**, $Y=0$) "
        "or unsolicited spam (**Spam**, $Y=1$) is a fundamental application of:\n"
        "1. **Classical & Conditional Probability**: Empirical event probabilities directly observed in the corpus.\n"
        "2. **Bayes' Theorem**: Inverting conditional probabilities to compute $P(\\text{Spam} \\mid \\text{Word})$.\n"
        "3. **Discrete Random Variables**: Modeling spam incidence as a **Bernoulli Random Variable** $Y \\sim \\text{Bernoulli}(p)$ with expectation $E(Y)$ and variance $\\text{Var}(Y)$.\n"
        "4. **Machine Learning via Multinomial Naive Bayes**: Applying the naive conditional independence assumption over bag-of-words count vectors to compute $P(\\text{Spam} \\mid \\mathbf{x})$.\n\n"
        "This notebook provides an end-to-end, rigorous mathematical and computational implementation using the official **UCI SMS Spam Collection dataset**."
    ))

    # 1. Imports and Setup
    cells.append(nbf.v4.new_markdown_cell(
        "## 1. Imports and Environment Setup\n"
        "We configure the Python runtime environment, import scientific libraries, and set up project directory paths."
    ))

    cells.append(nbf.v4.new_code_cell(
        "import os\n"
        "import sys\n"
        "import math\n"
        "import re\n"
        "import csv\n"
        "import numpy as np\n"
        "import pandas as pd\n"
        "import matplotlib.pyplot as plt\n\n"
        "# Add src module to python path\n"
        "SRC_DIR = os.path.abspath(os.path.join(os.getcwd(), '..', 'src'))\n"
        "if SRC_DIR not in sys.path:\n"
        "    sys.path.insert(0, SRC_DIR)\n\n"
        "from data_loader import load_and_preprocess\n"
        "from probability_analysis import (\n"
        "    calculate_class_probabilities,\n"
        "    calculate_word_probabilities,\n"
        "    calculate_bernoulli_statistics,\n"
        "    plot_class_distribution,\n"
        "    plot_word_probabilities,\n"
        ")\n"
        "from train_model import (\n"
        "    split_data,\n"
        "    train_multinomial_nb,\n"
        "    evaluate_model,\n"
        "    plot_confusion_matrix,\n"
        ")\n"
        "from predict import predict_message, format_prediction_card\n\n"
        "print('Environment successfully configured.')"
    ))

    # 2. Dataset Loading and Cleaning
    cells.append(nbf.v4.new_markdown_cell(
        "## 2. Dataset Acquisition, Inspection, and Cleaning\n"
        "The dataset is retrieved from the **UCI Machine Learning Repository** (Dataset ID: 228).\n"
        "The preprocessing pipeline performs:\n"
        "1. Acquisition via `ucimlrepo` with direct UCI archive fallback.\n"
        "2. Parsing with `quoting=csv.QUOTE_NONE` to preserve all 5,574 original records.\n"
        "3. Checking for missing values.\n"
        "4. Removing duplicate messages and documenting counts.\n"
        "5. Normalizing labels into binary format (Spam = 1, Ham = 0)."
    ))

    cells.append(nbf.v4.new_code_cell(
        "df_raw, df_clean, cleaning_stats = load_and_preprocess()\n\n"
        "print('--- Data Cleaning Audit ---')\n"
        "for k, v in cleaning_stats.items():\n"
        "    print(f'  {k:22}: {v:,}')\n\n"
        "print(f'\\nRaw dimensions   : {df_raw.shape}')\n"
        "print(f'Cleaned dimensions: {df_clean.shape}')\n"
        "print('\\nFirst 5 cleaned records:')\n"
        "df_clean.head()"
    ))

    # 3. Exploratory Data Analysis & Class Priors
    cells.append(nbf.v4.new_markdown_cell(
        "## 3. Exploratory Data Analysis & Class Priors\n"
        "Let the cleaned sample space $\\Omega$ consist of $N = 5,171$ unique SMS messages.\n"
        "The prior probabilities of legitimate ham and spam are:\n"
        "$$P(\\text{Ham}) = \\frac{N_{\\text{ham}}}{N}$$\n"
        "$$P(\\text{Spam}) = \\frac{N_{\\text{spam}}}{N}$$\n"
        "Where $P(\\text{Ham}) + P(\\text{Spam}) = 1$."
    ))

    cells.append(nbf.v4.new_code_cell(
        "class_stats = calculate_class_probabilities(df_clean)\n\n"
        "print('--- Class Probability Statistics ---')\n"
        "print(f\"Total Unique Messages (N) : {class_stats['total_messages']:,}\")\n"
        "print(f\"Legitimate Messages (Ham) : {class_stats['ham_count']:,} | P(Ham)  = {class_stats['p_ham']:.6f} ({class_stats['p_ham']:.2%})\")\n"
        "print(f\"Spam Messages (Spam)      : {class_stats['spam_count']:,} | P(Spam) = {class_stats['p_spam']:.6f} ({class_stats['p_spam']:.2%})\")\n\n"
        "# Generate and display publication-quality class distribution plot\n"
        "plot_path = plot_class_distribution(df_clean, output_dir='../outputs')\n"
        "from IPython.display import Image\n"
        "Image(filename=plot_path)"
    ))

    # 4. Word-based Conditional Probability Analysis
    cells.append(nbf.v4.new_markdown_cell(
        "## 4. Word-Based Conditional Probability Analysis\n"
        "We analyze five suspicious keywords: `free`, `prize`, `win`, `urgent`, and `offer`.\n\n"
        "### Mathematical Formulations:\n"
        "1. **Likelihood**:\n"
        "   $$P(\\text{Word} \\mid \\text{Spam}) = \\frac{\\text{Count}(\\text{Spam containing Word})}{N_{\\text{spam}}}$$\n"
        "   $$P(\\text{Word} \\mid \\text{Ham}) = \\frac{\\text{Count}(\\text{Ham containing Word})}{N_{\\text{ham}}}$$\n"
        "2. **Marginal Word Probability**:\n"
        "   $$P(\\text{Word}) = \\frac{\\text{Count}(\\text{Total messages containing Word})}{N}$$\n"
        "3. **Direct Posterior Calculation**:\n"
        "   $$P(\\text{Spam} \\mid \\text{Word})_{\\text{direct}} = \\frac{\\text{Count}(\\text{Spam containing Word})}{\\text{Count}(\\text{Total messages containing Word})}$$\n"
        "4. **Bayes' Theorem Formulation**:\n"
        "   $$P(\\text{Spam} \\mid \\text{Word})_{\\text{bayes}} = \\frac{P(\\text{Word} \\mid \\text{Spam}) \\cdot P(\\text{Spam})}{P(\\text{Word})}$$\n"
        "5. **Complementary Ham Posterior**:\n"
        "   $$P(\\text{Ham} \\mid \\text{Word}) = \\frac{\\text{Count}(\\text{Ham containing Word})}{\\text{Count}(\\text{Total messages containing Word})} = 1 - P(\\text{Spam} \\mid \\text{Word})$$\n\n"
        "*Methodological Note*: We enforce case-insensitive whole-word boundary matching (`\\bword\\b`) to avoid conflating words like `window` or `winter` with `win`."
    ))

    cells.append(nbf.v4.new_code_cell(
        "words_to_analyze = ['free', 'prize', 'win', 'urgent', 'offer']\n"
        "word_df = calculate_word_probabilities(df_clean, words=words_to_analyze, matching='whole_word')\n\n"
        "display_cols = [\n"
        "    'word',\n"
        "    'spam_messages',\n"
        "    'ham_messages',\n"
        "    'total_messages_with_word',\n"
        "    'p_word_given_spam',\n"
        "    'p_word_given_ham',\n"
        "    'p_word',\n"
        "    'p_spam_given_word_direct',\n"
        "    'p_spam_given_word_bayes',\n"
        "    'p_ham_given_word',\n"
        "    'bayes_direct_diff',\n"
        "    'bayes_verified',\n"
        "]\n\n"
        "print('--- Word Conditional Probability Table ---')\n"
        "display_df = word_df[display_cols].copy()\n"
        "display_df.columns = [\n"
        "    'Word',\n"
        "    'Spam Msg',\n"
        "    'Ham Msg',\n"
        "    'Total Msg',\n"
        "    'P(W|Spam)',\n"
        "    'P(W|Ham)',\n"
        "    'P(W)',\n"
        "    'P(Spam|W) Dir',\n"
        "    'P(Spam|W) Bayes',\n"
        "    'P(Ham|W)',\n"
        "    'Diff',\n"
        "    'Verified',\n"
        "]\n"
        "display_df.round(6)"
    ))

    # 5. Bayes' Theorem Verification & Comparative Chart
    cells.append(nbf.v4.new_markdown_cell(
        "## 5. Bayes' Theorem Verification & Comparative Chart\n"
        "We verify that direct conditional counting and Bayes' Theorem yield identical results within floating-point tolerance ($|\\Delta| < 10^{-9}$)."
    ))

    cells.append(nbf.v4.new_code_cell(
        "all_verified = word_df['bayes_verified'].all()\n"
        "max_diff = word_df['bayes_direct_diff'].max()\n"
        "print(f\"All 5 words mathematically verified via Bayes' Theorem: {all_verified}\")\n"
        "print(f\"Maximum floating point discrepancy: {max_diff:.2e}\")\n\n"
        "chart_path = plot_word_probabilities(word_df, output_dir='../outputs')\n"
        "Image(filename=chart_path)"
    ))

    # 6. Random Variable, Expectation, and Variance
    cells.append(nbf.v4.new_markdown_cell(
        "## 6. Random Variable, Expectation, and Variance\n\n"
        "### Modeling Spam as a Bernoulli Random Variable\n"
        "Let $Y$ be the binary indicator random variable:\n"
        "$$Y = \\begin{cases} 1, & \\text{if the message is Spam} \\\\ 0, & \\text{if the message is Ham} \\end{cases}$$\n"
        "Let parameter $p = P(Y = 1) = P(\\text{Spam})$.\n"
        "Then $Y \\sim \\text{Bernoulli}(p)$ with probability mass function (PMF):\n"
        "$$P(Y = y) = p^y (1 - p)^{1 - y}, \\quad y \\in \\{0, 1\\}$$\n\n"
        "### Mathematical Derivations:\n"
        "- **Expectation $E(Y)$**:\n"
        "  $$E(Y) = \\sum_{y \\in \\{0, 1\\}} y \\cdot P(Y = y) = 0 \\cdot (1 - p) + 1 \\cdot p = p$$\n"
        "- **Variance $\\text{Var}(Y)$**:\n"
        "  $$E(Y^2) = 0^2 \\cdot (1 - p) + 1^2 \\cdot p = p$$\n"
        "  $$\\text{Var}(Y) = E(Y^2) - [E(Y)]^2 = p - p^2 = p(1 - p)$$\n"
        "- **Standard Deviation $\\sigma(Y)$**:\n"
        "  $$\\sigma(Y) = \\sqrt{\\text{Var}(Y)} = \\sqrt{p(1 - p)}$$\n\n"
        "### Statistical Interpretation:\n"
        "- $E(Y) = p$ represents the long-run expected proportion of spam in any random sample from this population.\n"
        "- $\\text{Var}(Y) = p(1 - p)$ quantifies dispersion. For a balanced class ($p=0.5$), variance reaches its theoretical maximum of $0.25$. In our dataset, $p \\approx 0.1263$, leading to $\\text{Var}(Y) \\approx 0.1103$, reflecting heavy skew towards genuine messages."
    ))

    cells.append(nbf.v4.new_code_cell(
        "p_spam = class_stats['p_spam']\n"
        "bern = calculate_bernoulli_statistics(p_spam)\n\n"
        "print('--- Bernoulli Random Variable Y ~ Bernoulli(p) ---')\n"
        "print(f\"Success probability p = P(Y = 1) = P(Spam) : {bern['p']:.6f}\")\n"
        "print(f\"Failure probability q = P(Y = 0) = P(Ham)  : {bern['q']:.6f}\")\n"
        "print(f\"Expected Value E(Y) = p                   : {bern['expectation_E_Y']:.6f}\")\n"
        "print(f\"Theoretical Variance Var(Y) = p(1 - p)     : {bern['variance_Var_Y']:.6f}\")\n"
        "print(f\"Standard Deviation sigma(Y)               : {bern['std_dev_sigma_Y']:.6f}\")\n\n"
        "sample_mean = df_clean['label_num'].mean()\n"
        "sample_var = df_clean['label_num'].var(ddof=0)\n"
        "print(f\"\\nEmpirical dataset mean (sum(Y)/N)          : {sample_mean:.6f} (Diff: {abs(sample_mean - bern['expectation_E_Y']):.2e})\")\n"
        "print(f\"Empirical dataset variance (population var): {sample_var:.6f} (Diff: {abs(sample_var - bern['variance_Var_Y']):.2e})\")"
    ))

    # 7. Machine Learning - Multinomial Naive Bayes
    cells.append(nbf.v4.new_markdown_cell(
        "## 7. Machine Learning: Multinomial Naive Bayes Classifier\n\n"
        "### Model Pipeline:\n"
        "1. **80% Training / 20% Testing Split**: Stratified by label to preserve prior class balance.\n"
        "2. **CountVectorizer**: Bag-of-words tokenization and frequency counting, fit strictly on $X_{\\text{train}}$ to eliminate data leakage.\n"
        "3. **Multinomial Naive Bayes Formulation**:\n"
        "   $$P(Y = c \\mid \\mathbf{x}) \\propto P(Y = c) \\prod_{i=1}^V P(w_i \\mid Y = c)^{x_i}$$\n"
        "   With Laplace add-one smoothing ($\\alpha = 1.0$):\n"
        "   $$\\hat{P}(w_i \\mid Y = c) = \\frac{\\text{Count}(w_i, c) + \\alpha}{\\sum_{w} \\text{Count}(w, c) + \\alpha V}$$"
    ))

    cells.append(nbf.v4.new_code_cell(
        "X_train, X_test, y_train, y_test = split_data(df_clean, test_size=0.2, random_state=42)\n\n"
        "print(f'Training split size: {len(X_train):,} messages (Ham: {(y_train == 0).sum():,}, Spam: {(y_train == 1).sum():,})')\n"
        "print(f'Testing split size : {len(X_test):,} messages (Ham: {(y_test == 0).sum():,}, Spam: {(y_test == 1).sum():,})')\n\n"
        "# Fit vectorizer strictly on X_train and train MultinomialNB\n"
        "clf, vectorizer = train_multinomial_nb(X_train, y_train)\n"
        "vocab_size = len(vectorizer.vocabulary_)\n"
        "print(f'\\nVocabulary size fit on training corpus: {vocab_size:,} unique words.')"
    ))

    # 8. Model Evaluation & Confusion Matrix
    cells.append(nbf.v4.new_markdown_cell(
        "## 8. Model Evaluation on Held-Out Test Data\n"
        "We evaluate model predictions on the unseen test set ($n = 1,035$)."
    ))

    cells.append(nbf.v4.new_code_cell(
        "eval_results = evaluate_model(clf, vectorizer, X_test, y_test, output_dir='../outputs')\n\n"
        "print('--- Test Set Performance Metrics ---')\n"
        "print(f\"Accuracy : {eval_results['accuracy']:.4f} ({eval_results['accuracy']:.2%})\")\n"
        "print(f\"Precision: {eval_results['precision']:.4f} ({eval_results['precision']:.2%})\")\n"
        "print(f\"Recall   : {eval_results['recall']:.4f} ({eval_results['recall']:.2%})\")\n"
        "print(f\"F1-Score : {eval_results['f1_score']:.4f} ({eval_results['f1_score']:.2%})\")\n\n"
        "print('\\nConfusion Matrix [ [TN, FP], [FN, TP] ]:')\n"
        "print(eval_results['confusion_matrix'])\n\n"
        "print('\\nDetailed Classification Report:')\n"
        "print(eval_results['classification_report'])\n\n"
        "cm_img_path = os.path.join('../outputs', 'confusion_matrix.png')\n"
        "Image(filename=cm_img_path)"
    ))

    # 9. Academic Discussion: Confusion Matrix & Class Imbalance
    cells.append(nbf.v4.new_markdown_cell(
        "### Academic Discussion: Why Accuracy Alone is Misleading\n\n"
        "In our test partition of $1,035$ messages:\n"
        "- Actual Ham: $904$ messages ($87.34\\%$)\n"
        "- Actual Spam: $131$ messages ($12.66\\%$)\n\n"
        "**The Dummy Majority-Class Paradox**:\n"
        "If a naive baseline classifier simply classified every single message as **Ham**:\n"
        "- **Accuracy**: $904 / 1035 = 87.34\\%$\n"
        "- **Spam Recall**: $0 / 131 = 0.00\\%$\n\n"
        "Despite boasting an apparently high $87.34\\%$ accuracy, such a filter would fail completely in practice, "
        "allowing $100\\%$ of spam to penetrate the user's inbox.\n\n"
        "**Confusion Matrix Error Types in Spam Detection**:\n"
        "- **True Negative (TN = 898)**: Genuine message correctly identified as ham.\n"
        "- **True Positive (TP = 117)**: Spam message correctly identified as spam.\n"
        "- **False Positive (FP = 6)** [Type I Error]: Genuine message flagged as spam. "
        "In email/SMS filtering, FP is considered severe because legitimate personal or financial alerts may be lost.\n"
        "- **False Negative (FN = 14)** [Type II Error]: Spam message missed and delivered as ham.\n\n"
        "Our Multinomial Naive Bayes model achieves **Precision = 95.12%**, **Recall = 89.31%**, and **F1-Score = 92.13%**, "
        "confirming that it is learning genuine discriminant features rather than trivial majority guessing."
    ))

    # 10. Real-Time SMS Prediction
    cells.append(nbf.v4.new_markdown_cell(
        "## 9. Real-Time SMS Prediction Interface\n\n"
        "Using `clf.predict_proba()`, we compute the model's estimated posterior class probabilities for any SMS input.\n\n"
        "> **Important Conceptual Distinction**:\n"
        "> - The single-word calculation $P(\\text{Spam} \\mid \\text{Word})$ evaluates empirical probability based solely on that isolated keyword in the cleaned corpus.\n"
        "> - The Multinomial Naive Bayes model estimates $P(\\text{Spam} \\mid \\text{Message})$ over the complete joint message word-vector $\\mathbf{x}$ using learned likelihoods and naive conditional independence assumptions."
    ))

    cells.append(nbf.v4.new_code_cell(
        "sample_messages = [\n"
        "    'Congratulations! You have won a free prize. Claim now.',\n"
        "    'Hey, are we meeting for lunch today?',\n"
        "    'URGENT! You have won a 1 week FREE membership in our £100,000 prize draw!',\n"
        "    'Can you please send me the lecture slides for BAMAT207?',\n"
        "    'Exclusive offer: Get 50% discount on your next pizza order. Reply WIN to 8888.',\n"
        "    '',      # Empty test\n"
        "    '   '    # Whitespace test\n"
        "]\n\n"
        "for msg in sample_messages:\n"
        "    res = predict_message(msg, clf, vectorizer)\n"
        "    print(format_prediction_card(res))\n"
        "    print()"
    ))

    # 11. Interactive Testing Cell
    cells.append(nbf.v4.new_markdown_cell(
        "### Interactive Custom SMS Prediction Cell\n"
        "Modify the `custom_sms` string below to test any SMS message:"
    ))

    cells.append(nbf.v4.new_code_cell(
        "# Enter any custom SMS text here:\n"
        "custom_sms = 'Dear student, your VIT grade report for BAMAT207 is now ready to view.'\n\n"
        "result = predict_message(custom_sms, clf, vectorizer)\n"
        "print(format_prediction_card(result))"
    ))

    # 12. Conclusion
    cells.append(nbf.v4.new_markdown_cell(
        "## 10. Conclusion and Project Summary\n\n"
        "- **Dataset Audit**: 5,574 original records $\\to$ 5,171 cleaned records (403 duplicates eliminated).\n"
        "- **Class Priors**: $P(\\text{Ham}) = 0.8737$, $P(\\text{Spam}) = 0.1263$.\n"
        "- **Bayes' Theorem**: Numerically verified across suspicious words (`free`, `prize`, `win`, `urgent`, `offer`), with zero mathematical deviation ($|\\Delta| < 10^{-15}$).\n"
        "- **Bernoulli Modeling**: $E(Y) = 0.1263$, $\\text{Var}(Y) = 0.1103$, $\\sigma(Y) = 0.3322$.\n"
        "- **Model Generalization**: Multinomial Naive Bayes achieved **98.07% Accuracy**, **95.12% Precision**, **89.31% Recall**, and **92.13% F1-Score** on held-out test data."
    ))

    nb["cells"] = cells

    os.makedirs("notebooks", exist_ok=True)
    nb_path = os.path.join("notebooks", "HamSpam_Analysis.ipynb")
    with open(nb_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Generated notebook at: {nb_path}")

if __name__ == "__main__":
    generate_notebook()
