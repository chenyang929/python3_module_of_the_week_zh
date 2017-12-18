# re_flags_ignorecase.py
import re

text = "This is some text -- with punctuation."
pattern = r"\bT\w+"
with_case = re.compile(pattern)
without_case = re.compile(pattern, re.IGNORECASE)

print("Text:\n {!r}".format(text))
print("Pattern:\n {}".format(pattern))
print("Case-sensitive:")
for match in with_case.findall(text):
    print(" {!r}".format(match))
print("Case-insensitive:")
for match in without_case.findall(text):
    print(" {!r}".format(match))