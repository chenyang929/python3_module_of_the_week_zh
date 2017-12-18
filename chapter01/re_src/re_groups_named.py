# re_groups_named.py
import re

text = "This is some text -- with punctuation."

print(text)
print()

patterns = [
    r"^(?P<first_word>\w+)",
    r"(?P<last_word>\w+\S*$)",
    r"(?P<t_word>\bt\w+)(?P<other_word>\w+)",
    r"(?P<ends_with_t>\w+t)\b"
]

for pattern in patterns:
    regex = re.compile(pattern)
    match = regex.search(text)
    print("'{}'".format(pattern))
    print(" ", match.groups())
    print(" ", match.groupdict())
    print()