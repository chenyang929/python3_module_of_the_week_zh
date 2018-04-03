# re_flags_ascii.py
import re

text = u"Français złoty Österreich"
pattern = r"\w+"
ascii_pattern = re.compile(pattern, re.ASCII)
unicode_pattern = re.compile(pattern)

print("Text    :", text)
print("Pattern :", pattern)
print("ASCII   :", list(ascii_pattern.findall(text)))
print("Unicode :", list(unicode_pattern.findall(text)))
