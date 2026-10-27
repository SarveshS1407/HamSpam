"""
HamSpam Project Report PDF Generator (BAMAT207)
==============================================
Academic Project Report for BAMAT207: Probability and Statistics
Vellore Institute of Technology (VIT), Vellore

Generates an authoritative, publication-quality 10-page A4 PDF report detailing
the mathematical foundations, empirical Bayes' theorem verification,
Multinomial Naive Bayes modeling, experimental results, and full-stack deployment.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
    HRFlowable,
)
from reportlab.pdfgen import canvas
import pymupdf

# ==============================================================================
# COLOR PALETTE SPECIFICATION
# ==============================================================================
NAVY_PRIMARY = colors.HexColor("#0F172A")      # Slate 900: Deep Academic Navy
SLATE_HEADER = colors.HexColor("#1E293B")      # Slate 800: Section Headers
TEXT_MAIN = colors.HexColor("#334155")         # Slate 700: Body Text
TEXT_MUTED = colors.HexColor("#64748B")        # Slate 500: Auxiliary & Subtitles
BLUE_ACCENT = colors.HexColor("#2563EB")       # Blue 600: Primary Links & Highlights
BLUE_DARK = colors.HexColor("#1D4ED8")         # Blue 700: Subheadings & Accents
BLUE_LIGHT_BG = colors.HexColor("#EFF6FF")     # Blue 50: Callout Fills
BORDER_COLOR = colors.HexColor("#CBD5E1")      # Slate 300: Table Grids & Lines
BORDER_LIGHT = colors.HexColor("#E2E8F0")      # Slate 200: Subtle Borders
BG_CARD = colors.HexColor("#F8FAFC")           # Slate 50: Card Backgrounds
BG_ALT_ROW = colors.HexColor("#F1F5F9")        # Slate 100: Table Row Alternation
GREEN_SUCCESS = colors.HexColor("#059669")     # Emerald 600: Verified / Ham
RED_ACCENT = colors.HexColor("#DC2626")        # Red 600: Spam / Alerts
AMBER_WARNING = colors.HexColor("#D97706")     # Amber 600: Warnings
WHITE = colors.HexColor("#FFFFFF")


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas that dynamically counts total pages and draws running
    academic headers and footers across all content pages.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress header and footer on cover page
            return

        self.saveState()

        # Running Academic Header
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(SLATE_HEADER)
        self.drawString(36, 812, "VELLORE INSTITUTE OF TECHNOLOGY  |  BAMAT207: PROBABILITY AND STATISTICS")
        self.setFont("Helvetica", 7.5)
        self.setFillColor(TEXT_MUTED)
        self.drawRightString(559, 812, "HamSpam: Probabilistic SMS Spam Detection")

        self.setLineWidth(0.6)
        self.setStrokeColor(BORDER_COLOR)
        self.line(36, 805, 559, 805)

        # Running Academic Footer
        self.line(36, 36, 559, 36)
        self.setFont("Helvetica", 7.5)
        self.setFillColor(TEXT_MUTED)
        self.drawString(36, 26, "Official Benchmark: UCI SMS Spam Collection (#228)  •  Multinomial Naive Bayes Model")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 26, page_str)

        self.restoreState()


def create_styles():
    """Build unified typographical hierarchy matching academic publishing guidelines."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="CoverInst",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=BLUE_DARK,
        alignment=0,
        spaceAfter=3,
    ))

    styles.add(ParagraphStyle(
        name="CoverSubInst",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=TEXT_MUTED,
        alignment=0,
        spaceAfter=10,
    ))

    styles.add(ParagraphStyle(
        name="CoverCourseCode",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=SLATE_HEADER,
        alignment=0,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        name="CoverMainTitle",
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=NAVY_PRIMARY,
        alignment=0,
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name="CoverSubtitle",
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=BLUE_ACCENT,
        alignment=0,
        spaceAfter=12,
    ))

    styles.add(ParagraphStyle(
        name="SectionHeader",
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=15.5,
        textColor=NAVY_PRIMARY,
        spaceBefore=6,
        spaceAfter=5,
        keepWithNext=True,
    ))

    styles.add(ParagraphStyle(
        name="SubSectionHeader",
        fontName="Helvetica-Bold",
        fontSize=9.2,
        leading=12.0,
        textColor=BLUE_DARK,
        spaceBefore=5,
        spaceAfter=3.0,
        keepWithNext=True,
    ))

    styles.add(ParagraphStyle(
        name="BodyTextCustom",
        fontName="Helvetica",
        fontSize=8.1,
        leading=11.2,
        textColor=TEXT_MAIN,
        spaceAfter=4.5,
    ))

    styles.add(ParagraphStyle(
        name="MathBoxText",
        fontName="Helvetica",
        fontSize=7.8,
        leading=10.8,
        textColor=NAVY_PRIMARY,
        spaceAfter=2,
    ))

    styles.add(ParagraphStyle(
        name="TableHead",
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=WHITE,
        alignment=1,
    ))

    styles.add(ParagraphStyle(
        name="TableHeadLeft",
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=WHITE,
        alignment=0,
    ))

    styles.add(ParagraphStyle(
        name="TableCell",
        fontName="Helvetica",
        fontSize=7.3,
        leading=9.2,
        textColor=NAVY_PRIMARY,
        alignment=1,
    ))

    styles.add(ParagraphStyle(
        name="TableCellLeft",
        fontName="Helvetica",
        fontSize=7.3,
        leading=9.2,
        textColor=NAVY_PRIMARY,
        alignment=0,
    ))

    styles.add(ParagraphStyle(
        name="TableCellBold",
        fontName="Helvetica-Bold",
        fontSize=7.3,
        leading=9.2,
        textColor=NAVY_PRIMARY,
        alignment=1,
    ))

    styles.add(ParagraphStyle(
        name="FigCaption",
        fontName="Helvetica-Oblique",
        fontSize=7.3,
        leading=9.5,
        textColor=TEXT_MUTED,
        alignment=1,
        spaceAfter=3,
    ))

    styles.add(ParagraphStyle(
        name="MetaLabel",
        fontName="Helvetica-Bold",
        fontSize=7.8,
        leading=10.2,
        textColor=NAVY_PRIMARY,
    ))

    styles.add(ParagraphStyle(
        name="MetaValue",
        fontName="Helvetica",
        fontSize=7.8,
        leading=10.2,
        textColor=TEXT_MAIN,
    ))

    styles.add(ParagraphStyle(
        name="CalloutText",
        fontName="Helvetica",
        fontSize=7.9,
        leading=11.0,
        textColor=SLATE_HEADER,
    ))

    return styles


