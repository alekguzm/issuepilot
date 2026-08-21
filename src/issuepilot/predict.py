"""Predict standardized IssuePilot categories for GitHub issues."""

import joblib

def predict_issues(pipe_filename, data):
    """Load a trained pipeline and predict categories for prepared issue text."""

    pipe = joblib.load(pipe_filename)
    predictions = pipe.predict(data)
    
    return predictions