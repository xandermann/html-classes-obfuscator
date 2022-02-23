import glob
import shutil
import tempfile
import unittest

from html_classes_obfuscator import html_classes_obfuscator


class TestHtmlClassesObfuscator(unittest.TestCase):

    TMP_FOLDER = tempfile.mkdtemp()

    @classmethod
    def setUpClass(cls) -> None:
        # TODO : add for multiples test folders
        shutil.copytree('./tests/tests_1', cls.TMP_FOLDER + "/tests_1")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.TMP_FOLDER)

    def test_html_classes_obfuscator(self) -> None:
        htmlfiles = glob.glob(TestHtmlClassesObfuscator.TMP_FOLDER + "/tests_1/index.html", recursive=True)
        cssfiles = glob.glob(TestHtmlClassesObfuscator.TMP_FOLDER + "/tests_1/style.css", recursive=True)
        jsfiles = glob.glob(TestHtmlClassesObfuscator.TMP_FOLDER + "/tests_1/script.js", recursive=True)

        TestHtmlClassesObfuscator.counter = 0
        def generateclass(current_classes_list):
            TestHtmlClassesObfuscator.counter += 1
            return "test_" + str(TestHtmlClassesObfuscator.counter)

        html_classes_obfuscator.html_classes_obfuscator(htmlfiles, cssfiles, jsfiles, generateclass)

        # ASSERTS

        asserthtmlfiles = glob.glob(TestHtmlClassesObfuscator.TMP_FOLDER + "/**/expected_index.html", recursive=True)

        for i, htmlfile in enumerate(htmlfiles):
            html = open(htmlfile, 'r')
            asserthtml = open(asserthtmlfiles[i], 'r')

            self.assertEqual(asserthtml.readlines(), html.readlines())

            html.close()
            asserthtml.close()

        assertcssfiles = glob.glob(TestHtmlClassesObfuscator.TMP_FOLDER + "/**/expected_style.css", recursive=True)

        for i, cssfile in enumerate(cssfiles):
            css = open(cssfile, 'r')
            assertcss = open(assertcssfiles[i], 'r')

            self.assertEqual(assertcss.readlines(), css.readlines())

            css.close()
            assertcss.close()

        assertjsfiles = glob.glob(TestHtmlClassesObfuscator.TMP_FOLDER + "/**/expected_script.js", recursive=True)

        for i, jsfile in enumerate(jsfiles):
            js = open(jsfile, 'r')
            assertjs = open(assertjsfiles[i], 'r')

            self.assertEqual(assertjs.readlines(), js.readlines())

            js.close()
            assertjs.close()

if __name__ == '__main__':
    unittest.main()
