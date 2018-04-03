# string_template.py
import string

values = {"var": "foo"}

t = string.Template("""
Variable         : $var
Escape           : $$
Variable in text : ${var}iable
""")
print("TEMPLATE:", t.substitute(values))

s = """
Variable         : %(var)s
Escape           : %%
Variable in text : %(var)siable
"""
print("INTERPOLATION:", s % values)

p = """
Variable         : {var}
Escape           : {{}}
Variable in text : {var}iable
"""
print("FORMAT:", p.format(**values))
