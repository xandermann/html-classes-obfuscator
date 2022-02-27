import codecs as _
import os

from setuptools import find_packages, setup

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.5'

# Setting up
setup(
    name="html_classes_obfuscator",
    url="https://github.com/xandermann/html-classes-obfuscator",
    version=VERSION,
    author="xandermann (Alexandre Hublau)",
    author_email="<contact@alexandre-hublau.com>",
    description= 'Obfuscate class names in HTML, CSS and Javascript files.',
    long_description_content_type="text/markdown",
    long_description=open(os.path.join(THIS_DIR, "README.md"), "r").read(),
    packages=find_packages(),
    install_requires=[],
    keywords=['html', 'obfuscator'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
