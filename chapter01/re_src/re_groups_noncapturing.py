# re_groups_noncapturing.py

from re_test_patterns_groups import test_patterns

test_patterns("abbaabbba",
              [(r"a((a+)|(b+))", "capturing form"),
               (r"a((?:a+)|(?:b+))", "noncapturing")])