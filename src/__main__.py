#!/usr/bin/env python3
# stalk-ify™ is a tool that uses the instaloader library to increase your stalking level.
# Copyright (C) 2024~2024  Raiden Ishigami <contact.raidenishi69@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   any later version.
#
# This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.

import os
import io
import sys
import contextlib
import argparse
import datetime
import re
import configparser
import subprocess
from instaloader import Instaloader, Profile
from colorama import init, Fore, Style

def extract_date_from_filename(filename):
    match = re.search(r"following_(\d+)\.txt", filename)
    if match:
        date_str = match.group(1)
        date = datetime.datetime.strptime(date_str, "%d%m%Y%H%M")
        return date
    else:
        return None

class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            parts = []
            if action.nargs == 0:
                parts.extend(action.option_strings)
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append(f'{option_string}')
                parts[-1] += f' {args_string}'
            return ', '.join(parts)

def main():
    init()

    usage_msg = 'stalkify [--help | -h] [--analysis | -a TARGET_USERNAME] [--get_info | -g TARGET_USERNAME] [--compare | -c]'

    parser = argparse.ArgumentParser(
        description='A tool that uses the instaloader library to increase your stalking level.',
        formatter_class=CustomHelpFormatter,
        usage=usage_msg
    )

    parser.add_argument('--analysis', '-a', type=str, metavar='TARGET_USERNAME',
                        help='analyzes target user to collect information from instagram.')
    parser.add_argument('--get_info', '-g', type=str, metavar='TARGET_USERNAME',
                        help='collects informations from target user\'s instagram.')
    parser.add_argument('--compare', '-c', action='store_true',
                        help='compare previously performed analyses.')
    parser.add_argument('--login', '-l', action='store_true',
                        help='log in completely for full use of the program.')
    
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        parser.exit()

    current_dir = os.getcwd()
    target_dir = os.path.join(current_dir, 'target')

    if args.login:
       try:
           subprocess.run(['python', os.path.join(current_dir, 'src', 'login.py')], check=True)
       except FileNotFoundError:
           print(Fore.RED + "[-] Login script not found in ./src directory." + Style.RESET_ALL)
       return

    if args.compare:
        try:
            subprocess.run(['python', os.path.join(current_dir, 'src', 'compare.py')], check=True)
        except FileNotFoundError:
            print(Fore.RED + "[-] Comparison script not found in ./src directory." + Style.RESET_ALL)
        return

    target_profile = args.analysis
    last_analysis_date = None
    profile_dir = os.path.join(target_dir, target_profile)
    
    if os.path.exists(profile_dir):
        files = os.listdir(profile_dir)
        if files:
            files.sort(reverse=True)
            last_filename = files[0]
            last_analysis_date = extract_date_from_filename(last_filename)

    if last_analysis_date and datetime.datetime.now() - last_analysis_date < datetime.timedelta(days=1):
        time_left = last_analysis_date + datetime.timedelta(days=1) - datetime.datetime.now()
        print(Fore.RED + "[-] Another analysis is not permitted due to API limitations.")
        print(f"Attempting to bypass this restriction may result in being restricted from using the API for 72 hours.")
        print(f"You will be able to perform another analysis in {time_left.days} days and {time_left.seconds // 3600} hours." + Style.RESET_ALL)
        return
   
    config = configparser.ConfigParser()
    config_path = os.path.expanduser('~/.config/stalkify/config.ini')
    if not os.path.exists(config_path):
        print(Fore.RED + f"Config file not found at {config_path}. Please run 'stalkify --login' to create it." + Style.RESET_ALL)
        sys.exit()
    
    config.read(config_path)  

    try:
        login_name = config.get('instagram', 'login_name')
    except configparser.NoOptionError:
        print(Fore.RED + "No 'login_name' option found in the 'instagram' section. Please check your config file." + Style.RESET_ALL)
        sys.exit()
    
    loader = Instaloader()

    print(" ")
    print(Fore.BLUE + f'[#] Trying to log in as: {login_name}' + Style.RESET_ALL)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            loader.load_session_from_file(login_name)
        print(Fore.GREEN + "[+] Session found, you have been logged in successfully!\n" + Style.RESET_ALL)
    except FileNotFoundError:
        loader.context.log(Fore.RED + "[-] Session file does not exist yet - Logging in." + Style.RESET_ALL)
        print(" ")
        if not loader.context.is_logged_in:
            loader.interactive_login(login_name)
            loader.save_session_to_file()
            print(Fore.GREEN + "[+] Session found, you have been logged in successfully!\n" + Style.RESET_ALL)

    print(" ")
    print(Fore.BLUE + f'[#] Starting analysis of user {target_profile}...' + Style.RESET_ALL)
    profile = Profile.from_username(loader.context, target_profile)
    following = profile.get_followees()

    print(Fore.GREEN + "[+] Generating formatting for report file..." + Style.RESET_ALL)
    now = datetime.datetime.now().strftime("%d%m%Y%H%M")
    report_filename = os.path.join(profile_dir, f'following_{now}.txt')

    os.makedirs(os.path.dirname(report_filename), exist_ok=True)

    print(Fore.GREEN + "[+] Writing data collected from Instagram...\n" + Style.RESET_ALL)
    with open(report_filename, 'w') as report_file:
        report_file.write(f"### User analytics: {target_profile}.\n\n")
        report_file.write(f"This person follows a total of {profile.followees} people, namely:\n")
        for followee in following:
            report_file.write(f"{followee.username}\n")

    print(Fore.BLUE + "[#] Report generated successfully at: " + report_filename + Style.RESET_ALL)

if __name__ == "__main__":
    main()