from subprocess import run, CalledProcessError, STDOUT, DEVNULL
from pathlib import Path
import re


# Variables from cookiecutter
repo_name = '{{ cookiecutter.__repo_name }}'

# https://github.com/cookiecutter/cookiecutter/issues/824
#   our workaround is to include these utility functions in the CCDS package
from ccds.hook_utils.custom_config import write_custom_config
from ccds.hook_utils.dependencies import write_dependencies

#
#  TEMPLATIZED VARIABLES FILLED IN BY COOKIECUTTER
#
packages = [
    "black",
    "flake8",
    "isort",
    "pip",
    "python-dotenv",
]
if re.match("basic", "{{ cookiecutter.pydata_packages }}", re.I):
    packages += [
        "ipython",
        "jupyter",
        "matplotlib",
        "numpy",
        "pandas",
        "scikit-learn",
    ]
# track packages that are not available through conda
pip_only_packages = [
    "awscli",
    "python-dotenv",
    "ipykernel",
]

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
    run(['gh', 'repo', 'create', repo_name])
    run(['git', 'push', '--set-upstream', 'origin', 'main'])
    run(['git', 'switch', '-c', 'dev'])
    run(['git', 'push', '--set-upstream', 'origin', 'dev'])

#
#  POST-GENERATION FUNCTIONS
#
write_dependencies(
    "{{ cookiecutter.dependency_file }}",
    packages,
    pip_only_packages,
    repo_name=repo_name,
    module_name="src",
    python_version="{{ cookiecutter.python_version_number }}",
)

### Run Makefile
run(['make', 'create_environment'])


# write_custom_config("{{ cookiecutter.custom_config }}")

# Remove LICENSE if "No license file"
if "{{ cookiecutter.open_source_license }}" == "No license file":
    Path("LICENSE").unlink()

# Make single quotes prettier
# Jinja tojson escapes single-quotes with \u0027 since it's meant for HTML/JS
pyproject_text = Path("pyproject.toml").read_text()
Path("pyproject.toml").write_text(pyproject_text.replace(r"\u0027", "'"))


run(['make', 'clean'])