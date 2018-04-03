# re_split_groups.py
import re

text = '''Paragraph one
on two lines.

Paragraph two.


Paragraph three.'''

print('With split:')
for num, para in enumerate(re.split(r'(\n{2,})', text)):
    print(num, repr(para))
    print()