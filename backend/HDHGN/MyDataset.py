import os
import ast
from pycparser import c_parser, c_ast, parse_file
import torch
from torch_geometric.data import Dataset, Data

from utilities.utils import pre_walk_tree, pre_walk_tree_c
from vocab import Vocab

class HDHGData(Data):
    """
    Custom data class for HDHGN model.
    """
    def __init__(self, x=None, edge_types=None, **kwargs):
        super(HDHGData, self).__init__(x, edge_types=edge_types, **kwargs)

    def __inc__(self, key: str, value: int, *args, **kwargs):
        """
        Increment function for edge indices.
        """
        if key == 'edge_in_out_indexs':
            return torch.tensor([[self.edge_types.size(0)], [self.x.size(0)]])
        else:
            return super().__inc__(key, value, *args, **kwargs)

class HDHGNDataset(Dataset):
    """
    Custom dataset class for HDHGN Python model.
    """
    def __init__(self, root: str, paths_file_path: str, vocab: Vocab):
        """
        Initialize the Python dataset.

        Args:
            root (str): Root directory where the Python dataset should be saved.
            paths_file_path (str): Path to the file containing paths of the Python source files.
            vocab (Vocab): Python Vocabulary object.
        """
        self.paths_file_path = paths_file_path
        self.vocab = vocab
        self.processed_file_names_list = []

        # Read file paths and create processed file names list
        paths_file = open(self.paths_file_path)
        for i, file_path in enumerate(paths_file):
            self.processed_file_names_list.append(f"processed_data_{i}.pt")
        paths_file.close()

        super().__init__(root, transform=None, pre_transform=None, pre_filter=None)

    @property
    def processed_file_names(self):
        """
        Return the list of processed file names.
        """
        return self.processed_file_names_list

    def process(self):
        """
        Process the source files and save the processed data.
        """
        paths_file = open(self.paths_file_path)
        for i, file_path in enumerate(paths_file):
            file_path = "../" + file_path.strip()
            file = open(file_path, encoding="utf-8")
            code = file.read()

            root = ast.parse(code)
            index, edge_index, types, features, edge_types, edge_in_out_indexs_s, edge_in_out_indexs_t, edge_in_out_head_tail = pre_walk_tree(
                root, 0, 0)
            types_encoded = [self.vocab.vocab["types"].word2id[t] for t in types]
            types_encoded = torch.tensor(types_encoded, dtype=torch.long)
            features_encoded = [self.vocab.vocab[types[i]].word2id.get(f, 1) for (i, f) in enumerate(features)]
            features_encoded = torch.tensor(features_encoded, dtype=torch.long)
            edge_types_encoded = [self.vocab.vocab["edge_types"].word2id.get(e, 1) for e in edge_types]
            edge_types_encoded = torch.tensor(edge_types_encoded, dtype=torch.long)
            edge_in_out_indexs_encoded = torch.tensor([edge_in_out_indexs_s, edge_in_out_indexs_t], dtype=torch.long)
            edge_in_out_head_tail_encoded = torch.tensor(edge_in_out_head_tail, dtype=torch.long)
            file_path = file_path.strip()
            labels = torch.tensor([self.vocab.vocab["labels"].word2id[file_path.split("/")[-2]]], dtype=torch.long)

            d = HDHGData(x=features_encoded, types=types_encoded, edge_types=edge_types_encoded,
                         edge_in_out_indexs=edge_in_out_indexs_encoded,
                         edge_in_out_head_tail=edge_in_out_head_tail_encoded, labels=labels)

            torch.save(d, os.path.join(self.processed_dir, f"processed_data_{i}.pt"))

        paths_file.close()

    def len(self):
        """
        Return the length of the dataset.
        """
        return len(self.processed_file_names)

    def get(self, idx: int):
        """
        Get the data object at the specified index.

        Args:
            idx (int): Index of the data object to retrieve.

        Returns:
            HDHGData: Data object at the specified index.
        """
        import warnings
        warnings.simplefilter(action='ignore', category=FutureWarning)
        d = torch.load(os.path.join(self.processed_dir, f'processed_data_{idx}.pt'))
        return d


class HDHGNDataset_C(Dataset):
    """
    Custom dataset class for HDHGN C model.
    """
    def __init__(self, root: str, paths_file_path: str, vocab: Vocab):
        """
        Initialize the C dataset.

        Args:
            root (str): Root directory where the C dataset should be saved.
            paths_file_path (str): Path to the file containing paths of the C source files.
            vocab (Vocab): C Vocabulary object.
        """
        self.paths_file_path = paths_file_path
        self.vocab = vocab
        self.processed_file_names_list = []

        # Read file paths and create processed file names list
        paths_file = open(self.paths_file_path)
        for i, file_path in enumerate(paths_file):
            self.processed_file_names_list.append(f"processed_data_{i}.pt")
        paths_file.close()

        super().__init__(root, transform=None, pre_transform=None, pre_filter=None)

    @property
    def processed_file_names(self):
        """
        Return the list of processed file names.
        """
        return self.processed_file_names_list

    def process(self):
        """
        Process the source files and save the processed data.
        """
        paths_file = open(self.paths_file_path)
        for i, file_path in enumerate(paths_file):
            file_path = "../" + file_path.strip()
            root = parse_file(file_path, use_cpp=True, cpp_path="clang", cpp_args=["-E", "-I" + "../utilities/fake_libc_include", "-std=c99"])
            index, edge_index, types, features, edge_types, edge_in_out_indexs_s, edge_in_out_indexs_t, edge_in_out_head_tail = pre_walk_tree_c(
                root, 0, 0)
            types_encoded = [self.vocab.vocab["types"].word2id[t] for t in types]
            types_encoded = torch.tensor(types_encoded, dtype=torch.long)
            features_encoded = [self.vocab.vocab[types[i]].word2id.get(f, 1) for (i, f) in enumerate(features)]
            features_encoded = torch.tensor(features_encoded, dtype=torch.long)
            edge_types_encoded = [self.vocab.vocab["edge_types"].word2id.get(e, 1) for e in edge_types]
            edge_types_encoded = torch.tensor(edge_types_encoded, dtype=torch.long)
            edge_in_out_indexs_encoded = torch.tensor([edge_in_out_indexs_s, edge_in_out_indexs_t], dtype=torch.long)
            edge_in_out_head_tail_encoded = torch.tensor(edge_in_out_head_tail, dtype=torch.long)
            labels = torch.tensor([self.vocab.vocab["labels"].word2id[file_path.split("/")[-2]]], dtype=torch.long)

            d = HDHGData(x=features_encoded, types=types_encoded, edge_types=edge_types_encoded,
                         edge_in_out_indexs=edge_in_out_indexs_encoded,
                         edge_in_out_head_tail=edge_in_out_head_tail_encoded, labels=labels)

            torch.save(d, os.path.join(self.processed_dir, f"processed_data_{i}.pt"))

        paths_file.close()

    def len(self):
        """
        Return the length of the dataset.
        """
        return len(self.processed_file_names)

    def get(self, idx):
        """
        Get the data object at the specified index.

        Args:
            idx (int): Index of the data object to retrieve.

        Returns:
            HDHGData: Data object at the specified index.
        """
        import warnings
        warnings.simplefilter(action='ignore', category=FutureWarning)
        d = torch.load(os.path.join(self.processed_dir, f'processed_data_{idx}.pt'))
        return d