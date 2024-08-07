import os
import shutil
import subprocess
import time
import re
from pathlib import Path

import json5
import requests


def find_replace(directory, find, replace, file_pattern):
    for file in [f for f in directory.glob(file_pattern)]:
        try:
            file_contents = file.read_text()
            new_file_contents = re.sub(f"{find}", f"{replace}", file_contents)
            file.write_text(new_file_contents, newline='\n')
        except UnicodeDecodeError:
            pass


def packwiz_pretty_print(command, ignore_errors=False):
    try:
        output = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as err:
        output = err.output
        if not ignore_errors:
            print("Packwiz installation failed on command: ", command)
            print(output.decode('UTF-8').splitlines())
            return False

    lines = output.decode('UTF-8').splitlines()
    line_iter = iter(lines)
    for line in line_iter:
        if line.lower().startswith('dependencies found'):
            while not next(line_iter, None).lower().startswith('would you like to'):
                pass
        elif line.lower().startswith(('found mod', 'finding dependencies', 'all dependencies', 'loading modpack', 'removing mod', 'you don\'t have this mod')):
            pass
        elif line.lower().startswith("can't find this file;"):
            print(f"File was not removed, as it could not be found ({command})")
        else:
            print(line)
    return True


def main():
    # Constants
    event = 'carnival'
    mods_path = './mods/'
    pack_toml_path = './pack.toml'
    overrides_path = '../scripts/overrides'
    override_add_path = '../scripts/override_add.json5'
    override_remove_path = '../scripts/override_remove.json5'
    min_install_time = 0.1

    # Change working directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    os.chdir('../pack/')

    # Check working directory
    if not os.path.exists(pack_toml_path):
        print("Couldn't find pack.toml - make sure you're running this from the pack directory!")
        return

    # Assert empty mods folder

    if os.path.exists(mods_path):
        shutil.rmtree(mods_path)
        os.makedirs(mods_path)

    if not os.path.exists(overrides_path):
        os.makedirs(overrides_path)

    # Refresh to keep log clean
    os.system('packwiz refresh')

    # Retrieve submissions for slugs and versions
    submissions = json5.loads(requests.get(f'https://platform.modfest.net/event/{event}/submissions').text)

    # Retrieve override slugs and versions
    with open(override_add_path, 'r') as overrides_file:
        overrides_add = json5.load(overrides_file)

    with open(override_remove_path, 'r') as overrides_file:
        overrides_remove = json5.load(overrides_file)

    # Install mods based on slugs and versions
    for mod in overrides_add + submissions:
        platform = mod['platform'] if 'platform' in mod else mod
        if platform['project_id'] in [x['project_id'] for x in overrides_remove]:
            continue
        before_time = time.time()
        if not packwiz_pretty_print('packwiz mr add ' + (platform['project_id'] if 'version_id' not in platform or True else 'https://modrinth.com/mod/' + platform['project_id'] + '/version/' + platform['version_id']) + ' -y'):  # TODO: Re-enable versioning when platform updateversion isnt broken
            print('Update failed. Please see above for error.')
            return
        elapsed_time = time.time() - before_time
        time.sleep(0 if elapsed_time >= min_install_time else min_install_time - elapsed_time)

    for mod in overrides_remove:
        packwiz_pretty_print('packwiz remove ' + mod['project_id'], ignore_errors=True)

    # Swap server-side mods to both-sides for singleplayer use
    find_replace(Path(mods_path), "side = \"server\"", "side = \"both\"", "*.pw.toml")

    # Copy in overriding jar files, you heretic
    shutil.copytree(overrides_path, './mods', dirs_exist_ok=True)  # Python 3.8 :pineapple:

    # Refresh just in case
    os.system('packwiz refresh')

    # Prompt
    print('Update successful! Next Steps:')
    print('- `packwiz serve` and smoke test using local client+server')
    print('- commit and push')
    print('- restart server')


if __name__ == "__main__":
    main()
