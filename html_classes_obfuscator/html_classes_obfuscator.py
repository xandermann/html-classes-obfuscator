import glob
import random
import re
import string
import sys
import uuid
from typing import Callable, Dict


def html_classes_obfuscator(htmlfiles = [], cssfiles = [], jsfiles = [], generate_class : Callable[[Dict], str] = lambda current_classes_list : "_" + str(uuid.uuid4())):

    # Dict<HTMLClasses, ObfuscatedHTMLClasses>
    equivalents_HTMLClasses_ObfuscatedHTMLClasses = {}

    # Regex to fetch HTML classes in the file
    html_class_regex = "class=[\"\']?((?:.(?![\"\']?\s+(?:\S+)=|\s*\/?[>\"\']))+.)[\"\']?"

    # Fetch HTML classes and rename them
    for htmlfile in htmlfiles:

        with open(htmlfile, "r+") as f:
            file_content = f.read()

            # classes_groups can be ['navbar p-5', 'navbar-brand', 'navbar-item', 'title is-4']
            classes_groups = re.findall(html_class_regex, file_content)
            obfuscate_classes_groups = []

            for i, classes in enumerate(classes_groups):
                div_of_classes = classes.split()
                obfuscate_classes_groups.append([])

                for old_class_name in div_of_classes:
                    if not old_class_name in equivalents_HTMLClasses_ObfuscatedHTMLClasses:
                        equivalents_HTMLClasses_ObfuscatedHTMLClasses[old_class_name] = generate_class(equivalents_HTMLClasses_ObfuscatedHTMLClasses)
                    obfuscate_classes_groups[i].append(equivalents_HTMLClasses_ObfuscatedHTMLClasses[old_class_name])

            for i, classes in enumerate(obfuscate_classes_groups):
                obfuscate_classes_groups[i] = " ".join(classes)

            # obfuscate_classes_groups :
            # Shoud be [['test_1', 'test_2'], ['test_3'], ['test_4'], ['test_5', 'test_6']] at the end

            # --------------------------------------------------

            for i, classes in enumerate(classes_groups):

                old_no_quote = "class=" + classes_groups[i]
                old_with_quote = 'class="' + classes_groups[i] + '"'
                replace_by = 'class=' + obfuscate_classes_groups[i] + ''

                # Replace like : class=navbar-item by class="{{ obfuscate_classes_groups }}"
                # Or replace like : class="navbar p-5" (with quote this time)
                file_content = file_content.replace(old_no_quote, replace_by)
                file_content = file_content.replace(old_with_quote, replace_by)

            f.seek(0)
            f.write(file_content)
            f.truncate()

    # CSS FILES GENERATION
    for cssfile in cssfiles:

        with open(cssfile, "r+") as f:
            file_content = f.read()

            # We sort by the key length ; to first replace long classes names and after short one
            # ".navbar-brand", and then ".navbar" avoid "RENAMED_CLASS-brand" and "RENAMED_CLASS" bug
            for old_class_name in sorted(equivalents_HTMLClasses_ObfuscatedHTMLClasses, key=len, reverse=True):
                new_class_name = equivalents_HTMLClasses_ObfuscatedHTMLClasses[old_class_name]

                # CSS classes modifications
                # Example: a class like "lg:1/4" should be "lg\:1\/4" in CSS
                old_class_name = old_class_name.replace(":", "\\:")
                old_class_name = old_class_name.replace("/", "\\/")

                file_content = file_content.replace("." + old_class_name, "." + new_class_name)

            f.seek(0)
            f.write(file_content)
            f.truncate()

    # JS FILES GENERATION
    for jsfile in jsfiles:

        with open(jsfile, "r+") as f:
            file_content = f.read()

            # We sort by the key length ; to first replace long classes names and after short one
            # ".navbar-brand", and then ".navbar" avoid "RENAMED_CLASS-brand" and "RENAMED_CLASS" bug
            for old_class_name in sorted(equivalents_HTMLClasses_ObfuscatedHTMLClasses, key=len, reverse=True):
                new_class_name = equivalents_HTMLClasses_ObfuscatedHTMLClasses[old_class_name]

                # JS modifications
                # document.querySelectorAll(".navbar-burger")
                # myDiv.classList.toggle("is-active")

                file_content = file_content.replace('.querySelector(".' + old_class_name + '")', '.querySelector(".' + new_class_name + '")')
                file_content = file_content.replace('.querySelectorAll(".' + old_class_name + '")', '.querySelectorAll(".' + new_class_name + '")')
                file_content = file_content.replace('.classList.toggle("' + old_class_name + '")', '.classList.toggle("' + new_class_name + '")')

            f.seek(0)
            f.write(file_content)
            f.truncate()


if __name__ == '__main__':
    flags_command_line = dict(map(lambda x: x.lstrip('-').split('='),sys.argv[1:]))

    htmlfiles = glob.glob(flags_command_line['htmlpath'], recursive=True)
    cssfiles = glob.glob(flags_command_line['csspath'], recursive=True)
    jsfiles = glob.glob(flags_command_line['jspath'], recursive=True)

    print()
    print("HTML files are:" + str(htmlfiles))
    print("CSS files are:" + str(cssfiles))
    print("JS files are:" + str(jsfiles))
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

    html_classes_obfuscator(htmlfiles, cssfiles, jsfiles, generate_class)

