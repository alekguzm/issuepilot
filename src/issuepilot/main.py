"""Run IssuePilot predictions on open issues from a GitHub repository."""

from issuepilot.fetch_issues import full_retrieve
from issuepilot.predict import predict_issues
from issuepilot.text_processing import build_text
import sys
from pathlib import Path

def main():

    root_path = Path(__file__).resolve().parents[2]
    pipe_filename = root_path / "models" / "pipeline.joblib"

    if not pipe_filename.exists():
        print("Trained model could not be found. Run the training script first.")
        sys.exit(1)

    owner = input("Enter the GitHub repository owner: ").strip()
    repo = input("Enter the GitHub repository name: ").strip()

    issues = full_retrieve(owner, repo, state="open")
    if issues is None:
        print("No issues could be retrieved.")
        sys.exit()
    if not issues:
        print("No open issues were found.")
        sys.exit()

    inputs = [build_text(issue) for issue in issues]

    predictions = predict_issues(pipe_filename, inputs)

    for issue, prediction in zip(issues, predictions):
        print(f"#{issue['issue_number']}")
        print(issue["title"])
        print(f"Prediction: {prediction}\n")

if __name__ == "__main__":
    main()