"""
Real-Time SMS Spam Prediction Interface Module for HamSpam.

Provides real-time inference using trained Multinomial Naive Bayes and CountVectorizer:
- Computes estimated posterior class probabilities P(Spam | Message) and P(Ham | Message).
- Labels probabilities transparently as model-estimated probabilities under bag-of-words assumptions.
- Formats visual prediction cards.
- Handles empty or whitespace inputs gracefully without exceptions.
- Provides interactive command-line interface (CLI) and automated demonstration suite.
"""

from typing import Any, Dict, List, Optional
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


def predict_message(
    message: str,
    clf: MultinomialNB,
    vectorizer: CountVectorizer,
) -> Dict[str, Any]:
    """
    Predict whether an incoming SMS is Spam or Ham with estimated class probabilities.

    Parameters
    ----------
    message : str
        Raw SMS text string.
    clf : MultinomialNB
        Trained Multinomial Naive Bayes model.
    vectorizer : CountVectorizer
        Fitted CountVectorizer.

    Returns
    -------
    Dict[str, Any]
        Dictionary with input message, predicted label, estimated probabilities,
        and visual indicator.
    """
    if message is None or not message.strip():
        return {
            "original_message": message if message is not None else "",
            "is_valid": False,
            "predicted_label": "Empty / Invalid",
            "p_ham": None,
            "p_spam": None,
            "visual_indicator": "[ ⚠️  EMPTY INPUT ]",
            "explanation": "No text provided. Empty messages cannot be classified.",
        }

    # Transform input text using fitted vocabulary
    msg_cleaned = message.strip()
    msg_vec = vectorizer.transform([msg_cleaned])

    # Model estimated posterior probabilities
    probs = clf.predict_proba(msg_vec)[0]
    p_ham = float(probs[0])
    p_spam = float(probs[1])

    # Predicted class (threshold = 0.5)
    pred_class = int(clf.predict(msg_vec)[0])
    predicted_label = "Spam" if pred_class == 1 else "Ham"

    # Visual indicator formatting
    if predicted_label == "Spam":
        visual_indicator = f"[ 🚨 SPAM ALERT | Confidence: {p_spam:.1%} ]"
    else:
        visual_indicator = f"[ 🟢 LEGITIMATE HAM | Confidence: {p_ham:.1%} ]"

    return {
        "original_message": msg_cleaned,
        "is_valid": True,
        "predicted_label": predicted_label,
        "predicted_class": pred_class,
        "p_ham": p_ham,
        "p_spam": p_spam,
        "visual_indicator": visual_indicator,
        "explanation": (
            "Probabilities are model-estimated class likelihoods via Multinomial Naive Bayes "
            "using empirical word counts and Laplace smoothing, not absolute guarantees."
        ),
    }


def format_prediction_card(result: Dict[str, Any]) -> str:
    """
    Format the prediction result into a clear, readable text card.
    """
    lines = [
        "┌─────────────────────────────────────────────────────────────────────────────┐",
        f"│ {result['visual_indicator']:<75} │",
        "├─────────────────────────────────────────────────────────────────────────────┤",
        f"│ Message        : {result['original_message'][:60]:<60} │",
    ]
    if len(result["original_message"]) > 60:
        lines.append(f"│                  {result['original_message'][60:120]:<60} │")

    lines.append(f"│ Predicted Label: {result['predicted_label']:<60} │")

    if result["is_valid"]:
        lines.append(
            f"│ P(Spam|Message): {result['p_spam']:.4f} ({result['p_spam']:.2%}){'':<39} │"
        )
        lines.append(
            f"│ P(Ham|Message) : {result['p_ham']:.4f} ({result['p_ham']:.2%}){'':<39} │"
        )
    else:
        lines.append(f"│ Notice         : {result['explanation']:<60} │")

    lines.append("└─────────────────────────────────────────────────────────────────────────────┘")
    return "\n".join(lines)


def run_demo_predictions(
    clf: MultinomialNB,
    vectorizer: CountVectorizer,
    custom_samples: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Execute sample SMS predictions including the required examples.
    """
    if custom_samples is None:
        custom_samples = [
            "Congratulations! You have won a free prize. Claim now.",
            "Hey, are we meeting for lunch today?",
            "URGENT! You have won a 1 week FREE membership in our £100,000 prize draw!",
            "Can you please send me the lecture slides for BAMAT207?",
            "Exclusive offer: Get 50% discount on your next pizza order. Reply WIN to 8888.",
            "",  # empty test
            "   ",  # whitespace test
        ]

    results = []
    print("\n" + "=" * 79)
    print("HAMSPAM — REAL-TIME SMS PREDICTION DEMONSTRATION")
    print("=" * 79)

    for msg in custom_samples:
        res = predict_message(msg, clf, vectorizer)
        results.append(res)
        print(format_prediction_card(res))
        print()

    return results


def interactive_cli(clf: MultinomialNB, vectorizer: CountVectorizer) -> None:
    """
    Interactive command-line loop allowing real-time user SMS input.
    """
    print("\n" + "=" * 79)
    print("HAMSPAM — INTERACTIVE SMS CLASSIFICATION CONSOLE")
    print("Type any SMS message and press Enter to classify.")
    print("Type 'quit' or 'exit' to return.")
    print("=" * 79 + "\n")

    while True:
        try:
            user_input = input("Enter SMS > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting interactive console.")
            break

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        res = predict_message(user_input, clf, vectorizer)
        print("\n" + format_prediction_card(res) + "\n")


if __name__ == "__main__":
    from data_loader import load_and_preprocess
    from train_model import train_multinomial_nb, split_data

    _, clean_df, _ = load_and_preprocess()
    X_train, X_test, y_train, y_test = split_data(clean_df)
    clf, vec = train_multinomial_nb(X_train, y_train)

    run_demo_predictions(clf, vec)
