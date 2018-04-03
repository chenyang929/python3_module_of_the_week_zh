# re_negative_look_behind.py
import re

address = re.compile(
    '''
    ^

    # An address: username@domain.tld

    [\w\d.+-]+       # username

    # Ignore noreply addresses
    (?<!noreply)

    @
    ([\w\d.]+\.)+    # domain name prefix
    (com|org|edu)    # limit the allowed top-level domains

    $
    ''',
    re.VERBOSE)

candidates = [
    u'first.last@example.com',
    u'noreply@example.com',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print('  Match:', candidate[match.start():match.end()])
    else:
        print('  No match')