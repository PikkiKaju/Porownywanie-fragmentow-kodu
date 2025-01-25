import argparse
import ast
from pycparser import c_parser, c_ast, parse_file
from collections import Counter
from colorama import Fore, Style
import json
from os.path import abspath

from utilities.utils import pre_walk_tree, pre_walk_tree_c


class VocabEntry:
    """
    A class to represent a vocabulary entry.
    """
    def __init__(self, word2id=None, entry_class="not_label"):
        if word2id:
            self.word2id = word2id
        elif entry_class == "labels" or entry_class == "types":
            self.word2id = {}
        else:
            self.word2id = {'<pad>': 0, '<unk>': 1}

        self.id2word = {v: k for k, v in self.word2id.items()}

    def add(self, word):
        """
        Add a word to the vocabulary.

        Args:
            word (str): The word to add.

        Returns:
            int: The ID of the word.
        """
        if word not in self.word2id:
            wid = self.word2id[word] = len(self.word2id)
            self.id2word[wid] = word
            return wid
        else:
            return self.word2id[word]

class Vocab:
    """
    A class to represent a vocabulary.
    """
    def __init__(self, vocab):
        self.vocab = vocab

    @staticmethod
    def build_for_ast(paths_file_path: str):
        """
        Build a vocabulary for ASTs from the given Python file paths.

        Args:
            paths_file_path (str): Path to the Python file containing paths of the source files.

        Returns:
            Vocab: The built vocabulary for Python.
        """
        paths_file = open(paths_file_path)

        tokens = {"types": [], "edge_types": [], "labels": []}
        for file_path in paths_file:
            file = open(file_path[3:-1], encoding="utf-8")
            code = file.read()
            try:
                root = ast.parse(code)
                index, edge_index, types, features, edge_types, edge_in_out_indexs_s, edge_in_out_indexs_t, edge_in_out_head_tail = pre_walk_tree(root, 0, 0)
                for (type, feature) in zip(types, features):
                    if type in tokens:
                        tokens[type].append(feature)
                    else:
                        tokens[type] = [feature]
                tokens["types"].extend(types)
                tokens["edge_types"].extend(edge_types)
                tokens["labels"].append(file_path.split('/')[-2])
            except SyntaxError:
                print(f"Syntax error in file: {file_path} while building Python vocabulary. File will be ignored.")
                pass
            file.close()

        vocab = {}
        for f in tokens:
            tokens_count = dict(Counter(tokens[f]).most_common())
            token_vocab = VocabEntry(entry_class=f)
            for token in tokens_count:
                if tokens_count[token] >= 1:
                    token_vocab.add(token)
            vocab[f] = token_vocab

        paths_file.close()
        return Vocab(vocab)

    @staticmethod
    def build_for_ast_c(paths_file_path: str):
        """
        Build a vocabulary for ASTs from the given C file paths.

        Args:
            paths_file_path (str): Path to the C file containing paths of the source files.

        Returns:
            Vocab: The built vocabulary for C.
        """
        paths_file = open(paths_file_path)

        tokens = {"types": [], "edge_types": [], "labels": []}
        for file_path in paths_file:
            try:
                root = parse_file(file_path.strip(), use_cpp=True, cpp_path="clang", cpp_args=["-E", "-I" + "./utilities/fake_libc_include", "-std=c99"])
                index, edge_index, types, features, edge_types, edge_in_out_indexs_s, edge_in_out_indexs_t, edge_in_out_head_tail = pre_walk_tree_c(root, 0, 0)
                for (type, feature) in zip(types, features):
                    if type in tokens:
                        tokens[type].append(feature)
                    else:
                        tokens[type] = [feature]
                tokens["types"].extend(types)
                tokens["edge_types"].extend(edge_types)
                tokens["labels"].append(file_path.split('/')[-2])
            except c_parser.ParseError:
                print(f"Syntax error in file: {file_path} while building C vocabulary. File will be ignored.")
                pass

        vocab = {}
        for f in tokens:
            tokens_count = dict(Counter(tokens[f]).most_common())
            token_vocab = VocabEntry(entry_class=f)
            for token in tokens_count:
                if tokens_count[token] >= 1:
                    token_vocab.add(token)
            vocab[f] = token_vocab

        paths_file.close()
        return Vocab(vocab)

    def save(self, file_path: str):
        """
        Save the vocabulary to a file.

        Args:
            file_path (str): Path to the file where the vocabulary will be saved.
        """
        json.dump({t: self.vocab[t].word2id for t in self.vocab}, open(file_path, 'w'), indent=2)

    @staticmethod
    def load(file_path: str):
        """
        Load a vocabulary from a file.

        Args:
            file_path (str): Path to the file containing the vocabulary.

        Returns:
            Vocab: The loaded vocabulary.
        """
        entry = json.load(open(file_path, 'r'))
        vocab = {}
        for e in entry:
            vocab[e] = VocabEntry(entry[e])
        return Vocab(vocab)


if __name__ == '__main__':
    # Initialize argument parser
    parser = argparse.ArgumentParser(prog="MakeVocab", description="Make vocabularies based on the source files.")

    # Adding optional arguments
    parser.add_argument("-p", action=argparse.BooleanOptionalAction, help = "Wheter to make the vocab for the Python files or not", dest="make_Python_vocab", type = bool, default = False)
    parser.add_argument("-c", action=argparse.BooleanOptionalAction, help = "Wheter to make the vocab for the C files or not", dest="make_C_vocab", type = bool, default = False)

    # Read arguments from command line
    args = parser.parse_args()

    print(Fore.GREEN + "Building vocabularies:" + Style.RESET_ALL)
    if not args.make_Python_vocab and not args.make_C_vocab:
        print("Specify which files to process. Use the -p or -c flag.")
    if args.make_Python_vocab:
        print("Start building vocab for Python...")
        v1 = Vocab.build_for_ast("data/train_files_paths.txt")
        v1.save("data/vocab4ast.json")
        print("Finished building Python vocabulary \n")
    if args.make_C_vocab:
        print("Start building vocab for C...")
        v2 = Vocab.build_for_ast_c("data/train_files_paths_c.txt")
        v2.save("data/vocab4ast_c.json")
        print("Finished building C vocabulary \n")
