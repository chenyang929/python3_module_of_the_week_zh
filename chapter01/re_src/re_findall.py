# re_findall.py
import re

text = "abbaaabbbbaaaaa"
pattern = "ab"

for match in re.findall(pattern, text):
    print("Found {!r}".format(match))