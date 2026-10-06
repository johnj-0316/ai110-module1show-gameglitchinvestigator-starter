import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


@pytest.mark.parametrize(
    ("difficulty", "expected_range"),
    [
        ("Easy", (1, 20)),
        ("Normal", (1, 50)),
        ("Hard", (1, 100)),
    ],
)
# Checks that each valid difficulty maps to its expected guessing range.
def test_get_range_for_known_difficulties(difficulty, expected_range):
    assert get_range_for_difficulty(difficulty) == expected_range


@pytest.mark.parametrize(
    "difficulty",
    ["", "Expert", "easy", None, 12, 12.3],
)
# Checks that unexpected difficulty values fall back to the default range.
def test_get_range_for_unknown_or_faulty_difficulties_defaults_to_normal_range(difficulty):
    assert get_range_for_difficulty(difficulty) == (1, 100)


@pytest.mark.parametrize(
    ("raw", "expected_value"),
    [
        ("0", 0),
        ("101", 101),
        ("-101", -101),
        ("12", 12),
        ("12.3", 12),
        ("14.49", 14),
        (" 12 ", 12),
        (12, 12),
        (12.3, 12),
        (0, 0),
        (-101, -101),
    ],
)
# Checks that numeric guesses parse successfully, including decimals that truncate.
def test_parse_guess_accepts_numeric_values_and_truncates_decimals(raw, expected_value):
    assert parse_guess(raw) == (True, expected_value, None)


@pytest.mark.parametrize(
    "raw",
    [None, "", "abc", "12abc", [], {}, object()],
)
# Checks that blank, missing, and non-numeric guesses return validation errors.
def test_parse_guess_rejects_empty_or_non_numeric_values(raw):
    ok, value, message = parse_guess(raw)

    assert ok is False
    assert value is None
    assert message in ("Enter a guess.", "That is not a number.")


@pytest.mark.parametrize(
    ("guess", "secret", "expected_outcome"),
    [
        (50, 50, "Win"),
        (60, 50, "Too High"),
        (40, 50, "Too Low"),
        (0, 50, "Too Low"),
        (101, 50, "Too High"),
        (-101, 50, "Too Low"),
        (12.3, 12, "Too High"),
        (12.0, 12, "Win"),
    ],
)
# Checks win, too-high, and too-low outcomes for normal and edge numeric guesses.
def test_check_guess_compares_numeric_values(guess, secret, expected_outcome):
    assert check_guess(guess, secret) == expected_outcome


@pytest.mark.parametrize(
    ("guess", "secret"),
    [
        ("12", 12),
        (12, "12"),
        ("abc", 12),
        (None, 12),
    ],
)
# Checks that values with incompatible comparison types raise TypeError.
def test_check_guess_raises_type_error_for_faulty_comparison_types(guess, secret):
    with pytest.raises(TypeError):
        check_guess(guess, secret)


@pytest.mark.parametrize(
    ("current_score", "outcome", "attempt_number", "expected_score"),
    [
        (0, "Win", 1, 100),
        (10, "Win", 1, 110),
        (0, "Win", 10, 10),
        (0, "Win", 101, 10),
        (0, "Win", -101, 1120),
        (0, "Win", 12.3, 10),
        (20, "Too High", 3, 15),
        (20, "Too Low", 3, 15),
        (5, "Too High", 3, 0),
        (5, "Too Low", 3, 0),
        (0, "Too High", 3, 0),
        (0, "Too Low", 3, 0),
        (20, "Unknown", 3, 20),
    ],
)
# Checks scoring for wins, wrong guesses, unknown outcomes, and edge attempts.
def test_update_score_handles_outcomes_and_edge_attempts(
    current_score,
    outcome,
    attempt_number,
    expected_score,
):
    assert update_score(current_score, outcome, attempt_number) == expected_score


@pytest.mark.parametrize(
    ("current_score", "outcome", "attempt_number"),
    [
        ("0", "Win", 1),
        (0, "Win", "12"),
    ],
)
# Checks that faulty types raise TypeError when win scoring needs arithmetic.
def test_update_score_raises_type_error_for_faulty_win_score_types(
    current_score,
    outcome,
    attempt_number,
):
    with pytest.raises(TypeError):
        update_score(current_score, outcome, attempt_number)


@pytest.mark.parametrize(
    ("current_score", "outcome", "attempt_number", "expected_score"),
    [
        ("20", "Unknown", 1, "20"),
        (20, None, 1, 20),
        (20, "Too High", "12", 15),
        (20, "Too Low", 12.3, 15),
    ],
)
# Checks that unused attempt_number types do not matter for non-win outcomes.
def test_update_score_ignores_attempt_number_when_outcome_does_not_need_it(
    current_score,
    outcome,
    attempt_number,
    expected_score,
):
    assert update_score(current_score, outcome, attempt_number) == expected_score
