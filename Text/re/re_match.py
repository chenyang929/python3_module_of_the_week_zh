# re_match.py
import re

text = "This is some text -- with punctuation."
pattern = "is"

print("Text   :", text)
print("Pattern:", pattern)

m = re.match(pattern, text)
print("Match  :", m)
s = re.search(pattern, text)
print("Search :", s)