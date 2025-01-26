import sys
import os
import argparse
import torch
import ast
from colorama import Fore, Style
from pycparser import c_parser, parse_file

sys.path.append(os.path.dirname(__file__))

from HDHGN.MyDataset import HDHGData
from HDHGN.vocab import Vocab
from HDHGN.utilities.utils import pre_walk_tree, pre_walk_tree_c


def predict(file_path: str, model_path = "", vocab_path = ""):
    """
    Predict the label for a given file using a pre-trained model.

    Args:
        file_path (str): Path to the file to be predicted.
        model_path (str): Path to the pre-trained model.
        vocab_path (str): Path to the vocabulary file.

    Returns:
        [(str, float, float)]: List of tuples containing the label, similarity value, and probability.
        str: The type of file that was predicted (Python or C).
    """
    python_parsed = False # Tells if the file was parsed as a Python file
    c_parsed = False # Tells if the file was parsed as a C file

    # Process the file
    file_path = file_path.strip()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            None
    except FileNotFoundError:
        print(Fore.RED + "Error: The file could not be found: " + Style.RESET_ALL + file_path )
        return None, None

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            root = ast.parse(file.read())
        index, edge_index, types, features, edge_types, edge_in_out_indexs_s, edge_in_out_indexs_t, edge_in_out_head_tail = pre_walk_tree(root, 0, 0)

        vocab_path = os.path.join(os.path.dirname(__file__), "data/vocab4ast.json")
        model_path = os.path.join(os.path.dirname(__file__), "work_dir/HDHGN/HDHGN.pt")
        python_parsed = True
    except SyntaxError:
        print("The file could not be parsed as Python code due to a unknown syntax error.")
    except Exception as e:
        print("The file could not be parsed as Python code:")
        print(e)

    if not python_parsed:
        try:
            fake_lib_path = os.path.join(os.path.dirname(__file__), "utilities/fake_libc_include")  
            root = parse_file(file_path, use_cpp=True, cpp_path="clang", cpp_args=["-E", f"-I{fake_lib_path}", "-std=c99"])
            index, edge_index, types, features, edge_types, edge_in_out_indexs_s, edge_in_out_indexs_t, edge_in_out_head_tail = pre_walk_tree_c(root, 0, 0)

            vocab_path = os.path.join(os.path.dirname(__file__), "data/vocab4ast_c.json")
            model_path = os.path.join(os.path.dirname(__file__), "work_dir/HDHGN_C/HDHGN_C.pt")
            c_parsed = True
        except c_parser.ParseError:
            print("The file could not be parsed as C code due to a parsing error.")
        except Exception as e:
            print("The file could not be parsed as C code:")
            print(e)

    if not python_parsed and not c_parsed:
        print(Fore.RED + "Error: The file could not be processed as either Python or C code." + Style.RESET_ALL)
        return None, None
    else:
        print(Fore.GREEN + "Predicting " + Fore.LIGHTBLUE_EX + ("Python" if python_parsed else "C") + Fore.GREEN + " file..." + Style.RESET_ALL)

    # Load vocab
    vocab = Vocab.load(vocab_path)
    
    # Load model
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)
    model = torch.load(model_path)
    model = model.to(device)
    model.eval()

    # Encode types, features, and edge types
    types_encoded = [vocab.vocab["types"].word2id[t] for t in types]
    types_encoded = torch.tensor(types_encoded, dtype=torch.long)
    features_encoded = [vocab.vocab[types[i]].word2id.get(f, 1) for (i, f) in enumerate(features)]
    features_encoded = torch.tensor(features_encoded, dtype=torch.long)
    edge_types_encoded = [vocab.vocab["edge_types"].word2id.get(e, 1) for e in edge_types]
    edge_types_encoded = torch.tensor(edge_types_encoded, dtype=torch.long)
    edge_in_out_indexs_encoded = torch.tensor([edge_in_out_indexs_s, edge_in_out_indexs_t], dtype=torch.long)
    edge_in_out_head_tail_encoded = torch.tensor(edge_in_out_head_tail, dtype=torch.long)
    
    # Create data object
    data = HDHGData(x=features_encoded, types=types_encoded, edge_types=edge_types_encoded,
                    edge_in_out_indexs=edge_in_out_indexs_encoded, edge_in_out_head_tail=edge_in_out_head_tail_encoded)
    data.batch = torch.zeros(data.x.size(0), dtype=torch.long)  # Add batch index
    data = data.to(device)
    
    # Make prediction
    with torch.no_grad():
        output = model(data.x, data.types, data.edge_types, data.edge_in_out_indexs, data.edge_in_out_head_tail, data.batch)
        probabilities = torch.nn.functional.softmax(output, dim=-1)

    # Decode predictions
    labels = list(vocab.vocab["labels"].word2id.keys())

    sorted_indices = torch.argsort(output, descending=True)
    sorted_labels = [labels[i] for i in sorted_indices[0]]
    sorted_values = [output[0][i].item() for i in sorted_indices[0]]
    sorted_probabilities = torch.sort(probabilities, descending=True).values

    # Create output frame
    output_frame = []
    for label, value, probability in zip(sorted_labels, sorted_values, sorted_probabilities[0]):
        output_frame.append((label, value, probability.item()))

    print("Done predicting.")
    return output_frame, "Python" if python_parsed else "C"


if __name__ == '__main__':
    # Initialize argument parser
    parser = argparse.ArgumentParser(prog="PredictFile", description="Predict the label for a given file using a pre-trained model.")

    # Adding optional arguments
    parser.add_argument("-fp", "--file_path", help = "Path to the file to be predicted", type = str, required=True)
    parser.add_argument("-mp", "--model_path", help = "Path to the pre-trained model", type = str, default="")
    parser.add_argument("-vp", "--vocab_path", help = "Path to the vocabulary file", type = str, default="")
    parser.add_argument("-s", "--show_output", help = "Whether to show the probabilities for each label or not", type=bool, action = argparse.BooleanOptionalAction, default = False)

    # Read arguments from command line
    args = parser.parse_args()

    print(Fore.GREEN + "Making predictions..." + Style.RESET_ALL, end="\n", flush=True)
    model_path = args.model_path
    vocab_path = args.vocab_path
    file_to_test = args.file_path

    output_frame, file_type = predict(file_to_test, model_path, vocab_path)
    if output_frame is not None:
        label = output_frame[0][0]
        print(f"The predicted label for the file " + Fore.LIGHTBLUE_EX + os.path.basename(args.file_path) + Style.RESET_ALL + " is: " +  Fore.GREEN + label + Style.RESET_ALL)
        if args.show_output:
            print("\nSorted labels with probability values:")
            for label, value, probability in output_frame:
                print(f"{label:<30} {value:.2f}  {probability:.4f}")
