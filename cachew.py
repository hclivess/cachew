import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import json
import datetime

log_file = "cleanup_log.txt"
config_file = "config.json"

default_config_data = {
  "java": True,
  "ie": True,
  "edge": True,
  "chrome": False,
  "firefox": False,
  "clear_java_cache": True,
  "clear_ie_temp": True,
  "clear_edge_cache": True,
  "clear_chrome_cache": False,
  "clear_firefox_cache": False
}

try:
    with open(config_file, "r") as config:
        default_options = json.load(config)
except FileNotFoundError:
    with open(config_file, "w") as config:
        json.dump(default_config_data, config, indent=4)
    default_options = default_config_data

def print_to_log_window(message):
    log_window.configure(state='normal')
    log_window.insert(tk.END, message + "\n")
    log_window.see(tk.END)
    log_window.configure(state='disabled')
    root.update_idletasks()

def kill_processes(process_names):
    deleted_files = []
    for process_name in process_names:
        print_to_log_window(f"Killing {process_name}...")
        result = subprocess.run(['taskkill', '/F', '/IM', process_name], capture_output=True, text=True)
        if result.returncode == 0:
            deleted_files.append(f"Killed: {process_name}")
    return deleted_files

def clear_cache(cache_paths):
    deleted_files = []
    for cache_path in cache_paths:
        if os.path.exists(cache_path):
            if os.path.isdir(cache_path):
                print_to_log_window(f"Clearing cache directory: {cache_path}")
                deleted_files.extend(list_files_in_directory(cache_path))
                for root_dir, dirs, files in os.walk(cache_path):
                    for file in files:
                        file_path = os.path.join(root_dir, file)
                        os.remove(file_path)
                        deleted_files.append(f"Deleted: {file_path}")
            else:
                print_to_log_window(f"Removing cache file: {cache_path}")
                os.remove(cache_path)
                deleted_files.append(f"Deleted: {cache_path}")
    return deleted_files

def clear_cookies(cookie_paths):
    deleted_files = []
    for cookie_path in cookie_paths:
        if os.path.exists(cookie_path):
            print_to_log_window(f"Removing cookie file: {cookie_path}")
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
        print_to_log_window("Clearing Java Cache...")
        result = subprocess.run(['javaws', '-uninstall'], capture_output=True, text=True)
        if result.returncode == 0:
            deleted_files.append("Deleted: Java Cache")

    if clear_ie_temp_var.get():
        print_to_log_window("Clearing IE Temporary Files and Cookies...")
        result = subprocess.run(['RunDll32.exe', 'InetCpl.cpl,ClearMyTracksByProcess', '255'], capture_output=True, text=True)
        if result.returncode == 0:
            deleted_files.append("Deleted: IE Temporary Files and Cookies")

    if clear_edge_cache_var.get():
        edge_cache_path = os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.MicrosoftEdge_*', 'AC', 'MicrosoftEdge', 'Cache')
        edge_cookie_path = os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.MicrosoftEdge_*', 'AC', 'MicrosoftEdge', 'Cookies')

        edge_cache_paths = [
            edge_cache_path,
            os.path.join(os.environ['LocalAppData'], 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
        ]

        print_to_log_window("Clearing Edge Cache and Cookies...")
        deleted_files.extend(clear_cache(edge_cache_paths))
        deleted_files.extend(clear_cookies([edge_cookie_path]))

    if clear_chrome_cache_var.get():
        chrome_cache_path = os.path.join(os.environ['LocalAppData'], 'Google', 'Chrome', 'User Data', 'Default', 'Cache')
        chrome_cookie_path = os.path.join(os.environ['LocalAppData'], 'Google', 'Chrome', 'User Data', 'Default', 'Cookies')

        print_to_log_window("Clearing Chrome Cache and Cookies...")
        deleted_files.extend(clear_cache([chrome_cache_path]))
        deleted_files.extend(clear_cookies([chrome_cookie_path]))

    if clear_firefox_cache_var.get():
        firefox_cache_path = os.path.join(os.environ['LocalAppData'], 'Mozilla', 'Firefox', 'Profiles')
        firefox_cache_path = os.path.join(firefox_cache_path, os.listdir(firefox_cache_path)[0], 'cache2')

        print_to_log_window("Clearing Firefox Cache...")
        deleted_files.extend(clear_cache([firefox_cache_path]))

    print_to_log_window("Cleanup completed.")
    with open(log_file, 'a') as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n{timestamp}\n")
        for line in deleted_files:
            f.write(line + "\n")

root = tk.Tk()
root.title('CacheW Cleanup Utility')

log_window = tk.Text(root, wrap='word', height=15, width=50)
log_window.configure(state='disabled')
log_window.pack()

java_var = tk.BooleanVar(value=default_options["java"])
ie_var = tk.BooleanVar(value=default_options["ie"])
edge_var = tk.BooleanVar(value=default_options["edge"])
chrome_var = tk.BooleanVar(value=default_options["chrome"])
firefox_var = tk.BooleanVar(value=default_options["firefox"])
clear_java_cache_var = tk.BooleanVar(value=default_options["clear_java_cache"])
clear_ie_temp_var = tk.BooleanVar(value=default_options["clear_ie_temp"])
clear_edge_cache_var = tk.BooleanVar(value=default_options["clear_edge_cache"])
clear_chrome_cache_var = tk.BooleanVar(value=default_options["clear_chrome_cache"])
clear_firefox_cache_var = tk.BooleanVar(value=default_options["clear_firefox_cache"])

tk.Checkbutton(root, text='Java', variable=java_var).pack(anchor='w')
tk.Checkbutton(root, text='Internet Explorer', variable=ie_var).pack(anchor='w')
tk.Checkbutton(root, text='Edge', variable=edge_var).pack(anchor='w')
tk.Checkbutton(root, text='Chrome', variable=chrome_var).pack(anchor='w')
tk.Checkbutton(root, text='Firefox', variable=firefox_var).pack(anchor='w')
tk.Checkbutton(root, text='Clear Java cache', variable=clear_java_cache_var).pack(anchor='w')
tk.Checkbutton(root, text='Clear Internet Explorer temporary files', variable=clear_ie_temp_var).pack(anchor='w')
tk.Checkbutton(root, text='Clear Edge cache', variable=clear_edge_cache_var).pack(anchor='w')
tk.Checkbutton(root, text='Clear Chrome cache', variable=clear_chrome_cache_var).pack(anchor='w')
tk.Checkbutton(root, text='Clear Firefox cache', variable=clear_firefox_cache_var).pack(anchor='w')

tk.Button(root, text='Apply', command=apply_actions).pack(side='left', expand=True, fill='x')
tk.Button(root, text='Exit', command=root.destroy).pack(side='right', expand=True, fill='x')

root.mainloop()
