#!/usr/bin/env python3
import os
import glob
import re
from datetime import datetime
from colorama import init, Fore, Style
import time

def list_directories(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def list_files(path, pattern):
    return sorted(glob.glob(os.path.join(path, pattern)))

def extract_data_from_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
        
    username = re.search(r"### User analytics: ([\w\.]+).", content).group(1)
    total_following = int(re.search(r"This person follows a total of (\d+) people", content).group(1))
    following = re.findall(r"^([\w\.]+)$", content, re.MULTILINE)
    
    date_str = re.search(r"following_(\d+)\.txt", os.path.basename(filepath)).group(1)
    date = datetime.strptime(date_str, "%d%m%Y%H%M")
    
    return username, total_following, following, date

def compare_lists(list1, list2):
    set1, set2 = set(list1), set(list2)
    new_following = list(set2 - set1)
    unfollowed = list(set1 - set2)
    return new_following, unfollowed

def main():
    # Initialize colorama
    init(autoreset=True)
    
    print("")
    print(Fore.BLUE + "[#] Starting comparison..." + Style.RESET_ALL)
    time.sleep(1.5)
    print("")
    print(Fore.GREEN + "[+] Setting directory variable..." + Style.RESET_ALL)
    time.sleep(1.5)
    
    base_path = os.path.join(os.getcwd(), 'target')  # Define o diretório base como o diretório 'target' no diretório atual
    
    print(Fore.GREEN + "[+] Checking list of analyzed users..." + Style.RESET_ALL)
    time.sleep(1.5)
    print("")
    
    # List user directories
    users = list_directories(base_path)
    if not users:
        print(Fore.RED + "[#] No users found in ./target/" + Style.RESET_ALL)
        return
    
    # Select user
    print(Fore.BLUE + "[#] List of available users:" + Style.RESET_ALL)
    print("")
    for i, user in enumerate(users):
        print(f"{Fore.YELLOW}{i+1}. {user}{Style.RESET_ALL}")
        time.sleep(0.5)
    
    user_index = int(input(Fore.CYAN + "\n[?] Select the user number: " + Style.RESET_ALL)) - 1
    if user_index < 0 or user_index >= len(users):
        print("")
        print(Fore.RED + "[-] Invalid selection!" + Style.RESET_ALL)
        return
    
    selected_username = users[user_index]
    user_path = os.path.join(base_path, selected_username)
    
    # List analysis files
    files = list_files(user_path, "following_*.txt")
    if len(files) < 2:
        print("")
        print(Fore.RED + "[-] There are not enough analyses for comparison." + Style.RESET_ALL)
        return
    
    # Select files for comparison
    if len(files) > 2:
        print("")
        print(Fore.BLUE + "[#] Available files for comparison:" + Style.RESET_ALL)
        print("")
        for i, file in enumerate(files):
            filename = os.path.basename(file)
            file_date = datetime.strptime(re.search(r"following_(\d+)\.txt", filename).group(1), "%d%m%Y%H%M")
            print(f"{Fore.YELLOW}{i+1}. {filename} {Fore.BLUE}({file_date.strftime('%d/%m/%Y')}){Style.RESET_ALL}")
            time.sleep(0.5)
        
        file1_index = int(input(Fore.CYAN + "\n[?] Select the number of the first file: " + Style.RESET_ALL)) - 1
        file2_index = int(input(Fore.CYAN + "\n[?] Select the number of the second file: " + Style.RESET_ALL)) - 1
    else:
        file1_index = 0
        file2_index = 1
    
    if file1_index < 0 or file1_index >= len(files) or file2_index < 0 or file2_index >= len(files):
        print("")
        print(Fore.RED + "[-] Invalid selection!" + Style.RESET_ALL)
        return
    
    file1 = files[file1_index]
    file2 = files[file2_index]
    
    # Extract data from files
    user1, total_following1, following1, date1 = extract_data_from_file(file1)
    user2, total_following2, following2, date2 = extract_data_from_file(file2)
    
    # Check if the same user was analyzed
    if user1 != user2:
        print("")
        print(Fore.RED + "[-] The selected files belong to different users!" + Style.RESET_ALL)
        return
    
    # Comparison
    print("")
    print(Fore.BLUE + f"[#] Starting user comparison of {Fore.YELLOW}{user1}{Fore.BLUE}..." + Style.RESET_ALL)
    time.sleep(1)
    print("")
    
    new_following, unfollowed = compare_lists(following1, following2)
    
    if total_following1 != total_following2:
        print(Fore.GREEN + f"[+] The user {Fore.BLUE}{user1}{Fore.GREEN} followed {total_following1} people and now follows {total_following2} people." + Style.RESET_ALL)
        time.sleep(1)
        
        if new_following and unfollowed:
            print(Fore.GREEN + f"[+] This user stopped following {len(unfollowed)} person(s) and followed {len(new_following)} new person(s)." + Style.RESET_ALL)
            time.sleep(1)
            print(Fore.GREEN + f"[+] This user unfollowed these person(s): {Fore.BLUE}{', '.join(unfollowed)}{Fore.GREEN}." + Style.RESET_ALL)
            time.sleep(1)
            print(Fore.GREEN + f"[+] This user followed these person(s): {Fore.BLUE}{', '.join(new_following)}{Fore.GREEN}." + Style.RESET_ALL)
        elif new_following:
            print(Fore.GREEN + f"[+] This user followed {len(new_following)} new person(s): {Fore.BLUE}{', '.join(new_following)}{Fore.GREEN}." + Style.RESET_ALL)
        elif unfollowed:
            print(Fore.GREEN + f"[+] This user unfollowed {len(unfollowed)} person(s): {Fore.BLUE}{', '.join(unfollowed)}{Fore.GREEN}." + Style.RESET_ALL)
    else:
        print(Fore.GREEN + f"[+] The user {Fore.BLUE}{user1}{Fore.GREEN} remains following {total_following1} people." + Style.RESET_ALL)
    
    # Save the lists of changes
    if new_following or unfollowed:
        filename = f"changes_{datetime.now().strftime('%d%m%Y%H%M')}.txt"
        filepath = os.path.join(user_path, filename)
        with open(filepath, 'w') as f:
            if new_following:
                f.write("New followers:\n")
                f.write("\n".join(new_following))
                f.write("\n\n")
            if unfollowed:
                f.write("Unfollowed:\n")
                f.write("\n".join(unfollowed))
        print(Fore.GREEN + f"[+] Changes saved to: {Fore.BLUE}{filepath}" + Style.RESET_ALL)
        print("")
    else:
        print(Fore.RED + "[-] No changes in the following list." + Style.RESET_ALL)
        print("")

if __name__ == "__main__":
    main()