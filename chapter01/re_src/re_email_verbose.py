# re_email_verbose.py
import re

address = re.compile(
    '''
    [\w\d.+-]      # username
    @
    ([\w\d.+\.])+  # domain name prefix
    (com|org|edu)  # TODO: support more top-level domains
    ''',
    re.VERBOSE

)

candidates = [
    u"first.last@example.com",
    u"first.last+category@gmail.com",
    u"valid-address@mail.example.com",
    u"not-valid@example.foo",
]

for candidate in candidates:
    match = address.search(candidate)
    print("{:<30} {}".format(candidate, "Matches" if match else "No match"),)