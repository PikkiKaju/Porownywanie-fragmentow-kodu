import sys
import shutil
import os
from colorama import Fore, Style

def clear_train_directories():
    items_to_delete = [
        "./work_dir",
        "./data/test",
        "./data/test_c",
        "./data/train",
        "./data/train_c",
        "./data/valid",
        "./data/valid_c",
        "./data/test_files_paths.txt",
        "./data/test_files_paths_c.txt",
        "./data/train_files_paths.txt",
        "./data/train_files_paths_c.txt",
        "./data/valid_files_paths.txt",
        "./data/valid_files_paths_c.txt",
        "./data/vocab4ast.json",
        "./data/vocab4ast_c.json"
    ]

    print(Fore.GREEN + "Clearing train directories:" + Style.RESET_ALL)

    # delete directories and files
    for item_to_delete in items_to_delete:
        if os.path.isdir(item_to_delete):
            try:
                shutil.rmtree(item_to_delete)
                print(f"Directory '{item_to_delete}' deleted successfully.")
            except FileNotFoundError:
                print(f"Directory '{item_to_delete}' not found.")
            except OSError as e:
                print(f"Error deleting directory '{item_to_delete}': {e}")

        elif os.path.isfile(item_to_delete):
            try:
                os.remove(item_to_delete)
                print(f"File '{item_to_delete}' deleted successfully.")
            except FileNotFoundError:
                print(f"File '{item_to_delete}' not found.")
            except OSError as e:
                print(f"Error deleting file '{item_to_delete}': {e}")  
        
    # Verify if directories and files are deleted
    for item_to_delete in items_to_delete:
        if os.path.exists(item_to_delete):
            print(f"Item '{item_to_delete}' was not deleted. Check permissions or other processes using it.")
            break
    else:
        print("All items have been successfully deleted. \n")


if __name__ == '__main__':
    clear_train_directories()

