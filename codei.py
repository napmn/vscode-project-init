#!/usr/local/bin/python3
import argparse
import json
from pathlib import Path, PurePath


SETTINGS_PATH = '.vscode/settings.json'


def parse_args():
    class ListAction(argparse.Action):
        """ Custom action to list available predefined settings """
        def __init__(self, *args, **kwargs):
            super().__init__(nargs=0, *args, **kwargs)

        def __call__(self, parser, *args, **kwargs):
            path = PurePath(Path(__file__).resolve().parent).joinpath('configs')
            configs = [
                Path(f).stem for f in Path(path).iterdir() if
                str(f).endswith('.json')
            ]
            print(f'Available settings: {", ".join(configs)}')
            parser.exit()

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', action=ListAction)
    parser.add_argument(
        'project_type', type=str, help='Settings to use for initialization.'
    )
    parser.add_argument(
        '-o', '--overwrite', action='store_true', default=False,
        help='Flag which determines whether to overwrite setting with common'
        'keys in current and new settings or not.'
    )
    args = parser.parse_args()
    return vars(args)


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
        # final_settings = {**current_settings, **settings}
    else:
        final_settings = merge_settings(current_settings, settings)
        # final_settings = {**settings, **current_settings}
    with open(SETTINGS_PATH, 'w') as output_f:
        json.dump(final_settings, output_f, sort_keys=True, indent=4)


if __name__ == '__main__':
    args = parse_args()
    settings = load_settings(args['project_type'])
    if not settings:
        print('Settings for provided project type does not exist')
        exit(1)
    Path('.vscode').mkdir(exist_ok=True)
    if Path(SETTINGS_PATH).exists():
        update_local_settings(settings, args['overwrite'])
    else:
        create_local_settings(settings)
