"""Evaluation helpers for binary matching predictions."""

from sklearn.metrics import classification_report, f1_score


def evaluate(y_true, y_pred) -> dict:
    """Return the primary F1 score and a readable classification report."""
    return {"f1": f1_score(y_true, y_pred), "report": classification_report(y_true, y_pred)}