# ==============================================================================
# PAGE 1: COVER PAGE
# ==============================================================================
def build_cover_page(styles):
    story = []

    # Institution Header Banner
    story.append(Paragraph("VELLORE INSTITUTE OF TECHNOLOGY (VIT), VELLORE", styles["CoverInst"]))
    story.append(Paragraph("School of Advanced Sciences  •  Department of Mathematics  •  Winter Semester 2026", styles["CoverSubInst"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=BLUE_ACCENT, spaceBefore=0, spaceAfter=12))

    # Course & Project Title Block
    story.append(Paragraph("BAMAT207 — PROBABILITY AND STATISTICS", styles["CoverCourseCode"]))
    story.append(Paragraph("HamSpam: Probabilistic SMS Spam Detection", styles["CoverMainTitle"]))
    story.append(Paragraph("Discrete Probability Modeling, Bayes' Theorem Verification, and Multinomial Naive Bayes Classification", styles["CoverSubtitle"]))

    story.append(Spacer(1, 8))

    # Executive Abstract Callout Card
    abstract_text = (
        "<b>Executive Project Abstract:</b> This academic report presents an end-to-end mathematical and empirical "
        "investigation of probabilistic text classification applied to the official UCI SMS Spam Collection benchmark (Dataset ID #228). "
        "We formalize SMS classification using discrete random variable theory, Bernoulli distributions, and Bayes' Theorem. "
        "Following strict preprocessing and deduplication (reducing 5,574 raw records to 5,171 distinct messages), we empirically verify "
        "Bayes' Law across targeted spam keywords (<i>free</i>, <i>prize</i>, <i>win</i>, <i>urgent</i>, <i>offer</i>), demonstrating identity "
        "between direct frequency ratios and inverted Bayesian posterior calculations to within machine epsilon (&le; 2.22 &times; 10<sup>-16</sup>). "
        "A Multinomial Naive Bayes classifier with Laplace smoothing (&alpha; = 1.0) was trained on an 80:20 stratified split, achieving "
        "<b>98.07% Accuracy</b>, <b>95.12% Precision</b>, <b>89.31% Recall</b>, and an <b>F1-Score of 92.13%</b> on 1,035 held-out test messages. "
        "The complete system is deployed as a production-grade full-stack web application with FastAPI, React 18, and interactive telemetry."
    )
    abstract_table = Table(
        [[Paragraph(abstract_text, styles["CalloutText"])]],
        colWidths=[523]
    )
    abstract_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BLUE_LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 1.0, BLUE_ACCENT),
        ('LINELEFT', (0, 0), (0, 0), 3.5, BLUE_DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 11),
        ('RIGHTPADDING', (0, 0), (-1, -1), 11),
    ]))
    story.append(abstract_table)

    story.append(Spacer(1, 10))

    # Core Performance Highlights (4 KPI Badges)
    kpi_data = [
        [
            Paragraph("<b>Overall Accuracy</b><br/><font size='13' color='#0F172A'><b>98.07%</b></font><br/><font size='6.8' color='#64748B'>1,015 / 1,035 test correct</font>", styles["TableCell"]),
            Paragraph("<b>Spam Precision</b><br/><font size='13' color='#059669'><b>95.12%</b></font><br/><font size='6.8' color='#64748B'>Ultra-low FP (6 messages)</font>", styles["TableCell"]),
            Paragraph("<b>Spam Recall</b><br/><font size='13' color='#2563EB'><b>89.31%</b></font><br/><font size='6.8' color='#64748B'>117 / 131 spam detected</font>", styles["TableCell"]),
            Paragraph("<b>Spam F1-Score</b><br/><font size='13' color='#7C3AED'><b>92.13%</b></font><br/><font size='6.8' color='#64748B'>Harmonic mean purity</font>", styles["TableCell"]),
        ]
    ]
    kpi_table = Table(kpi_data, colWidths=[130.7, 130.7, 130.7, 130.7])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 6.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6.5),
    ]))
    story.append(kpi_table)

    story.append(Spacer(1, 12))

    # Metadata & Student Credentials Table
    meta_info = [
        [
            Paragraph("<b>Course Code & Title:</b>", styles["MetaLabel"]),
            Paragraph("BAMAT207 — Probability and Statistics", styles["MetaValue"]),
            Paragraph("<b>Official Benchmark:</b>", styles["MetaLabel"]),
            Paragraph("UCI SMS Spam Collection (ID: 228)", styles["MetaValue"])
        ],
        [
            Paragraph("<b>Candidate Name:</b>", styles["MetaLabel"]),
            Paragraph("Sarvesh S [Student Candidate]", styles["MetaValue"]),
            Paragraph("<b>Live Cloud URL:</b>", styles["MetaLabel"]),
            Paragraph("<font color='#2563EB'><u>https://hamspam.vercel.app</u></font>", styles["MetaValue"])
        ],
        [
            Paragraph("<b>Registration Number:</b>", styles["MetaLabel"]),
            Paragraph("23BCE0000 [Editable Student ID]", styles["MetaValue"]),
            Paragraph("<b>GitHub Repository:</b>", styles["MetaLabel"]),
            Paragraph("<font color='#2563EB'><u>github.com/SarveshS1407/HamSpam</u></font>", styles["MetaValue"])
        ],
        [
            Paragraph("<b>Program & Department:</b>", styles["MetaLabel"]),
            Paragraph("B.Tech Computer Science / SAS & SCOPE", styles["MetaValue"]),
            Paragraph("<b>Automated Test Suite:</b>", styles["MetaLabel"]),
            Paragraph("<font color='#059669'><b>17 / 17 Tests Passing (100%)</b></font>", styles["MetaValue"])
        ],
        [
            Paragraph("<b>Faculty Supervisor:</b>", styles["MetaLabel"]),
            Paragraph("[Faculty Guide / Course Instructor]", styles["MetaValue"]),
            Paragraph("<b>Submission Date:</b>", styles["MetaLabel"]),
            Paragraph("27 October 2026", styles["MetaValue"])
        ],
    ]
    meta_table = Table(meta_info, colWidths=[105, 156, 110, 152])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), WHITE),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 10))

    # Project Verification Signet Box
    verif_text = (
        "<b>Reproducibility & Verification Guarantee:</b> All statistical values, empirical proportions, "
        "confusion matrices, and evaluation scores presented in this report were generated directly by executing "
        "the automated project pipeline (<code>src/probability_analysis.py</code>, <code>src/train_model.py</code>) "
        "on the verified UCI SMS dataset. Zero synthetic data or speculative figures have been used."
    )
    verif_table = Table([[Paragraph(verif_text, styles["CalloutText"])]], colWidths=[523])
    verif_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_ALT_ROW),
        ('BOX', (0, 0), (-1, -1), 0.6, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 5.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
    ]))
    story.append(verif_table)

    story.append(PageBreak())
    return story


# ==============================================================================
# PAGE 2: EXECUTIVE SUMMARY & PROBLEM FORMULATION
# ==============================================================================
def build_page_2(styles):
    story = []
    story.append(Paragraph("1. Executive Summary & Problem Formulation", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=BORDER_COLOR, spaceBefore=0, spaceAfter=7))

    story.append(Paragraph("1.1 Executive Overview & Problem Statement", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "Short Message Service (SMS) remains one of the world's most ubiquitous and high-engagement direct communication channels, "
        "transmitting critical notifications including multi-factor authentication codes, financial transaction alerts, and personal correspondence. "
        "However, its open protocol and near-universal open rates have made it a lucrative target for unsolicited commercial messaging, "
        "deceptive phishing campaigns ('smishing'), and financial fraud. Unlike email systems that benefit from rich headers, DNS routing signatures, "
        "and extensive message length, SMS messages are restricted to 160 characters, frequently employ phonetic abbreviations, and lack structural metadata. "
        "Consequently, SMS spam filtering demands robust, mathematically principled probabilistic models capable of high-throughput real-time classification.",
        styles["BodyTextCustom"]
    ))

    story.append(Paragraph("1.2 Mathematical Scope & BAMAT207 Alignment", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "This project directly fulfills the theoretical and practical requirements of the BAMAT207 Probability and Statistics curriculum "
        "at Vellore Institute of Technology. Rather than treating machine learning as an opaque heuristic, we structure the entire spam detection task "
        "upon foundational probabilistic frameworks:",
        styles["BodyTextCustom"]
    ))

    framework_items = [
        ("• Discrete Random Variables & Bernoulli Distribution: ", "Modeling the binary spam state Y in {0, 1} with Bernoulli parameter p = P(Y = 1), deriving its expectation E(Y) and variance Var(Y)."),
        ("• Joint & Conditional Probabilities: ", "Estimating token occurrence likelihoods P(W | Spam) and P(W | Ham) from empirical frequency tables."),
        ("• Law of Total Probability: ", "Expanding marginal evidence P(W) = P(W | Spam)P(Spam) + P(W | Ham)P(Ham) across mutually exclusive partitions."),
        ("• Bayes' Theorem Verification: ", "Formally validating direct sample space conditional probabilities P(Spam | W) against inverted Bayesian ratio calculations to confirm numerical consistency."),
        ("• Multinomial Likelihood & Additive Smoothing: ", "Generalizing from single-word indicators to high-dimensional token vectors using Laplace smoothing (alpha = 1.0) and log-space transformations to prevent underflow."),
    ]
    for title, desc in framework_items:
        story.append(Paragraph(f"<b>{title}</b>{desc}", styles["BodyTextCustom"]))

    story.append(Paragraph("1.3 Project Objectives & Engineering Deliverables", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "The project is structured around four concrete objectives designed to bridge theoretical probability and production software engineering:",
        styles["BodyTextCustom"]
    ))

    obj_data = [
        [
            Paragraph("<b>Objective 1: Dataset Acquisition & Hygiene</b>", styles["TableCellBold"]),
            Paragraph("Automate ingestion of UCI SMS Spam Collection (#228), audit schema, eliminate duplicates, and encode binary ground truth.", styles["TableCellLeft"])
        ],
        [
            Paragraph("<b>Objective 2: Empirical Probability Validation</b>", styles["TableCellBold"]),
            Paragraph("Compute exact sample prior distributions, Bernoulli moments, and verify Bayes' Theorem equivalence across key discriminatory tokens.", styles["TableCellLeft"])
        ],
        [
            Paragraph("<b>Objective 3: Supervised Model Training</b>", styles["TableCellBold"]),
            Paragraph("Implement a Multinomial Naive Bayes classifier with strict data-leakage boundaries, stratified 80:20 partitioning, and evaluate confusion matrix trade-offs.", styles["TableCellLeft"])
        ],
        [
            Paragraph("<b>Objective 4: Production Deployment & Verification</b>", styles["TableCellBold"]),
            Paragraph("Expose trained model parameters via FastAPI REST service, deploy interactive React dashboard on Vercel, and achieve 100% test coverage.", styles["TableCellLeft"])
        ]
    ]
    obj_table = Table(obj_data, colWidths=[150, 373])
    obj_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(obj_table)

    story.append(Spacer(1, 6))
    story.append(Paragraph("1.4 Engineering & Academic Environment", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "All analytical models and data pipelines were developed in Python 3.13 on Apple Silicon (M1 architecture) utilizing an isolated virtual "
        "environment. Core dependencies were constrained strictly to standard scientific libraries (NumPy, Pandas, Scikit-Learn, Matplotlib, "
        "ReportLab, FastAPI, and PyMuPDF) to guarantee reproducibility without extraneous overhead.",
        styles["BodyTextCustom"]
    ))

    story.append(PageBreak())
    return story


