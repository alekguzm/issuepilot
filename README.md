# issuepilot
Machine-learning system for classifying and retrieving related Github issues.

## Problem

A GitHub issue contains user-generated content and metadata used to track bugs, tasks, and ideas within a repository. Inconsistent repository labels can cause broken search filters, skewed project metrics, and communication problems. IssuePilot will retrieve GitHub issues and use their data to predict each issue's category. Companies and development teams can benefit from this because it allows issues to be classified automatically when there are too many to review manually.

## Initial Scope

For the first version, IssuePilot will:

- Collect public issues from selected GitHub repositories
- Convert repository-specific labels into a smaller shared category system
- Train and evaluate a text-classification model
- Predict a category for a new issue title and description

## Non-Goals

The first version will not use advanced neural networks immediately. It will also not include a complete website before the machine-learning system works. It will not automatically close, edit, or otherwise modify GitHub issues, and it is not intended to replace repository maintainers.

## Development Setup

This project currently uses Python 3.13.

```powershell
git clone https://github.com/alekguzm/issuepilot.git
cd issuepilot
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1