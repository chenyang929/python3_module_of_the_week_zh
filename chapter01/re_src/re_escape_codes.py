# re_escape_codes.py
from re_test_patterns import test_patterns

test_patterns(
    "A prime #1 example!",
    [(r"\d+", "sequence of digits"),
     (r"\D+", "sequence of non-digits"),
     (r"\s+", "sequence of whitespace"),
     (r"\S+", "sequence of non-whitespace"),
     (r"\w+", "alphanumeric characters"),
     (r"\W", "non-alphanumeric")]
)