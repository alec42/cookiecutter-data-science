from subprocess import run, CalledProcessError, STDOUT, DEVNULL
from pathlib import Path
import re


# Variables from cookiecutter
repo_name = '{{ cookiecutter.__repo_name }}'

### Configure Git
if re.match(r"y(es)?|o(ui)?", "{{ cookiecutter.first_time_git }}" , re.I):
    run(['git', 'config', '--global', '--add', 'safe.directory', '*'])
    run(['git', 'config', '--global', 'init.defaultBranch', 'main'])
    run(['git', 'config', '--global', 'push.autoSetupRemote', 'true'])
    run(['brew', 'install', 'gh', repo_name])

run(['pip', 'install', 'nbstripout>=0.6.0,<1.0.0'])
run(['nbstripout', '--install'])

if re.match(r"y(es)?|o(ui)?", "{{ cookiecutter.init_git }}" , re.I):
    run(['git', 'init'])
    run(['git', 'remote', 'add', 'origin', f"git@github.com:alec42/{repo_name}.git"])
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', '\"Initial Commit\"'])
    if re.match(r"y(es)?|o(ui)?", "{{ cookiecutter.private_git_repo }}" , re.I):
        run(['gh', 'repo', 'create', repo_name, '--private'])
    elif re.match(r"no?n?", "{{ cookiecutter.private_git_repo }}" , re.I):
        run(['gh', 'repo', 'create', repo_name, '--public'])
    run(['git', 'push', '--set-upstream', 'origin', 'main'])
    run(['git', 'switch', '-c', 'dev'])
    run(['git', 'push', '--set-upstream', 'origin', 'dev'])


### Run Makefile
run(['make', 'create_environment'])


# Remove LICENSE if "No license file"
if "{{ cookiecutter.open_source_license }}" == "No license file":
    Path("LICENSE").unlink()

run(['make', 'clean'])