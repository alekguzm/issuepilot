"""Train and evaluate the IssuePilot text-classification pipeline."""

import json
import joblib
import numpy as np
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline

from issuepilot.text_processing import build_text

ROOT_PATH = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_PATH / "data" / "processed" / "scikit_learn_issues_processed.json"
MODEL_PATH = ROOT_PATH / "models" / "pipeline.joblib"

def make_pipeline():
    """Create the TF-IDF and class-balanced Logistic Regression pipeline."""

    pipe = Pipeline([
        ('tfidf', TfidfVectorizer()), 
        # Balanced weighting improved minority-class recall during evaluation
        ('logreg', LogisticRegression(class_weight='balanced'))
        ])
    return pipe

def train_model(X, y, path_filename):
    """Evaluate the pipeline with stratified CV, then fit and save the final model."""

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    macro_f1_scores = []
    
    for fold, (train_index, test_index) in enumerate(skf.split(X, y)):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        pipe = make_pipeline()
        pipe.fit(X_train, y_train)

        y_pred = pipe.predict(X_test)
        score = f1_score(y_test, y_pred, average='macro')
        macro_f1_scores.append(score)

        print(f"Fold {fold+1}: {score:.4f}")

    mean_f1 = np.mean(macro_f1_scores)
    std = np.std(macro_f1_scores)
    print(f"Mean macro F1: {mean_f1:.4f}")
    print(f"Standard deviation: {std:.4f}")

    final_pipe = make_pipeline()
    final_pipe.fit(X, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(final_pipe, path_filename)
    print(f"Pipeline successfully saved to {path_filename}")

if __name__ == '__main__':

    with open (DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    X = []
    y = []
    for issue in data:
        X.append(build_text(issue))
        y.append(issue["target"])

    X = np.array(X)
    y = np.array(y)

    train_model(X, y, MODEL_PATH)

