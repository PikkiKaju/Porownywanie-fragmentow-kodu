import os
import shutil

def change_files_extensions(directory):
    """Changes file extensions from .txt to .py in a given directory.

    Args:
        directory: The path to the directory containing the files.
    """

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            base_name = os.path.splitext(filename)[0]
            new_filename = base_name + ".py"
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            os.rename(old_path, new_path)


def change_files_extensions_c(directory):
    """Changes file extensions from .txt to .c in a given directory.

    Args:
        directory: The path to the directory containing the files.
    """

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            base_name = os.path.splitext(filename)[0]
            new_filename = base_name + ".c"
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            os.rename(old_path, new_path)


def move_files(source_path, new_path, num_files=11):
    """
    Places Python files from the source directory in a different one with each file in a separate folder.
    Args:
        source_path: The path to the directory containing Python the files.
        new_path: The path to the directory where the new Python files will be saved.
    """
    # Delete the old directory if it exists
    if os.path.exists(new_path):
        shutil.rmtree(new_path)

    # Create a new directory
    try:
        os.mkdir(new_path)
        print(f"Directory '{new_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{new_path}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{new_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Move files to the new directory
    for filename in os.listdir(source_path):
        if filename.endswith(".py"):
            base_name = os.path.splitext(filename)[0]
            new_filename = base_name + ".py"
            old_path = os.path.join(source_path, filename)
            new_folder_path = os.path.join(new_path, base_name)
            os.makedirs(new_folder_path, exist_ok=True)
            for i in range(1, num_files + 1):
                new_file_path = os.path.join(new_folder_path, f"{i}_{new_filename}")
                shutil.copy2(old_path, new_file_path)


def move_files_c(source_path, new_path, num_files=11):
    """
    Places C files from the source directory in a different one with each file in a separate folder.
    Args:
        source_path: The path to the directory containing the C files.
        new_path: The path to the directory where the new C files will be saved.
    """
    # Delete the old directory if it exists
    if os.path.exists(new_path):
        shutil.rmtree(new_path)

    # Create a new directory
    try:
        os.mkdir(new_path)
        print(f"Directory '{new_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{new_path}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{new_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Move files to the new directory
    for filename in os.listdir(source_path):
        if filename.endswith(".c"):
            base_name = os.path.splitext(filename)[0]
            new_filename = base_name + ".c"
            old_path = os.path.join(source_path, filename)
            new_folder_path = os.path.join(new_path, base_name)
            os.makedirs(new_folder_path, exist_ok=True)
            for i in range(1, num_files + 1):
                new_file_path = os.path.join(new_folder_path, f"{i}_{new_filename}")
                #shutil.copy2(old_path, new_file_path)
                # Read the file and filter out lines with #include
                with open(old_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                # Write the filtered content to the new file
                with open(new_file_path, 'w', encoding='utf-8') as new_file:
                    new_file.writelines(lines)


if __name__ == "__main__":
    num_files = 11

    source_path_python = "data/txt_python_files"
    new_path_python = "data/python_files"
    change_files_extensions(source_path_python)
    move_files(source_path_python, new_path_python, num_files=num_files)
    print(f"Python file extensions changed in {source_path_python} to .py and saved in {new_path_python} in separate folders.")

    source_path_c = "data/txt_c_files"
    new_path_c = "data/c_files"
    change_files_extensions_c(source_path_c)
    move_files_c(source_path_c, new_path_c, num_files=num_files)
    print(f"C file extensions changed in {source_path_c} to .c and saved in {new_path_c} in separate folders.")
