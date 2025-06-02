import subprocess
import os
import shutil
def get_device_info():
    try:
        result = subprocess.run(
            ["adb", "shell", "getprop", "ro.product.brand"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error detecting device: {e}"
    
def get_device_folder(path="/sdcard"):
    """
    Fetch and clean the list of files/folders from a given path on Android device via ADB.
    Removes trailing slashes from folders for proper navigation.
    """
    try:
        output = subprocess.check_output(["adb", "shell", "ls", "-p", path], stderr=subprocess.STDOUT, text=True)
        entries = output.strip().split("\n")
        
        # Remove empty lines, remove any ANSI codes, and strip trailing slashes
        cleaned_entries = [entry.rstrip('/') for entry in entries if entry and entry not in [".", ".."]]
        
        return cleaned_entries
    except subprocess.CalledProcessError as e:
        print("ADB command failed:", e.output)
        return []
    except FileNotFoundError:
        return ["ADB not found - please install platform-tools and add to PATH"]
    
def extract_files(selected_items, specific_folder=None, specific_file=None):
    target_root = "output_data"
    os.makedirs(target_root, exist_ok=True)

    # If a specific file was selected
    if specific_file:
        if os.path.isfile(specific_file):
            shutil.copy2(specific_file, os.path.join(target_root, os.path.basename(specific_file)))
        return

    # If a specific folder was selected
    if specific_folder:
        if os.path.isdir(specific_folder):
            dest_folder = os.path.join(target_root, os.path.basename(specific_folder))
            shutil.copytree(specific_folder, dest_folder, dirs_exist_ok=True)
        return

    # Default: extract based on selected_items
    for item in selected_items:
        source_path = os.path.join("extracted_data", item)
        if os.path.exists(source_path):
            dest_path = os.path.join(target_root, item)
            if os.path.isdir(source_path):
                shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
            else:
                shutil.copy2(source_path, dest_path)

def get_call_logs():
    try:
        result = subprocess.run(
            ["adb", "shell", "content", "query", "--uri", "content://call_log/calls"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8'
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error fetching call logs: {e}"

def get_sms_messages():
    try:
        result = subprocess.run(
            ["adb", "shell", "content", "query", "--uri", "content://sms"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8'
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error fetching SMS messages: {e}"

def list_directory_contents(path):
    contents = []
    if not os.path.exists(path):
        return contents

    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            contents.append((item, "<DIR>", os.path.basename(path)))
        else:
            try:
                size = os.path.getsize(full_path)
                size_kb = f"{size / 1024:.2f} KB"
                contents.append((item, size_kb, os.path.basename(path)))
            except OSError:
                contents.append((item, "Unknown size", os.path.basename(path)))

    return contents
