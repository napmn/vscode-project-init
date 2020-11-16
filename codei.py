#!/usr/local/bin/python3
import argparse
import json
from pathlib import Path, PurePath


SETTINGS_PATH = '.vscode/settings.json'


def parse_args():
    parser = argparse.ArgumentParser()

    # parent parser for create and init commands
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        '-o', '--overwrite', action='store_true', default=False,
        help='Flag which determines whether to overwrite settings if they '
            'already exist'
    )

    # subparsers for commands
    subparsers = parser.add_subparsers(dest='command', required=True)
    subparsers.add_parser(
        'list',
        description='Lists all existing predefined settings',
        help='List predefined settings'
    )

    save_parser = subparsers.add_parser(
        'create',
        description='Saves vscode settings for later usage',
        help='Saves settings',
        parents=[parent_parser]
    )
    save_parser.add_argument(
        'name', help='Name under which settings should be saved'
    )

    init_parser = subparsers.add_parser(
        'init',
        description='Initialize current directory with given vscode settings',
        help='Initialize current directory with vscode settings',
        parents=[parent_parser]
    )
    init_parser.add_argument(
        'project_type', help='Settings to use for initialization'
    )

    return vars(parser.parse_args())


def load_settings(project_type):
    # resolve path to target of possible simlink
    settings_path = PurePath(
        Path(__file__).resolve().parent
    ).joinpath(f'configs/{project_type}.json')
    if not Path(settings_path).exists():
        return None
    with open(settings_path, 'r') as settings_f:
        return json.load(settings_f)


def create_local_settings(settings):
    print('Creating new settings.json file...')
    with open(SETTINGS_PATH, 'w') as settings_f:
        json.dump(settings, settings_f, sort_keys=True, indent=4)


def merge_settings(a, b):
    """
    Deep merge of settings dicts.
    Conflicting keys keeps value of dict 'a'.
    """
    final = {**a}
    for key, val in b.items():
        if key in a.keys():
            if isinstance(b[key], dict) and isinstance(a[key], dict):
                final[key] = merge_settings(a[key], b[key])
        else:
            final[key] = val
    return final


def update_local_settings(settings, overwrite):
    print('Updating existing settings.json file...')
    with open(SETTINGS_PATH, 'r') as current_f:
        current_settings = json.load(current_f)
    if overwrite:
        final_settings = merge_settings(settings, current_settings)
    else:
        final_settings = merge_settings(current_settings, settings)
    with open(SETTINGS_PATH, 'w') as output_f:
        json.dump(final_settings, output_f, sort_keys=True, indent=4)


def get_available_configs():
    path = PurePath(Path(__file__).resolve().parent).joinpath('configs')
    return path, [
        Path(f).stem for f in Path(path).iterdir() if str(f).endswith('.json')
    ]


def list_available_configs():
    _, configs = get_available_configs()
    print(f'Available configs: {", ".join(configs)}')


def init_local_directory_with_settings(project_type, overwrite):
    settings = load_settings(project_type)
    if not settings:
        print('Settings for provided project type does not exist')
        exit(1)
    Path('.vscode').mkdir(exist_ok=True)
    if Path(SETTINGS_PATH).exists():
        update_local_settings(settings, overwrite)
    else:
        create_local_settings(settings)


def create_config_from_local_settings(name, overwrite):
    path, configs = get_available_configs()
    if name in configs and not overwrite:
        print(
            f'Config with name {name} already exist! Choose different name '
            'or run command with -o option to overwrite it'
        )
        exit(0)

    if not Path(SETTINGS_PATH).exists():
        print('Local vscode settings were not found')
        exit(1)

    print(f'Saving local settings to available configs under name: {name}')
    with open(SETTINGS_PATH, 'r') as local_f:
        current_settings = json.load(local_f)

    with open(path.joinpath(f'{name}.json'), 'w') as config_f:
        json.dump(current_settings, config_f, sort_keys=True, indent=4)


if __name__ == '__main__':
    args = parse_args()
    if args['command'] == 'list':
        list_available_configs()
    elif args['command'] == 'init':
        init_local_directory_with_settings(
            args['project_type'], args['overwrite']
        )
    elif args['command'] == 'create':
        create_config_from_local_settings(args['name'], args['overwrite'])