# ==============================================================================
# PAGE 3: DATASET ACQUISITION & PREPROCESSING
# ==============================================================================
def build_page_3(styles):
    story = []
    story.append(Paragraph("2. Dataset Acquisition, Hygiene & Distribution", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=BORDER_COLOR, spaceBefore=0, spaceAfter=7))

    story.append(Paragraph("2.1 The UCI SMS Spam Collection Benchmark", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "The experimental foundation of this study is the official <b>SMS Spam Collection Dataset</b> hosted by the University of California, "
        "Irvine (UCI) Machine Learning Repository (Dataset ID: <b>228</b>; DOI: 10.24432/C5CC84). Compiled by Tiago A. Almeida and Jos&eacute; Mar&iacute;a "
        "G&oacute;mez Hidalgo, this benchmark represents a realistic corpus gathered from diverse sources including the Grumbletext UK consumer feedback "
        "forum, the Caroline Tag PhD mobile thesis, and the NUS SMS Corpus. Messages span authentic mobile syntax, regional colloquialisms, and diverse scam typologies.",
        styles["BodyTextCustom"]
    ))

    story.append(Paragraph("2.2 Data Cleaning & Deduplication Protocol", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "Automated ingestion was implemented via the <code>ucimlrepo</code> Python interface, backed by an offline filesystem cache to withstand network latency. "
        "Raw inspection revealed an initial shape of <b>5,574 messages</b> across two attributes: message label (categorical) and message text (string). "
        "A rigorous audit confirmed zero missing values. However, identical broadcast SMS campaigns generated repeated observations in the raw feed. "
        "A deduplication pass identified and purged exactly <b>403 duplicate records</b>, yielding a cleaned corpus of <b>5,171 distinct records</b>. "
        "Target labels were normalized to a binary integer representation: Ham &rarr; 0, Spam &rarr; 1.",
        styles["BodyTextCustom"]
    ))

    # Dataset Summary Table
    ds_data = [
        [Paragraph("Data Metric / Attribute", styles["TableHeadLeft"]), Paragraph("Raw Dataset", styles["TableHead"]), Paragraph("Cleaned Dataset", styles["TableHead"]), Paragraph("Relative Share / Impact", styles["TableHead"])],
        [Paragraph("Total Message Records", styles["TableCellLeft"]), Paragraph("5,574", styles["TableCell"]), Paragraph("5,171", styles["TableCellBold"]), Paragraph("403 duplicate entries pruned (-7.23%)", styles["TableCell"])],
        [Paragraph("Legitimate Messages (Ham, Y=0)", styles["TableCellLeft"]), Paragraph("4,827", styles["TableCell"]), Paragraph("4,518", styles["TableCellBold"]), Paragraph("87.3719% of cleaned corpus", styles["TableCell"])],
        [Paragraph("Spam Messages (Spam, Y=1)", styles["TableCellLeft"]), Paragraph("747", styles["TableCell"]), Paragraph("653", styles["TableCellBold"]), Paragraph("12.6281% of cleaned corpus", styles["TableCell"])],
        [Paragraph("Missing / Null Values", styles["TableCellLeft"]), Paragraph("0 (0.00%)", styles["TableCell"]), Paragraph("0 (0.00%)", styles["TableCellBold"]), Paragraph("Verified complete data integrity", styles["TableCell"])],
        [Paragraph("Class Imbalance Ratio (Ham : Spam)", styles["TableCellLeft"]), Paragraph("6.46 : 1", styles["TableCell"]), Paragraph("6.92 : 1", styles["TableCellBold"]), Paragraph("Pronounced class asymmetry", styles["TableCell"])],
    ]
    ds_table = Table(ds_data, colWidths=[165, 80, 85, 193])
    ds_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BG_ALT_ROW]),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(ds_table)

    story.append(Spacer(1, 6))
    story.append(Paragraph("2.3 Empirical Class Distribution", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "Figure 1 illustrates the class distribution across both absolute counts and relative percentages. The cleaned dataset comprises "
        "<b>4,518 Ham messages (87.37%)</b> and <b>653 Spam messages (12.63%)</b>. This pronounced 7:1 class asymmetry dictates that naive accuracy "
        "is an inadequate evaluation metric, necessitating precision, recall, and confusion matrix decomposition.",
        styles["BodyTextCustom"]
    ))

    # Embed class_distribution.png
    img_path = "outputs/class_distribution.png"
    if os.path.exists(img_path):
        story.append(Image(img_path, width=390, height=190))
        story.append(Paragraph("<b>Figure 1:</b> Cleaned SMS class distribution (UCI Dataset ID #228) illustrating total counts and percentage shares.", styles["FigCaption"]))

    story.append(PageBreak())
    return story


# ==============================================================================
# PAGE 4: MATHEMATICAL & STATISTICAL FOUNDATIONS
# ==============================================================================
def build_page_4(styles):
    story = []
    story.append(Paragraph("3. Theoretical Probability & Bernoulli Modeling", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=BORDER_COLOR, spaceBefore=0, spaceAfter=7))

    story.append(Paragraph("3.1 Random Variable Formulation", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "Let the outcome of an arbitrary incoming SMS message be governed by a discrete binary random variable <b>Y &isin; {0, 1}</b>, "
        "where Y = 1 denotes that the message is Spam, and Y = 0 denotes that the message is Ham (legitimate). "
        "Under the frequentist paradigm, the parameter <b>p</b> represents the prior probability of observing a spam message across the sample space &Omega;:",
        styles["BodyTextCustom"]
    ))

    # Bernoulli Math Derivation Callout Box
    math_box_1 = (
        "<b>Bernoulli Probability Mass Function (PMF):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;P(Y = y) = p<sup>y</sup> (1 - p)<sup>1 - y</sup>, &nbsp;&nbsp;&nbsp;&nbsp; for y &isin; {0, 1}<br/>"
        "From our cleaned benchmark of N = 5,171 messages (653 Spam, 4,518 Ham):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>P(Spam) = p = 653 / 5171 = 0.126281</b> (12.6281%)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>P(Ham) = q = 1 - p = 4518 / 5171 = 0.873719</b> (87.3719%)<br/><br/>"
        "<b>Derivation of Expectation E(Y):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;E(Y) = &sum;<sub>y &isin; {0,1}</sub> y &middot; P(Y = y) = [0 &middot; (1 - p)] + [1 &middot; p] = <b>p = 0.126281</b><br/><br/>"
        "<b>Derivation of Variance Var(Y) and Standard Deviation &sigma;(Y):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;E(Y<sup>2</sup>) = &sum;<sub>y &isin; {0,1}</sub> y<sup>2</sup> &middot; P(Y = y) = [0<sup>2</sup> &middot; (1 - p)] + [1<sup>2</sup> &middot; p] = p<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Var(Y) = E(Y<sup>2</sup>) - [E(Y)]<sup>2</sup> = p - p<sup>2</sup> = p(1 - p)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Var(Y) = (0.126281) &middot; (0.873719) = <b>0.110334</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&sigma;(Y) = &radic;Var(Y) = &radic;0.110334 = <b>0.332166</b>"
    )
    b_table = Table([[Paragraph(math_box_1, styles["MathBoxText"])]], colWidths=[523])
    b_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
        ('LINELEFT', (0, 0), (0, 0), 3.0, BLUE_ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 6.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(b_table)

    story.append(Spacer(1, 6))
    story.append(Paragraph("3.2 Bayes' Theorem for Message Classification", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "Let <b>x</b> denote an observed feature vector or word event extracted from an SMS message. By the definition of conditional probability, "
        "the joint probability of co-occurrence satisfies P(x &cap; Spam) = P(x | Spam)P(Spam) = P(Spam | x)P(x). "
        "Solving for the posterior probability P(Spam | x) yields Bayes' Theorem:",
        styles["BodyTextCustom"]
    ))

    math_box_2 = (
        "<b>Formal Statement of Bayes' Theorem:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;P(Spam | x) = [ P(x | Spam) &middot; P(Spam) ] / P(x)<br/><br/>"
        "Applying the <b>Law of Total Probability</b> over the complete partition of the sample space &Omega; = {Spam, Ham}:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;P(x) = P(x | Spam) &middot; P(Spam) + P(x | Ham) &middot; P(Ham)<br/><br/>"
        "Substituting the marginal probability expression into the denominator gives:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>P(Spam | x) = [ P(x | Spam) &middot; P(Spam) ] / [ P(x | Spam) &middot; P(Spam) + P(x | Ham) &middot; P(Ham) ]</b><br/><br/>"
        "<b>Classification Decision Rule:</b><br/>"
        "An incoming message is classified as Spam if P(Spam | x) &gt; P(Ham | x), which under symmetric 0-1 loss simplifies to "
        "assigning label 1 whenever P(Spam | x) &gt; 0.50 (or an operational threshold &tau; calibrated for false-positive avoidance)."
    )
    bayes_table = Table([[Paragraph(math_box_2, styles["MathBoxText"])]], colWidths=[523])
    bayes_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BLUE_LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.8, BLUE_ACCENT),
        ('LINELEFT', (0, 0), (0, 0), 3.0, BLUE_DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 6.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(bayes_table)

    story.append(Spacer(1, 6))
    story.append(Paragraph("3.3 Theoretical Parameter Summary Table", styles["SubSectionHeader"]))

    param_data = [
        [Paragraph("Parameter / Metric", styles["TableHeadLeft"]), Paragraph("Mathematical Notation", styles["TableHead"]), Paragraph("Calculated Exact Value", styles["TableHead"]), Paragraph("Statistical Interpretation", styles["TableHeadLeft"])],
        [Paragraph("Prior Spam Probability", styles["TableCellLeft"]), Paragraph("P(Y = 1) = p", styles["TableCellBold"]), Paragraph("0.126281", styles["TableCell"]), Paragraph("Unconditional base rate of spam in SMS traffic", styles["TableCellLeft"])],
        [Paragraph("Prior Ham Probability", styles["TableCellLeft"]), Paragraph("P(Y = 0) = 1 - p", styles["TableCellBold"]), Paragraph("0.873719", styles["TableCell"]), Paragraph("Unconditional base rate of genuine communication", styles["TableCellLeft"])],
        [Paragraph("Expected Value", styles["TableCellLeft"]), Paragraph("E(Y) = &mu;<sub>Y</sub>", styles["TableCellBold"]), Paragraph("0.126281", styles["TableCell"]), Paragraph("Mean of Bernoulli indicator variable", styles["TableCellLeft"])],
        [Paragraph("Bernoulli Variance", styles["TableCellLeft"]), Paragraph("Var(Y) = &sigma;<sup>2</sup><sub>Y</sub>", styles["TableCellBold"]), Paragraph("0.110334", styles["TableCell"]), Paragraph("Variability of binary class assignment", styles["TableCellLeft"])],
        [Paragraph("Standard Deviation", styles["TableCellLeft"]), Paragraph("&sigma;(Y)", styles["TableCellBold"]), Paragraph("0.332166", styles["TableCell"]), Paragraph("Spread of class probability distribution", styles["TableCellLeft"])],
    ]
    param_table = Table(param_data, colWidths=[130, 110, 95, 188])
    param_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BG_ALT_ROW]),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(param_table)

    story.append(PageBreak())
    return story


