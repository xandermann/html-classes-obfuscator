"""Obsucate HTML"""

import glob
import random
import re
import string
import sys
import uuid
from typing import Callable, Dict, Tuple


def parse_html_class_names(old_html: string,
                           equivalents_obfuscated_html_classes: Dict,
                           class_generator: Callable[[Dict],
                                                     str]) -> Tuple:
    """Parse HTML class names

    Args:
        old_html (string): HTML we want to parse
        equivalents_obfuscated_html_classes (Dict): Dict<HTMLClasses, ObfuscatedHTMLClasses>
        class_generator (Callable[[Dict], str]): function to generate the HTML classes

    Returns:
        Tuple: _description_
    """

    # Regex to fetch HTML classes in the file
    html_class_regex = r"class=[\"\']?((?:.(?![\"\']?\s+(?:\S+)=|\s*\/?[>\"\']))+.)[\"\']?"

    # classes_groups can be ['navbar p-5', 'navbar-brand', 'navbar-item',
    # 'title is-4']
    classes_groups = re.findall(html_class_regex, old_html)
    obfuscate_classes_groups = []

    for i, classes in enumerate(classes_groups):
        div_of_classes = classes.split()
        obfuscate_classes_groups.append([])

        for old_class_name in div_of_classes:
            if old_class_name not in equivalents_obfuscated_html_classes:
                equivalents_obfuscated_html_classes[old_class_name] = class_generator(
                    equivalents_obfuscated_html_classes)
            obfuscate_classes_groups[i].append(
                equivalents_obfuscated_html_classes[old_class_name])

    for i, classes in enumerate(obfuscate_classes_groups):
        obfuscate_classes_groups[i] = " ".join(classes)

    return (
        classes_groups,
        obfuscate_classes_groups,
        equivalents_obfuscated_html_classes)


def generate_html(
        html_content: str = "",
        classes_groups: Dict = (),
        obfuscate_classes_groups: Dict = ()) -> str:
    """Generate the obfuscated HTML

    Args:
        html_content (str, optional): HTML content before obfuscation. Defaults to "".
        classes_groups (Dict, optional): Class groups, like ["navbar", "btn btn-primary"]. Defaults to ().
        obfuscate_classes_groups (Dict, optional): _description_. Defaults to ().

    Returns:
        str: Obfuscated HTML
    """

    for i, classes_group in enumerate(classes_groups):

        old_no_quote = "class=" + classes_group
        old_with_simple_quote = "class='" + classes_group + "'"
        old_with_double_quote = 'class="' + classes_group + '"'

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
        html_content = html_content.replace(old_with_simple_quote, replace_by)
        html_content = html_content.replace(old_with_double_quote, replace_by)

    return html_content


def generate_css(css_content: str = "", equivalent_class: Dict = ()) -> str:
    """Generate the obfuscated CSS

    Args:
        css_content (str, optional): CSS before obfuscation. Defaults to "".
        equivalent_class (Dict, optional): Dictionnary of new class names. Defaults to ().

    Returns:
        str: Obfuscated CSS
    """

    # We sort by the key length ; to first replace long classes names and after short one
    # ".navbar-brand", and then ".navbar" avoid "RENAMED_CLASS-brand" and "RENAMED_CLASS" bug
    for old_class_name in sorted(equivalent_class, key=len, reverse=True):
        new_class_name = equivalent_class[old_class_name]

        # CSS classes modifications
        # Example: a class like "lg:1/4" should be "lg\:1\/4" in CSS
        old_class_name = old_class_name.replace(":", "\\:")
        old_class_name = old_class_name.replace("/", "\\/")
        old_class_name = old_class_name.replace("[", "\\[")
        old_class_name = old_class_name.replace("]", "\\]")
        old_class_name = old_class_name.replace("%", "\\%")

        css_content = css_content.replace(
            "." + old_class_name, "." + new_class_name)
    return css_content


