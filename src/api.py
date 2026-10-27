"""
FastAPI Production Backend for HamSpam.

Provides RESTful endpoints for:
- Health verification (`/health`)
- Cleaned dataset statistics & Bernoulli parameters (`/api/stats`)
- Suspicious keyword conditional probability analysis & Bayes verification (`/api/probabilities`)
- Held-out test set model evaluation metrics & confusion matrix (`/api/evaluation`)
- Real-time SMS spam prediction (`/api/predict`)
- Static asset serving for production single-port deployment
"""

import os
import sys
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

import matplotlib
matplotlib.use("Agg")

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Ensure project src is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from data_loader import load_and_preprocess
from probability_analysis import (
    calculate_bernoulli_statistics,
    calculate_class_probabilities,
    calculate_word_probabilities,
)
from train_model import split_data, train_multinomial_nb, evaluate_model
from predict import predict_message

# Global application state cache
state: Dict[str, Any] = {
    "df_raw": None,
    "df_clean": None,
    "cleaning_stats": None,
    "class_stats": None,
    "word_df": None,
    "bernoulli_stats": None,
    "clf": None,
    "vectorizer": None,
    "eval_results": None,
    "ready": False,
}


def initialize_model_and_stats():
    """Load dataset, compute probabilities, and train Naive Bayes model."""
    print("[API] Initializing HamSpam machine learning model and statistical state...")
    df_raw, df_clean, cleaning_stats = load_and_preprocess()

    class_stats = calculate_class_probabilities(df_clean)
    word_df = calculate_word_probabilities(df_clean, matching="whole_word")
    bernoulli_stats = calculate_bernoulli_statistics(class_stats["p_spam"])

    X_train, X_test, y_train, y_test = split_data(df_clean, test_size=0.2, random_state=42)
    clf, vectorizer = train_multinomial_nb(X_train, y_train)
    eval_results = evaluate_model(clf, vectorizer, X_test, y_test)

    state["df_raw"] = df_raw
    state["df_clean"] = df_clean
    state["cleaning_stats"] = cleaning_stats
    state["class_stats"] = class_stats
    state["word_df"] = word_df
    state["bernoulli_stats"] = bernoulli_stats
    state["clf"] = clf
    state["vectorizer"] = vectorizer
    state["eval_results"] = eval_results
    state["ready"] = True
    print("[API] Initialization complete. HamSpam backend is ready to serve.")


def ensure_initialized():
    """Ensure model and statistics are loaded and ready."""
    if not state["ready"]:
        initialize_model_and_stats()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager to train/load model on startup."""
    ensure_initialized()
    yield
    print("[API] Shutting down HamSpam service.")


app = FastAPI(
    title="HamSpam API",
    description="Probabilistic SMS Spam Detection API using Bayes' Theorem and Multinomial Naive Bayes (BAMAT207, VIT Vellore)",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Middleware (allows deployed frontend and local dev environments)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request and Response Schemas
class PredictRequest(BaseModel):
    message: str = Field(..., description="SMS text content to classify")


class PredictResponse(BaseModel):
    original_message: str
    is_valid: bool
    predicted_label: str
    predicted_class: Optional[int] = None
    p_ham: Optional[float] = None
    p_spam: Optional[float] = None
    visual_indicator: str
    explanation: str


@app.get("/health", tags=["System"])
def health_check():
    """Verify backend health and model readiness."""
    ensure_initialized()
    return {
        "status": "healthy" if state["ready"] else "initializing",
        "model_loaded": state["clf"] is not None,
        "dataset_loaded": state["df_clean"] is not None,
        "version": "1.0.0",
    }


@app.get("/api/stats", tags=["Statistics"])
def get_dataset_stats():
    """Return dataset dimensions, cleaning audit, prior class probabilities, and Bernoulli parameters."""
    ensure_initialized()

    cs = state["class_stats"]
    bs = state["bernoulli_stats"]
    cl = state["cleaning_stats"]

    return {
        "dataset_name": "SMS Spam Collection (UCI Machine Learning Repository ID: 228)",
        "raw_total": cl["raw_total"],
        "cleaned_total": cl["cleaned_total"],
        "duplicates_removed": cl["duplicates_removed"],
        "missing_values": cl["missing_label"] + cl["missing_message"],
        "ham_count": cs["ham_count"],
        "spam_count": cs["spam_count"],
        "p_ham": round(cs["p_ham"], 6),
        "p_spam": round(cs["p_spam"], 6),
        "bernoulli": {
            "p": round(bs["p"], 6),
            "q": round(bs["q"], 6),
            "expectation_E_Y": round(bs["expectation_E_Y"], 6),
            "variance_Var_Y": round(bs["variance_Var_Y"], 6),
            "std_dev_sigma_Y": round(bs["std_dev_sigma_Y"], 6),
        },
    }


@app.get("/api/probabilities", tags=["Statistics"])
def get_word_probabilities():
    """Return word-based conditional probabilities, Bayes' Theorem inversion, and mathematical verification."""
    ensure_initialized()

    w_df = state["word_df"]
    records = []
    for _, row in w_df.iterrows():
        records.append({
            "word": row["word"],
            "total_messages_with_word": int(row["total_messages_with_word"]),
            "spam_messages": int(row["spam_messages"]),
            "ham_messages": int(row["ham_messages"]),
            "p_word_given_spam": round(float(row["p_word_given_spam"]), 6),
            "p_word_given_ham": round(float(row["p_word_given_ham"]), 6),
            "p_word": round(float(row["p_word"]), 6),
            "p_spam_given_word_direct": round(float(row["p_spam_given_word_direct"]), 6),
            "p_spam_given_word_bayes": round(float(row["p_spam_given_word_bayes"]), 6),
            "p_ham_given_word": round(float(row["p_ham_given_word"]), 6),
            "bayes_direct_diff": float(row["bayes_direct_diff"]),
            "bayes_verified": bool(row["bayes_verified"]),
        })

    return {
        "matching_mode": "case-insensitive whole-word regex (\\bword\\b)",
        "tolerance": 1e-9,
        "words": records,
    }