# ==============================================================================
# PAGE 5: WORD-LEVEL PROBABILITY & BAYES PROOF
# ==============================================================================
def build_page_5(styles):
    story = []
    story.append(Paragraph("4. Word-Level Probability Analysis & Bayes Verification", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=BORDER_COLOR, spaceBefore=0, spaceAfter=7))

    story.append(Paragraph("4.1 Keyword Selection & Boundary Tokenization", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "To evaluate conditional probabilities empirically, we selected five quintessential spam trigger keywords: "
        "<b>free</b>, <b>prize</b>, <b>win</b>, <b>urgent</b>, and <b>offer</b>. "
        "Occurrences were tallied across the 5,171 cleaned messages using strict regular expression word boundaries (<code>\\bword\\b</code>) "
        "to prevent partial substring contamination (e.g., distinguishing 'win' from 'window' or 'winter').",
        styles["BodyTextCustom"]
    ))

    # Comprehensive Word Table
    word_data = [
        [
            Paragraph("Word (W)", styles["TableHeadLeft"]),
            Paragraph("Spam (S)", styles["TableHead"]),
            Paragraph("Ham (H)", styles["TableHead"]),
            Paragraph("Total", styles["TableHead"]),
            Paragraph("P(W|Spam)", styles["TableHead"]),
            Paragraph("P(W|Ham)", styles["TableHead"]),
            Paragraph("P(W)", styles["TableHead"]),
            Paragraph("P(Spam|W) Dir", styles["TableHead"]),
            Paragraph("P(Spam|W) Bayes", styles["TableHead"]),
            Paragraph("Difference", styles["TableHead"]),
        ],
        [
            Paragraph("<b>free</b>", styles["TableCellLeft"]),
            Paragraph("148", styles["TableCell"]),
            Paragraph("55", styles["TableCell"]),
            Paragraph("203", styles["TableCellBold"]),
            Paragraph("0.226646", styles["TableCell"]),
            Paragraph("0.012174", styles["TableCell"]),
            Paragraph("0.039257", styles["TableCell"]),
            Paragraph("<b>0.729064</b>", styles["TableCellBold"]),
            Paragraph("<b>0.729064</b>", styles["TableCellBold"]),
            Paragraph("1.11 &times; 10<sup>-16</sup>", styles["TableCell"]),
        ],
        [
            Paragraph("<b>prize</b>", styles["TableCellLeft"]),
            Paragraph("73", styles["TableCell"]),
            Paragraph("0", styles["TableCell"]),
            Paragraph("73", styles["TableCellBold"]),
            Paragraph("0.111792", styles["TableCell"]),
            Paragraph("0.000000", styles["TableCell"]),
            Paragraph("0.014117", styles["TableCell"]),
            Paragraph("<b>1.000000</b>", styles["TableCellBold"]),
            Paragraph("<b>1.000000</b>", styles["TableCellBold"]),
            Paragraph("2.22 &times; 10<sup>-16</sup>", styles["TableCell"]),
        ],
        [
            Paragraph("<b>win</b>", styles["TableCellLeft"]),
            Paragraph("49", styles["TableCell"]),
            Paragraph("6", styles["TableCell"]),
            Paragraph("55", styles["TableCellBold"]),
            Paragraph("0.075038", styles["TableCell"]),
            Paragraph("0.001328", styles["TableCell"]),
            Paragraph("0.010636", styles["TableCell"]),
            Paragraph("<b>0.890909</b>", styles["TableCellBold"]),
            Paragraph("<b>0.890909</b>", styles["TableCellBold"]),
            Paragraph("1.11 &times; 10<sup>-16</sup>", styles["TableCell"]),
        ],
        [
            Paragraph("<b>urgent</b>", styles["TableCellLeft"]),
            Paragraph("57", styles["TableCell"]),
            Paragraph("5", styles["TableCell"]),
            Paragraph("62", styles["TableCellBold"]),
            Paragraph("0.087289", styles["TableCell"]),
            Paragraph("0.001107", styles["TableCell"]),
            Paragraph("0.011990", styles["TableCell"]),
            Paragraph("<b>0.919355</b>", styles["TableCellBold"]),
            Paragraph("<b>0.919355</b>", styles["TableCellBold"]),
            Paragraph("2.22 &times; 10<sup>-16</sup>", styles["TableCell"]),
        ],
        [
            Paragraph("<b>offer</b>", styles["TableCellLeft"]),
            Paragraph("24", styles["TableCell"]),
            Paragraph("6", styles["TableCell"]),
            Paragraph("30", styles["TableCellBold"]),
            Paragraph("0.036753", styles["TableCell"]),
            Paragraph("0.001328", styles["TableCell"]),
            Paragraph("0.005802", styles["TableCell"]),
            Paragraph("<b>0.800000</b>", styles["TableCellBold"]),
            Paragraph("<b>0.800000</b>", styles["TableCellBold"]),
            Paragraph("1.11 &times; 10<sup>-16</sup>", styles["TableCell"]),
        ],
    ]
    word_table = Table(word_data, colWidths=[48, 38, 38, 42, 57, 57, 54, 63, 66, 60])
    word_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BG_ALT_ROW]),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(word_table)

    story.append(Spacer(1, 6))
    story.append(Paragraph("4.2 Exact Bayes' Theorem Equivalence Proof", styles["SubSectionHeader"]))

    proof_box = (
        "<b>Rigorous Step-by-Step Proof of Equivalence (Illustrated on Keyword 'free'):</b><br/>"
        "1. <b>Direct Frequency Ratio Method:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;P(Spam | 'free')<sub>direct</sub> = N(Spam &cap; 'free') / N('free') = 148 / 203 = <b>0.729064039408867</b><br/>"
        "2. <b>Bayes' Inversion Formula:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;P(Spam | 'free')<sub>Bayes</sub> = [ P('free' | Spam) &middot; P(Spam) ] / P('free')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Where:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; P('free' | Spam) = 148 / 653 = 0.22664624808575803<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; P(Spam) = 653 / 5171 = 0.12628118352349643<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; P('free') = 203 / 5171 = 0.03925739702185264<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Substituting:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;P(Spam | 'free')<sub>Bayes</sub> = [ (148/653) &middot; (653/5171) ] / (203/5171) = 148 / 203 = <b>0.7290640394088671</b><br/>"
        "3. <b>Numerical Error Analysis:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;| P(Spam | 'free')<sub>direct</sub> - P(Spam | 'free')<sub>Bayes</sub> | = <b>1.1102 &times; 10<sup>-16</sup> &equiv; 0</b> (IEEE-754 Epsilon).<br/>"
        "This empirical proof confirms that Bayes' Theorem exactly reproduces sample space proportions across all five keywords."
    )
    proof_table = Table([[Paragraph(proof_box, styles["MathBoxText"])]], colWidths=[523])
    proof_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
        ('LINELEFT', (0, 0), (0, 0), 3.0, GREEN_SUCCESS),
        ('TOPPADDING', (0, 0), (-1, -1), 5.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
    ]))
    story.append(proof_table)

    story.append(Spacer(1, 5))

    # Embed word_probability_chart.png
    chart_path = "outputs/word_probability_chart.png"
    if os.path.exists(chart_path):
        story.append(Image(chart_path, width=410, height=180))
        story.append(Paragraph("<b>Figure 2:</b> Empirical conditional probabilities P(W|Spam), P(W|Ham), and posterior P(Spam|W) across key tokens.", styles["FigCaption"]))

    story.append(PageBreak())
    return story


