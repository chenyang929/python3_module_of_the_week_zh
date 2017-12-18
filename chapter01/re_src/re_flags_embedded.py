# re_flags_embedded.py
import re

text = "This is some text -- with punctuation."
pattern = r"(?i)\bT\w+"
regex = re.compile(pattern)

print("Text    :", text)
print("Pattern :", pattern)
print("Matches :", regex.findall(text))
