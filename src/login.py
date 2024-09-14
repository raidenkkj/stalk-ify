import os
import subprocess
import configparser
from colorama import init, Fore, Style

def create_config():
    init()

    print(" ")
    print(Fore.CYAN + "[+] Creating config.ini..." + Style.RESET_ALL)
    print(" ")
    login_name = input(Fore.YELLOW + "[#] Enter your Instagram login name: " + Style.RESET_ALL).strip()

    session_path = os.path.expanduser(f"~/.config/instaloader/session-{login_name}")

    if os.path.exists(session_path):
        print(" ")
        redo_login = input(Fore.YELLOW + f"[#] Session file found at {session_path}. Do you want to redo the login? (yes/no): " + Style.RESET_ALL).strip().lower()
        if redo_login in ['yes', 'y']:
            print(" ")
            print(Fore.RED + f"[#] Removing the existing session file at {session_path}..." + Style.RESET_ALL)
            os.remove(session_path)
            print(" ")
            print(Fore.GREEN + "[#] Session file removed. Redirecting to Instaloader for login..." + Style.RESET_ALL)
            try:
                subprocess.run(['instaloader', '--login', login_name], check=True)
            except subprocess.CalledProcessError as e:
                print(" ")
                print(Fore.RED + f"[-] Error occurred while trying to log in: {e}" + Style.RESET_ALL)
                return
        else:
            print(" ")
            print(Fore.GREEN + "[#] Using the existing session file." + Style.RESET_ALL)
    else:
        print(" ")
        print(Fore.YELLOW + f"[-] No session file was found with username {login_name}, proceed to login with Instaloader..." + Style.RESET_ALL)
        print(" ")
        try:
            subprocess.run(['instaloader', '--login', login_name], check=True)
        except subprocess.CalledProcessError as e:
            print(" ")
            print(Fore.RED + f"[-] Error occurred while trying to log in: {e}" + Style.RESET_ALL)
            return

    config_content = f"""[instagram]
login_name = {login_name}
"""
    config_path = os.path.expanduser('~/.config/stalkify/config.ini')
    
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    with open(config_path, 'w') as config_file:
        config_file.write(config_content)
    
    print(" ")
    print(Fore.GREEN + f"[+] config.ini created successfully at {config_path}" + Style.RESET_ALL)

if __name__ == "__main__":
    create_config()