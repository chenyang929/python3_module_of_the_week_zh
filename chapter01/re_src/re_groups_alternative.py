# re_groups_alternative.py

from re_test_patterns_groups import test_patterns

test_patterns("abbaabbba", [(r"a((a+)|(b+))", "a then seq. of a or ser. of b"),
(r"a((a|b)+)", "a then seq. of [ab]")])