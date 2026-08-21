"""Inspect raw GitHub label frequencies and target-label coverage."""

import json
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = ROOT_PATH / "data" / "raw" / "scikit_learn_issues.json"

with open (RAW_DATA_PATH, 'r', encoding="utf-8") as f:
    data = json.load(f)

total_issues = len(data)
print(f"# of Issues: {total_issues}\n")

label_counts = {}

target_labels = ['Bug', 'New Feature', 'Documentation']
target_num_dict = {"zero": 0, "one": 0, "two_plus": 0}

for issue in data:
    target_matches = 0
    labels = issue['labels']
    for label in labels:
        label_counts[label] = label_counts.get(label, 0) + 1

        if label in target_labels: 
            target_matches += 1
    if target_matches == 0:
            target_num_dict['zero'] += 1
    elif target_matches == 1:
        target_num_dict['one'] += 1
    else:
        target_num_dict['two_plus'] += 1

print(f"Bug: {label_counts.get("Bug", 0)}")
print(f"Feature: {label_counts.get("New Feature", 0)}")
print(f"Documentation: {label_counts.get("Documentation", 0)}")

print("\nTarget Coverage:")

print(f"0 target: {target_num_dict['zero']}")
print(f"1 target: {target_num_dict['one']}")
print(f"2+ target: {target_num_dict['two_plus']}")

print(f"Usable examples: {target_num_dict['one']} / {total_issues} ({(target_num_dict['one']/total_issues * 100):.1f}%)")
