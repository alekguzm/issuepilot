"""Create the labeled IssuePilot training dataset from collected GitHub issues."""

import json
from pathlib import Path

from issuepilot.prepare import prepare_training_data

ROOT_PATH = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = ROOT_PATH / "data" / "raw" / "scikit_learn_issues.json"
PROCESSED_DATA_PATH = (
    ROOT_PATH
    / "data"
    / "processed"
    / "scikit_learn_issues_processed.json"
)


if __name__ == "__main__":
    with open (RAW_DATA_PATH, 'r', encoding="utf-8") as f:
        raw_issues = json.load(f)

    issues_processed, class_counts = prepare_training_data(raw_issues)

    print(f"Raw examples: {len(raw_issues)}")
    print(f"Processed examples: {len(issues_processed)}\n")

    print("Class distribution:")
    print(f"bug: {class_counts['Bug']}")
    print(f"feature: {class_counts['New Feature']}")
    print(f"documentation: {class_counts['Documentation']}\n\n")

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open (PROCESSED_DATA_PATH, 'w', encoding="utf-8") as f:
        json.dump(issues_processed, f, indent=4, ensure_ascii=False)
