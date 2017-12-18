# re_charset_exclude.py
from re_test_patterns import test_patterns

test_patterns(
    "This is some text -- with punctuation",
    [("[^-. ]+", "sequences without -, ., or space")]
)