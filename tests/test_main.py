import unittest
from unittest.mock import Mock, patch
import json
from snowglobe import __main__


class TestArgParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_args_list(self):
        res = __main__.parse_args(['list'])

        self.assertEqual(res.command, 'list')

    def test_parse_args_template(self):
        res = __main__.parse_args(['template'])

        self.assertEqual(res.command, 'template')

    def test_parse_args_inspect(self):
        res = __main__.parse_args(['inspect', 'NAME'])

        self.assertEqual(res.command, 'inspect')
        self.assertEqual(res.name, 'NAME')

    def test_parse_args_setup(self):
        res = __main__.parse_args(['setup', 'NAME', '-f', 'FILE'])

        self.assertEqual(res.command, 'setup')
        self.assertEqual(res.name, 'NAME')
        self.assertEqual(res.file, 'FILE')

    def test_parse_args_remove(self):
        res = __main__.parse_args(['remove', 'NAME'])

        self.assertEqual(res.command, 'remove')
        self.assertEqual(res.name, 'NAME')

    def test_parse_args_reset(self):
        res = __main__.parse_args(['reset', 'NAME'])

        self.assertEqual(res.command, 'reset')
        self.assertEqual(res.name, 'NAME')

    def test_parse_args_start(self):
        res = __main__.parse_args(['start', 'NAME'])

        self.assertEqual(res.command, 'start')
        self.assertEqual(res.name, 'NAME')

    def test_parse_args_exec(self):
        res = __main__.parse_args(['exec', 'NAME', 'EXEC-NAME'])

        self.assertEqual(res.command, 'exec')
        self.assertEqual(res.name, 'NAME')
        self.assertEqual(res.exec_name, 'EXEC-NAME')

    def test_parse_args_stop(self):
        res = __main__.parse_args(['stop', 'NAME'])

        self.assertEqual(res.command, 'stop')
        self.assertEqual(res.name, 'NAME')


