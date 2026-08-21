# IssuePilot

IssuePilot is a machine-learning tool that retrieves open GitHub issues and predicts a standardized category for each issue: **bug**, **feature**, or **documentation**.

The project uses cleaned issue titles and descriptions, TF-IDF text features, and a class-balanced Logistic Regression classifier.

## Problem

GitHub repositories often use different or inconsistent labels for similar types of issues. This can make issues harder to organize, search, and analyze across repositories.

IssuePilot addresses this by mapping issue text to a smaller shared category system. Given a public GitHub repository, it retrieves its open issues and predicts whether each issue is a bug, feature request, or documentation issue.

## Features

- Retrieve issues from a user-specified public GitHub repository using the GitHub REST API
- Filter pull requests from GitHub issue responses
- Clean issue titles and descriptions to reduce category-label leakage
- Combine issue titles and descriptions for text classification
- Predict standardized `bug`, `feature`, and `documentation` categories
- Use a persisted scikit-learn Pipeline containing TF-IDF and Logistic Regression
- Evaluate model performance with stratified cross-validation
- Run automated tests with pytest

## Model

IssuePilot currently uses:

- **TF-IDF** for text feature extraction
- **Logistic Regression** with class-balanced weighting for classification
- Cleaned issue titles and descriptions as model input

The current training dataset contains **121 labeled scikit-learn issues**.

Using 5-fold stratified cross-validation, the model achieved:

- **Mean macro F1: 0.845**
- **Standard deviation: 0.065**

## Limitations

The current model was trained using labeled issues from the scikit-learn repository, so its performance on substantially different repositories has not yet been fully evaluated.

IssuePilot currently supports three standardized categories:

- `bug`
- `feature`
- `documentation`

The project does not modify, close, or relabel GitHub issues. Predictions are intended to assist with issue organization rather than replace repository maintainers.

## Development Setup

IssuePilot was developed using Python 3.13.

Clone the repository:

```powershell
git clone https://github.com/alekguzm/issuepilot.git
cd issuepilot
```

Create and activate a virtual environment:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install IssuePilot and its development dependencies:

```powershell
pip install -e ".[dev]"
```

Run the automated tests:

```powershell
pytest
```

## Example Usage

Run IssuePilot from the project root:

```powershell
python -m issuepilot.main
```

Enter the GitHub repository owner and repository name when prompted:

```text
Enter the GitHub Repository Owner: scikit-learn
Enter the GitHub Repository Repo: scikit-learn
```

Example output:

```text
Raw API results inspected: 30
Ordinary results inspected: 9

#34764
Impact of active wait policy of OMP implementations in scikit-learn
Prediction: feature

#34745
BUG sample-weight ignored by `min_sample_leaf` in HGBDT
Prediction: bug

#34732
⚠️ CI failed on Unit tests Linux pymin_conda_forge_arm (last failure: Aug 12, 2026) ⚠️
Prediction: documentation
```

## Project Structure

```text
issuepilot/
├── data/
│   ├── raw/
│   └── processed/
├── models/
│   └── pipeline.joblib
├── scripts/
│   ├── inspect_labels.py
│   ├── prepare_training_data.py
│   └── train.py
├── src/
│   └── issuepilot/
│       ├── __init__.py
│       ├── fetch_issues.py
│       ├── main.py
│       ├── predict.py
│       └── text_processing.py
├── tests/
│   ├── test_fetch_issues.py
│   ├── test_predict.py
│   └── test_text_processing.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Training Pipeline

```text
GitHub REST API
      ↓
Raw GitHub issues
      ↓
Filter pull requests
      ↓
Normalize issue data
      ↓
Map supported repository labels
      ↓
Keep issues with exactly one target label
      ↓
Clean titles and descriptions
      ↓
Combine title + description
      ↓
TF-IDF vectorization
      ↓
Class-balanced Logistic Regression
      ↓
5-fold stratified cross-validation
      ↓
Train final model on all labeled examples
      ↓
Save scikit-learn Pipeline
```

For the current scikit-learn training dataset, source labels are mapped as follows:

| GitHub Label | IssuePilot Category |
| --- | --- |
| `Bug` | `bug` |
| `New Feature` | `feature` |
| `Documentation` | `documentation` |

Issues containing zero or multiple supported target labels are excluded from the current supervised training dataset.

The final model combines TF-IDF feature extraction and Logistic Regression into a single persisted scikit-learn Pipeline so the same text transformation is used during training and prediction.

## Future Work

IssuePilot currently demonstrates the complete workflow from GitHub issue retrieval through machine-learning prediction. Future improvements include:

- Evaluate performance using repository-level holdout testing to better measure cross-repository generalization
- Expand the training dataset with labeled issues from additional GitHub repositories
- Support additional standardized issue categories and repository-specific label mappings
- Add a **FastAPI** backend for programmatic issue classification
- Use **PostgreSQL** to store retrieved issues, predictions, and repository metadata
- **Dockerize** the application for reproducible setup and deployment
- Compare the current Logistic Regression model with additional text-classification approaches
- Add a more user-friendly interface on top of the API and machine-learning pipeline