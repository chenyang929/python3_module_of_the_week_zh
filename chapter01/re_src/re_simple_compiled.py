# re_simple_compiled.py
import re

# 预编译模式
regexes = [re.compile(p) for p in ["this", "that"]]
text = "Does this text match the pattern?"

print("Text: {!r}\n".format(text))

for regex in regexes:
    print("Seeking '{}' ->".format(regex.pattern), end=" ")
    if regex.search(text):
        print("match!")
    else:
        print("no match")
