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


class Config:
    def __init__(self):
        self.CONFIG_PATH = path.join(path.dirname(path.abspath(__file__)), 'configs')
        self.confs = [ele.replace('.json', '') for ele in listdir(self.CONFIG_PATH)]

    def get_config(self, conf: str) -> dict:
        if conf not in self.confs:
            raise RuntimeError('Environment not found')

        with open(path.join(self.CONFIG_PATH, f'{conf}.json')) as f:
            return json.load(f)

    def set_config(self, conf: str, data: dict) -> None:
        validator = Validator(SCHEMA)
        if not validator.validate(data):
            raise RuntimeError(f'Error in config format. Error: {validator.errors}')

        with open(path.join(self.CONFIG_PATH, f'{conf}.json'), 'w') as f:
            json.dump(validator.document, f, indent=4)

        self.confs = [ele.replace('.json', '') for ele in listdir(self.CONFIG_PATH)]

    def del_config(self, conf) -> None:
        if conf not in self.confs:
            raise RuntimeError('Environment not found')

        remove(path.join(self.CONFIG_PATH, f'{conf}.json'))
