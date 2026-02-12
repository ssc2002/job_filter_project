import re

EXPERIENCE_LIMIT = 3

VISA_BLOCK_PHRASES = [
    "visa sponsorship not available",
    "no visa sponsorship",
    "cannot sponsor visa",
    "must have right to work",
    "no sponsorship",
    "no work permit",
    "cannot provide sponsorship",
    "not eligible for sponsorship"
]

YEAR_PATTERN = r"(\d+)\s*(\+|plus)?\s*(years?|yrs?)"
MIN_PATTERN = r"(minimum|at least)\s*(\d+)\s*(years?|yrs?)"


def requires_too_much_experience(text):
    text = text.lower()

    matches1 = re.findall(YEAR_PATTERN, text)
    matches2 = re.findall(MIN_PATTERN, text)

    # matches1 returns tuples like ('3', '', 'years')
    for match in matches1:
        years = int(match[0])
        if years >= EXPERIENCE_LIMIT:
            return True

    # matches2 returns tuples like ('minimum', '4', 'years')
    for match in matches2:
        years = int(match[1])
        if years >= EXPERIENCE_LIMIT:
            return True

    return False


def visa_not_available(text):
    text = text.lower()
    return any(phrase in text for phrase in VISA_BLOCK_PHRASES)


def should_keep_job(text):
    if requires_too_much_experience(text):
        return False
    if visa_not_available(text):
        return False
    return True
