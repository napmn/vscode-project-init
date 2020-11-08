# VSCode Project Init Utility

This simple python 3.6+ utility script helps initializing new
(or updating existing) VSCode workspace settings.
Let's say you like to use diffent color theme
depending on project language - simply create JSON configs in *configs*
directory.
Name of the config is used as argument to the script for initializing
current working directory with predefined settings from the config file.

## Setup

- Clone repo anywhere you want and create your configuration JSON files
in *configs* directory.
- Make codei.py executable: `chmod +x codei.py`.
- Create symlink so the utility can be used globally:
`ln -s {PROJECT_ABSOLUTE_PATH}/codei.py /usr/local/bin/codei`


## Usage

When you have your configs ready you can list available configs using
**-l / --list** argument:

```bash
$ codei --list
Available settings: python, js, ...
```

Initialize local directory with predefined settings
(or update existing settings):

```bash
$ codei js
Creating new settings.json file... / Updating existing settings.json file...
```

If optional argument **-o / --overwrite** is present, common properties in
settings are overwriten by new values. If not, settings are merged
in depth and values of conflicting keys are not changed.

## TODO

- implement settings config creation from local settings
