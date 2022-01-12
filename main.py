import os
import sys
import subprocess

#check if (non-default) packages are installed, if not install them
try:
    from colorama import Fore

except ImportError as error:
    package = error.name
    subprocess.check_output(f'pip install {package}', shell=True)
    from colorama import Fore

#status
ok = f'{Fore.GREEN}[+]{Fore.RESET}'
alert = f'{Fore.RED}[!]{Fore.RESET}'
#from colorama import Fore


def check_for_sudo():
    sudo = os.getuid()
    if sudo != 0:
        print(f'{alert} Please run this script as root')
        sys.exit()
    else:
        pass


def add_users(i):
    x = 6
    while i < x:
        try:
            os.popen(f'useradd -m user{i} 2>/dev/null')
        except Exception as e:
            print(e)
            pass
        i += 1
    if i >= x:
        print(f'{ok} Done adding users')


def expire_password(i):
    x = 6
    while i < x:
        try:
            os.popen(f'chage -M 90 user{i}')

        except Exception as e:
            print(e)
            pass
        i += 1
    if i >= x:
        print(f'{ok} Done adding passwd expire date')


def add_groups(i):
    x = 6
    while i < x:
        try:
            os.popen(f'groupadd group{i} 2>/dev/null')
        except Exception as e:
            print(e)
            pass
        i += 1
    if i >= x:
        print(f'{ok} Done adding groups')


def add_users_to_groups(i):
    x = 6
    while i < x:
        os.popen(f'usermod -a user{i} -G group{i}')
        i += 1
    if i >= x:
        print(f'{ok} Done adding users to group')


def add_group_dirs(i):
    x = 6
    while i < x:
        try:
            os.mkdir(f'/home/group{i}')
            i += 1
        except FileExistsError:
            i += 1
    if i >= x:
        print(f'{ok} Done adding group dirs')


def set_perms_of_dir(i):
    x = 6
    while i < x:
        try:
            os.popen(f'chgrp -R group{i} /home/group{i}')
        except Exception as e:
            print(e)
            pass
        i += 1
    if i >= x:
        print(f'{ok} Done adding dirs to group')


def make_files_in_dirs(i):
    x = 6
    while i < x:
        try:
            os.popen(f'touch /home/group{i}/file')
        except Exception as e:
            print(e)
            pass
        i += 1
    if i >= x:
        print(f'{ok} Done adding files')


def main():
    check_for_sudo()
    add_users(1)
    expire_password(1)
    add_groups(1)
    add_users_to_groups(1)
    add_group_dirs(1)
    set_perms_of_dir(1)
    make_files_in_dirs(1)
    print(f'{ok} All done!')


if __name__ == '__main__':
    main()
