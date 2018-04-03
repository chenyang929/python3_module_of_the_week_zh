# string_template_newsyntax.py
import re
import string

class MyTemplate(string.Template):
    delimiter = "{{"
    pattern = r"""
    \{\{(?:
    (?P<escaped>\{\{)|
    (?P<named>[_a-z][_a-z0-9]*)\}\}|
    (?P<braced>[_a-z][_a-z0-9]*)\}\}|
    (?P<invalid>)
    )
    """
t = MyTemplate("""
{{{{
{{var}}
""")
print("MATCHES:", t.pattern.findall(t.template))
print("SUBSTITUTED:", t.safe_substitute(var="replacement"))