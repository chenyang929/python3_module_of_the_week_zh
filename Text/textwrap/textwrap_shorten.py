# textwrap_shorten.py
import textwrap
from textwrap_example import sample_text

dedented_text = textwrap.dedent(sample_text)
original = textwrap.fill(dedented_text, width=50)

print("Original:\n")
print(original)

shortened = textwrap.shorten(original, 100)
shortened_wrapped = textwrap.fill(shortened, width=50)
print("\nShortened:\n")
print(shortened_wrapped)