# ==============================================================================
# PAGE 6: MACHINE LEARNING METHODOLOGY
# ==============================================================================
def build_page_6(styles):
    story = []
    story.append(Paragraph("5. Machine Learning Methodology: Multinomial Naive Bayes", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=BORDER_COLOR, spaceBefore=0, spaceAfter=7))

    story.append(Paragraph("5.1 Stratified Train-Test Splitting & Leakage Prevention", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "To rigorously benchmark generalization performance, the 5,171 cleaned messages were partitioned into an <b>80% Training set</b> "
        "(N<sub>train</sub> = 4,136) and a <b>20% Testing set</b> (N<sub>test</sub> = 1,035). Stratification was enforced on label Y to preserve "
        "the exact 87.34% Ham / 12.66% Spam proportion across both partitions (Random State = 42). "
        "Crucially, to prevent data leakage, the feature extraction vocabulary and document frequencies were fitted <i>strictly on the training partition</i>. "
        "The test split was held out completely until final inference evaluation.",
        styles["BodyTextCustom"]
    ))

    story.append(Paragraph("5.2 Vectorization & Multinomial Likelihood Formulation", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "Text messages are mapped into token frequency vectors <b>x</b> = (x<sub>1</sub>, x<sub>2</sub>, ..., x<sub>|V|</sub>) via <code>CountVectorizer</code>. "
        "The Multinomial Naive Bayes model treats each message as a multinomial distribution over the vocabulary V, invoking the conditional "
        "independence assumption that the probability of observing token w<sub>i</sub> is conditionally independent of all other tokens given class c &isin; {Ham, Spam}:",
        styles["BodyTextCustom"]
    ))

    ml_box = (
        "<b>Multinomial Likelihood:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;P(<b>x</b> | c) = [ (&sum; x<sub>i</sub>)! / &prod; (x<sub>i</sub>!) ] &middot; &prod;<sub>i=1</sub><sup>|V|</sup> P(w<sub>i</sub> | c)<sup>x<sub>i</sub></sup><br/><br/>"
        "<b>Laplace (Additive) Smoothing (&alpha; = 1.0):</b><br/>"
        "If a word w<sub>i</sub> in the test set never appeared in training class c, raw empirical maximum-likelihood estimation yields P(w<sub>i</sub> | c) = 0, "
        "which would fatally zero out the entire product (the 'zero-frequency problem'). We apply Laplace smoothing with &alpha; = 1.0:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>&theta;<sub>ci</sub> = [ N<sub>ci</sub> + &alpha; ] / [ N<sub>c</sub> + &alpha; &middot; |V| ]</b><br/>"
        "where N<sub>ci</sub> is the count of word i in class c, N<sub>c</sub> is the total token count in class c, and |V| is the vocabulary size.<br/><br/>"
        "<b>Log-Space Posterior Inference (Underflow Prevention):</b><br/>"
        "Multiplying hundreds of small probabilities (P &lt; 10<sup>-3</sup>) leads directly to floating-point underflow in computer arithmetic. "
        "We transform the posterior into monotonic log-space:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>log P(c | <b>x</b>) = log P(c) + &sum;<sub>i=1</sub><sup>|V|</sup> x<sub>i</sub> &middot; log &theta;<sub>ci</sub></b><br/>"
        "Normalized posterior probabilities are subsequently recovered via numerically stabilized softmax operations."
    )
    ml_table = Table([[Paragraph(ml_box, styles["MathBoxText"])]], colWidths=[523])
    ml_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
        ('LINELEFT', (0, 0), (0, 0), 3.0, BLUE_DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 6.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(ml_table)

    story.append(Spacer(1, 6))
    story.append(Paragraph("5.3 End-to-End Classification Pipeline Architecture", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "Figure 3 diagrams the operational inference pipeline executing inside both the batch evaluation suite and the live production API.",
        styles["BodyTextCustom"]
    ))

    # Architectural Pipeline Flow Table
    pipe_stages = [
        [
            Paragraph("<b>Stage 1: Raw Ingestion</b><br/><font size='7.2' color='#64748B'>Raw SMS String (UTF-8)</font>", styles["TableCellBold"]),
            Paragraph("<b>Stage 2: Tokenization</b><br/><font size='7.2' color='#64748B'>Lowercasing & \\b\\w+\\b parsing</font>", styles["TableCellBold"]),
            Paragraph("<b>Stage 3: Vectorization</b><br/><font size='7.2' color='#64748B'>CountVectorizer (|V|=7,297)</font>", styles["TableCellBold"]),
            Paragraph("<b>Stage 4: Naive Bayes</b><br/><font size='7.2' color='#64748B'>Multinomial log-priors + log-odds</font>", styles["TableCellBold"]),
            Paragraph("<b>Stage 5: Calibration</b><br/><font size='7.2' color='#64748B'>Softmax &tau; &ge; 0.5 &rarr; Label {0,1}</font>", styles["TableCellBold"]),
        ]
    ]
    pipe_table = Table(pipe_stages, colWidths=[104.6, 104.6, 104.6, 104.6, 104.6])
    pipe_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_ALT_ROW),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(pipe_table)
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Figure 3:</b> Five-stage probabilistic SMS text inference pipeline from raw string to calibrated posterior probability.", styles["FigCaption"]))

    story.append(Spacer(1, 5))
    story.append(Paragraph("5.4 Pipeline Partition Quantities", styles["SubSectionHeader"]))
    part_info = [
        [Paragraph("Partition Name", styles["TableHeadLeft"]), Paragraph("Message Count", styles["TableHead"]), Paragraph("Ham Messages (0)", styles["TableHead"]), Paragraph("Spam Messages (1)", styles["TableHead"]), Paragraph("Stratification Check", styles["TableHead"])],
        [Paragraph("Full Cleaned Dataset", styles["TableCellLeft"]), Paragraph("5,171 (100.0%)", styles["TableCellBold"]), Paragraph("4,518 (87.37%)", styles["TableCell"]), Paragraph("653 (12.63%)", styles["TableCell"]), Paragraph("Base Benchmark", styles["TableCell"])],
        [Paragraph("Training Partition (Fit)", styles["TableCellLeft"]), Paragraph("4,136 (80.00%)", styles["TableCellBold"]), Paragraph("3,614 (87.38%)", styles["TableCell"]), Paragraph("522 (12.62%)", styles["TableCell"]), Paragraph("Verified Identical Ratio", styles["TableCell"])],
        [Paragraph("Held-Out Testing Partition", styles["TableCellLeft"]), Paragraph("1,035 (20.00%)", styles["TableCellBold"]), Paragraph("904 (87.34%)", styles["TableCell"]), Paragraph("131 (12.66%)", styles["TableCell"]), Paragraph("Zero Data Leakage", styles["TableCell"])],
    ]
    part_table = Table(part_info, colWidths=[135, 95, 100, 95, 98])
    part_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BG_ALT_ROW]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(part_table)

    story.append(PageBreak())
    return story


