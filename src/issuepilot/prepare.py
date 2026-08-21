"""Prepare labeled GitHub issues for IssuePilot model training."""

LABEL_MAPPING = {"Bug": "bug", 
                 "New Feature": "feature", 
                 "Documentation": "documentation"}


def prepare_training_data(raw_issues):
    """Keep issues matching exactly one supported source label and map it to an IssuePilot category."""

    issues_processed = []

    class_counts = {label: 0 for label in LABEL_MAPPING}

    for issue in raw_issues:

        labels = issue["labels"]
        temp_dict = {}

        matching_labels = [
            label for label in labels
            if label in LABEL_MAPPING
            ]

        if len(matching_labels) != 1:
            continue

        source_label = matching_labels[0]

        temp_dict["repository"] = issue["repository"]
        temp_dict["issue_number"] = issue["issue_number"]
        temp_dict["title"] = issue["title"]
        temp_dict["body"] = issue["body"]
        temp_dict["original_labels"] = issue["labels"]

        temp_dict["target"] = LABEL_MAPPING[source_label]
        class_counts[source_label] += 1

        issues_processed.append(temp_dict)

    return issues_processed, class_counts