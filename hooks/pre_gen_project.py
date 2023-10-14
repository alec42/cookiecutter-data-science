# Functions here run before the project is generated.

# For the use of these hooks, see
# See https://cookiecutter.readthedocs.io/en/1.7.2/advanced/hooks.html
import re
from subprocess import run

if re.match(r"y(es)?|o(ui)?", "{{ cookiecutter.first_time_git }}" , re.I):
    run(["git", "config", "--global", "alias.lg",
         "log --color --graph --date=format:'%Y-%m-%d %H:%M:%S' --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%ad) %C(bold blue)<%an>%Creset'"])
    
    run(['git', 'config', '--global', 'pull.ff', 'only'])

    git_user_name = input("Git user name:")
    run(["git", "config", "--global", "user.name", git_user_name])
    git_email = input("Git email address:")
    run(["git", "config", "--global", "user.email", git_email])
    git_password = input("Git password (https authentification):")
    run(["git", "config", "--global", "user.password", git_password])

run(['gh', 'auth', ])