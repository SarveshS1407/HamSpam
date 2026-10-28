# HamSpam — Probabilistic SMS Spam Detection Using Bayes' Theorem and Naive Bayes

**Course**: BAMAT207 — Probability and Statistics  
**Institution**: Vellore Institute of Technology (VIT), Vellore  
**Live Application**: [https://hamspam.vercel.app](https://hamspam.vercel.app)  
**Google Colab (One-Click Viva Evaluation)**: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SarveshS1407/HamSpam/blob/main/notebooks/HamSpam_Colab_Evaluation.ipynb)  
**Academic Report PDF**: [reports/HamSpam_Project_Report.pdf](reports/HamSpam_Project_Report.pdf)  
**Report Source Script**: [reports/HamSpam_Project_Report_Source.py](reports/HamSpam_Project_Report_Source.py)  
**Repository**: [https://github.com/SarveshS1407/HamSpam](https://github.com/SarveshS1407/HamSpam)  
**Platform**: macOS (Apple Silicon M1 / ARM64 compatible) & Linux cloud hosts  
**Backend**: Python 3.13, FastAPI, scikit-learn, pandas, NumPy, Uvicorn  
**Frontend**: React 18, Vite, TypeScript, Tailwind CSS, Recharts, Lucide React  

---

## 1. Project Overview & Objective

**HamSpam** is an end-to-end, mathematically rigorous, and publicly deployed probabilistic classification system that discriminates between legitimate messages (**Ham**, encoded as $0$) and unsolicited promotional or fraudulent messages (**Spam**, encoded as $1$).

Rather than treating text classification as a black-box problem, this project bridges core concepts from Probability and Statistics:
1. **Empirical Prior Probabilities**: Directly computed from the cleaned official UCI SMS Spam Collection dataset.
2. **Bayes' Theorem**: Inverting conditional probabilities to compute $P(\text{Spam} \mid \text{Word})$ and numerically proving exact equivalence with direct empirical counting ($|\Delta| < 10^{-15}$).
3. **Discrete Random Variables**: Formally modeling spam occurrence as a **Bernoulli Random Variable** $Y \sim \text{Bernoulli}(p)$ with expectation $E(Y) = p$, variance $\text{Var}(Y) = p(1 - p)$, and standard deviation $\sigma(Y) = \sqrt{\text{Var}(Y)}$.
4. **Multinomial Naive Bayes (Supervised Machine Learning)**: Applying the conditional independence assumption across a bag-of-words feature space (`CountVectorizer`) with Laplace add-one smoothing ($\alpha = 1.0$) to estimate joint posterior class probabilities $P(Y \mid \mathbf{x})$.
5. **Interactive Web Application & Production API**: A responsive, modern dashboard featuring an interactive SMS Spam Detector, Probability Laboratory, and Model Evaluation center, deployed publicly at [https://hamspam.vercel.app](https://hamspam.vercel.app).

---

## 2. Architecture & Public Deployment

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          HAMSPAM ARCHITECTURE                               │
└─────────────────────────────────────────────────────────────────────────────┘

  [ Web Client (React 18 + Vite + TS) ]  ───► [ Vercel Production Deployment ]
                │                                 https://hamspam.vercel.app
                ▼
  [ REST API / Live Backend (FastAPI) ]   ───► [ Unified Server / Render Service ]
    ├── GET  /health                                 http://localhost:8000
    ├── GET  /api/stats                              render.yaml Blueprint
    ├── GET  /api/probabilities
    ├── GET  /api/evaluation
    └── POST /api/predict
                │
                ▼
  [ Probability & ML Core (Python 3.13) ]
    ├── Data Loader (UCI Repository ID: 228)
    ├── Bayes' Theorem Inversion & Bernoulli Modeling
    └── Multinomial Naive Bayes + CountVectorizer (80/20 Stratified Split)
```

- **Live Public Website**: [https://hamspam.vercel.app](https://hamspam.vercel.app)
- **Local Server (Full-Stack)**: `http://localhost:8000` (FastAPI serving both the REST API and the compiled React frontend)
- **Dual-Engine Inference**: The application queries the live FastAPI backend, with an embedded client-side Naive Bayes engine executing the exact mathematical log-sum-exp equation over the trained model parameters ($|\Delta| < 10^{-14}$) during backend cold-starts.

---

## ⚡ One-Click Google Colab Evaluation Notebook

For academic project evaluation, viva presentations, or independent review, you can open and run the complete project in Google Colab with one click:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SarveshS1407/HamSpam/blob/main/notebooks/HamSpam_Colab_Evaluation.ipynb)

- **Direct Colab Link**: [**`https://colab.research.google.com/github/SarveshS1407/HamSpam/blob/main/notebooks/HamSpam_Colab_Evaluation.ipynb`**](https://colab.research.google.com/github/SarveshS1407/HamSpam/blob/main/notebooks/HamSpam_Colab_Evaluation.ipynb)
- **Comprehensive Analysis Notebook**: [**`https://colab.research.google.com/github/SarveshS1407/HamSpam/blob/main/notebooks/HamSpam_Analysis.ipynb`**](https://colab.research.google.com/github/SarveshS1407/HamSpam/blob/main/notebooks/HamSpam_Analysis.ipynb)

### Showing Outputs During Evaluation (Zero Setup Required)
1. **Instant Output Display**: When you open the Colab link, **all outputs, tables, and charts are already pre-computed and displayed**. You can immediately scroll through the results without having to run or wait for any cells.
2. **Auto-Cloning & Dependencies**: If an evaluator asks you to execute a cell live (`Shift + Enter`) or run all cells (**Runtime &rarr; Run all**), Cell 1 automatically detects the Colab environment, clones the `HamSpam` repository, installs any missing packages (`ucimlrepo`), and configures the `src/` modules in under 5 seconds.
3. **Interactive Prediction**: Cell 15 includes an interactive viva demonstration cell where you can type any custom SMS message and view its real-time posterior probabilities $P(\text{Spam} \mid \text{Msg})$ and $P(\text{Ham} \mid \text{Msg})$.

---

## 3. Dataset Source & Preprocessing

The project strictly uses the **SMS Spam Collection dataset** from the **UCI Machine Learning Repository** (Dataset ID: 228).

- **Official UCI URL**: [https://archive.ics.uci.edu/dataset/228/sms+spam+collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)
- **Direct UCI Archive**: `https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip`

### Citation
```bibtex
@misc{sms_spam_collection_228,
  author       = {Almeida, Tiago and Hidalgo, José},
  title        = {{SMS Spam Collection}},
  year         = {2011},
  howpublished = {UCI Machine Learning Repository},
  note         = {{DOI}: https://doi.org/10.24432/C5CC84}
}
```

### Preprocessing and Cleaning Audit
1. **Acquisition**: Retrieved via `ucimlrepo.fetch_ucirepo(id=228)` with automated direct UCI archive download fallback.
2. **Parsing**: Preserved all original rows using `quoting=csv.QUOTE_NONE` to prevent quote-merging truncation.
3. **Audit**:
   - Original uncleaned messages: **5,574**
   - Missing values: **0**
   - Duplicate messages identified and removed: **403**
   - Final cleaned dataset: **5,171** messages
   - Normalized binary encoding: **Spam = 1**, **Ham = 0**
   - Legitimate (Ham) messages: **4,518** ($87.37\%$)
   - Spam messages: **653** ($12.63\%$)

---

## 4. Mathematical Foundations

### 4.1 Empirical Prior Class Probabilities
Let total cleaned messages be $N = 5,171$.
$$P(\text{Ham}) = \frac{N_{\text{ham}}}{N} = \frac{4518}{5171} \approx 0.873719 \quad (87.37\%)$$
$$P(\text{Spam}) = \frac{N_{\text{spam}}}{N} = \frac{653}{5171} \approx 0.126281 \quad (12.63\%)$$
$$P(\text{Ham}) + P(\text{Spam}) = 1.000000$$

---

### 4.2 Word-Based Conditional Probability & Bayes' Theorem

For any suspicious keyword $w$ using case-insensitive whole-word matching (`\b<word>\b`):
1. **Likelihoods**:
   $$P(w \mid \text{Spam}) = \frac{\text{Count}(\text{Spam with } w)}{N_{\text{spam}}}, \quad P(w \mid \text{Ham}) = \frac{\text{Count}(\text{Ham with } w)}{N_{\text{ham}}}$$
2. **Marginal Word Evidence**:
   $$P(w) = \frac{\text{Count}(\text{Total with } w)}{N} = P(w \mid \text{Spam})P(\text{Spam}) + P(w \mid \text{Ham})P(\text{Ham})$$
3. **Direct Posterior Counting**:
   $$P(\text{Spam} \mid w)_{\text{direct}} = \frac{\text{Count}(\text{Spam with } w)}{\text{Count}(\text{Total with } w)}$$
4. **Bayes' Theorem Inversion**:
   $$P(\text{Spam} \mid w)_{\text{bayes}} = \frac{P(w \mid \text{Spam}) \cdot P(\text{Spam})}{P(w)}$$

#### Verified Results for the Five Required Keywords

| Word | Total Msgs | Spam Msgs | Ham Msgs | $P(w \mid \text{Spam})$ | $P(w \mid \text{Ham})$ | $P(w)$ | $P(\text{Spam} \mid w)_{\text{dir}}$ | $P(\text{Spam} \mid w)_{\text{bayes}}$ | $P(\text{Ham} \mid w)$ | Discrepancy $|\Delta|$ | Verified |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **free** | 203 | 148 | 55 | 0.226646 | 0.012174 | 0.039257 | **0.729064** | **0.729064** | 0.270936 | $1.11 \times 10^{-16}$ | **PASS** |
| **prize** | 73 | 73 | 0 | 0.111792 | 0.000000 | 0.014117 | **1.000000** | **1.000000** | 0.000000 | $2.22 \times 10^{-16}$ | **PASS** |
| **win** | 55 | 49 | 6 | 0.075038 | 0.001328 | 0.010636 | **0.890909** | **0.890909** | 0.109091 | $1.11 \times 10^{-16}$ | **PASS** |
| **urgent** | 62 | 57 | 5 | 0.087289 | 0.001107 | 0.011990 | **0.919355** | **0.919355** | 0.080645 | $2.22 \times 10^{-16}$ | **PASS** |
| **offer** | 30 | 24 | 6 | 0.036753 | 0.001328 | 0.005802 | **0.800000** | **0.800000** | 0.200000 | $1.11 \times 10^{-16}$ | **PASS** |

*Note on `prize`*: The token `prize` appears in 73 spam messages and **0** legitimate ham messages in the cleaned dataset, yielding an empirical conditional probability of exactly $1.0000$ ($100\%$).

---

### 4.3 Bernoulli Random Variable Modeling

We define the binary indicator random variable $Y$:
$$Y = \begin{cases} 1, & \text{if message is Spam} \\ 0, & \text{if message is Ham} \end{cases}$$
With parameter $p = P(Y = 1) = P(\text{Spam}) \approx 0.126281$:
- **$P(Y = 1) = p$**: $0.126281$
- **$P(Y = 0) = 1 - p$**: $0.873719$
- **Expected Value**:
  $$E(Y) = 1 \cdot p + 0 \cdot (1 - p) = p = 0.126281$$
- **Variance**:
  $$\text{Var}(Y) = E(Y^2) - [E(Y)]^2 = p - p^2 = p(1 - p) \approx 0.110334$$
- **Standard Deviation**:
  $$\sigma(Y) = \sqrt{\text{Var}(Y)} = \sqrt{0.110334} \approx 0.332166$$

*Statistical Significance*: $E(Y)$ equals the proportion of spam messages in the population. The variance ($0.1103$) is far below the balanced maximum of $0.25$ ($p=0.5$), mathematically quantifying the substantial class imbalance towards legitimate messages.

---

### 4.4 Conceptual Distinction: Empirical Single-Word vs. Multinomial Naive Bayes

> **The Empirical Direct Probability $P(\text{Spam} \mid \text{Word})$** measures the isolated probability of messages containing that single specific token within the historical corpus. It conditions on that single keyword alone, ignoring all surrounding words.
>
> **The Multinomial Naive Bayes Model** instead estimates the joint posterior probability $P(\text{Spam} \mid \text{Message})$ given the complete sequence of words $\mathbf{x} = (x_1, x_2, \dots, x_V)$ in the message, applying learned word likelihoods under the conditional independence assumption.

---

### 4.5 Multinomial Naive Bayes Mathematical Decision Rule

Given a message feature count vector $\mathbf{x} = (x_1, x_2, \dots, x_V)$:
$$P(Y = c \mid \mathbf{x}) \propto P(Y = c) \prod_{i=1}^{V} P(w_i \mid Y = c)^{x_i}$$

In log-space:
$$\log P(Y = c \mid \mathbf{x}) \propto \log P(Y = c) + \sum_{i=1}^{V} x_i \log \hat{P}(w_i \mid Y = c)$$

With Laplace smoothing ($\alpha = 1.0$):
$$\hat{P}(w_i \mid Y = c) = \frac{\text{Count}(w_i, c) + 1}{\sum_{w \in V} \text{Count}(w, c) + |V|}$$

---

## 5. Model Evaluation & Confusion Matrix

Evaluated on the held-out stratified test set ($n = 1,035$, 80% train / 20% test, `random_state=42`):

| Metric | Formula | Test Result |
| :--- | :--- | :---: |
| **Accuracy** | $\frac{TP + TN}{\text{Total}}$ | **98.07%** ($0.9807$) |
| **Precision (Spam)** | $\frac{TP}{TP + FP}$ | **95.12%** ($0.9512$) |
| **Recall (Spam)** | $\frac{TP}{TP + FN}$ | **89.31%** ($0.8931$) |
| **F1-Score (Spam)** | $2 \cdot \frac{P \cdot R}{P + R}$ | **92.13%** ($0.9213$) |

### Confusion Matrix Breakdown
$$\begin{bmatrix} TN & FP \\ FN & TP \end{bmatrix} = \begin{bmatrix} 898 & 6 \\ 14 & 117 \end{bmatrix}$$

- **True Negative (TN = 898)**: Genuine messages correctly identified as Ham.
- **True Positive (TP = 117)**: Spam messages correctly caught and filtered.
- **False Positive (FP = 6) [Type I Error]**: Genuine messages falsely flagged as spam ($0.66\%$ false alarm rate).
- **False Negative (FN = 14) [Type II Error]**: Spam messages missed and delivered to user inbox.

### Why Accuracy Alone is Misleading (The Majority Baseline Paradox)
In the test set:
- Actual Ham: $904$ messages ($87.34\%$)
- Actual Spam: $131$ messages ($12.66\%$)

A dummy baseline classifier that blindly labels every incoming message as **Ham** without reading it achieves an apparent **$87.34\%$ accuracy**, yet detects **$0$** spam messages ($\text{Recall} = 0.00\%$). Our model's **$95.12\%$ Precision** and **$89.31\%$ Recall** prove that it learns discriminative token distributions rather than defaulting to the majority class.

---

## 6. Sample SMS Prediction Results

| Input Message | Predicted Class | $P(\text{Spam} \mid \text{Msg})$ | $P(\text{Ham} \mid \text{Msg})$ | Indicator |
| :--- | :---: | :---: | :---: | :--- |
| `"Congratulations! You have won a free prize. Claim now."` | **Spam** | **1.0000** ($100.00\%$) | **0.0000** ($0.00\%$) | `[ 🚨 SPAM ALERT ]` |
| `"Hey, are we meeting for lunch today?"` | **Ham** | **0.0000** ($0.00\%$) | **1.0000** ($100.00\%$) | `[ 🟢 LEGITIMATE HAM ]` |
| `"URGENT! You have won a 1 week FREE membership in our £100,000 prize draw!"` | **Spam** | **1.0000** ($100.00\%$) | **0.0000** ($0.00\%$) | `[ 🚨 SPAM ALERT ]` |
| `"Can you please send me the lecture slides for BAMAT207?"` | **Ham** | **0.0017** ($0.17\%$) | **0.9983** ($99.83\%$) | `[ 🟢 LEGITIMATE HAM ]` |
| `""` or `"   "` (Empty string) | **Empty / Invalid** | `None` | `None` | `[ ⚠️  EMPTY INPUT ]` (Handled safely without error) |

---

## 7. Project Structure

```
HamSpam/
├── README.md                           # Master academic documentation
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Git ignore specification
├── Procfile                            # Process file for cloud container deployment
├── render.yaml                         # Render Cloud Blueprint
├── vercel.json                         # Vercel deployment configuration
├── package.json                        # Monorepo build orchestrator
├── data/
│   ├── README.md                       # UCI dataset citation & schema documentation
│   └── SMSSpamCollection               # Cached raw dataset (auto-downloaded)
├── notebooks/
│   └── HamSpam_Analysis.ipynb          # Fully executed Jupyter notebook
├── src/
│   ├── __init__.py                     # Package declaration
│   ├── data_loader.py                  # Dataset acquisition, audit & cleaning
│   ├── probability_analysis.py         # Bayes calculations, Bernoulli stats & charts
│   ├── train_model.py                  # Naive Bayes training, metrics & evaluation
│   ├── predict.py                      # CLI inference & demonstration runner
│   └── api.py                          # FastAPI production server & static mounter
├── api/
│   └── index.py                        # Serverless entrypoint
├── frontend/                           # React 18 + Vite + TypeScript web application
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── src/
│   │   ├── App.tsx                     # Main layout & tab router
│   │   ├── api.ts                      # Client-side API caller & exact Bayes fallback
│   │   ├── types.ts                    # TypeScript data definitions
│   │   ├── model_data.json             # Exported real model parameters from scikit-learn
│   │   └── components/
│   │       ├── Navbar.tsx              # Navigation & live API status indicator
│   │       ├── Dashboard.tsx           # KPI cards & distribution charts
│   │       ├── Detector.tsx            # Real-time SMS classifier console
│   │       ├── ProbabilityLab.tsx      # Bayes verification table & comparison chart
│   │       ├── ModelEvaluation.tsx     # Confusion matrix & metrics breakdown
│   │       └── About.tsx               # Methodology, math & UCI citation
│   └── dist/                           # Compiled production static bundle
├── outputs/
│   ├── dataset_summary.csv             # Statistical breakdown of cleaned corpus
│   ├── word_probability_analysis.csv   # Direct vs Bayes results for 5 keywords
│   ├── class_distribution.png          # High-resolution class distribution bar chart
│   ├── word_probability_chart.png      # Comparative P(Spam | Word) bar chart
│   ├── confusion_matrix.png            # Annotated confusion matrix heatmap
│   ├── evaluation_report.txt           # Academic performance analysis report
│   └── model_artifact.json             # Serialized trained model parameters
├── tests/
│   ├── __init__.py
│   ├── test_probability_analysis.py    # 9 statistical & mathematical unit tests
│   └── test_api.py                     # 8 FastAPI integration tests
└── scripts/
    └── build_notebook.py               # Notebook generator script
```

---

## 8. Installation & Reproduction Commands (macOS M1)

### Step 1: Clone Repository
```bash
git clone https://github.com/SarveshS1407/HamSpam.git
cd HamSpam
```

### Step 2: Set Up Python Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Run Data Acquisition & Cleaning
```bash
python src/data_loader.py
```

### Step 4: Run Statistical Analysis & Bayes Verification
```bash
python src/probability_analysis.py
```

### Step 5: Train and Evaluate Naive Bayes Model
```bash
python src/train_model.py
```

### Step 6: Run Automated Test Suite (17 Tests)
```bash
python -m unittest discover tests -v
```

### Step 7: Build Frontend & Run Full-Stack Web Server
```bash
# Build frontend static bundle
cd frontend && npm install && npm run build && cd ..

# Launch FastAPI fullstack server (serves API and React UI on port 8000)
python -m uvicorn src.api:app --host 0.0.0.0 --port 8000
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

### Step 8: (Optional) Run Frontend Dev Server with Hot Reloading
```bash
# In terminal 1:
python -m uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload

# In terminal 2:
cd frontend && npm run dev
```
Open **[http://localhost:3000](http://localhost:3000)**.

---

## 9. Automated Test Verification Summary

Ran the complete test suite:
```
Ran 17 tests in 0.584s
OK (17/17 Passed)
```

- `test_01_health_endpoint`: Verified `/health` returns status healthy and model ready.
- `test_02_stats_endpoint`: Verified actual UCI dataset cleaning metrics (5,171 cleaned rows).
- `test_03_probabilities_endpoint`: Verified all 5 suspicious words and Bayes verification flags.
- `test_04_evaluation_endpoint`: Verified held-out test split metrics (98.07% accuracy, confusion matrix).
- `test_05_predict_canonical_spam`: Verified promotional message classified as Spam with 100% confidence.
- `test_06_predict_canonical_ham`: Verified lunch message classified as Ham with 100% confidence.
- `test_07_predict_empty_and_whitespace`: Verified empty and whitespace inputs handled safely without error.
- `test_08_root_serves_static_frontend`: Verified root URL `/` serves compiled React application.
- `test_01_label_encoding`: Verified ham -> 0, spam -> 1 binary encoding.
- `test_02_class_probabilities_sum_to_one`: Verified $P(\text{Ham}) + P(\text{Spam}) = 1.0$.
- `test_03_bernoulli_expectation_and_variance`: Verified $E(Y) = p$ and $\text{Var}(Y) = p(1 - p)$.
- `test_04_bayes_theorem_agrees_with_direct_calculation`: Verified direct conditional counting and Bayes' theorem agree ($|\Delta| < 10^{-15}$).
- `test_05_train_test_split_no_overlap`: Verified zero index overlap between train and test sets and preserved stratification.
- `test_06_model_returns_valid_class_predictions`: Verified output classes are strictly in $\{0, 1\}$.
- `test_07_predicted_probabilities_sum_to_one`: Verified $P(\text{Ham} \mid \text{Msg}) + P(\text{Spam} \mid \text{Msg}) = 1.0$.
- `test_08_empty_and_whitespace_input_handling`: Verified prediction engine handles empty inputs gracefully.
- `test_09_absent_word_zero_division_safety`: Verified division-by-zero resilience for out-of-vocabulary tokens.

---

## 10. Submission-Ready Academic Project Report (PDF)

The complete academic project report is available inside the repository as a publication-ready 10-page A4 PDF document, along with its reproducible Python generator script:

- **PDF Document**: [**`reports/HamSpam_Project_Report.pdf`**](reports/HamSpam_Project_Report.pdf)
- **Generator Script**: [**`reports/HamSpam_Project_Report_Source.py`**](reports/HamSpam_Project_Report_Source.py)
- **Report Documentation**: [**`reports/README.md`**](reports/README.md)

### Report Page Structure Overview
1. **Page 1 — Cover Page & Abstract**: Institutional banner (VIT Vellore), course credentials, title, subtitle, executive abstract card, 4 KPI badges (98.07% Accuracy, 95.12% Precision, 89.31% Recall, 92.13% F1), candidate metadata, and verification signet.
2. **Page 2 — Executive Summary & Objectives**: SMS channel characteristics, 160-char constraints, smishing risks, alignment with BAMAT207 curriculum, and 4 project objectives.
3. **Page 3 — Dataset Acquisition & Preprocessing**: UCI SMS Spam Collection (#228), 5,574 raw -> 403 duplicates eliminated -> 5,171 cleaned messages, 0 nulls, summary table, and embedded `outputs/class_distribution.png` (Figure 1).
4. **Page 4 — Theoretical Probability & Bernoulli Modeling**: Discrete random variable $Y \in \{0, 1\}$, $p = 0.126281$, derivations of $E(Y) = p$, $\text{Var}(Y) = p(1-p) = 0.110334$, $\sigma(Y) = 0.332166$, and formal Bayes' Theorem derivation.
5. **Page 5 — Word-Level Probability Analysis & Bayes Proof**: Word boundary tokenization (`\bword\b`) across 5 keywords (`free`, `prize`, `win`, `urgent`, `offer`), empirical contingency table, exact proof of identity ($|\Delta| \le 2.22 \times 10^{-16}$), and embedded `outputs/word_probability_chart.png` (Figure 2).
6. **Page 6 — Machine Learning Methodology**: 80/20 stratified split ($N_{\text{train}} = 4,136$, $N_{\text{test}} = 1,035$), zero data leakage, CountVectorizer ($|V| = 7,297$), Multinomial Naive Bayes likelihood, Laplace smoothing ($\alpha = 1.0$), log-space transformations, and 5-stage pipeline diagram (Figure 3).
7. **Page 7 — Experimental Results & Evaluation**: Performance metrics table (Accuracy: 98.07%, Precision: 95.12%, Recall: 89.31%, F1: 92.13%), confusion matrix breakdown ($TN=898$, $FP=6$, $FN=14$, $TP=117$), embedded `outputs/confusion_matrix.png` (Figure 4), and deep dive into the Class Imbalance Accuracy Paradox (87.34% trivial baseline vs genuine discriminative learning).
8. **Page 8 — Full-Stack Architecture & Deployment**: FastAPI backend, React 18 / Tailwind / Recharts UI, Vercel deployment (`https://hamspam.vercel.app`), real-time test inference on canonical messages (100% confidence), and 17/17 automated tests.
9. **Page 9 — Discussion, Limitations & Future Scope**: The "Naive" conditional independence paradox and Domingos & Pazzani (1997) optimality proof under 0-1 loss, qualitative error breakdown (6 FP, 14 FN), comparison table with discriminative classifiers, and future enhancements (BPE, online updating, transformers).
10. **Page 10 — References & Academic Declaration**: Formal bibliography (Almeida et al. 2011, UCI #228, Domingos & Pazzani 1997, Pedregosa et al. 2011, Devore 2015), deliverable artifact links, mathematical notation glossary, and signed Academic Integrity Declaration.

### How to Recompile the PDF Report
```bash
# Ensure report dependencies are installed in your virtual environment
pip install reportlab pymupdf

# Compile the 10-page academic PDF report
python reports/HamSpam_Project_Report_Source.py
```

---

*Project developed for BAMAT207 Probability and Statistics at Vellore Institute of Technology (VIT), Vellore.*
