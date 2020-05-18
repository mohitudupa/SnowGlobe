import unittest
from unittest.mock import Mock, patch, call
import json
from snowglobe import environment, config


class TestEnvironment(unittest.TestCase):
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

    @patch('snowglobe.environment.config.Config')
    @patch('snowglobe.environment.print')
    def test_list(self, mocked_print,  mocked_config):
        mocked_config_object = Mock()
        mocked_config_object.confs = ['NAME-1', 'NAME-2']
        mocked_config.return_value = mocked_config_object
        mocked_print.return_value = None
        env = environment.Environment()

        env.list()

        mocked_print.assert_has_calls([
            call('Environments:'),
            call('NAME-1\nNAME-2')
        ])

    @patch('snowglobe.environment.config.Config')
    @patch('snowglobe.environment.print')
    def test_template(self, mocked_print, mocked_config):
        mocked_config_object = Mock()
        mocked_config_object.get_template.return_value = {}
        mocked_config.return_value = mocked_config_object
        mocked_print.return_value = None
        env = environment.Environment()

        env.template()

        mocked_print.assert_called_with(json.dumps({}, indent=4))
        mocked_config_object.get_template.assert_called_with()

    @patch('snowglobe.environment.config.Config')
    @patch('snowglobe.environment.print')
    def test_inspect(self, mocked_print, mocked_config):
        mocked_config_object = Mock()
        mocked_config_object.get_config.return_value = {}
        mocked_config.return_value = mocked_config_object
        mocked_print.return_value = None
        env = environment.Environment()

        env.inspect('NAME')

        mocked_config_object.get_config.assert_called_with('NAME')
        mocked_print.assert_called_with(json.dumps({}, indent=4))
        mocked_config_object.get_config.assert_called_with('NAME')

    @patch('snowglobe.environment.config.Config')
    @patch('snowglobe.environment.print')
    def test_setup(self, mocked_print, mocked_config):
        mocked_config_object = Mock()
        mocked_config_object.set_config.return_value = None
        mocked_config.return_value = mocked_config_object
        mocked_print.return_value = None
        env = environment.Environment()
        env.create = Mock()

        env.setup('NAME', {})

        mocked_print.assert_called_with('Setting up environment: NAME')
        mocked_config_object.set_config.assert_called_with('NAME', {})
        env.create.assert_called_with('NAME')

    @patch('snowglobe.environment.config.Config')
    @patch('snowglobe.environment.print')
    def test_remove(self, mocked_print, mocked_config):
        mocked_config_object = Mock()
        mocked_config_object.del_config.return_value = None
        mocked_config.return_value = mocked_config_object
        mocked_print.return_value = None
        env = environment.Environment()
        env.stop = Mock()
        env.delete = Mock()

        env.remove('NAME')

        mocked_print.assert_called_with('Removing up environment: NAME')
        mocked_config_object.del_config.assert_called_with('NAME')
        env.stop.assert_called_with('NAME')
        env.delete.assert_called_with('NAME')

    @patch('snowglobe.environment.config.Config')
    @patch('snowglobe.environment.print')
    def test_reset(self, mocked_print, mocked_config):
        mocked_config_object = Mock()
        mocked_config_object.del_config.return_value = None
        mocked_config.return_value = mocked_config_object
        mocked_print.return_value = None
        env = environment.Environment()
        env.stop = Mock()
        env.delete = Mock()
        env.create = Mock()

        env.reset('NAME')

        mocked_print.assert_called_with('Resetting environment: NAME')
        env.stop.assert_called_with('NAME')
        env.delete.assert_called_with('NAME')
        env.create.assert_called_with('NAME')

    @patch('snowglobe.environment.config.Config')
    @patch('snowglobe.environment.print')
    def test_create_container_does_not_exist(self, mocked_print, mocked_config):
        mocked_config_object = Mock()
        mocked_config_object.get_config.return_value = {'name': 'NAME', 'image': 'IMAGE', 'create': {}}
        mocked_config.return_value = mocked_config_object
        mocked_print.return_value = None
        env = environment.Environment()
        env.runtime.inspect = Mock()
        env.runtime.inspect.side_effect = RuntimeError
        env.runtime.create = Mock()

        env.create('NAME')

        mocked_config_object.get_config.assert_called_with('NAME')
        env.runtime.inspect.assert_called_with('NAME')
        mocked_print.assert_called_with('Creating container: NAME')
        env.runtime.create.assert_called_with('NAME', 'IMAGE', {})

    @patch('snowglobe.environment.config.Config')
    @patch('snowglobe.environment.print')
    def test_create_container_exists(self, mocked_print, mocked_config):
        mocked_config_object = Mock()
        mocked_config_object.get_config.return_value = {'name': 'NAME', 'image': 'IMAGE', 'create': {}}
        mocked_config.return_value = mocked_config_object
        mocked_print.return_value = None
        env = environment.Environment()
        env.runtime.inspect = Mock()
        env.runtime.inspect.return_value = {}
        env.runtime.create = Mock()

        with self.assertRaises(RuntimeError):
            env.create('NAME')

        mocked_config_object.get_config.assert_called_with('NAME')
        env.runtime.inspect.assert_called_with('NAME')

    @patch('snowglobe.environment.config.Config')
    @patch('snowglobe.environment.print')
    def test_start_container_does_not_exist(self, mocked_print, mocked_config):
        mocked_config_object = Mock()
        mocked_config_object.get_config.return_value = {'name': 'NAME', 'image': 'IMAGE', 'start': '-i'}
        mocked_config.return_value = mocked_config_object
        mocked_print.return_value = None
        env = environment.Environment()
        env.runtime.inspect = Mock()
        env.runtime.inspect.side_effect = RuntimeError
        env.create = Mock()
        env.runtime.start = Mock()

        env.start('NAME')

        mocked_config_object.get_config.assert_called_with('NAME')
        env.runtime.inspect.assert_called_with('NAME')
        env.create.assert_called_with('NAME')
        mocked_print.assert_called_with('Starting container: NAME')
        env.runtime.start.assert_called_with('NAME', '-i')

    @patch('snowglobe.environment.config.Config')
    @patch('snowglobe.environment.print')
    def test_start_container_exists(self, mocked_print, mocked_config):
        mocked_config_object = Mock()
        mocked_config_object.get_config.return_value = {'name': 'NAME', 'image': 'IMAGE', 'start': '-i'}
        mocked_config.return_value = mocked_config_object
        mocked_print.return_value = None
        env = environment.Environment()
        env.runtime.inspect = Mock()
        env.runtime.inspect.return_value = {}
        env.runtime.start = Mock()

        env.start('NAME')

        mocked_config_object.get_config.assert_called_with('NAME')
        env.runtime.inspect.assert_called_with('NAME')
        mocked_print.assert_called_with('Starting container: NAME')
        env.runtime.start.assert_called_with('NAME', '-i')

    @patch('snowglobe.environment.config.Config')
    @patch('snowglobe.environment.print')
    def test_exec_container_does_not_exist(self, mocked_print, mocked_config):
        mocked_config_object = Mock()
        mocked_config_object.get_config.return_value = {'name': 'NAME', 'image': 'IMAGE', 'execs': [
            {
                'name': 'EXEC-NAME',
                'command': 'EXEC-COMMAND',
                'options': '-it',
            }
        ]}
        mocked_config.return_value = mocked_config_object
        mocked_print.return_value = None
        env = environment.Environment()
        env.runtime.inspect = Mock()
        env.runtime.inspect.side_effect = RuntimeError
        env.create = Mock()
        env.runtime.exec = Mock()

        env.exec('NAME', 'EXEC-NAME')

        mocked_config_object.get_config.assert_called_with('NAME')
        env.runtime.inspect.assert_called_with('NAME')
        env.create.assert_called_with('NAME')
        mocked_print.assert_called_with('Executing container: NAME. Exec name: EXEC-NAME')
        env.runtime.exec.assert_called_with('NAME', 'EXEC-NAME', [
            {
                'name': 'EXEC-NAME',
                'command': 'EXEC-COMMAND',
                'options': '-it',
            }
        ])

    @patch('snowglobe.environment.config.Config')
    @patch('snowglobe.environment.print')
    def test_exec_container_exists(self, mocked_print, mocked_config):
        mocked_config_object = Mock()
        mocked_config_object.get_config.return_value = {'name': 'NAME', 'image': 'IMAGE', 'execs': [
            {
                'name': 'EXEC-NAME',
                'command': 'EXEC-COMMAND',
                'options': '-it',
            }
        ]}
        mocked_config.return_value = mocked_config_object
        mocked_print.return_value = None
        env = environment.Environment()
        env.runtime.inspect = Mock()
        env.runtime.inspect.return_value = {}
        env.runtime.exec = Mock()

        env.exec('NAME', 'EXEC-NAME')

        mocked_config_object.get_config.assert_called_with('NAME')
        env.runtime.inspect.assert_called_with('NAME')
        mocked_print.assert_called_with('Executing container: NAME. Exec name: EXEC-NAME')
        env.runtime.exec.assert_called_with('NAME', 'EXEC-NAME', [
            {
                'name': 'EXEC-NAME',
                'command': 'EXEC-COMMAND',
                'options': '-it',
            }
        ])

    @patch('snowglobe.environment.config.Config')
    @patch('snowglobe.environment.print')
    def test_stop(self, mocked_print, mocked_config):
        mocked_config_object = Mock()
        mocked_config_object.get_config.return_value = {'name': 'NAME'}
        mocked_config.return_value = mocked_config_object
        mocked_print.return_value = None
        env = environment.Environment()
        env.runtime.stop = Mock()

        env.stop('NAME')

        mocked_config_object.get_config.assert_called_with('NAME')
        mocked_print.assert_called_with('Stopping container: NAME')
        env.runtime.stop.assert_called_with('NAME')

    @patch('snowglobe.environment.config.Config')
    @patch('snowglobe.environment.print')
    def test_delete(self, mocked_print, mocked_config):
        mocked_config_object = Mock()
        mocked_config_object.get_config.return_value = {'name': 'NAME'}
        mocked_config.return_value = mocked_config_object
        mocked_print.return_value = None
        env = environment.Environment()
        env.runtime.remove = Mock()

        env.delete('NAME')

        mocked_config_object.get_config.assert_called_with('NAME')
        mocked_print.assert_called_with('Deleting container: NAME')
        env.runtime.remove.assert_called_with('NAME')


if __name__ == '__main__':
    unittest.main()
