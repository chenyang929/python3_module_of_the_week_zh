# re_test_patterns_groups.py
import re

def test_patterns(text, patterns):
    """
    给定源文本和模式列表，在文本中查找每个模式的匹配，
    并将它们打印到stdout
    """
    # 在文本中查找每个模式并打印结果
    for pattern, desc in patterns:
        print("{!r}({})\n".format(pattern, desc))
        print("{!r}".format(text))
        for match in re.finditer(pattern, text):
            s = match.start()
            e = match.end()
            prefix = " " * (s)
            print("{}{!r}{}".format(prefix, text[s:e], " " * (len(text) - e)), end=" ",)
            print(match.groups())
            if match.groupdict():
                print("{}{}".format(" " * (len(text) - s), match.groupdict()))
        print()
    return
            