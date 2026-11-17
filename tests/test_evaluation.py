from nexus_cloud.evaluation import extract_code, score_code_response


def test_extracts_python_fence() -> None:
    text = "Here is the answer:\n\n```python\ndef answer():\n    return 42\n```"
    assert extract_code(text) == "def answer():\n    return 42"


def test_valid_python_is_accepted_without_execution() -> None:
    score = score_code_response("def answer():\n    return 42")
    assert score.has_code is True
    assert score.syntax_valid is True
    assert score.line_count == 2
    assert score.syntax_error is None


def test_invalid_python_is_rejected() -> None:
    score = score_code_response("def answer(:\n    return 42")
    assert score.has_code is True
    assert score.syntax_valid is False
    assert "line 1" in (score.syntax_error or "")


def test_empty_response_is_not_code() -> None:
    score = score_code_response("  ")
    assert score.has_code is False
    assert score.syntax_valid is False


def test_plain_response_is_checked_as_python() -> None:
    score = score_code_response("This is an explanation, not Python")
    assert score.syntax_valid is False