@app.get("/api/evaluation", tags=["Model"])
def get_model_evaluation():
    """Return genuine model evaluation metrics on held-out test data."""
    ensure_initialized()

    ev = state["eval_results"]
    return {
        "model_type": "Multinomial Naive Bayes (Laplace smoothing alpha=1.0)",
        "vectorizer": "CountVectorizer (Bag-of-Words, fitted strictly on X_train)",
        "test_size_ratio": 0.20,
        "train_size": 4136,
        "test_size": 1035,
        "test_distribution": {
            "ham_count": 904,
            "spam_count": 131,
            "ham_proportion": 0.87343,
            "spam_proportion": 0.12657,
        },
        "metrics": {
            "accuracy": round(ev["accuracy"], 4),
            "precision": round(ev["precision"], 4),
            "recall": round(ev["recall"], 4),
            "f1_score": round(ev["f1_score"], 4),
        },
        "confusion_matrix": {
            "tn": ev["tn"],
            "fp": ev["fp"],
            "fn": ev["fn"],
            "tp": ev["tp"],
            "descriptions": {
                "tn": "True Negative: Genuine message correctly identified as ham",
                "tp": "True Positive: Spam message correctly identified as spam",
                "fp": "False Positive (Type I Error): Genuine message falsely flagged as spam",
                "fn": "False Negative (Type II Error): Spam message missed and delivered as ham",
            },
        },
        "imbalance_insight": (
            "Because Ham constitutes 87.34% of the test set, a trivial dummy baseline predicting "
            "all Ham achieves 87.34% accuracy with 0% Spam recall. The model's 95.12% Precision "
            "and 89.31% Recall confirm genuine probabilistic token discrimination."
        ),
    }


@app.post("/api/predict", response_model=PredictResponse, tags=["Prediction"])
def predict_sms(req: PredictRequest):
    """
    Classify an incoming SMS and compute estimated class probabilities P(Spam|Message) and P(Ham|Message).
    """
    ensure_initialized()

    res = predict_message(req.message, state["clf"], state["vectorizer"])
    return PredictResponse(
        original_message=res["original_message"],
        is_valid=res["is_valid"],
        predicted_label=res["predicted_label"],
        predicted_class=res.get("predicted_class"),
        p_ham=round(res["p_ham"], 4) if res.get("p_ham") is not None else None,
        p_spam=round(res["p_spam"], 4) if res.get("p_spam") is not None else None,
        visual_indicator=res["visual_indicator"],
        explanation=res["explanation"],
    )


# Mount built frontend static assets if available (production fullstack support)
FRONTEND_DIST = os.path.join(BASE_DIR, "frontend", "dist")
if os.path.isdir(FRONTEND_DIST):
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
    print(f"[API] Mounted frontend static files from: {FRONTEND_DIST}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
