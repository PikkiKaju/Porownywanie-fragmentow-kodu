import os
from sklearn.model_selection import train_test_split
import ast
from pycparser import c_parser, c_ast, parse_file

def splitdata(source_files_path: str):
    """
    Split the dataset into training, validation, and test sets.

    Reads Python source files from the specified directory, parses them to ensure they are syntactically correct,
    and then splits the dataset. The file paths for each set are saved to separate text files.

    The source files directory should have the following structure:
        **source_files** \n
        ├⫟ **label1** \n
        │   ├─ file1.py \n
        │   ├─ file2.py \n
        │   └─ ... \n
        ├⫟ **label2** \n
        │   ├─ file3.py \n
        │   ├─ file4.py \n
        │   └─ ... \n
        └─ ... \n

    Args:
        dir_path (str): Path to the directory containing the Python source files.
    """

    files_paths = []
    labels = []
    for root, dir, files in os.walk(source_files_path):
        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                code = open(file_path, encoding='utf-8').read()
                try:
                    ast.parse(code)
                    files_paths.append('../' + file_path.replace("\\", "/"))
                    labels.append(root)
                except SyntaxError:
                    print(f"Syntax error in file: {file_path}. File will be ignored.")
                    pass

    # Split the dataset into training, validation, and test sets
    train_files_paths, vt_files_paths, train_labels, vt_labels = train_test_split(files_paths, labels, test_size=0.4)#, stratify=labels)
    valid_files_paths, test_files_paths, valid_labels, test_labels = train_test_split(vt_files_paths, vt_labels, test_size=0.5)#, stratify=vt_labels)
    
    # Save the file paths to text files
    train_file = open("data/train_files_paths.txt", "w+")
    valid_file = open("data/valid_files_paths.txt", "w+")
    test_file = open("data/test_files_paths.txt", "w+")
    for train_file_path in train_files_paths:
        train_file.write(train_file_path)
        train_file.write("\n")

    for valid_file_path in valid_files_paths:
        valid_file.write(valid_file_path)
        valid_file.write("\n")

    for test_file_path in test_files_paths:
        test_file.write(test_file_path)
        test_file.write("\n")

    train_file.close()
    valid_file.close()
    test_file.close()
    print("Finished splitting Python data \n")


def splitdata_c(source_files_path: str):
    """
    Split the dataset into training, validation, and test sets.

    Reads C source files from the specified directory, parses them to ensure they are syntactically correct,
    and then splits the dataset. The file paths for each set are saved to separate text files.

    The source files directory should have the following structure:
        **source_files** \n
        ├⫟ **label1** \n
        │   ├─ file1.c \n
        │   ├─ file2.c \n
        │   └─ ... \n
        ├⫟ **label2** \n
        │   ├─ file3.c \n
        │   ├─ file4.c \n
        │   └─ ... \n
        └─ ... \n

    Args:
        dir_path (str): Path to the directory containing the C source files.
    """

    files_paths = []
    labels = []
    for root, dir, files in os.walk(source_files_path):
        for file_name in files:
            if file_name.endswith('.c'):
                file_path = os.path.join(root, file_name)
                try:
                    parse_file(file_path, use_cpp=True, cpp_path="clang", cpp_args=["-E", "-I" + "./utilities/fake_libc_include", "-std=c99"])
                    files_paths.append('./' + file_path.replace("\\", "/"))
                    labels.append(root)
                except c_parser.ParseError as e:
                    print(f"Syntax error in file: {file_path}. File will be ignored. Error: {e}")
                    pass
                except Exception as e:
                    print(f"Failed to process file: {file_path}. Error: {e}")
                    pass


    # Split the dataset into training, validation, and test sets
    train_files_paths, vt_files_paths, train_labels, vt_labels = train_test_split(files_paths, labels, test_size=0.4)#, stratify=labels)
    valid_files_paths, test_files_paths, valid_labels, test_labels = train_test_split(vt_files_paths, vt_labels, test_size=0.5)#, stratify=vt_labels)

    # Save the file paths to text files
    train_file = open("data/train_files_paths_c.txt", "w+")
    valid_file = open("data/valid_files_paths_c.txt", "w+")
    test_file = open("data/test_files_paths_c.txt", "w+")
    for train_file_path in train_files_paths:
        train_file.write(train_file_path)
        train_file.write("\n")

    for valid_file_path in valid_files_paths:
        valid_file.write(valid_file_path)
        valid_file.write("\n")

    for test_file_path in test_files_paths:
        test_file.write(test_file_path)
        test_file.write("\n")

    train_file.close()
    valid_file.close()
    test_file.close()
    print("Finished splitting C data \n")

if __name__ == '__main__':
    print("Start splitting Python data...")
    source_files_path = "data/python_files"
    splitdata(source_files_path)
    print("Start spliting C data...")
    source_files_path_c = "data/c_files"
    splitdata_c(source_files_path_c)
