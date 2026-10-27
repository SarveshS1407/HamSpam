# HamSpam — Probabilistic SMS Spam Detection Using Bayes' Theorem and Naive Bayes

**Course**: BAMAT207 — Probability and Statistics  
**Institution**: Vellore Institute of Technology (VIT), Vellore  
**Platform**: macOS (Apple Silicon M1 / ARM64 compatible)  
**Language**: Python 3.13  

---

## 1. Project Overview & Objective

The objective of **HamSpam** is to design, mathematically formulate, and computationally implement a complete probabilistic classification system that discriminates between legitimate messages (**Ham**, encoded as $0$) and unsolicited promotional or fraudulent messages (**Spam**, encoded as $1$). 

Rather than treating text classification as a black-box problem, this project bridges core concepts from Probability and Statistics:
- **Empirical Probability & Classical Conditioning**: Computing prior probabilities $P(\text{Spam})$ and $P(\text{Ham})$ and empirical event intersections.
- **Bayes' Theorem**: Inverting conditional probabilities to compute $P(\text{Spam} \mid \text{Word})$ and validating against direct empirical counts.
- **Discrete Random Variables**: Formally modeling the occurrence of spam as a **Bernoulli Random Variable** $Y \sim \text{Bernoulli}(p)$ and analyzing its expectation $E(Y)$, variance $\text{Var}(Y)$, and standard deviation $\sigma(Y)$.
- **Multinomial Naive Bayes (Supervised Machine Learning)**: Applying the conditional independence assumption across a high-dimensional bag-of-words feature space to predict the probability distribution $P(Y \mid \mathbf{x})$ for multi-word SMS messages.

---

## 2. Problem Statement

Mobile spam represents a significant privacy, security, and financial threat to mobile subscribers, ranging from phishing scams to premium-rate fraud. Automatic text categorization must process unstructured natural language strings, tokenize vocabulary tokens, and compute posterior class probabilities efficiently. 

Key statistical challenges addressed in this project include:
1. **Severe Class Imbalance**: Genuine messages substantially outnumber spam messages (~87.37% vs ~12.63%), meaning that trivial accuracy metrics can be deceptive.
2. **Mathematical Equivalence**: Ensuring that theoretical derivations via Bayes' Theorem reconcile with empirical frequency counts.
3. **Data Leakage Prevention**: Ensuring that vocabulary extraction (`CountVectorizer`) is strictly isolated to training partitions.

---

## 3. Dataset Source & Citation

The project uses the **SMS Spam Collection dataset** from the **UCI Machine Learning Repository** (Dataset ID: 228).

