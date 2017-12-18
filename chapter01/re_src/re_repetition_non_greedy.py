# re_repetition_non_greedy.py
from re_test_patterns import test_patterns

test_patterns(
    "abbaabbba",
    [("ab*?", "a followed by zero or more b"),
     ("ab+?", "a followed by one or more b"),
     ("ab??", "a followed by zero or one b"),
     ("ab{3}?", "a follows by three b"),
     ("ab{2,3}?", "a followed by two to three b")]
)