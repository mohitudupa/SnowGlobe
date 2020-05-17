from snowglobe import config, runtime
import json


class Environment:
    """
    Environment class. Holds functions for all snowglobe commands.
    """
    def __init__(self):
        """
        Initialises environment and config objects
        """
        self.runtime = runtime.Runtime()
        self.config = config.Config()

    def list(self) -> None:
        """
        Prints the list of existing environments.
        :return: None.
        """
        print('Environments: ')
        print('\n'.join(self.config.confs))

    def template(self) -> None:
        """
        Prints the template config.
        :return: None.
        """
        print(json.dumps(self.config.get_template(), indent=4))

    def inspect(self, name: str) -> None:
        """
        Prints the config of a specific environment.
        :param name: Name of the environment.
        :return: None.
        """
        print(json.dumps(self.config.get_config(name), indent=4))

    def setup(self, name: str, data: dict) -> None:
        """
        Creates a new environment.
        :param name: Name of the environment.
        :param data: Environment config.
        :return: None.
        """
        print(f'Setting up environment: {name}')
        self.config.set_config(name, data)
        self.create(name)

    def remove(self, name: str) -> None:
        """
        Deletes an environment.
        :param name: Name of the environment.
        :return: None.
        """
        print(f'Deleting up environment: {name}')
        self.stop(name)
        self.delete(name)
        self.config.del_config(name)

    def reset(self, name: str) -> None:
        """
        Resets an environment.
        :param name: Name of the environment.
        :return: None.
        """
        print(f'Resetting environment: {name}')
        self.stop(name)
        self.delete(name)
        self.create(name)

    def create(self, name: str) -> None:
        """
        Creates the docker container for an environment.
        :param name: Name of the environment.
        :return: None.
        """
        env = self.config.get_config(name)
        try:
            self.runtime.inspect(env['name'])
        except RuntimeError:
            print(f'Creating container: {env["name"]}')
            self.runtime.create(env['name'], env['image'], env['create'])
        else:
            raise RuntimeError(f'Container: {env["name"]} already exists. Delete the container before recreating it.')

    def start(self, name: str) -> None:
        """
        Starts the docker container.
        :param name: Name of the environment.
        :return: None.
        """
        env = self.config.get_config(name)
        try:
            self.runtime.inspect(env['name'])
        except RuntimeError:
            self.create(name)

        print(f'Starting container: {env["name"]}')
        self.runtime.start(env['name'], env['start'])

    def exec(self, name: str, exec_name: str) -> None:
        """
        Executes a command on the docker container.
        :param name: Name of the environment.
        :param exec_name: Name of the exec profile.
        :return: None.
        """
        env = self.config.get_config(name)
        try:
            self.runtime.inspect(env['name'])
        except RuntimeError:
            self.create(name)

        print(f'Executing container: {env["name"]}. Exec name: {exec_name}')
        self.runtime.exec(env['name'], exec_name, env['execs'])

    def stop(self, name):
        """
        Stops the docker container.
        :param name: Name of the environment.
        :return: None.
        """
        env = self.config.get_config(name)
        print(f'Stopping container: {env["name"]}')
        self.runtime.stop(env['name'])

    def delete(self, name):
        """
        Deletes the docker container
        :param name: Name of the environment.
        :return: None.
        """
        env = self.config.get_config(name)
        print(f'Deleting container: {env["name"]}')
        self.runtime.remove(env['name'])