- **UCI Repository URL**: [https://archive.ics.uci.edu/dataset/228/sms+spam+collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)
- **Direct Official Archive**: `https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip`
- **Original Uncleaned Size**: 5,574 labelled SMS messages.
- **Cleaned Size**: 5,171 labelled SMS messages (403 duplicates eliminated).

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

---

## 4. Technologies Used

- **Python 3.13** (macOS Apple Silicon M1 native)
- **pandas**: Tabular data manipulation, schema normalization, and cleaning audits.
- **numpy**: Vectorized mathematical arrays and numerical operations.
- **matplotlib**: Publication-quality scientific figures and confusion matrix heatmaps.
- **scikit-learn**: Stratified data partitioning (`train_test_split`), bag-of-words tokenization (`CountVectorizer`), `MultinomialNB`, and evaluation metrics (`accuracy_score`, `precision_score`, `recall_score`, `f1_score`, `confusion_matrix`, `classification_report`).
- **ucimlrepo**: Official programmatic client for UCI Machine Learning Repository datasets.
- **jupyter**: Interactive computational notebook for academic presentation and reproducible workflows.

---

## 5. Directory Structure

```
HamSpam/
├── README.md                           # Comprehensive documentation & mathematical report
├── requirements.txt                    # Project dependencies
├── .gitignore                          # Git ignore specification
├── data/
│   ├── README.md                       # Dataset documentation and schema specifications
│   └── SMSSpamCollection               # Cached raw dataset (auto-downloaded)
├── notebooks/
│   └── HamSpam_Analysis.ipynb          # Fully executed end-to-end Jupyter notebook
├── src/
│   ├── __init__.py                     # Package declaration
│   ├── data_loader.py                  # Dataset acquisition, audit, and cleaning
│   ├── probability_analysis.py         # Empirical Bayes, Bernoulli stats, and plots
│   ├── train_model.py                  # Naive Bayes training, metrics, and report
│   └── predict.py                      # Real-time SMS prediction interface & CLI
├── outputs/
│   ├── dataset_summary.csv             # Statistical breakdown of cleaned corpus
│   ├── word_probability_analysis.csv   # Direct vs Bayes results for 5 keywords
│   ├── class_distribution.png          # High-resolution class distribution bar chart
│   ├── word_probability_chart.png      # Comparative P(Spam | Word) bar chart
│   ├── confusion_matrix.png            # Annotated confusion matrix heatmap
│   └── evaluation_report.txt           # Academic performance analysis report
├── tests/
│   ├── __init__.py                     # Test package declaration
│   └── test_probability_analysis.py    # Automated unit tests
└── scripts/
    └── build_notebook.py               # Notebook generator script
```

---

## 6. Installation & Environment Setup (macOS / MacBook Air M1)

### Prerequisites
- macOS terminal (zsh)
- Python 3.10+ (tested on Python 3.13)

### Step 1: Clone Repository
```bash
git clone https://github.com/SarveshS1407/HamSpam.git
cd HamSpam
```

### Step 2: Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Upgrade pip and Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 7. Execution Commands

### 1. Run Data Preprocessing and Cleaning Audit
```bash
python src/data_loader.py
```
*Output*: Downloads and caches `SMSSpamCollection`, cleans duplicates, and outputs the data audit summary.

### 2. Run Probability and Statistical Analysis
```bash
python src/probability_analysis.py
```
*Output*: Computes class priors, Bernoulli parameters, analyzes the 5 suspicious words, verifies Bayes' Theorem, and saves CSV summaries and PNG charts into `outputs/`.

### 3. Train and Evaluate the Multinomial Naive Bayes Model
```bash
python src/train_model.py
```
*Output*: Performs 80/20 stratified split, fits `CountVectorizer` on training data, fits `MultinomialNB`, generates performance metrics, writes `outputs/evaluation_report.txt`, and generates `outputs/confusion_matrix.png`.

### 4. Real-Time SMS Inference & Demonstration
```bash
python src/predict.py
```
*Output*: Classifies canonical test examples (e.g., prize notifications vs lunch invitations) and displays estimated class probabilities and prediction cards.

### 5. Run Automated Unit Test Suite
```bash
python -m unittest tests/test_probability_analysis.py -v
```
*Output*: Runs all 9 verification tests covering label encodings, prior probabilities, Bernoulli expectation/variance, Bayes' Theorem mathematical consistency, stratified split isolation, and empty input handling.

### 6. Launch the Interactive Jupyter Notebook
```bash
jupyter notebook notebooks/HamSpam_Analysis.ipynb
```
Or execute headless:
```bash
cd notebooks && jupyter nbconvert --to notebook --execute HamSpam_Analysis.ipynb --output HamSpam_Analysis.ipynb && cd ..
```

---

## 8. Mathematical Foundations & Probability Theory

### 8.1 Empirical Prior Class Probabilities
Let the sample space $\Omega$ consist of $N = 5,171$ unique SMS messages.
- $N_{\text{ham}} = 4,518$ (legitimate messages)
- $N_{\text{spam}} = 653$ (unsolicited spam)

Prior probabilities are computed as:
$$P(\text{Ham}) = \frac{N_{\text{ham}}}{N} = \frac{4518}{5171} \approx 0.873719 \quad (87.37\%)$$
$$P(\text{Spam}) = \frac{N_{\text{spam}}}{N} = \frac{653}{5171} \approx 0.126281 \quad (12.63\%)$$
Notice that:
$$P(\text{Ham}) + P(\text{Spam}) = 1.000000$$

---

### 8.2 Word-Based Conditional Probability & Bayes' Theorem

For any suspicious keyword $w$ appearing in the text corpus:
1. **Likelihoods**:
   $$P(w \mid \text{Spam}) = \frac{\text{Count}(\text{Spam messages containing } w)}{N_{\text{spam}}}$$
   $$P(w \mid \text{Ham}) = \frac{\text{Count}(\text{Ham messages containing } w)}{N_{\text{ham}}}$$
2. **Marginal Evidence Probability**:
   $$P(w) = \frac{\text{Count}(\text{Total messages containing } w)}{N}$$
   By the Law of Total Probability:
   $$P(w) = P(w \mid \text{Spam})P(\text{Spam}) + P(w \mid \text{Ham})P(\text{Ham})$$
3. **Direct Posterior Calculation**:
   $$P(\text{Spam} \mid w)_{\text{direct}} = \frac{\text{Count}(\text{Spam messages containing } w)}{\text{Count}(\text{Total messages containing } w)}$$
4. **Posterior Calculation via Bayes' Theorem**:
   $$P(\text{Spam} \mid w)_{\text{bayes}} = \frac{P(w \mid \text{Spam}) \cdot P(\text{Spam})}{P(w)}$$

#### Keyword Matching Methodology
This project uses **case-insensitive whole-word boundary matching** (regex `\b<word>\b`). This prevents substring collisions where legitimate, common words inadvertently trigger spam rules (e.g. without whole-word boundaries, "win" would trigger on "winter", "window", "Darwin", and "unwind").

#### Results for Five Suspicious Keywords

| Word | Total Msgs | Spam Msgs | Ham Msgs | $P(w \mid \text{Spam})$ | $P(w \mid \text{Ham})$ | $P(w)$ | $P(\text{Spam} \mid w)_{\text{direct}}$ | $P(\text{Spam} \mid w)_{\text{bayes}}$ | $P(\text{Ham} \mid w)$ | Discrepancy $|\Delta|$ | Verified |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **free** | 203 | 148 | 55 | 0.226646 | 0.012174 | 0.039257 | **0.729064** | **0.729064** | 0.270936 | $1.11 \times 10^{-16}$ | **PASS** |
| **prize** | 73 | 73 | 0 | 0.111792 | 0.000000 | 0.014117 | **1.000000** | **1.000000** | 0.000000 | $2.22 \times 10^{-16}$ | **PASS** |
| **win** | 55 | 49 | 6 | 0.075038 | 0.001328 | 0.010636 | **0.890909** | **0.890909** | 0.109091 | $1.11 \times 10^{-16}$ | **PASS** |
| **urgent** | 62 | 57 | 5 | 0.087289 | 0.001107 | 0.011990 | **0.919355** | **0.919355** | 0.080645 | $2.22 \times 10^{-16}$ | **PASS** |
| **offer** | 30 | 24 | 6 | 0.036753 | 0.001328 | 0.005802 | **0.800000** | **0.800000** | 0.200000 | $1.11 \times 10^{-16}$ | **PASS** |

**Observation**: For every single word, the direct frequency counting and the analytical Bayes' Theorem formula match up to machine floating-point precision ($|\Delta| < 10^{-15}$). Notably, the word **`prize`** appears in 73 spam messages and exactly 0 ham messages in the cleaned dataset, yielding an empirical conditional probability of $P(\text{Spam} \mid \text{prize}) = 1.0000$ (100%).

---

### 8.3 Spam Occurrence as a Bernoulli Random Variable

We define the binary indicator random variable $Y$:
$$Y = \begin{cases} 1, & \text{if message is Spam} \\ 0, & \text{if message is Ham} \end{cases}$$

Let $p = P(Y = 1) = P(\text{Spam}) = \frac{653}{5171} \approx 0.126281$.  
Then $Y \sim \text{Bernoulli}(p)$ with probability mass function (PMF):
$$P(Y = y) = p^y (1 - p)^{1 - y}, \quad y \in \{0, 1\}$$

#### Theoretical Parameters vs Dataset Reality:
1. **Expectation $E(Y)$**:
   $$E(Y) = \sum_{y \in \{0, 1\}} y \cdot P(Y = y) = 0 \cdot (1 - p) + 1 \cdot p = p \approx 0.126281$$
2. **Second Moment $E(Y^2)$**:
   $$E(Y^2) = 0^2 \cdot (1 - p) + 1^2 \cdot p = p$$
3. **Variance $\text{Var}(Y)$**:
   $$\text{Var}(Y) = E(Y^2) - [E(Y)]^2 = p - p^2 = p(1 - p) = 0.126281 \times (1 - 0.126281) \approx 0.110334$$
4. **Standard Deviation $\sigma(Y)$**:
   $$\sigma(Y) = \sqrt{\text{Var}(Y)} = \sqrt{0.110334} \approx 0.332166$$

#### Statistical Interpretation
- **Expectation**: $E(Y) = p$ signifies the expected value of the Bernoulli indicator, which equals the population proportion of spam messages.
- **Variance**: $\text{Var}(Y) = p(1 - p)$ quantifies the statistical dispersion or uncertainty of a single message drawn at random. For a perfectly balanced dataset ($p = 0.5$), the Bernoulli variance achieves its maximum possible value of $0.25$. Because our dataset is predominantly ham ($p \approx 0.1263$), the variance is substantially smaller ($\text{Var}(Y) \approx 0.1103$), reflecting that the distribution is concentrated near $Y = 0$.

---

## 9. Conceptual Distinction: Empirical Probability vs. Naive Bayes

A critical conceptual distinction in probability theory must be drawn between the single-word empirical calculations and the machine learning model:

> **The Empirical Direct Probability $P(\text{Spam} \mid \text{Word})$** measures the isolated conditional probability of messages containing that single specific token within the historical cleaned dataset. It treats the presence of that single keyword as the entire conditioning event, ignoring all other words in the text.
>
> **The Multinomial Naive Bayes Model** instead estimates the joint posterior probability $P(\text{Spam} \mid \text{Message})$ given the complete sequence of words $\mathbf{x} = (x_1, x_2, \dots, x_V)$ in the message. It does this by combining the prior $P(\text{Spam})$ with the product of individual token likelihoods $P(w_i \mid \text{Spam})^{x_i}$, under the explicit (and naive) simplifying assumption that word occurrences are conditionally independent given the message class.

---

## 10. How Multinomial Naive Bayes Works

### 10.1 Feature Representation via `CountVectorizer`
`CountVectorizer` converts a collection of text documents into a matrix of token counts (Bag-of-Words representation). 
- It tokenizes raw strings, converts characters to lowercase, strips punctuation, and builds a fixed vocabulary $V$ of unique words observed in the **training set**.
- Each message is transformed into a sparse feature vector:
  $$\mathbf{x} = [x_1, x_2, \dots, x_{|V|}]$$
  where $x_i$ represents the frequency count of vocabulary word $w_i$ in that message.
- **Strict Protocol**: To prevent data leakage, `fit_transform()` is executed exclusively on $X_{\text{train}}$. The held-out evaluation set $X_{\text{test}}$ is transformed using `transform()` only, meaning words appearing exclusively in the test set are treated as unseen out-of-vocabulary words.

### 10.2 Mathematical Decision Rule
By Bayes' Theorem, the posterior probability of class $c \in \{0, 1\}$ given message vector $\mathbf{x}$ is:
$$P(Y = c \mid \mathbf{x}) = \frac{P(Y = c) P(\mathbf{x} \mid Y = c)}{P(\mathbf{x})}$$
Since $P(\mathbf{x}) = \sum_{c'} P(Y = c') P(\mathbf{x} \mid Y = c')$ is constant across classes for any given message:
$$P(Y = c \mid \mathbf{x}) \propto P(Y = c) P(\mathbf{x} \mid Y = c)$$

Under the **conditional independence assumption**:
$$P(\mathbf{x} \mid Y = c) = \prod_{i=1}^{|V|} P(w_i \mid Y = c)^{x_i}$$

In log-space to prevent numerical underflow:
$$\log P(Y = c \mid \mathbf{x}) \propto \log P(Y = c) + \sum_{i=1}^{|V|} x_i \log P(w_i \mid Y = c)$$

### 10.3 Laplace (Add-One) Smoothing
If a word $w_i$ never appeared in class $c$ in the training corpus, its maximum likelihood estimate would be $\frac{0}{N_c} = 0$, causing the entire product $\prod P(w_i \mid Y = c)^{x_i}$ to collapse to zero.
To resolve this zero-frequency issue, **Laplace add-one smoothing** ($\alpha = 1.0$) is applied:
$$\hat{P}(w_i \mid Y = c) = \frac{\text{Count}(w_i, c) + \alpha}{\sum_{w \in V} \text{Count}(w, c) + \alpha |V|}$$

---

## 11. Model Evaluation & Confusion Matrix Analysis

The model was evaluated on a held-out test split of $n = 1,035$ messages (80% train / 20% test, stratified sampling, `random_state=42`).

### 11.1 Quantitative Test Performance

| Metric | Formula | Test Result |
| :--- | :--- | :---: |
| **Accuracy** | $\frac{TP + TN}{TP + TN + FP + FN}$ | **98.07%** ($0.9807$) |
| **Precision (Spam)** | $\frac{TP}{TP + FP}$ | **95.12%** ($0.9512$) |
| **Recall (Spam)** | $\frac{TP}{TP + FN}$ | **89.31%** ($0.8931$) |
| **F1-Score (Spam)** | $2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$ | **92.13%** ($0.9213$) |

### 11.2 Confusion Matrix Interpretation

$$\begin{bmatrix} TN & FP \\ FN & TP \end{bmatrix} = \begin{bmatrix} 898 & 6 \\ 14 & 117 \end{bmatrix}$$

- **True Negative (TN = 898)**: Genuine messages correctly classified as Ham.
- **True Positive (TP = 117)**: Spam messages correctly caught and flagged as Spam.
- **False Positive (FP = 6) [Type I Error]**: Genuine messages mistakenly classified as Spam.
  - *Operational Impact*: In SMS/email filtering, Type I errors are critical because an important personal, educational, or transactional notification is sent to junk. Our model produced only 6 false positives out of 904 genuine messages ($0.66\%$ false alarm rate).
- **False Negative (FN = 14) [Type II Error]**: Spam messages mistakenly classified as Ham.
  - *Operational Impact*: An annoyance where promotional or spam SMS slips into the user's primary inbox.

### 11.3 Why Accuracy Alone is Misleading

In our held-out test partition:
- Genuine messages: $904$ ($87.34\%$)
- Spam messages: $131$ ($12.66\%$)

Consider a trivial **dummy majority-class classifier** that blindly predicts **Ham** for every incoming message without reading a single word:
$$\text{Accuracy}_{\text{dummy}} = \frac{904}{1035} \approx 87.34\%$$
$$\text{Recall}_{\text{dummy}} = \frac{0}{131} = 0.00\%$$
$$\text{Precision}_{\text{dummy}} = \text{Undefined} / 0.00\%$$

Despite presenting a seemingly impressive $87.34\%$ accuracy, this dummy filter completely fails to detect even a single spam message. Therefore, evaluating precision, recall, and the F1-score is mandatory when dealing with class-imbalanced datasets.

---

## 12. Real-Time SMS Prediction Results

The real-time inference engine (`src/predict.py`) applies `clf.predict_proba()` to output estimated posterior probabilities:

### Example 1: Promotional / Spam Message
- **Input**: `"Congratulations! You have won a free prize. Claim now."`
- **Prediction**: **`Spam`**
- **$P(\text{Spam} \mid \text{Message})$**: $1.0000$ ($100.00\%$)
- **$P(\text{Ham} \mid \text{Message})$**: $0.0000$ ($0.00\%$)

### Example 2: Ordinary Conversational Message
- **Input**: `"Hey, are we meeting for lunch today?"`
- **Prediction**: **`Ham`**
- **$P(\text{Spam} \mid \text{Message})$**: $0.0000$ ($0.00\%$)
- **$P(\text{Ham} \mid \text{Message})$**: $1.0000$ ($100.00\%$)

### Example 3: Academic / University Notification
- **Input**: `"Can you please send me the lecture slides for BAMAT207?"`
- **Prediction**: **`Ham`**
- **$P(\text{Spam} \mid \text{Message})$**: $0.0017$ ($0.17\%$)
- **$P(\text{Ham} \mid \text{Message})$**: $0.9983$ ($99.83\%$)

### Example 4: Urgent Financial Draw
- **Input**: `"URGENT! You have won a 1 week FREE membership in our £100,000 prize draw!"`
- **Prediction**: **`Spam`**
- **$P(\text{Spam} \mid \text{Message})$**: $1.0000$ ($100.00\%$)
- **$P(\text{Ham} \mid \text{Message})$**: $0.0000$ ($0.00\%$)

### Example 5: Empty Input Handling
- **Input**: `""` or `"   "`
- **Prediction**: **`Empty / Invalid`**
- **Notice**: Input is validated safely without runtime exceptions or fabricated probabilities.

---

## 13. Limitations & Future Improvements

1. **Conditional Independence Assumption**: Naive Bayes assumes all words are conditionally independent given the class label. In natural human language, strong word correlations exist (e.g., "prize" and "claim"). Despite this violation, Naive Bayes often performs well for text categorization because optimal decision boundaries can be preserved even when probability calibrations are skewed.
2. **Out-of-Vocabulary (OOV) Tokens**: New slang, obfuscated spellings (e.g. `w!n`, `fr33`), or emojis not observed in the training vocabulary provide zero likelihood signal.
3. **Context and Semantic Modeling**: Word order and negation are disregarded in simple unigram bag-of-words. For instance, "I did not win the prize" contains suspicious tokens despite being legitimate context. Future work could integrate n-grams (bigrams/trigrams) or transformer-based contextual embeddings (e.g. DistilBERT).
4. **Adaptive Thresholding**: For practical deployment, the classification threshold could be tuned (e.g., $P(\text{Spam} \mid \mathbf{x}) \ge 0.8$) to suppress Type I False Positives to near-zero at the expense of marginal recall.

---

*Project developed for BAMAT207 Probability and Statistics, VIT Vellore.*
