import os
import sys
import subprocess
import argparse

#check if (non-default) packages are installed, if not install them
try:
    from colorama import Fore
except ImportError as error:
    package = str(error.name)
    subprocess.check_output(f'pip install {package}', shell=True)
    from colorama import Fore

#status
ok = f'{Fore.GREEN}[+]{Fore.RESET}'
alert = f'{Fore.RED}[!]{Fore.RESET}'
exception = f'{Fore.YELLOW}[?]{Fore.RESET}'
info = f'{Fore.LIGHTBLUE_EX}[*]{Fore.RESET}'


def check_for_sudo():
    sudo = os.getuid()
    if sudo != 0:
        print(f'{alert} Please run this script as root')
        sys.exit()
    else:
        pass


def add_users(x):
    i = 0
    while i < x:
        try:
            os.popen(f'useradd -m user{i} 2>/dev/null')
        except Exception as e:
            print(f'{exception} {e}')
            pass
        i += 1
    if i >= x:
        print(f'{ok} Created users')


def expire_password(x):
    i = 0
    while i < x:
        try:
            os.popen(f'chage -M 90 user{i}')

        except Exception as e:
            print(f'{exception} {e}')
            pass
        i += 1
    if i >= x:
        print(f'{ok} Added passwd expire date for users')


def add_groups(x):
    i = 0
    while i < x:
        try:
            os.popen(f'groupadd group{i} 2>/dev/null')
        except Exception as e:
            print(f'{exception} {e}')
            pass
        i += 1
    if i >= x:
        print(f'{ok} Created groups')


def add_users_to_groups(x):
    i = 0
    while i < x:
        os.popen(f'usermod -a user{i} -G group{i}')
        i += 1
    if i >= x:
        print(f'{ok} Added users to groups')


def add_group_dirs(x):
    i = 0
    while i < x:
        try:
            os.mkdir(f'/home/group{i}')
            os.popen(f'chgrp -R group{i} /home/group{i}')
            i += 1
        except FileExistsError:
            i += 1
    if i >= x:
        print(f'{ok} Created group dirs')


def make_files_in_dirs(x):
    i = 0
    while i < x:
        try:
            os.popen(f'touch /home/group{i}/file')
        except Exception as e:
            print(f'{exception} {e}')
            pass
        i += 1
    if i >= x:
        print(f'{ok} Created files in group dirs')


def remove_everything(x):
    i = 0
    while i < x:
        try:
            os.system(f'rm -r /home/group{i} 2>/dev/null')
            os.system(f'rm -r /home/user{i} 2>/dev/null')
            os.system(f'groupdel group{i} 2>/dev/null')
            os.system(f'userdel user{i} 2>/dev/null')
        except Exception as e:
            print(f'{exception} {e}')
            pass
        i += 1
    if i >= x:
        print(f'{ok} Clear complete')


def main():
    check_for_sudo()

    parser = argparse.ArgumentParser(description='OsycTools | https://github.com/SoudruhDanny/osyc | By: Soudruh Danny')

    parser.add_argument("-u", "--users", help="--users [number]   | Creates [number] users (with home dir)", type=int)
    parser.add_argument("-p", "--passwd", help="--passwd [days]   | Set user passwd to expire in [days]", type=int)
    parser.add_argument("-g", "--groups", help="--groups [number] | Creates [number] groups", type=int)
    parser.add_argument("-ug", "--user_to_group", help="move users to groups", type=int)
    parser.add_argument("-gd", "--group_dirs", help="Make dirs for groups", type=int)
    parser.add_argument("-mf", "--make_files", help="Make files in dirs", type=int)
    parser.add_argument("-r", "--remove", help="--remove [number] | Removes created files, folders, groups and users", type=int)
    args = parser.parse_args()

    if args.users:
        add_users(args.users)
    if args.passwd:
        expire_password(args.passwd)
    if args.groups:
        add_groups(args.groups)
    if args.user_to_group:
        add_users_to_groups(args.user_to_group)
    if args.group_dirs:
        add_group_dirs(args.group_dirs)
    if args.make_files:
        make_files_in_dirs(args.make_files)
    if args.remove:
        remove_everything(args.remove)

    print(f'{ok} All done!')


if __name__ == '__main__':
    main()
