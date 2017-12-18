# re_escape_escapes.py
from re_test_patterns import test_patterns

test_patterns(
    r"\d+ \D+ \s+",
    [(r"\\.\+", "escape code")]
)