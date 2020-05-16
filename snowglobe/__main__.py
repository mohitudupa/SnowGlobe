from snowglobe import environment
import argparse
import json


def parse_arguments() -> argparse.Namespace:
    snowglobe = argparse.ArgumentParser(prog='snowglobe')
    subparsers = snowglobe.add_subparsers(help='Sub commands for snowglobe', required=True)

    list_parser = subparsers.add_parser('list', help='Get list configured environments')
    list_parser.set_defaults(command='list')

    inspect_parser = subparsers.add_parser('inspect', help='Inspect a configured environment')
    inspect_parser.set_defaults(command='inspect')
    inspect_parser.add_argument('name', help='Name of the environment', type=str)

    setup_parser = subparsers.add_parser('setup', help='Setup a new environment')
    setup_parser.set_defaults(command='setup')
    setup_parser.add_argument('name', help='Name of the environment', type=str)
    setup_parser.add_argument('--file', '-f', help='Path to the config file', required=True, type=str)

    remove_parser = subparsers.add_parser('remove', help='Remove an existing environment')
    remove_parser.set_defaults(command='remove')
    remove_parser.add_argument('name', help='Name of the environment', type=str)

    reset_parser = subparsers.add_parser('reset', help='Reset an existing environment')
    reset_parser.set_defaults(command='reset')
    reset_parser.add_argument('name', help='Name of the environment', type=str)

    start_parser = subparsers.add_parser('start', help='Start an existing environment')
    start_parser.set_defaults(command='start')
    start_parser.add_argument('name', help='Name of the environment', type=str)

    exec_parser = subparsers.add_parser('exec', help='Exec commands on an existing environment')
    exec_parser.set_defaults(command='exec')
    exec_parser.add_argument('name', help='Name of the environment', type=str)
    exec_parser.add_argument('exec_name', help='Exec name', type=str)

    stop_parser = subparsers.add_parser('stop', help='Stop an existing environment')
    stop_parser.set_defaults(command='stop')
    stop_parser.add_argument('name', help='Name of the environment', type=str)

    return snowglobe.parse_args()


def main():
    try:
        args = parse_arguments()
        snowglobe = environment.Environment()

        if args.command == 'list':
            snowglobe.list()

        elif args.command == 'inspect':
            snowglobe.inspect(args.name)

        elif args.command == 'setup':
            try:
                with open(args.file, 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                raise RuntimeError(f'File {args.file} not found')

            snowglobe.setup(args.name, data)

        elif args.command == 'remove':
            snowglobe.remove(args.name)

        elif args.command == 'reset':
            snowglobe.reset(args.name)

        elif args.command == 'start':
            snowglobe.start(args.name)

        elif args.command == 'exec':
            snowglobe.exec(args.name, args.exec_name)

        elif args.command == 'stop':
            snowglobe.stop(args.name)
        return 0
    except TypeError as te:
        print(f'Error: {te}.\nUse snowglobe -h for command syntax.')
        return -1
    except RuntimeError as re:
        print(f'Error: {re}.')
        return -1
    except Exception as e:
        print(f'Error: {e}.\nAn unknown exception occurred.')
        return -1


if __name__ == '__main__':
    main()
