from issuepilot.predict import predict_issues
from issuepilot.text_processing import build_text
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT_PATH / "models" / "pipeline.joblib"
ALLOWED_CATEGORIES = {"bug", "feature", "documentation"}

def test_predict_returns_valid_category():

    issue = {
        "title": "BUG: CountVectorizer crashes on short strings",
        "body": "CountVectorizer raises an error when strings are shorter than the ngram range."
    }

    model_input = [build_text(issue)]

    predictions = predict_issues(MODEL_PATH, model_input)
    
    assert len(predictions) == 1
    assert predictions[0] in ALLOWED_CATEGORIES