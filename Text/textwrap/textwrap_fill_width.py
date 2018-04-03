# textwrap_fill_width.py
import textwrap
from textwrap_example import sample_text

dedented_text = textwrap.dedent(sample_text).strip()
for width in [45, 60]:
    print("{} Columns:\n".format(width))
    print(textwrap.fill(dedented_text, width=width))
    print()