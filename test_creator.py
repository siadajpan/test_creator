import argparse
import os
import re

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--file_path',
                    help='Path to file that should be tested')

args = parser.parse_args()


TAB = '    '
T2 = 2 * TAB
FUNCTION_FILL = T2 + '# given\n' + T2 + '\n' + \
                T2 + '# when\n' + T2 + '\n' + \
                T2 + '# then\n' + T2 + '\n'


class TestFileCreator:
    def __init__(self):
        self.file_path = args.file_path
        self.tests_path = 'tests/unittests'
        self.test_file_name = self.create_test_file_name()
        self.output_text = ''
        self.imports = self.init_imports()

    def create_test_file_name(self):
        return 'test_' + os.path.basename(self.file_path)

    def init_imports(self):
        test_case = 'from unittest import TestCase\n'
        magic_mock = 'from unittest.mock import MagicMock\n'
        return test_case + magic_mock + '\n\n'

    def create_test_folder_structure(self):
        parent_folder = os.path.dirname(self.file_path)
        sub_folder = os.path.join(* parent_folder.split('/')[1:])
        test_folder = os.path.join(self.tests_path, sub_folder)
        if not os.path.exists(test_folder):
            os.makedirs(test_folder)

        return test_folder

    @staticmethod
    def convert_camel(name: str):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def parse_test_class(self, line: str):
        class_name = re.search(r'class (.*?)[(:]', line).group(1)
        self.output_text += 'class Test' + class_name + \
                            '(TestCase):\n'
        self.output_text += TAB + 'def setUp(self) -> None:\n'
        self.output_text += f'{T2}self.{self.convert_camel(class_name)} = ' \
                            f'{class_name}()\n\n'

    def parse_test_function(self, line: str):
        function_name = re.search(r'def (.*)\(', line).group(1)
        self.output_text += TAB + 'def test_' + function_name + '(self):\n'
        self.output_text += T2 + '# given\n' + T2 + '\n' + \
            T2 + '# when\n' + T2 + '\n' + \
            T2 + '# then\n' + T2 + 'pass\n\n'

    def parse_line(self, line: str):
        if 'class' in line:
            self.parse_test_class(line)

        if 'def' in line:
            self.parse_test_function(line)

    def parse_file(self):
        with open(self.file_path, 'r') as file:
            content = file.readlines()

        for line in content:
            self.parse_line(line)

    def create_test_file(self):
        test_folder = self.create_test_folder_structure()
        test_file_path = os.path.join(test_folder, self.test_file_name)
        self.parse_file()
        with open(test_file_path, 'w') as file:
            file.write(self.imports)
            file.write(self.output_text)


t = TestFileCreator()
t.create_test_file()
