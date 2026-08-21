from issuepilot.text_processing import clean_title, clean_body, build_text



def test_clean_title_prefix():
    result = clean_title("BUG: Estimator crashes with NaN values")
    assert result == "Estimator crashes with NaN values"

def test_clean_title_keeps_normal_bug_word():
    result = clean_title("Estimator has a bug when fitting")
    assert result == "Estimator has a bug when fitting"


def test_clean_body_removes_template_phrase():
    body = "Describe the bug Something crashes when fitting"
    result = clean_body(body)

    assert result == "Something crashes when fitting"

def test_clean_body_none():
    result = clean_body(None)

    assert result == ""


def test_build_text():
    issue = {
        "title": "BUG: Estimator crashes",
        "body": "Happens when input contains NaN values"
    }

    result = build_text(issue)

    assert result == (
        "Estimator crashes\n\n"
        "Happens when input contains NaN values"
    )