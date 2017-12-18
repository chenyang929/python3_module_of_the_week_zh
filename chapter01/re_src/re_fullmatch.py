# re_fullmatch.py
import re

text = "This is some text -- with punctuation."
pattern = "is"

text1 = "python"
pattern1 = "python"
print("Text       :", text)
print("Pattern    :", pattern)

m = re.search(pattern, text)
print("Search     :", m)
s = re.fullmatch(pattern, text)
print("Full match :", s)
s1 = re.fullmatch(pattern1, text1)
print("Full match1:", s1)