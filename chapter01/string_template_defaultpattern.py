# string_template_defaultpattern.py
import string

t = string.Template("$var")
print(t.pattern.pattern)