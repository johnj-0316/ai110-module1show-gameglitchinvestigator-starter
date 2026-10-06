def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # Fixed the difficulty ranges so harder modes use larger number ranges.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        # Generalized parsing so integer and decimal inputs both become integer guesses.
        value = int(float(raw))
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return the outcome.

    outcome examples: "Win", "Too High", "Too Low"
    """
    # Added integer type hints and removed the old string-comparison fallback.
    if guess == secret:
        return "Win"

    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    wrong_guess_penalty = 5

    if outcome == "Win":
        # Edited attempt_number to count for 1 shot guesses.
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        # Fixed wrong guesses so they consistently subtract points without going below 0.
        return max(0, current_score - wrong_guess_penalty)

    if outcome == "Too Low":
        return max(0, current_score - wrong_guess_penalty)

    return current_score
