# re_test_patterns.py
import re

def test_patterns(text, patterns):
    """
    给定源文本和模式列表，在文本中查找每个模式的匹配，
    并将它们打印到stdout
    """
    for pattern, desc in patterns:
        print("'{}' ({})\n".format(pattern, desc))
        print("'{}'".format(text))
        for match in re.finditer(pattern, text):
            s = match.start()
            e = match.end()
            substr = text[s:e]
            n_backslashes = text[:s].count("\\")
            prefix = "." * (s + n_backslashes)
            print("{}'{}'".format(prefix, substr))
        print()
    return

if __name__ == "__main__":
    test_patterns("abbaaabbbbaaaaa", [("ab", "'a' followed by 'b'")])