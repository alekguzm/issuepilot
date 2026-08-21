
from issuepilot.fetch_issues import filter_pulls

#Test 1: 
#   filter_pulls() : pull requests are filtered out of list
def test_filter_pulls():
    """Pull requests should be removed from GitHub issue results."""

    test_issues = [
    {
        "number": 1,
        "title": "Estimator crashes with NaN values",
        "state": "open"
    },
    {
        "number": 2,
        "title": "Fix estimator crash",
        "state": "open",
        "pull_request": {
            "url": "https://api.github.com/repos/test/test/pulls/2"
        }
    },
    {
        "number": 3,
        "title": "Improve documentation for PCA",
        "state": "open"
    }
    ]

    result = filter_pulls(test_issues)
    remaining_numbers = [issue["number"] for issue in result]

    assert len(result) == 2
    assert 2 not in remaining_numbers

    