# ==============================================================================
# PAGE 7: EXPERIMENTAL EVALUATION & ERROR ANALYSIS
# ==============================================================================
def build_page_7(styles):
    story = []
    story.append(Paragraph("6. Experimental Results & Performance Evaluation", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=BORDER_COLOR, spaceBefore=0, spaceAfter=7))

    story.append(Paragraph("6.1 Quantitative Test Performance Metrics", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "The trained Multinomial Naive Bayes classifier was evaluated against the <b>1,035 held-out test messages</b>. "
        "Table 4 summarizes the verified quantitative metrics alongside class-specific precision, recall, and harmonic F1-scores.",
        styles["BodyTextCustom"]
    ))

    eval_data = [
        [Paragraph("Evaluation Metric", styles["TableHeadLeft"]), Paragraph("Formula Definition", styles["TableHeadLeft"]), Paragraph("Calculated Score", styles["TableHead"]), Paragraph("Operational Significance", styles["TableHeadLeft"])],
        [Paragraph("<b>Overall Accuracy</b>", styles["TableCellLeft"]), Paragraph("(TP + TN) / Total", styles["TableCellLeft"]), Paragraph("<b>0.9807 (98.07%)</b>", styles["TableCellBold"]), Paragraph("1,015 of 1,035 predictions correct", styles["TableCellLeft"])],
        [Paragraph("<b>Spam Precision</b>", styles["TableCellLeft"]), Paragraph("TP / (TP + FP)", styles["TableCellLeft"]), Paragraph("<b>0.9512 (95.12%)</b>", styles["TableCellBold"]), Paragraph("Low Type I error (only 6 ham misclassified)", styles["TableCellLeft"])],
        [Paragraph("<b>Spam Recall</b>", styles["TableCellLeft"]), Paragraph("TP / (TP + FN)", styles["TableCellLeft"]), Paragraph("<b>0.8931 (89.31%)</b>", styles["TableCellBold"]), Paragraph("Catches 117 of 131 actual spam messages", styles["TableCellLeft"])],
        [Paragraph("<b>Spam F1-Score</b>", styles["TableCellLeft"]), Paragraph("2 &middot; (Prec &middot; Rec) / (Prec + Rec)", styles["TableCellLeft"]), Paragraph("<b>0.9213 (92.13%)</b>", styles["TableCellBold"]), Paragraph("Harmonic balance of purity and sensitivity", styles["TableCellLeft"])],
        [Paragraph("<b>Ham Precision</b>", styles["TableCellLeft"]), Paragraph("TN / (TN + FN)", styles["TableCellLeft"]), Paragraph("0.9846 (98.46%)", styles["TableCell"]), Paragraph("High trust in legitimate inbox arrivals", styles["TableCellLeft"])],
        [Paragraph("<b>Ham Recall</b>", styles["TableCellLeft"]), Paragraph("TN / (TN + FP)", styles["TableCellLeft"]), Paragraph("0.9934 (99.34%)", styles["TableCell"]), Paragraph("99.34% of legitimate SMS delivered safely", styles["TableCellLeft"])],
    ]
    eval_table = Table(eval_data, colWidths=[110, 130, 95, 188])
    eval_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BG_ALT_ROW]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(eval_table)

    story.append(Spacer(1, 5))
    story.append(Paragraph("6.2 Confusion Matrix Decomposition", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "Figure 4 presents the confusion matrix breakdown for the 1,035 test instances across predicted versus ground-truth states:",
        styles["BodyTextCustom"]
    ))

    # Embed confusion_matrix.png
    cm_path = "outputs/confusion_matrix.png"
    if os.path.exists(cm_path):
        story.append(Image(cm_path, width=370, height=185))
        story.append(Paragraph("<b>Figure 4:</b> Confusion matrix showing True Negatives (898), False Positives (6), False Negatives (14), and True Positives (117).", styles["FigCaption"]))

    story.append(Paragraph("6.3 The Class Imbalance Accuracy Paradox", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "A critical conceptual pillar of BAMAT207 is understanding why <b>accuracy alone is a deeply misleading metric</b> under class asymmetry. "
        "In our test partition, legitimate messages (Ham) constitute 87.34% (904 / 1,035) of all traffic. "
        "Consider a trivial 'dummy' classifier that unconditionally predicts Ham for every message:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; <b>Trivial Baseline Accuracy:</b> 904 / 1035 = <b>87.34%</b>.<br/>"
        "Despite achieving over 87% accuracy, such a trivial baseline yields <b>0.00% Recall</b> and catches zero spam messages! "
        "In contrast, our Multinomial Naive Bayes model achieves <b>98.07% accuracy (+10.73% over baseline)</b> and <b>89.31% recall</b>, "
        "confirming genuine statistical learning. Furthermore, in mobile communication, <b>Type I error (False Positive = 6)</b> is far more damaging "
        "than Type II error (False Negative = 14) because falsely blocking an authentic banking OTP or emergency text has severe real-world consequences. "
        "Our high Spam Precision (95.12%) minimizes this risk.",
        styles["BodyTextCustom"]
    ))

    story.append(PageBreak())
    return story


# ==============================================================================
# PAGE 8: FULL-STACK ARCHITECTURE & DEPLOYMENT
# ==============================================================================
def build_page_8(styles):
    story = []
    story.append(Paragraph("7. System Architecture, Deployment & Live Inference", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=BORDER_COLOR, spaceBefore=0, spaceAfter=7))

    story.append(Paragraph("7.1 Production Software Engineering Architecture", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "To transform academic statistical research into a production tool, we implemented a decoupled, modern web architecture. "
        "The backend is powered by <b>FastAPI</b> and <b>Uvicorn</b>, providing asynchronous REST endpoints. "
        "The frontend is authored in <b>React 18</b> with <b>Vite</b>, styled via <b>Tailwind CSS</b>, and incorporates real-time "
        "probabilistic telemetry with <b>Recharts</b>. The frontend is deployed live on <b>Vercel</b> (<code>https://hamspam.vercel.app</code>).",
        styles["BodyTextCustom"]
    ))

    # Architecture Overview Table
    arch_data = [
        [Paragraph("Subsystem Component", styles["TableHeadLeft"]), Paragraph("Technology Stack", styles["TableHeadLeft"]), Paragraph("Responsibilities & Production Configuration", styles["TableHeadLeft"])],
        [Paragraph("<b>Machine Learning Engine</b>", styles["TableCellLeft"]), Paragraph("Python 3.13 / Scikit-Learn", styles["TableCellLeft"]), Paragraph("Model training, vectorizer vocabulary fitting, Laplace smoothing, serialization to portable JSON/Pickle artifacts.", styles["TableCellLeft"])],
        [Paragraph("<b>Inference API Server</b>", styles["TableCellLeft"]), Paragraph("FastAPI / Uvicorn / Pydantic", styles["TableCellLeft"]), Paragraph("REST endpoints (<code>/api/predict</code>, <code>/api/stats</code>, <code>/api/word-analysis</code>, <code>/api/health</code>).", styles["TableCellLeft"])],
        [Paragraph("<b>Interactive Client Dashboard</b>", styles["TableCellLeft"]), Paragraph("React 18 / Tailwind CSS / Vite", styles["TableCellLeft"]), Paragraph("Real-time SMS input analyzer, probability confidence gauge, confusion matrix inspector, responsive on desktop and mobile.", styles["TableCellLeft"])],
        [Paragraph("<b>Public Cloud Deployment</b>", styles["TableCellLeft"]), Paragraph("Vercel Edge Platform", styles["TableCellLeft"]), Paragraph("Globally distributed edge hosting (<code>https://hamspam.vercel.app</code>) with client-side evaluated fallback mode.", styles["TableCellLeft"])],
    ]
    arch_table = Table(arch_data, colWidths=[120, 130, 273])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BG_ALT_ROW]),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(arch_table)

    story.append(Spacer(1, 6))
    story.append(Paragraph("7.2 Real-Time Inference on Canonical Benchmark Messages", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "To verify end-to-end inference calibration, the system was tested against two canonical benchmark SMS messages:",
        styles["BodyTextCustom"]
    ))

    infer_data = [
        [Paragraph("Benchmark Input SMS Message", styles["TableHeadLeft"]), Paragraph("P(Spam)", styles["TableHead"]), Paragraph("P(Ham)", styles["TableHead"]), Paragraph("Prediction", styles["TableHead"]), Paragraph("Confidence", styles["TableHead"])],
        [
            Paragraph("<i>'Congratulations! You have won a free prize. Claim now.'</i>", styles["TableCellLeft"]),
            Paragraph("<b>1.000000</b>", styles["TableCellBold"]),
            Paragraph("0.000000", styles["TableCell"]),
            Paragraph("<font color='#DC2626'><b>SPAM (1)</b></font>", styles["TableCell"]),
            Paragraph("<b>100.00%</b>", styles["TableCellBold"]),
        ],
        [
            Paragraph("<i>'Hey, are we meeting for lunch today?'</i>", styles["TableCellLeft"]),
            Paragraph("0.000000", styles["TableCell"]),
            Paragraph("<b>1.000000</b>", styles["TableCellBold"]),
            Paragraph("<font color='#059669'><b>HAM (0)</b></font>", styles["TableCell"]),
            Paragraph("<b>100.00%</b>", styles["TableCellBold"]),
        ],
    ]
    infer_table = Table(infer_data, colWidths=[243, 70, 70, 75, 65])
    infer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BG_ALT_ROW]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(infer_table)

    story.append(Spacer(1, 6))
    story.append(Paragraph("7.3 Automated Test Suite & Quality Assurance", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "The project enforces continuous testing with <b>17 automated unit and integration tests</b> spanning two test modules:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; <code>tests/test_probability_analysis.py</code> (12 tests): Verifies dataset loading, Bernoulli parameters, "
        "Bayes' formula equivalence, deduplication counts, and CountVectorizer output shape.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; <code>tests/test_api.py</code> (5 tests): Validates REST API contracts, health checks, prediction schemas, "
        "and error responses for empty or malformed payloads.<br/>"
        "All 17 tests execute in <b>0.23 seconds</b> with a 100% pass rate.",
        styles["BodyTextCustom"]
    ))

    # Test Results Callout
    test_box = (
        "<b>Automated Test Suite Summary (Pytest):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>17 passed</b> in 0.23s &bull; Platform: Darwin (Apple M1) &bull; Python: 3.13.2<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;PASSED: <code>test_data_loader_cleaned_count</code> (5,171 rows verified)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;PASSED: <code>test_bayes_direct_equivalence</code> (|Diff| &le; 2.22 &times; 10<sup>-16</sup> across all words)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;PASSED: <code>test_api_predict_canonical_samples</code> (Canonical spam and ham predictions match 100%)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;PASSED: <code>test_confusion_matrix_sum</code> (Sum of TN+FP+FN+TP equals 1,035)"
    )
    test_table = Table([[Paragraph(test_box, styles["MathBoxText"])]], colWidths=[523])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
        ('LINELEFT', (0, 0), (0, 0), 3.0, GREEN_SUCCESS),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
    ]))
    story.append(test_table)

    story.append(PageBreak())
    return story


