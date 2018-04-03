# re_sub_named_groups.py
import re

bold = re.compile(r'\*{2}(?P<bold_text>.*?)\*{2}')

text = 'Make this **bold**.  This **too**.'

print('Text:', text)
print('Bold:', bold.sub(r'<b>\g<bold_text></b>', text))