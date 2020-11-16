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
in *configs* directory (or later use create command of **codei** to create
config from local settings).
- Make codei.py executable: `chmod +x codei.py`.
- Create symlink so the utility can be used globally:
`ln -s {PROJECT_ABSOLUTE_PATH}/codei.py /usr/local/bin/codei`


## Usage

You can list available configs using
***list*** command:

```bash
$ codei list
Available settings: python, js, ...
```

Initialize local directory with predefined settings (or update existing settings)
using ***init*** command
:

```bash
$ codei init js
Creating new settings.json file... / Updating existing settings.json file...
```

Create settings.json config from local settings.json using ***create*** command:

```bash
$ codei create ts
Saving local settings to available configs under name: ts
```

Optional argument **-o / --overwrite** can be supplied for ***init*** and
***create*** command.

- when supplied for ***init***, common properties in settings are overwriten by
new values
- when supplied for ***create***, if there is config under the same name it will
be completly overwriten by the contents of local settings.
