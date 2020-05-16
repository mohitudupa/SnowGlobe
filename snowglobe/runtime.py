import subprocess
import json


class Runtime:
    def __init__(self):
        pass

    @staticmethod
    def inspect(name: str) -> dict:
        cmd = ['docker', 'container', 'inspect', name]
        response = subprocess.run(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        containers = json.loads(response.stdout.decode())
        if not containers:
            raise RuntimeError(f'Container: {name} not found')

        return containers[0]

    @staticmethod
    def create(name: str, image: str, create: dict) -> None:
        cmd = ['docker', 'container', 'create']

        if create.get('entrypoint'):
            cmd.extend(['--entrypoint', create['entrypoint']])
        if create.get('envs'):
            for key, value in create['envs'].items():
                cmd.extend(['-e', f'{key}={value}'])
        if create.get('ports'):
            for port in create['ports']:
                if 'hostIP' in port:
                    cmd.extend(
                        [
                            '-p',
                            f'{port["hostIP"]}:{port["hostPort"]}:{port["containerPort"]}/{port.get("protocol", "tcp")}'
                        ])
                else:
                    cmd.extend(['-p', f'{port["hostPort"]}:{port["containerPort"]}/{port.get("protocol", "tcp")}'])
        if create.get('volumes'):
            for volume in create['volumes']:
                cmd.extend(['-v', f'{volume["hostPath"]}:{volume["containerPath"]}:{volume.get("mode", "rw")}'])
        if create.get('options'):
            cmd.extend(create['options'].split())

        cmd.extend(['--name', name, image] + create['command'])
        subprocess.run(cmd)

    @staticmethod
    def start(name: str, start: str) -> None:
        cmd = ['docker', 'container', 'start'] + start.split() + [name]
        subprocess.run(cmd)

    @staticmethod
    def exec(name: str, exec_name: str, execs: list) -> None:
        execs = {ele['name']: ele for ele in execs}

        if exec_name not in execs:
            raise ValueError(f'Exec name: {exec_name} not found')

        cmd = ['docker', 'container', 'exec'] + \
            execs[exec_name]['options'].split() + [name] + execs[exec_name]['command'].split()
        subprocess.run(cmd)

    @staticmethod
    def stop(name: str) -> None:
        cmd = ['docker', 'container', 'stop', name]
        subprocess.run(cmd)

    @staticmethod
    def remove(name: str) -> None:
        cmd = ['docker', 'container', 'rm', name]
        subprocess.run(cmd)
