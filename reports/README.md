# HamSpam Academic Project Report (BAMAT207)

This directory contains the submission-ready academic project report for the **BAMAT207 Probability and Statistics** curriculum at **Vellore Institute of Technology (VIT), Vellore**.

---

## Deliverables

| Deliverable File | Description | Verification Status |
| :--- | :--- | :--- |
| **[`HamSpam_Project_Report.pdf`](./HamSpam_Project_Report.pdf)** | Official 10-page publication-quality A4 academic PDF report | Verified (Exactly 10 Pages) |
| **[`HamSpam_Project_Report_Source.py`](./HamSpam_Project_Report_Source.py)** | Standalone Python script (ReportLab) to reproducibly generate the PDF | Passing (`python reports/HamSpam_Project_Report_Source.py`) |
| **[`README.md`](./README.md)** | Technical overview and compilation documentation | Current document |

---

## Report Structure & Contents (10 Pages)

1. **Page 1 — Academic Cover Page & Executive Abstract**
   - Institutional banner: *Vellore Institute of Technology (VIT), Vellore*
   - Course: *BAMAT207 — Probability and Statistics*
   - Title: *HamSpam: Probabilistic SMS Spam Detection*
   - Subtitle: *Discrete Probability Modeling, Bayes' Theorem Verification, and Multinomial Naive Bayes Classification*
   - Executive Abstract callout and 4 KPI badges (98.07% Accuracy, 95.12% Precision, 89.31% Recall, 92.13% F1).
   - Candidate details, registration number placeholders, live deployment link (`https://hamspam.vercel.app`), GitHub URL, and 17/17 test verification status.

2. **Page 2 — Executive Summary & Problem Formulation**
   - SMS channel characteristics vs. legacy email systems (160-char length limits, absent IP headers, smishing risks).
   - Theoretical alignment with BAMAT207 syllabus (discrete random variables, joint distributions, marginal evidence, Bayes' rule).
   - Four project engineering and research objectives.

3. **Page 3 — Dataset Acquisition, Hygiene & Distribution**
   - Official UCI Machine Learning Repository benchmark: SMS Spam Collection (Dataset ID **228**, DOI: 10.24432/C5CC84).
   - Deduplication protocol: 5,574 raw records &rarr; 403 duplicates eliminated &rarr; **5,171 cleaned records** (0 missing values).
   - Class breakdown: 4,518 Ham (87.37%) and 653 Spam (12.63%).
   - Embedded high-resolution graphic: `outputs/class_distribution.png` (Figure 1).

4. **Page 4 — Theoretical Probability & Bernoulli Modeling**
   - Discrete binary random variable formulation $Y \in \{0, 1\}$.
   - Bernoulli parameter estimation: $P(\text{Spam}) = p = 0.126281$, $P(\text{Ham}) = q = 0.873719$.
   - Theoretical derivations of $E(Y) = p = 0.126281$, $\text{Var}(Y) = p(1-p) = 0.110334$, and $\sigma(Y) = 0.332166$.
   - Formal Bayes' Theorem derivation with the Law of Total Probability expansion.

5. **Page 5 — Word-Level Probability Analysis & Bayes Verification**
   - Word boundary regex tokenization (`\bword\b`) across 5 targeted trigger keywords: `free`, `prize`, `win`, `urgent`, `offer`.
   - Comprehensive contingency table comparing direct sample ratios $P(\text{Spam}|W)_{\text{direct}}$ to inverted Bayes posteriors $P(\text{Spam}|W)_{\text{Bayes}}$.
   - Exact mathematical proof of equivalence confirming difference $\le 2.22 \times 10^{-16}$ (floating-point precision limit).
   - Embedded high-resolution graphic: `outputs/word_probability_chart.png` (Figure 2).

6. **Page 6 — Machine Learning Methodology: Multinomial Naive Bayes**
   - 80:20 stratified partition ($N_{\text{train}} = 4,136$, $N_{\text{test}} = 1,035$) with zero data leakage.
   - Bag-of-Words representation ($|V| = 7,297$ vocabulary dimension).
   - Multinomial likelihood formulation and Laplace (additive) smoothing ($\alpha = 1.0$) to avoid zero-probability collapse.
   - Log-space posterior transformations to prevent floating-point underflow.
   - Five-stage end-to-end inference pipeline architecture diagram (Figure 3).

7. **Page 7 — Experimental Results & Performance Evaluation**
   - Full quantitative metrics table (Accuracy: 0.9807, Precision: 0.9512, Recall: 0.8931, F1-Score: 0.9213).
   - Confusion matrix breakdown: True Negatives (898), False Positives (6), False Negatives (14), True Positives (117).
   - Embedded high-resolution graphic: `outputs/confusion_matrix.png` (Figure 4).
   - In-depth analysis of the **Class Imbalance Accuracy Paradox**: why a naive 87.34% baseline has 0% recall, and why high Precision (95.12%) is mission-critical to avoid blocking legitimate communications.

8. **Page 8 — System Architecture, Deployment & Live Inference**
   - Decoupled full-stack architecture: FastAPI / Uvicorn backend + React 18 / Tailwind CSS / Recharts frontend.
   - Production cloud deployment hosted on Vercel at `https://hamspam.vercel.app`.
   - Real-time inference verification on benchmark messages:
     - *"Congratulations! You have won a free prize. Claim now."* &rarr; **SPAM** ($P=1.000000$, 100.0% confidence).
     - *"Hey, are we meeting for lunch today?"* &rarr; **HAM** ($P=1.000000$, 100.0% confidence).
   - Automated testing verification: 17/17 passing tests in 0.23 seconds.

9. **Page 9 — Critical Discussion, Limitations & Future Scope**
   - The "Naive" conditional independence paradox and Domingos & Pazzani (1997) optimality conditions under 0-1 loss.
   - Qualitative audit of the 20 misclassifications (6 False Positives, 14 False Negatives).
   - Comparison table: Multinomial Naive Bayes vs Logistic Regression vs SVM vs Transformers for SMS traffic.
   - Roadmap for subword tokenization (BPE), online Bayesian parameter updates, and transformer ensemble architectures.

10. **Page 10 — References, Artifacts & Academic Declaration**
    - Formal citations (Almeida et al. 2011, UCI Dataset #228, Domingos & Pazzani 1997, Pedregosa et al. 2011, Devore 2015).
    - Links to open-source repository and live web deployment.
    - Mathematical notation quick reference table ($Y, p, q, E(Y), \text{Var}(Y), \sigma(Y), \theta_{ci}, \alpha$).
    - Formal Student Academic Integrity Declaration and Faculty Evaluation sign-off block.

---

## Reproduction & Build Instructions

To re-generate the PDF report from source:

1. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Ensure dependencies are installed**:
   ```bash
   pip install reportlab pymupdf
   ```

3. **Execute the generator script**:
   ```bash
   python reports/HamSpam_Project_Report_Source.py
   ```

4. **Verify the generated deliverable**:
   ```bash
   ls -la reports/HamSpam_Project_Report.pdf
   ```
