# re_groups.py
from re_test_patterns import test_patterns

test_patterns(
    "abbaaabbbbaaaaa",
    [("a(ab)", "a followed by literal ab"),
     ("a(a*b*)", "a followed by 0-n a and 0-n b"),
     ("a(ab)*", "a followed by 0-n ab"),
     ("a(ab)+", "a followed by 1-n ab")]
)