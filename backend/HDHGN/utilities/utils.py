import numpy as np
import random
import matplotlib
import ast
from pycparser import c_parser, c_ast, parse_file

matplotlib.use('Agg')
from matplotlib import pyplot as plt

def show_score(score_list: list, yname: str, train_name: str, color: str, save_path: str, show=False):
    """
    Plot and save a single score over epochs.

    Args:
        score_list (list): List of scores.
        yname (str): Label for the y-axis.
        train_name (str): Name of the training.
        color (str): Color of the plot.
        save_path (str): Path to save the plot.
    """
    score_list = np.array(score_list)
    plt.xlabel('Epoch')
    plt.ylabel(yname)
    plt.plot(score_list, color=color, label=train_name)
    plt.xlim((-0.5, len(score_list) - 0.5))
    plt.xticks(np.arange(0, len(score_list), 1))
    plt.legend(loc=1)
    plt.grid()
    plt.savefig(save_path)
    if show:
        plt.show()
        plt.clf()

def show_2scores(score_list1: list, score_list2: list, yname: str, train_name1: str, train_name2: str, color1: str, color2: str, save_path: str, show=False):
    """
    Plot and save two scores over epochs.

    Args:
        score_list1 (list): List of scores for the first training.
        score_list2 (list): List of scores for the second training.
        yname (str): Label for the y-axis.
        train_name1 (str): Name of the first training.
        train_name2 (str): Name of the second training.
        color1 (str): Color of the first plot.
        color2 (str): Color of the second plot.
        save_path (str): Path to save the plot.
    """
    score_list1 = np.array(score_list1)
    score_list2 = np.array(score_list2)
    plt.xlabel('Epoch')
    plt.ylabel(yname)
    plt.plot(score_list1, color=color1, label=train_name1)
    plt.plot(score_list2, color=color2, label=train_name2)
    plt.xlim((-0.5, len(score_list2) - 0.5))
    plt.xticks(np.arange(0, len(score_list2), 1))
    plt.legend(loc=1)
    plt.grid()
    plt.savefig(save_path)
    if show:
        plt.show()
        plt.clf()

def pre_walk_tree(node: ast.AST, index: int, edge_index: int):
    """
    Pre-walk the Python AST and extract features.

    Args:
        node (ast.AST): The AST node.
        index (int): The current node index.
        edge_index (int): The current edge index.

    Returns:
        tuple: A tuple containing the updated indices, types, features, edge types, and edge indices.
    """
    types = []
    features = []
    edge_types = []
    edge_in_out_indexs_s, edge_in_out_indexs_t = [], []
    edge_in_out_head_tail = []

    child_index = index + 1
    types.append("ast")

    features.append(str(type(node)))

    for field_name, field in ast.iter_fields(node):
        if isinstance(field, ast.AST):
            edge_types.append(field_name)
            edge_in_out_indexs_s.extend([edge_index, edge_index])
            edge_in_out_indexs_t.extend([index, child_index])
            edge_in_out_head_tail.extend([0, 1])
            child_edge_index = edge_index + 1
            child_index, child_edge_index, child_types, child_features, child_edge_types, child_edge_in_out_indexs_s, child_edge_in_out_indexs_t, child_edge_in_out_head_tail = pre_walk_tree(
                field, child_index, child_edge_index)
            types.extend(child_types)
            features.extend(child_features)
            edge_types.extend(child_edge_types)
            edge_in_out_indexs_s.extend(child_edge_in_out_indexs_s)
            edge_in_out_indexs_t.extend(child_edge_in_out_indexs_t)
            edge_in_out_head_tail.extend(child_edge_in_out_head_tail)
            edge_index = child_edge_index
        elif isinstance(field, list) and field and isinstance(field[0], ast.AST):
            edge_types.append(field_name)
            edge_in_out_indexs_s.append(edge_index)
            edge_in_out_indexs_t.append(index)
            edge_in_out_head_tail.append(0)
            child_edge_index = edge_index + 1
            for item in field:
                edge_in_out_indexs_s.append(edge_index)
                edge_in_out_indexs_t.append(child_index)
                edge_in_out_head_tail.append(1)
                child_index, child_edge_index, child_types, child_features, child_edge_types, child_edge_in_out_indexs_s, child_edge_in_out_indexs_t, child_edge_in_out_head_tail = pre_walk_tree(item, child_index, child_edge_index)
                types.extend(child_types)
                features.extend(child_features)
                edge_types.extend(child_edge_types)
                edge_in_out_indexs_s.extend(child_edge_in_out_indexs_s)
                edge_in_out_indexs_t.extend(child_edge_in_out_indexs_t)
                edge_in_out_head_tail.extend(child_edge_in_out_head_tail)
            edge_index = child_edge_index
        elif isinstance(field, list) and field:
            edge_types.append(field_name)
            edge_in_out_indexs_s.append(edge_index)
            edge_in_out_indexs_t.append(index)
            edge_in_out_head_tail.append(0)
            for item in field:
                types.append("ident")
                features.append(str(item))
                edge_in_out_indexs_s.append(edge_index)
                edge_in_out_indexs_t.append(child_index)
                edge_in_out_head_tail.append(1)
                child_index += 1
            edge_index += 1
        elif field:
            edge_types.append(field_name)
            edge_in_out_indexs_s.append(edge_index)
            edge_in_out_indexs_t.append(index)
            edge_in_out_head_tail.append(0)
            types.append("ident")
            features.append(str(field))
            edge_in_out_indexs_s.append(edge_index)
            edge_in_out_indexs_t.append(child_index)
            edge_in_out_head_tail.append(1)
            child_index += 1
            edge_index += 1

    return child_index, edge_index, types, features, edge_types, edge_in_out_indexs_s, edge_in_out_indexs_t, edge_in_out_head_tail


