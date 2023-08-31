import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import json
import datetime
import glob

log_file = "cleanup_log.txt"
config_file = "config.json"

# Read default options from config file
with open(config_file, "r") as config:
    default_options = json.load(config)

def kill_processes(process_names):
    deleted_files = []
    for process_name in process_names:
        print(f"Killing {process_name}...")
        result = subprocess.run(['taskkill', '/F', '/IM', process_name], capture_output=True, text=True)
        if result.returncode == 0:
            deleted_files.append(f"Killed: {process_name}")
    return deleted_files

def clear_cache(cache_paths):
    deleted_files = []
    for cache_path in cache_paths:
        if os.path.exists(cache_path):
            if os.path.isdir(cache_path):
                print(f"Clearing cache directory: {cache_path}")
                deleted_files.extend(list_files_in_directory(cache_path))
                for root, dirs, files in os.walk(cache_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                        deleted_files.append(f"Deleted: {file_path}")
            else:
                print(f"Removing cache file: {cache_path}")
                os.remove(cache_path)
                deleted_files.append(f"Deleted: {cache_path}")
    return deleted_files

def clear_cookies(cookie_paths):
    deleted_files = []
    for cookie_path in cookie_paths:
        if os.path.exists(cookie_path):
            print(f"Removing cookie file: {cookie_path}")
            os.remove(cookie_path)
            deleted_files.append(f"Deleted: {cookie_path}")
    return deleted_files

def list_files_in_directory(directory):
    deleted_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            deleted_files.append(f"Deleted: {file_path}")
    return deleted_files

def apply_actions():
    selected_actions = []
    deleted_files = []

    if java_var.get():
        selected_actions.extend(['javaw.exe', 'java.exe'])
    if ie_var.get():
        selected_actions.append('iexplore.exe')
    if edge_var.get():
        selected_actions.append('msedge.exe')
    if chrome_var.get():
        selected_actions.append('chrome.exe')
    if firefox_var.get():
        selected_actions.append('firefox.exe')

    deleted_files.extend(kill_processes(selected_actions))

    if clear_java_cache_var.get():
        print("Clearing Java Cache...")
        result = subprocess.run(['javaws', '-uninstall'], capture_output=True, text=True)
        if result.returncode == 0:
            deleted_files.append("Deleted: Java Cache")

    if clear_ie_temp_var.get():
        print("Clearing IE Temporary Files and Cookies...")
        result = subprocess.run(['RunDll32.exe', 'InetCpl.cpl,ClearMyTracksByProcess', '255'], capture_output=True, text=True)
        if result.returncode == 0:
            deleted_files.append("Deleted: IE Temporary Files and Cookies")

    if clear_edge_cache_var.get():
        edge_cache_path = os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.MicrosoftEdge_*', 'AC', 'MicrosoftEdge', 'Cache')
        edge_cookie_path = os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.MicrosoftEdge_*', 'AC', 'MicrosoftEdge', 'Cookies')

        # Include the Edge cache directory and additional cache directories
        edge_cache_paths = [
            edge_cache_path,
            os.path.join(os.environ['LocalAppData'], 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
            # Add more cache directories here if needed
        ]

        print("Clearing Edge Cache and Cookies...")
        deleted_files.extend(clear_cache(edge_cache_paths))
        deleted_files.extend(clear_cookies([edge_cookie_path]))

    if clear_chrome_cache_var.get():
        chrome_cache_path = os.path.join(os.environ['LocalAppData'], 'Google', 'Chrome', 'User Data', 'Default', 'Cache')
        chrome_cookie_path = os.path.join(os.environ['LocalAppData'], 'Google', 'Chrome', 'User Data', 'Default', 'Cookies')
        print("Clearing Chrome Cache and Cookies...")
        deleted_files.extend(clear_cache([chrome_cache_path]))
        deleted_files.extend(clear_cookies([chrome_cookie_path]))

    if clear_firefox_cache_var.get():
        firefox_cache_path = os.path.join(os.environ['LocalAppData'], 'Mozilla', 'Firefox', 'Profiles', '*', 'cache2')
        firefox_cookie_path = os.path.join(os.environ['LocalAppData'], 'Mozilla', 'Firefox', 'Profiles', '*', 'cookies.sqlite')
        print("Clearing Firefox Cache and Cookies...")
        deleted_files.extend(clear_cache([firefox_cache_path]))
        deleted_files.extend(clear_cookies([firefox_cookie_path]))

    log_deleted_files(deleted_files)
    messagebox.showinfo('Done', 'Actions applied successfully!')

def log_deleted_files(deleted_files):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as log:
        log.write(f"Log Timestamp: {timestamp}\n")
        for action in deleted_files:
            log.write(action + "\n")
        log.write("\n")


# Create GUI
root = tk.Tk()
root.title("CacheW Cleanup Script")

java_var = tk.IntVar(value=default_options["java"])
ie_var = tk.IntVar(value=default_options["ie"])
edge_var = tk.IntVar(value=default_options["edge"])
chrome_var = tk.IntVar(value=default_options["chrome"])
firefox_var = tk.IntVar(value=default_options["firefox"])
clear_java_cache_var = tk.IntVar(value=default_options["clear_java_cache"])
clear_ie_temp_var = tk.IntVar(value=default_options["clear_ie_temp"])
clear_edge_cache_var = tk.IntVar(value=default_options["clear_edge_cache"])
clear_chrome_cache_var = tk.IntVar(value=default_options["clear_chrome_cache"])
clear_firefox_cache_var = tk.IntVar(value=default_options["clear_firefox_cache"])

java_checkbox = tk.Checkbutton(root, text='Kill Java Applications', variable=java_var)
ie_checkbox = tk.Checkbutton(root, text='Kill Internet Explorer', variable=ie_var)
edge_checkbox = tk.Checkbutton(root, text='Kill Microsoft Edge', variable=edge_var)
chrome_checkbox = tk.Checkbutton(root, text='Kill Google Chrome', variable=chrome_var)
firefox_checkbox = tk.Checkbutton(root, text='Kill Firefox', variable=firefox_var)
clear_java_cache_checkbox = tk.Checkbutton(root, text='Clear Java Cache', variable=clear_java_cache_var)
clear_ie_temp_checkbox = tk.Checkbutton(root, text='Clear IE Temporary Files and Cookies', variable=clear_ie_temp_var)
clear_edge_cache_checkbox = tk.Checkbutton(root, text='Clear Edge Cache and Cookies', variable=clear_edge_cache_var)
clear_chrome_cache_checkbox = tk.Checkbutton(root, text='Clear Chrome Cache and Cookies', variable=clear_chrome_cache_var)
clear_firefox_cache_checkbox = tk.Checkbutton(root, text='Clear Firefox Cache and Cookies', variable=clear_firefox_cache_var)

apply_button = tk.Button(root, text='Apply Actions', command=apply_actions)

java_checkbox.pack(anchor='w')
ie_checkbox.pack(anchor='w')
edge_checkbox.pack(anchor='w')
chrome_checkbox.pack(anchor='w')
firefox_checkbox.pack(anchor='w')
clear_java_cache_checkbox.pack(anchor='w')
clear_ie_temp_checkbox.pack(anchor='w')
clear_edge_cache_checkbox.pack(anchor='w')
clear_chrome_cache_checkbox.pack(anchor='w')
clear_firefox_cache_checkbox.pack(anchor='w')
apply_button.pack()

root.mainloop()
