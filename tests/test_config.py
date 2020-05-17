import unittest
from unittest.mock import Mock, patch
from snowglobe import config


class TestConfig(unittest.TestCase):
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

    def test_get_template(self):
        res = config.Config.get_template()

        self.assertEqual(res, config.TEMPLATE)

    @patch('snowglobe.config.path.abspath')
    @patch('snowglobe.config.listdir')
    def test_get_config_config_does_not_exist(self, mocked_listdir, mocked_abspath):
        mocked_abspath.return_value = '/PACKAGE/DIRECTORY/config.py'
        mocked_listdir.return_value = ['README']
        conf = config.Config()

        with self.assertRaises(RuntimeError):
            conf.get_config('NAME')

    @patch('snowglobe.config.path.abspath')
    @patch('snowglobe.config.listdir')
    @patch('snowglobe.config.open')
    @patch('snowglobe.config.json.load')
    def test_get_config(self, mocked_json_load, mocked_open, mocked_listdir, mocked_abspath):
        mocked_abspath.return_value = '/PACKAGE/DIRECTORY/config.py'
        mocked_listdir.return_value = ['NAME.json', 'README']
        mocked_file_handler = Mock()
        mocked_file_handler.__enter__ = Mock()
        mocked_file_handler.__exit__ = Mock()
        mocked_file_handler.__enter__.return_value = mocked_file_handler
        mocked_open.return_value = mocked_file_handler
        mocked_json_load.return_value = {'KEY': 'VALUE'}
        conf = config.Config()

        res = conf.get_config('NAME')

        mocked_open.assert_called_with('/PACKAGE/DIRECTORY/configs/NAME.json', 'r')
        mocked_json_load.assert_called_with(mocked_file_handler)
        self.assertEqual(res, {'KEY': 'VALUE'})

    @patch('snowglobe.config.path.abspath')
    @patch('snowglobe.config.listdir')
    @patch('snowglobe.config.Validator')
    def test_set_config_validation_error(self, mocked_validator, mocked_listdir, mocked_abspath):
        mocked_abspath.return_value = '/PACKAGE/DIRECTORY/config.py'
        mocked_listdir.return_value = ['NAME.json', 'README']
        mocked_validator_object = Mock()
        mocked_validator_object.validate.return_value = False
        mocked_validator.return_value = mocked_validator_object
        conf = config.Config()

        with self.assertRaises(RuntimeError):
            conf.set_config('NAME', {})

        mocked_validator_object.validate.assert_called_with({})

    @patch('snowglobe.config.path.abspath')
    @patch('snowglobe.config.listdir')
    @patch('snowglobe.config.Validator')
    @patch('snowglobe.config.open')
    @patch('snowglobe.config.json.dump')
    def test_set_config(self, mocked_json_dump, mocked_open, mocked_validator, mocked_listdir, mocked_abspath):
        mocked_abspath.return_value = '/PACKAGE/DIRECTORY/config.py'
        mocked_listdir.return_value = ['NAME.json', 'README']
        mocked_validator_object = Mock()
        mocked_validator_object.validate.return_value = True
        mocked_validator_object.document = {}
        mocked_validator.return_value = mocked_validator_object
        mocked_file_handler = Mock()
        mocked_file_handler.__enter__ = Mock()
        mocked_file_handler.__exit__ = Mock()
        mocked_file_handler.__enter__.return_value = mocked_file_handler
        mocked_open.return_value = mocked_file_handler
        mocked_json_dump.return_value = None
        conf = config.Config()

        conf.set_config('NAME', {})

        mocked_validator_object.validate.assert_called_with({})
        mocked_open.assert_called_with('/PACKAGE/DIRECTORY/configs/NAME.json', 'w')
        mocked_json_dump.assert_called_with({}, mocked_file_handler, indent=4)

    @patch('snowglobe.config.path.abspath')
    @patch('snowglobe.config.listdir')
    def test_del_config_config_does_not_exist(self, mocked_listdir, mocked_abspath):
        mocked_abspath.return_value = '/PACKAGE/DIRECTORY/config.py'
        mocked_listdir.return_value = ['README']
        conf = config.Config()

        with self.assertRaises(RuntimeError):
            conf.del_config('NAME')

    @patch('snowglobe.config.path.abspath')
    @patch('snowglobe.config.listdir')
    @patch('snowglobe.config.remove')
    def test_del_config(self, mocked_remove, mocked_listdir, mocked_abspath):
        mocked_abspath.return_value = '/PACKAGE/DIRECTORY/config.py'
        mocked_listdir.return_value = ['NAME', 'README']
        conf = config.Config()

        conf.del_config('NAME')
        mocked_remove.assert_called_with('/PACKAGE/DIRECTORY/configs/NAME.json')


if __name__ == '__main__':
    unittest.main()