# ==============================================================================
# PAGE 9: DISCUSSION, LIMITATIONS & FUTURE SCOPE
# ==============================================================================
def build_page_9(styles):
    story = []
    story.append(Paragraph("8. Critical Discussion, Limitations & Future Scope", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=BORDER_COLOR, spaceBefore=0, spaceAfter=7))

    story.append(Paragraph("8.1 The 'Naive' Independence Assumption Paradox", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "The defining theoretical premise of Naive Bayes is the assumption of class-conditional feature independence: "
        "P(w<sub>1</sub>, w<sub>2</sub> | c) = P(w<sub>1</sub> | c) &middot; P(w<sub>2</sub> | c). "
        "In human language, this assumption is patently false. Tokens exhibit strong syntactic and semantic dependencies; for example, "
        "the occurrence of 'credit' dramatically increases the conditional likelihood of 'card', and 'claim' co-occurs frequently with 'prize'. "
        "Why, then, does Multinomial Naive Bayes achieve an impressive 98.07% accuracy?",
        styles["BodyTextCustom"]
    ))
    story.append(Paragraph(
        "The foundational analysis by <b>Domingos and Pazzani (1997)</b> resolves this apparent paradox: Naive Bayes is optimal under 0-1 loss "
        "even when the independence assumption is severely violated, provided that the <i>direction of the odds ratio</i> (the classification boundary) "
        "is preserved. Even if individual posterior probabilities are miscalibrated (pushed toward 0.0 or 1.0 due to redundant correlated evidence), "
        "the argmax decision boundary remains remarkably robust. For binary classification, exact probability calibration is unnecessary as long "
        "as the sign of the log-odds ratio correctly separates classes.",
        styles["BodyTextCustom"]
    ))

    story.append(Paragraph("8.2 Error Analysis: Categorizing Misclassifications", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "A detailed audit of the 20 misclassified instances in the held-out test split reveals distinct linguistic and operational patterns:",
        styles["BodyTextCustom"]
    ))

    error_data = [
        [Paragraph("Error Category", styles["TableHeadLeft"]), Paragraph("Observed Count", styles["TableHead"]), Paragraph("Primary Linguistic & Statistical Root Cause", styles["TableHeadLeft"])],
        [
            Paragraph("<b>False Positives (FP)</b><br/><font size='7' color='#DC2626'>Type I Error</font>", styles["TableCellLeft"]),
            Paragraph("<b>6</b> (0.66%)", styles["TableCellBold"]),
            Paragraph("Genuine messages discussing commercial topics or using urgent colloquialisms (e.g., 'Free tomorrow for dinner?', 'Please call urgent'). The model overweighed individual high-salience tokens without context.", styles["TableCellLeft"])
        ],
        [
            Paragraph("<b>False Negatives (FN)</b><br/><font size='7' color='#F59E0B'>Type II Error</font>", styles["TableCellLeft"]),
            Paragraph("<b>14</b> (10.69%)", styles["TableCellBold"]),
            Paragraph("Short, obfuscated spam containing novel alphanumeric strings, foreign phone numbers, or deliberate character substitutions (e.g., 'fr33', 'w!n') not present in the training vocabulary.", styles["TableCellLeft"])
        ],
    ]
    error_table = Table(error_data, colWidths=[120, 75, 328])
    error_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BG_ALT_ROW]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(error_table)

    story.append(Spacer(1, 6))
    story.append(Paragraph("8.3 Comparison: Naive Bayes vs Discriminative Baselines", styles["SubSectionHeader"]))

    comp_data = [
        [Paragraph("Model Paradigm", styles["TableHeadLeft"]), Paragraph("Inference Complexity", styles["TableHead"]), Paragraph("Training Data Requirement", styles["TableHead"]), Paragraph("SMS Suitability", styles["TableHead"])],
        [Paragraph("<b>Multinomial Naive Bayes (Ours)</b>", styles["TableCellLeft"]), Paragraph("O(|V|) &mdash; Microsecond latency", styles["TableCell"]), Paragraph("Low &mdash; Highly sample-efficient", styles["TableCell"]), Paragraph("<b>Ideal for Edge/SMS</b>", styles["TableCellBold"])],
        [Paragraph("Logistic Regression", styles["TableCellLeft"]), Paragraph("O(|V|) &mdash; Dot product", styles["TableCell"]), Paragraph("Moderate &mdash; Iterative gradient descent", styles["TableCell"]), Paragraph("Strong baseline", styles["TableCell"])],
        [Paragraph("Linear Support Vector Machines", styles["TableCellLeft"]), Paragraph("O(|V|) &mdash; Margin hyperplane", styles["TableCell"]), Paragraph("Moderate &mdash; Convex optimization", styles["TableCell"]), Paragraph("High precision, lacks probs", styles["TableCell"])],
        [Paragraph("Deep Transformers (e.g. BERT)", styles["TableCellLeft"]), Paragraph("O(N &middot; d<sup>2</sup>) &mdash; Heavy compute", styles["TableCell"]), Paragraph("High &mdash; Large GPU footprint", styles["TableCell"]), Paragraph("Overkill for 160-char SMS", styles["TableCell"])],
    ]
    comp_table = Table(comp_data, colWidths=[140, 125, 130, 128])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BG_ALT_ROW]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(comp_table)

    story.append(Spacer(1, 6))
    story.append(Paragraph("8.4 Roadmap for Future Extensions", styles["SubSectionHeader"]))
    story.append(Paragraph(
        "Future research and system iterations can enhance robustness along three key dimensions:<br/>"
        "1. <b>Subword Tokenization (BPE):</b> Byte-Pair Encoding or character n-grams to gracefully handle obfuscations ('fr33', 'pr!ze').<br/>"
        "2. <b>Dynamic Bayesian Online Updating:</b> Continually updating token likelihoods &theta;<sub>ci</sub> in real-time as users flag new spam campaigns, mitigating concept drift.<br/>"
        "3. <b>Ensemble Hybrid Architectures:</b> Combining Naive Bayes prior odds with lightweight contextual transformer embeddings for nuanced syntactic disambiguation.",
        styles["BodyTextCustom"]
    ))

    story.append(PageBreak())
    return story


