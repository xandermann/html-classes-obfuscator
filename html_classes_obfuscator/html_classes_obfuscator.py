import glob
import random
import re
import string
import sys
import uuid
from typing import Callable, Dict, Tuple


def parse_html_class_names(old_html, equivalents_HTMLClasses_ObfuscatedHTMLClasses, class_generator: Callable[[Dict], str]) -> Tuple:
    # Regex to fetch HTML classes in the file
    html_class_regex = r"class=[\"\']?((?:.(?![\"\']?\s+(?:\S+)=|\s*\/?[>\"\']))+.)[\"\']?"

    # equivalents_HTMLClasses_ObfuscatedHTMLClasses = {}

    # classes_groups can be ['navbar p-5', 'navbar-brand', 'navbar-item', 'title is-4']
    classes_groups = re.findall(html_class_regex, old_html)
    obfuscate_classes_groups = []

    for i, classes in enumerate(classes_groups):
        div_of_classes = classes.split()
        obfuscate_classes_groups.append([])

        for old_class_name in div_of_classes:
            if old_class_name not in equivalents_HTMLClasses_ObfuscatedHTMLClasses:
                equivalents_HTMLClasses_ObfuscatedHTMLClasses[old_class_name] = class_generator(equivalents_HTMLClasses_ObfuscatedHTMLClasses)
            obfuscate_classes_groups[i].append(equivalents_HTMLClasses_ObfuscatedHTMLClasses[old_class_name])

    for i, classes in enumerate(obfuscate_classes_groups):
        obfuscate_classes_groups[i] = " ".join(classes)

    return (classes_groups, obfuscate_classes_groups, equivalents_HTMLClasses_ObfuscatedHTMLClasses)

def generate_html(html_content: str = "", classes_groups: Dict = (), obfuscate_classes_groups: Dict = ()) -> str:
    for i, classes in enumerate(classes_groups):

            old_no_quote = "class=" + classes_groups[i]
            old_with_quote = 'class="' + classes_groups[i] + '"'

            # Check if we need to generate quotes or not for the attributes
            # class=test_1
            # class="test_1 test_2"
            if len(obfuscate_classes_groups[i].split()) > 1:
                replace_by = 'class="' + obfuscate_classes_groups[i] + '"'
            else:
                replace_by = 'class=' + obfuscate_classes_groups[i] + ''

            # Replace like : class=navbar-item by class="{{ obfuscate_classes_groups }}"
            # Or replace like : class="navbar p-5" (with quote this time)
            html_content = html_content.replace(old_no_quote, replace_by)
            html_content = html_content.replace(old_with_quote, replace_by)

    return html_content

def generate_css(css_content: str = "", equivalent_class: Dict = ()) -> str:
    # We sort by the key length ; to first replace long classes names and after short one
    # ".navbar-brand", and then ".navbar" avoid "RENAMED_CLASS-brand" and "RENAMED_CLASS" bug
    for old_class_name in sorted(equivalent_class, key=len, reverse=True):
        new_class_name = equivalent_class[old_class_name]

        # CSS classes modifications
        # Example: a class like "lg:1/4" should be "lg\:1\/4" in CSS
        old_class_name = old_class_name.replace(":", "\\:")
        old_class_name = old_class_name.replace("/", "\\/")

        css_content = css_content.replace("." + old_class_name, "." + new_class_name)
    return css_content

def generate_js(js_content: str = "", equivalent_class: Dict = ()) -> str:
    # We sort by the key length ; to first replace long classes names and after short one
    # ".navbar-brand", and then ".navbar" avoid "RENAMED_CLASS-brand" and "RENAMED_CLASS" bug
    for old_class_name in sorted(equivalent_class, key=len, reverse=True):
        new_class_name = equivalent_class[old_class_name]

        # JS modifications
        # document.querySelectorAll(".navbar-burger")
        # myDiv.classList.toggle("is-active")
        js_content = js_content.replace('.querySelector(".' + old_class_name + '")', '.querySelector(".' + new_class_name + '")')
        js_content = js_content.replace('.querySelectorAll(".' + old_class_name + '")', '.querySelectorAll(".' + new_class_name + '")')
        js_content = js_content.replace('.classList.toggle("' + old_class_name + '")', '.classList.toggle("' + new_class_name + '")')

    return js_content


def html_classes_obfuscator(htmlfiles = (), cssfiles = (), jsfiles = (), class_generator : Callable[[Dict], str] = lambda current_classes_list : "_" + str(uuid.uuid4())):

    # # Dict<HTMLClasses, ObfuscatedHTMLClasses>
    equivalents_HTMLClasses_ObfuscatedHTMLClasses = {}

    # HTML FILES GENERATION : Fetch HTML classes and rename them
    for htmlfile in htmlfiles:

        with open(htmlfile, "r+") as f:
            old_html = f.read()

            # Fetch and parse the HTML file
            (classes_groups, obfuscate_classes_groups, equivalents_HTMLClasses_ObfuscatedHTMLClasses) = parse_html_class_names(old_html, equivalents_HTMLClasses_ObfuscatedHTMLClasses, class_generator)

            # obfuscate_classes_groups :
            # Shoud be [['test_1', 'test_2'], ['test_3'], ['test_4'], ['test_5', 'test_6']]

            # --------------------------------------------------

            new_html = generate_html(old_html, classes_groups, obfuscate_classes_groups)

            f.seek(0)
            f.write(new_html)
            f.truncate()

    # CSS FILES GENERATION
    for cssfile in cssfiles:

        with open(cssfile, "r+") as f:

            old_css = f.read()
            new_css = generate_css(old_css, equivalents_HTMLClasses_ObfuscatedHTMLClasses)

            f.seek(0)
            f.write(new_css)
            f.truncate()

    # JS FILES GENERATION
    for jsfile in jsfiles:

        with open(jsfile, "r+") as f:
            old_js = f.read()
            new_js = generate_js(old_js, equivalents_HTMLClasses_ObfuscatedHTMLClasses)

            f.seek(0)
            f.write(new_js)
            f.truncate()


def get_files():
    return {
        "htmlfiles": glob.glob(flags_command_line['htmlpath'], recursive=True),
        "cssfiles": glob.glob(flags_command_line['csspath'], recursive=True),
        "jsfiles": glob.glob(flags_command_line['jspath'], recursive=True),
    }


if __name__ == '__main__':
    flags_command_line = dict(map(lambda x: x.lstrip('-').split('='),sys.argv[1:]))

    files = get_files()

    print()
    print("HTML files are: " + str(files["htmlfiles"]))
    print("CSS files are: " + str(files["cssfiles"]))
    print("JS files are: " + str(files["jsfiles"]))
    print()

    # Generate random string
    def generate_class(current_classes_list):

        def random_class():
            # Offers (26*2)^6 random class name possibilities
            return ''.join(random.choice(string.ascii_letters) for i in range(6))

        res = random_class()

        while res in current_classes_list.values():
            res = random_class()

        return res

    html_classes_obfuscator(files["htmlfiles"], files["cssfiles"], files["jsfiles"], generate_class)
