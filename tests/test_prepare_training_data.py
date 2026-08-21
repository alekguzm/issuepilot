from issuepilot.prepare import prepare_training_data

def test_prepare_training_data_keeps_only_single_target_labels():
    raw_issues = [
        {
            "repository": "test/test",
            "issue_number": 1,
            "title": "Estimator crashes",
            "body": "An error occurs during fitting.",
            "labels": ["Bug"],
        },
        {
            "repository": "test/test",
            "issue_number": 2,
            "title": "Improve user guide",
            "body": "The documentation needs another example.",
            "labels": ["Documentation"],
        },
        {
            "repository": "test/test",
            "issue_number": 3,
            "title": "Issue with documentation",
            "body": "This issue matches multiple supported labels.",
            "labels": ["Bug", "Documentation"],
        },
        {
            "repository": "test/test",
            "issue_number": 4,
            "title": "Update CI workflow",
            "body": "This label is not part of the target categories.",
            "labels": ["CI"],
        },
    ]

    processed_issues, class_counts = prepare_training_data(raw_issues)

    assert len(processed_issues) == 2

    assert processed_issues[0]["issue_number"] == 1
    assert processed_issues[0]["target"] == "bug"

    assert processed_issues[1]["issue_number"] == 2
    assert processed_issues[1]["target"] == "documentation"

    assert class_counts["Bug"] == 1
    assert class_counts["New Feature"] == 0
    assert class_counts["Documentation"] == 1