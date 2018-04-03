# re_flags_dotall.py
import re

text = "This is some text -- with punctuation.\nA second line."
pattern = r".+"
no_newlines = re.compile(pattern)
dotall = re.compile(pattern, re.DOTALL)

print("Text:\n {!r}".format(text))
print("Pattern:\n {}".format(pattern))
print("No newline :")
for match in no_newlines.findall(text):
    print(" {!r}".format(match))
print("Dotall     :")
for match in dotall.findall(text):
    print(" {!r}".format(match))
