# 👋 HTML-Classes-Obfuscator 🔒

> CLI tool that obfuscates HTML classes:
>
> _Normal HTML file_ :

```html
<div class="card w-50">
  <div class="card-body">Hello World</div>
</div>
```

> _Obfuscated HTML file_ :

```html
<div class="oywdon tgmvkg">
  <div class=emnpzm>Hello World</div>
</div>
```

## 🚀 Usage

Via command line...

```bash
git clone git@github.com:xandermann/html-classes-obfuscator.git

cp html-classes-obfuscator/html_classes_obfuscator/html_classes_obfuscator.py ./YOUR_PROJECT

python3 html_classes_obfuscator.py --htmlpath="**/*.html" --csspath="**/*.css" --jspath="**/*.js"
```

...Or via a python script

```bash
# https://pypi.org/project/html-classes-obfuscator/
pip install html-classes-obfuscator
```

```python
import glob
import random
import string
from html_classes_obfuscator import html_classes_obfuscator

# [...]

htmlfiles = glob.glob("./**/*.html", recursive=True)
cssfiles = glob.glob("./**/*.css", recursive=True)
jsfiles = glob.glob("./**/*.js", recursive=True)

print(htmlfiles)
print(cssfiles)
print(jsfiles)

# Generate random string
def generate_class(current_classes_list):

    def random_class():
        # Offers (26*2)^6 random class name possibilities
        return ''.join(random.choice(string.ascii_letters) for i in range(6))

    res = random_class()

    while res in current_classes_list.values():
        res = random_class()

    return res

html_classes_obfuscator.html_classes_obfuscator(htmlfiles, cssfiles, jsfiles, generate_class)
```

---

## ⚠️️ Important notes

1. **Make a backup before use.**
2. DON'T use if you have duplicate class names in your css files.
3. If you modify the class generator, be sure that the generated name doesn’t begin with a number:

> In CSS, identifiers (including element names, classes, and IDs in selectors) can contain only the characters [a-zA-Z0-9] and ISO 10646 characters U+00A0 and higher, plus the hyphen (-) and the underscore (_); they cannot start with a digit, two hyphens, or a hyphen followed by a digit. Identifiers can also contain escaped characters and any ISO 10646 character as a numeric code (see next item). For instance, the identifier “B&W?” may be written as “B&W?” or “B\26 W\3F”.
> https://www.w3.org/TR/CSS21/syndata.html#characters

## ✅ Run tests

```python
python3 -m unittest tests/*.py
```

## 🤝 Contributing

Contributions, issues and feature requests are welcome.

Feel free to check issues page if you want to contribute.

Check the contributing guide.
