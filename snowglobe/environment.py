from snowglobe import config, runtime
import json


class Environment:
    def __init__(self):
        self.environment = runtime.Runtime()
        self.config = config.Config()

    def list(self) -> None:
        print('Environments: ')
        print('\n'.join(self.config.confs))

    def template(self) -> None:
        print(json.dumps(self.config.get_template(), indent=4))

    def inspect(self, name: str) -> None:
        print(json.dumps(self.config.get_config(name), indent=4))

    def setup(self, name: str, data: dict) -> None:
        print(f'Setting up environment: {name}')
        self.config.set_config(name, data)
        self.create(name)

    def remove(self, name: str) -> None:
        print(f'Deleting up environment: {name}')
        self.stop(name)
        self.delete(name)
        self.config.del_config(name)

    def reset(self, name: str) -> None:
        print(f'Resetting environment: {name}')
        self.stop(name)
        self.delete(name)
        self.create(name)

    def create(self, name: str) -> None:
        try:
            self.environment.inspect(name)
        except RuntimeError:
            print(f'Creating environment: {name}')
            conf = self.config.get_config(name)
            self.environment.create(conf['name'], conf['image'], conf['create'])
        else:
            raise RuntimeError(f'Environment: {name} already exists. Delete the container before recreating it.')

    def start(self, name: str) -> None:
        try:
            self.environment.inspect(name)
        except RuntimeError:
            self.create(name)

        print(f'Starting environment: {name}')
        conf = self.config.get_config(name)
        self.environment.start(conf['name'], conf['start'])

    def exec(self, name: str, exec_name: str) -> None:
        try:
            self.environment.inspect(name)
        except RuntimeError:
            self.create(name)

        print(f'Executing environment: {name}. Exec name: {exec_name}')
        conf = self.config.get_config(name)
        self.environment.exec(conf['name'], exec_name, conf['execs'])

    def stop(self, name):
        print(f'Stopping environment: {name}')
        self.environment.stop(name)

    def delete(self, name):
        print(f'Deleting environment: {name}')
        self.environment.remove(name)