class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('snowglobe.__main__.sys.argv', ['PROGRAM', 'list'])
    @patch('snowglobe.__main__.environment.Environment')
    def test_main_list(self, mocked_environment):
        mocked_environment_object = Mock()
        mocked_environment.return_value = mocked_environment_object
        res = __main__.main()

        mocked_environment_object.list.assert_called_with()
        self.assertEqual(res, 0)

    @patch('snowglobe.__main__.sys.argv', ['PROGRAM', 'template'])
    @patch('snowglobe.__main__.environment.Environment')
    def test_main_template(self, mocked_environment):
        mocked_environment_object = Mock()
        mocked_environment.return_value = mocked_environment_object
        res = __main__.main()

        mocked_environment_object.template.assert_called_with()
        self.assertEqual(res, 0)

    @patch('snowglobe.__main__.sys.argv', ['PROGRAM', 'inspect', 'NAME'])
    @patch('snowglobe.__main__.environment.Environment')
    def test_main_inspect(self, mocked_environment):
        mocked_environment_object = Mock()
        mocked_environment.return_value = mocked_environment_object
        res = __main__.main()

        mocked_environment_object.inspect.assert_called_with('NAME')
        self.assertEqual(res, 0)

    @patch('snowglobe.__main__.sys.argv', ['PROGRAM', 'setup', 'NAME', '-f', 'FILE'])
    @patch('snowglobe.__main__.environment.Environment')
    @patch('snowglobe.__main__.open')
    @patch('snowglobe.__main__.print')
    def test_main_setup_file_not_found(self, mocked_print, mocked_open, mocked_environment):
        mocked_environment_object = Mock()
        mocked_environment.return_value = mocked_environment_object
        mocked_open.side_effect = FileNotFoundError
        mocked_print.return_value = None

        res = __main__.main()

        mocked_open.assert_called_with('FILE', 'r')
        self.assertEqual(res, -1)

    @patch('snowglobe.__main__.sys.argv', ['PROGRAM', 'setup', 'NAME', '-f', 'FILE'])
    @patch('snowglobe.__main__.environment.Environment')
    @patch('snowglobe.__main__.open')
    @patch('snowglobe.__main__.json.loads')
    @patch('snowglobe.__main__.print')
    def test_main_setup_json_error(self, mocked_print, mocked_json_loads, mocked_open, mocked_environment):
        mocked_environment_object = Mock()
        mocked_environment.return_value = mocked_environment_object
        mocked_file_handler = Mock()
        mocked_file_handler.__enter__ = Mock()
        mocked_file_handler.__exit__ = Mock()
        mocked_file_handler.__enter__.return_value = mocked_file_handler
        mocked_file_handler.read.return_value = 'JSON-CONFIG'
        mocked_open.return_value = mocked_file_handler
        mocked_json_loads.side_effect = json.JSONDecodeError('', '', 0)
        mocked_print.return_value = None

        res = __main__.main()

        mocked_open.assert_called_with('FILE', 'r')
        self.assertEqual(res, -1)

    @patch('snowglobe.__main__.sys.argv', ['PROGRAM', 'setup', 'NAME', '-f', 'FILE'])
    @patch('snowglobe.__main__.environment.Environment')
    @patch('snowglobe.__main__.open')
    @patch('snowglobe.__main__.json.loads')
    @patch('snowglobe.__main__.print')
    def test_main_setup(self, mocked_print, mocked_json_loads, mocked_open, mocked_environment):
        mocked_environment_object = Mock()
        mocked_environment.return_value = mocked_environment_object
        mocked_file_handler = Mock()
        mocked_file_handler.__enter__ = Mock()
        mocked_file_handler.__exit__ = Mock()
        mocked_file_handler.__enter__.return_value = mocked_file_handler
        mocked_file_handler.read.return_value = '{"KEY": "VALUE"}'
        mocked_open.return_value = mocked_file_handler
        mocked_json_loads.return_value = {'KEY': 'VALUE'}
        mocked_print.return_value = None

        res = __main__.main()

        mocked_open.assert_called_with('FILE', 'r')
        mocked_environment_object.setup.assert_called_with('NAME', {'KEY': 'VALUE'})
        self.assertEqual(res, 0)

    @patch('snowglobe.__main__.sys.argv', ['PROGRAM', 'remove', 'NAME'])
    @patch('snowglobe.__main__.environment.Environment')
    def test_main_remove(self, mocked_environment):
        mocked_environment_object = Mock()
        mocked_environment.return_value = mocked_environment_object
        res = __main__.main()

        mocked_environment_object.remove.assert_called_with('NAME')
        self.assertEqual(res, 0)

    @patch('snowglobe.__main__.sys.argv', ['PROGRAM', 'reset', 'NAME'])
    @patch('snowglobe.__main__.environment.Environment')
    def test_main_reset(self, mocked_environment):
        mocked_environment_object = Mock()
        mocked_environment.return_value = mocked_environment_object
        res = __main__.main()

        mocked_environment_object.reset.assert_called_with('NAME')
        self.assertEqual(res, 0)

    @patch('snowglobe.__main__.sys.argv', ['PROGRAM', 'start', 'NAME'])
    @patch('snowglobe.__main__.environment.Environment')
    def test_main_start(self, mocked_environment):
        mocked_environment_object = Mock()
        mocked_environment.return_value = mocked_environment_object
        res = __main__.main()

        mocked_environment_object.start.assert_called_with('NAME')
        self.assertEqual(res, 0)

    @patch('snowglobe.__main__.sys.argv', ['PROGRAM', 'exec', 'NAME', 'EXEC-NAME'])
    @patch('snowglobe.__main__.environment.Environment')
    def test_main_exec(self, mocked_environment):
        mocked_environment_object = Mock()
        mocked_environment.return_value = mocked_environment_object
        res = __main__.main()

        mocked_environment_object.exec.assert_called_with('NAME', 'EXEC-NAME')
        self.assertEqual(res, 0)

    @patch('snowglobe.__main__.sys.argv', ['PROGRAM', 'stop', 'NAME'])
    @patch('snowglobe.__main__.environment.Environment')
    def test_main_stop(self, mocked_environment):
        mocked_environment_object = Mock()
        mocked_environment.return_value = mocked_environment_object
        res = __main__.main()

        mocked_environment_object.stop.assert_called_with('NAME')
        self.assertEqual(res, 0)

    @patch('snowglobe.__main__.sys.argv', ['PROGRAM', 'list'])
    @patch('snowglobe.__main__.environment.Environment')
    @patch('snowglobe.__main__.print')
    def test_main_unexpected_error(self, mocked_print, mocked_environment):
        mocked_environment.side_effect = Exception
        mocked_print.return_value = None

        res = __main__.main()

        self.assertEqual(res, -1)


if __name__ == '__main__':
    unittest.main()
