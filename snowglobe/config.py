import json
from os import path, listdir, remove
from cerberus import Validator


SCHEMA = {
    'image': {
        'type': 'string',
        'required': True,
    },
    'name': {
        'type': 'string',
        'required': True,
    },
    'create': {
        'type': 'dict',
        'required': True,
        'schema': {
            'entrypoint': {
                'type': 'string',
            },
            'command': {
                'type': 'list',
                'schema': {'type': 'string'},
            },
            'envs': {
                'type': 'dict',
                'allow_unknown': True,
            },
            'ports': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'hostPort': {'type': 'integer', 'required': True},
                        'containerPort': {'type': 'integer', 'required': True},
                        'protocol': {'type': 'string', 'allowed': ['tcp', 'udp']},
                        'hostIP': {'type': 'string'},
                    }
                }
            },
            'volumes': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'hostPath': {'type': 'string', 'required': True},
                        'containerPath': {'type': 'string', 'required': True},
                        'mode': {'type': 'string', 'allowed': ['ro', 'rw']}
                    }
                }
            },
            'options': {
                'type': 'string',
            },
        }
    },
    'execs': {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'dict',
            'schema': {
                'name': {'type': 'string', 'required': True},
                'command': {'type': 'string', 'required': True},
                'options': {'type': 'string'}
            }
        },
    },
    'start': {
        'type': 'string',
        'required': True,
    }
}


TEMPLATE = {
    'image': 'IMAGE:TAG',
    'name': 'NAME',
    'create': {
        'command': [],
        'entrypoint': 'ENTRYPOINT',
        'envs': {
            'KEY': 'VALUE',
        },
        'ports': [
            {
                'containerPort': 8080,
                'hostPort': 8080,
            }
        ],
        'volumes': [
            {
                'hostPath': '/PATH/ON/HOST',
                'containerPath': '/PATH/ON/CONTAINER',
                'mode': 'rw',
            }
        ],
        'options': '-it --hostname HOSTNAME',
    },
    'start': '',
    'execs': [
        {
            'name': 'EXEC-NAME',
            'command': 'EXEC_COMMAND',
            'options': '-it',
        }
    ]
}


class Config:
    """
    Config class.
    """
    def __init__(self):
        """
        Sets up the config path and gets the list of installed configs.
        """
        self.CONFIG_PATH = path.join(path.dirname(path.abspath(__file__)), 'configs')
        self.confs = {ele.replace('.json', '') for ele in listdir(self.CONFIG_PATH)}
        self.confs.remove('README')

    @staticmethod
    def get_template() -> dict:
        """
        Returns the template config.
        :return:
        """
        return TEMPLATE

    def get_config(self, conf: str) -> dict:
        """
        Returns the a config.
        :param conf: Name of the config.
        :return: Config data.
        """
        if conf not in self.confs:
            raise RuntimeError('Environment not found')

        with open(path.join(self.CONFIG_PATH, f'{conf}.json')) as f:
            return json.load(f)

    def set_config(self, conf: str, data: dict) -> None:
        """
        Validates and writes a new config.
        :param conf: Name of the config.
        :param data: Config data.
        :return: None.
        """
        validator = Validator(SCHEMA)
        if not validator.validate(data):
            raise RuntimeError(f'Error in config format. Error: {validator.errors}')

        with open(path.join(self.CONFIG_PATH, f'{conf}.json'), 'w') as f:
            json.dump(validator.document, f, indent=4)

        self.confs = [ele.replace('.json', '') for ele in listdir(self.CONFIG_PATH)]
        self.confs.remove('README')

    def del_config(self, conf) -> None:
        """
        Deletes a config.
        :param conf: Name of the config.
        :return: None.
        """
        if conf not in self.confs:
            raise RuntimeError('Environment not found')

        remove(path.join(self.CONFIG_PATH, f'{conf}.json'))
