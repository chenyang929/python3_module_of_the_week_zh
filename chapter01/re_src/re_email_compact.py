# re_email_compact.py
import re

address = re.compile("[\w\d.+-]+@([\w\d.]+\.)+(com|org|edu)")

candidates = [
    u"first.last@example.com",
    u"first.last+category@gmail.com",
    u"valid-address@mail.example.com",
    u"not-valid@example.foo",
]

for candidate in candidates:
    match = address.search(candidate)
    print("{:<30} {}".format(candidate, "Matches" if match else "No match"))
    