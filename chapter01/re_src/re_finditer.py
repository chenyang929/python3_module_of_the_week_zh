# re_finditer.py
import re

text = "abbaaabbbbaaaaa"
pattern = "ab"

for match in re.finditer(pattern, text):
    print("match:", match)
    s = match.start()
    e = match.end()
    print("Found {!r} at {:d}:{:d}".format(text[s:e], s, e))