def generate_js(js_content: str = "", equivalent_class: Dict = ()) -> str:
    """Generate the obfuscated JS

    Args:
        js_content (str, optional): JS before obfuscation. Defaults to "".
        equivalent_class (Dict, optional): Dictionnary of new class names. Defaults to ().

    Returns:
        str: Obfuscated JS
    """

    # We sort by the key length ; to first replace long classes names and after short one
    # ".navbar-brand", and then ".navbar" avoid "RENAMED_CLASS-brand" and "RENAMED_CLASS" bug
    for old_class_name in sorted(equivalent_class, key=len, reverse=True):
        new_class_name = equivalent_class[old_class_name]

        # JS modifications
        # document.querySelectorAll(".navbar-burger")
        # myDiv.classList.toggle("is-active")
        js_content = js_content.replace(
            '.querySelector(".' + old_class_name + '")',
            '.querySelector(".' + new_class_name + '")')
        js_content = js_content.replace(
            '.querySelectorAll(".' + old_class_name + '")',
            '.querySelectorAll(".' + new_class_name + '")')
        js_content = js_content.replace(
            '.classList.toggle("' + old_class_name + '")',
            '.classList.toggle("' + new_class_name + '")')

    return js_content


def html_classes_obfuscator(htmlfiles=(), cssfiles=(), jsfiles=(), class_generator: Callable[[
                            Dict], str] = lambda _: "_" + str(uuid.uuid4())):
    """MAIN

    Args:
        htmlfiles (tuple, optional): HTML files path. Defaults to ().
        cssfiles (tuple, optional): CSS files path. Defaults to ().
        jsfiles (tuple, optional): JS files path. Defaults to ().
        class_generator (_type_, optional): A function which generates obsucated classes.
    """

    # Dict<HTMLClasses, ObfuscatedHTMLClasses>
    equivalents_obfuscated_html_classes = {}

    # HTML FILES GENERATION : Fetch HTML classes and rename them
    for htmlfile in htmlfiles:

        with open(htmlfile, "r+", encoding="utf-8") as file:
            old_html = file.read()

            # Fetch and parse the HTML file
            (
                classes_groups,
                obfuscate_classes_groups,
                equivalents_obfuscated_html_classes) = parse_html_class_names(
                old_html,
                equivalents_obfuscated_html_classes,
                class_generator)

            # obfuscate_classes_groups :
            # Shoud be [['test_1', 'test_2'], ['test_3'], ['test_4'],
            # ['test_5', 'test_6']]

            # --------------------------------------------------

            new_html = generate_html(
                old_html, classes_groups, obfuscate_classes_groups)

            file.seek(0)
            file.write(new_html)
            file.truncate()

    # CSS FILES GENERATION
    for cssfile in cssfiles:

        with open(cssfile, "r+", encoding="utf-8") as file:

            old_css = file.read()
            new_css = generate_css(
                old_css, equivalents_obfuscated_html_classes)

            file.seek(0)
            file.write(new_css)
            file.truncate()

    # JS FILES GENERATION
    for jsfile in jsfiles:

        with open(jsfile, "r+", encoding="utf-8") as file:
            old_js = file.read()
            new_js = generate_js(
                old_js, equivalents_obfuscated_html_classes)

            file.seek(0)
            file.write(new_js)
            file.truncate()


def get_files() -> Dict:
    """Get the source files

    Returns:
        Dict: Dict of the source files
    """
    return {
        "htmlfiles": glob.glob(flags_command_line['htmlpath'], recursive=True),
        "cssfiles": glob.glob(flags_command_line['csspath'], recursive=True),
        "jsfiles": glob.glob(flags_command_line['jspath'], recursive=True),
    }


if __name__ == '__main__':
    flags_command_line = dict(
        map(lambda x: x.lstrip('-').split('='), sys.argv[1:]))

    files = get_files()

    print()
    print("HTML files are: " + str(files["htmlfiles"]))
    print("CSS files are: " + str(files["cssfiles"]))
    print("JS files are: " + str(files["jsfiles"]))
    print()

    # Generate random string
    def generate_class(current_classes_list) -> str:
        """Generate random class string

        Args:
            current_classes_list (_type_): _description_
        """

        def random_class():
            # Offers (26*2)^6 random class name possibilities
            return ''.join(random.choice(string.ascii_letters)
                           for i in range(6))

        res = random_class()

        while res in current_classes_list.values():
            res = random_class()

        return res

    html_classes_obfuscator(
        files["htmlfiles"],
        files["cssfiles"],
        files["jsfiles"],
        generate_class)
