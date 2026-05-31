from unittest import TestCase

from oop_spells.helpers import *


class TestHelpers(TestCase):
    def test_format_column_line(self):
        self.assertEqual(format_column_line(["first", "second"], 10),
                         "| first      | second     |")
        self.assertEqual(format_column_line(["first", "second", "third"], 10),
                         "| first      | second     | third      |")
        self.assertEqual(format_column_line(["first", "second", "third"], 15),
                         "| first           | second          | third           |")
        self.assertEqual(format_column_line(["first", "second", "third"], 3),
                         "| fir | sec | thi |")

    def test_can_be_int(self):
        self.assertEqual(can_be_int("1"), True)
        self.assertEqual(can_be_int("0"), True)
        self.assertEqual(can_be_int("-1"), True)
        self.assertEqual(can_be_int("999"), True)
        self.assertEqual(can_be_int("e"), False)
        self.assertEqual(can_be_int(""), False)

    def test_can_be_float(self):
        self.assertEqual(can_be_float("1"), True)
        self.assertEqual(can_be_float("0"), True)
        self.assertEqual(can_be_float("-1"), True)
        self.assertEqual(can_be_float("999"), True)
        self.assertEqual(can_be_float("2.5"), True)
        self.assertEqual(can_be_float("-4.98"), True)
        self.assertEqual(can_be_float("e"), False)
        self.assertEqual(can_be_float(""), False)

    def test_is_valid_file_name(self):
        self.assertEqual(is_valid_file_name("file"), True)
        self.assertEqual(is_valid_file_name("F1le$"), True)
        self.assertEqual(is_valid_file_name("    File    e"), True)
        self.assertEqual(is_valid_file_name(" file"), True)
        self.assertEqual(is_valid_file_name("file "), False)
        self.assertEqual(is_valid_file_name("file."), False)
        self.assertEqual(is_valid_file_name("f/le"), False)
        self.assertEqual(is_valid_file_name("f?le"), False)
        self.assertEqual(is_valid_file_name("f:le"), False)
        self.assertEqual(is_valid_file_name("CON"), False)
        self.assertEqual(is_valid_file_name("COM3"), False)

    def test_written_list(self):
        self.assertEqual(written_list([3]), "3")
        self.assertEqual(written_list([3, 5]), "3 and 5")
        self.assertEqual(written_list([3, 5, 7]), "3, 5, and 7")
        self.assertEqual(written_list([3, 5, 7, 9]), "3, 5, 7, and 9")