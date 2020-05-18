import unittest
from unittest.mock import Mock, patch
import subprocess
from snowglobe import runtime


class TestRuntime(unittest.TestCase):
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

    @patch('snowglobe.runtime.subprocess.run')
    def test_inspect_json_decode_error(self, mocked_run):
        mocked_run_response = Mock()
        mocked_run_response.stdout.decode.return_value = 'INVALID-JSON'
        mocked_run.return_value = mocked_run_response

        with self.assertRaises(RuntimeError):
            runtime.Runtime.inspect('NAME')

        mocked_run.assert_called_with(['docker', 'container', 'inspect', 'NAME'],
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

    @patch('snowglobe.runtime.subprocess.run')
    def test_inspect_container_not_found(self, mocked_run):
        mocked_run_response = Mock()
        mocked_run_response.stdout.decode.return_value = '[]'
        mocked_run.return_value = mocked_run_response

        with self.assertRaises(RuntimeError):
            runtime.Runtime.inspect('NAME')

        mocked_run.assert_called_with(['docker', 'container', 'inspect', 'NAME'],
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

    @patch('snowglobe.runtime.subprocess.run')
    def test_inspect(self, mocked_run):
        mocked_run_response = Mock()
        mocked_run_response.stdout.decode.return_value = '[{}]'
        mocked_run.return_value = mocked_run_response

        res = runtime.Runtime.inspect('NAME')

        mocked_run.assert_called_with(['docker', 'container', 'inspect', 'NAME'],
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        self.assertEqual(res, {})

    @patch('snowglobe.runtime.subprocess.run')
    def test_create(self, mocked_run):

        create = {
            'command': [],
            'entrypoint': 'ENTRYPOINT',
            'envs': {
                'KEY': 'VALUE',
            },
            'ports': [
                {
                    'containerPort': 8080,
                    'hostPort': 8080,
                },
                {
                    'containerPort': 80,
                    'hostPort': 80,
                    'hostIP': '120.0.0.1',
                    'protocol': 'udp'
                },
            ],
            'volumes': [
                {
                    'hostPath': '/PATH/ON/HOST',
                    'containerPath': '/PATH/ON/CONTAINER',
                    'mode': 'rw',
                }
            ],
            'options': '-it --hostname HOSTNAME',
        }

        runtime.Runtime.create('NAME', 'IMAGE', create)

        mocked_run.assert_called_with(['docker', 'container', 'create', '--entrypoint', 'ENTRYPOINT', '-e',
                                       'KEY=VALUE', '-p', '8080:8080/tcp', '-p', '120.0.0.1:80:80/udp', '-v',
                                       '/PATH/ON/HOST:/PATH/ON/CONTAINER:rw', '-it', '--hostname', 'HOSTNAME',
                                       '--name', 'NAME', 'IMAGE'],
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE)

    @patch('snowglobe.runtime.subprocess.run')
    def test_start(self, mocked_run):

        runtime.Runtime.start('NAME', '-i')
        mocked_run.assert_called_with(['docker', 'container', 'start', '-i', 'NAME'])

    def test_exec_exec_name_not_found(self):
        with self.assertRaises(RuntimeError):
            runtime.Runtime.exec('NAME', 'EXEC-NAME', [])

    @patch('snowglobe.runtime.subprocess.run')
    def test_exec(self, mocked_run):
        runtime.Runtime.exec('NAME', 'EXEC-NAME', [
            {
                'name': 'EXEC-NAME',
                'command': 'EXEC_COMMAND',
                'options': '-it',
            }
        ])
        mocked_run.assert_called_with(['docker', 'container', 'exec', '-it', 'NAME', 'EXEC_COMMAND'])

    @patch('snowglobe.runtime.subprocess.run')
    def test_stop(self, mocked_run):
        runtime.Runtime.stop('NAME')

        mocked_run.assert_called_with(['docker', 'container', 'stop', 'NAME'],
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE)

    @patch('snowglobe.runtime.subprocess.run')
    def test_remove(self, mocked_run):
        runtime.Runtime.remove('NAME')

        mocked_run.assert_called_with(['docker', 'container', 'rm', 'NAME'],
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE)


if __name__ == '__main__':
    unittest.main()