def pre_walk_tree_c(node, index, edge_index):
    """
    Pre-walk the C AST and extract features.

    Args:
        node (c_ast.Node): The AST node.
        index (int): The current node index.
        edge_index (int): The current edge index.

    Returns:
        tuple: A tuple containing the updated indices, types, features, edge types, and edge indices.
    """
    types = []
    features = []
    edge_types = []
    edge_in_out_indexs_s, edge_in_out_indexs_t = [], []
    edge_in_out_head_tail = []

    child_index = index + 1
    types.append("ast")

    features.append(str(type(node)))

    for field_name, field in node.children():
        if isinstance(field, c_ast.Node):
            edge_types.append(field_name)
            edge_in_out_indexs_s.extend([edge_index, edge_index])
            edge_in_out_indexs_t.extend([index, child_index])
            edge_in_out_head_tail.extend([0, 1])
            child_edge_index = edge_index + 1
            child_index, child_edge_index, child_types, child_features, child_edge_types, child_edge_in_out_indexs_s, child_edge_in_out_indexs_t, child_edge_in_out_head_tail = pre_walk_tree_c(
                field, child_index, child_edge_index)
            types.extend(child_types)
            features.extend(child_features)
            edge_types.extend(child_edge_types)
            edge_in_out_indexs_s.extend(child_edge_in_out_indexs_s)
            edge_in_out_indexs_t.extend(child_edge_in_out_indexs_t)
            edge_in_out_head_tail.extend(child_edge_in_out_head_tail)
            edge_index = child_edge_index
        elif isinstance(field, list) and field and isinstance(field[0], c_ast.Node):
            edge_types.append(field_name)
            edge_in_out_indexs_s.append(edge_index)
            edge_in_out_indexs_t.append(index)
            edge_in_out_head_tail.append(0)
            child_edge_index = edge_index + 1
            for item in field:
                edge_in_out_indexs_s.append(edge_index)
                edge_in_out_indexs_t.append(child_index)
                edge_in_out_head_tail.append(1)
                child_index, child_edge_index, child_types, child_features, child_edge_types, child_edge_in_out_indexs_s, child_edge_in_out_indexs_t, child_edge_in_out_head_tail = pre_walk_tree_c(
                    item, child_index, child_edge_index)
                types.extend(child_types)
                features.extend(child_features)
                edge_types.extend(child_edge_types)
                edge_in_out_indexs_s.extend(child_edge_in_out_indexs_s)
                edge_in_out_indexs_t.extend(child_edge_in_out_indexs_t)
                edge_in_out_head_tail.extend(child_edge_in_out_head_tail)
            edge_index = child_edge_index
        elif isinstance(field, list) and field:
            edge_types.append(field_name)
            edge_in_out_indexs_s.append(edge_index)
            edge_in_out_indexs_t.append(index)
            edge_in_out_head_tail.append(0)
            for item in field:
                types.append("ident")
                features.append(str(item))
                edge_in_out_indexs_s.append(edge_index)
                edge_in_out_indexs_t.append(child_index)
                edge_in_out_head_tail.append(1)
                child_index += 1
            edge_index += 1
        elif field:
            edge_types.append(field_name)
            edge_in_out_indexs_s.append(edge_index)
            edge_in_out_indexs_t.append(index)
            edge_in_out_head_tail.append(0)
            types.append("ident")
            features.append(str(field))
            edge_in_out_indexs_s.append(edge_index)
            edge_in_out_indexs_t.append(child_index)
            edge_in_out_head_tail.append(1)
            child_index += 1
            edge_index += 1

    return child_index, edge_index, types, features, edge_types, edge_in_out_indexs_s, edge_in_out_indexs_t, edge_in_out_head_tail
