# 👋 HTML-Classes-Obfuscator 🔒

> CLI that obfuscate HTML classes:
>
> _Normal HTML file_ :

```html
<div class="content">
  <div class="text">Hello World</div>
</div>
```

> _Obfuscated HTML file_ :

```html
<div class="oywdon">
  <div class="emnpzm">Hello World</div>
</div>
```

## 🚀 Usage

Using by command line

```bash
git clone git@github.com:xandermann/html-classes-obfuscator.git

cp html-classes-obfuscator/html_classes_obfuscator/html_classes_obfuscator.py ./YOUR_PROJECT

python3 html_classes_obfuscator.py --htmlpath="**/*.html" --csspath="**/*.css" --jspath="**/*.js"
```

Or using in python script

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

## ✅ Run tests

```python
python3 -m unittest tests/*.py
```

## 🤝 Contributing

Contributions, issues and feature requests are welcome.

Feel free to check issues page if you want to contribute.

Check the contributing guide.