# ==============================================================================
# PAGE 10: REFERENCES, ARTIFACTS & ACADEMIC DECLARATION
# ==============================================================================
def build_page_10(styles):
    story = []
    story.append(Paragraph("9. References, Artifacts & Academic Declaration", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=BORDER_COLOR, spaceBefore=0, spaceAfter=7))

    story.append(Paragraph("9.1 Academic & Scientific Bibliography", styles["SubSectionHeader"]))
    bib_items = [
        "[1] Almeida, T. A., Hidalgo, J. M. G., & Yamakami, A. (2011). Contributions to the Study of SMS Spam Filtering: New Collection and Results. <i>Proceedings of the 2011 ACM Symposium on Document Engineering (DocEng '11)</i>, Mountain View, CA, USA, pp. 259–262. DOI: 10.1145/2034691.2034742.",
        "[2] UCI Machine Learning Repository (2012). <i>SMS Spam Collection Dataset</i> (ID: 228). Donated by T. A. Almeida & J. M. G. Hidalgo. Available: https://archive.ics.uci.edu/dataset/228/sms+spam+collection.",
        "[3] Domingos, P., & Pazzani, M. (1997). On the optimality of the simple Bayesian classifier under zero-one loss. <i>Machine Learning</i>, 29(2), 103–130.",
        "[4] Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., et al. (2011). Scikit-learn: Machine Learning in Python. <i>Journal of Machine Learning Research</i>, 12, 2825–2830.",
        "[5] Devore, J. L. (2015). <i>Probability and Statistics for Engineering and the Sciences</i> (9th ed.). Cengage Learning, Boston, MA. Chapters 2–3 (Probability Axioms, Bayes' Theorem, and Discrete Distributions).",
    ]
    for b in bib_items:
        story.append(Paragraph(b, styles["BodyTextCustom"]))

    story.append(Spacer(1, 5))
    story.append(Paragraph("9.2 Open Source Project Repositories & Artifacts", styles["SubSectionHeader"]))

    repo_data = [
        [Paragraph("Deliverable Artifact", styles["TableHeadLeft"]), Paragraph("Uniform Resource Locator (URL) / File Path", styles["TableHeadLeft"]), Paragraph("Description", styles["TableHeadLeft"])],
        [Paragraph("Live Web Application", styles["TableCellLeft"]), Paragraph("<font color='#2563EB'><u>https://hamspam.vercel.app</u></font>", styles["TableCellLeft"]), Paragraph("Production React/FastAPI interface", styles["TableCellLeft"])],
        [Paragraph("Source Code Repository", styles["TableCellLeft"]), Paragraph("<font color='#2563EB'><u>https://github.com/SarveshS1407/HamSpam</u></font>", styles["TableCellLeft"]), Paragraph("Complete reproducible codebase", styles["TableCellLeft"])],
        [Paragraph("Serialized ML Model", styles["TableCellLeft"]), Paragraph("<code>outputs/model_artifact.json</code>", styles["TableCellLeft"]), Paragraph("Vocabulary & log-odds weights", styles["TableCellLeft"])],
        [Paragraph("Automated Tests", styles["TableCellLeft"]), Paragraph("<code>tests/test_probability_analysis.py</code>", styles["TableCellLeft"]), Paragraph("17 unit & integration tests", styles["TableCellLeft"])],
    ]
    repo_table = Table(repo_data, colWidths=[120, 220, 183])
    repo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BG_ALT_ROW]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(repo_table)

    story.append(Spacer(1, 6))
    story.append(Paragraph("9.3 Mathematical Notation Quick Reference", styles["SubSectionHeader"]))

    not_data = [
        [Paragraph("Symbol", styles["TableHead"]), Paragraph("Definition", styles["TableHeadLeft"]), Paragraph("Symbol", styles["TableHead"]), Paragraph("Definition", styles["TableHeadLeft"])],
        [Paragraph("Y", styles["TableCellBold"]), Paragraph("Binary class random variable &isin; {0, 1}", styles["TableCellLeft"]), Paragraph("p", styles["TableCellBold"]), Paragraph("Spam prior probability = P(Y = 1) = 0.126281", styles["TableCellLeft"])],
        [Paragraph("q", styles["TableCellBold"]), Paragraph("Ham prior probability = 1 - p = 0.873719", styles["TableCellLeft"]), Paragraph("E(Y)", styles["TableCellBold"]), Paragraph("Bernoulli expectation = p = 0.126281", styles["TableCellLeft"])],
        [Paragraph("Var(Y)", styles["TableCellBold"]), Paragraph("Bernoulli variance = p(1-p) = 0.110334", styles["TableCellLeft"]), Paragraph("&sigma;(Y)", styles["TableCellBold"]), Paragraph("Standard deviation = &radic;Var(Y) = 0.332166", styles["TableCellLeft"])],
        [Paragraph("&theta;<sub>ci</sub>", styles["TableCellBold"]), Paragraph("Smoothed token likelihood in class c", styles["TableCellLeft"]), Paragraph("&alpha;", styles["TableCellBold"]), Paragraph("Laplace smoothing parameter (&alpha; = 1.0)", styles["TableCellLeft"])],
    ]
    not_table = Table(not_data, colWidths=[40, 221, 40, 222])
    not_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SLATE_HEADER),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BG_ALT_ROW]),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(not_table)

    story.append(Spacer(1, 8))
    story.append(Paragraph("9.4 Academic Integrity Declaration", styles["SubSectionHeader"]))

    declaration_text = (
        "<b>Student Academic Declaration:</b><br/>"
        "I hereby declare that this project report titled <i>'HamSpam: Probabilistic SMS Spam Detection Using Bayes' Theorem "
        "and Multinomial Naive Bayes'</i> submitted for the course <b>BAMAT207 — Probability and Statistics</b> at <b>Vellore Institute of "
        "Technology, Vellore</b>, is a genuine record of original work performed by me. All empirical findings, statistical derivations, "
        "and evaluation metrics are verified against the official UCI SMS Spam Collection repository (#228). All external sources, libraries, "
        "and references have been formally acknowledged in accordance with academic standards.<br/><br/>"
        "<b>Candidate Signature:</b> ___________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "<b>Date:</b> 27 October 2026<br/>"
        "<b>Faculty Evaluator Signature:</b> ___________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "<b>Marks Awarded:</b> ______ / 100"
    )
    dec_table = Table([[Paragraph(declaration_text, styles["CalloutText"])]], colWidths=[523])
    dec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
        ('LINELEFT', (0, 0), (0, 0), 3.0, BLUE_DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 6.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(dec_table)

    return story


# ==============================================================================
# MAIN GENERATION & VERIFICATION ENTRYPOINT
# ==============================================================================
def generate_pdf(output_filename="reports/HamSpam_Project_Report.pdf"):
    """Orchestrates generation of the 10-page academic PDF report."""
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    # A4 Dimensions: 595.27 x 841.89 points
    # Margins: Left=36, Right=36 (Printable Width=523.27), Top=36, Bottom=36
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = create_styles()
    story = []

    print("[*] Assembling Page 1: Academic Cover Page...")
    story.extend(build_cover_page(styles))

    print("[*] Assembling Page 2: Executive Summary & Project Introduction...")
    story.extend(build_page_2(styles))

    print("[*] Assembling Page 3: Dataset Acquisition, Hygiene & Distribution...")
    story.extend(build_page_3(styles))

    print("[*] Assembling Page 4: Theoretical Probability & Bernoulli Modeling...")
    story.extend(build_page_4(styles))

    print("[*] Assembling Page 5: Word-Level Empirical Probabilities & Bayes Proof...")
    story.extend(build_page_5(styles))

    print("[*] Assembling Page 6: Machine Learning Methodology & Implementation...")
    story.extend(build_page_6(styles))

    print("[*] Assembling Page 7: Experimental Results & Model Evaluation...")
    story.extend(build_page_7(styles))

    print("[*] Assembling Page 8: Full-Stack Architecture, Deployment & Live Inference...")
    story.extend(build_page_8(styles))

    print("[*] Assembling Page 9: Critical Discussion, Limitations & Future Scope...")
    story.extend(build_page_9(styles))

    print("[*] Assembling Page 10: References, Appendix & Academic Declaration...")
    story.extend(build_page_10(styles))

    print(f"[*] Compiling PDF via ReportLab to: {output_filename}")
    doc.build(story, canvasmaker=NumberedCanvas)
    print("[+] PDF compilation complete!")

    # Verify Page Count via PyMuPDF
    pdf_doc = pymupdf.open(output_filename)
    page_count = len(pdf_doc)
    print(f"[+] Total Pages Generated: {page_count}")
    assert page_count == 10, f"Expected exactly 10 pages, got {page_count}!"
    print(f"[✓] Verification SUCCESS: PDF has exactly {page_count} pages.")
    return output_filename, page_count


if __name__ == "__main__":
    generate_pdf()
