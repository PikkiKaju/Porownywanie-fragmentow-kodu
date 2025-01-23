import argparse
import torch
import ast
from colorama import Fore, Style

from MyDataset import HDHGData
from vocab import Vocab
from utilities.utils import pre_walk_tree


# Initialize argument parser
parser = argparse.ArgumentParser(prog="PredictFile", description="Predict the label for a given file using a pre-trained model.")

# Adding optional arguments
parser.add_argument("-fp", "--file_path", help = "Path to the file to be predicted", type = str, required=True)
parser.add_argument("-mp", "--model_path", help = "Path to the pre-trained model", type = str, default = "work_dir/HDHGN/HDHGN.pt")
parser.add_argument("-vp", "--vocab_path", help = "Path to the vocabulary file", type = str, default = "data/vocab4ast.json")
parser.add_argument("-s", "--show_output", help = "Whether to show the probabilities for each label or not", type=bool, action = argparse.BooleanOptionalAction, default = False)

# Read arguments from command line
args = parser.parse_args()


def predict(file_path: str, model_path: str, vocab_path: str):
    """
    Predict the label for a given file using a pre-trained model.

    Args:
        file_path (str): Path to the file to be predicted.
        model_path (str): Path to the pre-trained model.
        vocab_path (str): Path to the vocabulary file.

    Returns:
        torch.Tensor: Predicted output tensor.
        [(str, float, float)]: List of tuples containing the label, similarity value, and probability.
        str: Predicted label for the file.
    """
    # Load vocab
    vocab = Vocab.load(vocab_path)
    
    # Load model
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)
    model = torch.load(model_path)
    model = model.to(device)
    model.eval()
    
    # Process the file
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
    root = ast.parse(code)
    index, edge_index, types, features, edge_types, edge_in_out_indexs_s, edge_in_out_indexs_t, edge_in_out_head_tail = pre_walk_tree(root, 0, 0)
    
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
        # probabilities = torch.nn.functional.softmax(output, dim=-1)
        probabilities = torch.nn.functional.softmax(output)

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

    sorted_values_max = 0
    for value in sorted_values:
        if value > 0:
            sorted_values_max += value
    sorted_probabilities = (value / sorted_values_max for value in sorted_values)
    output_frame = []
    for label, value, probability in zip(sorted_labels, sorted_values, sorted_probabilities):
        output_frame.append((label, value, probability))

    return output_frame


if __name__ == '__main__':
    print(Fore.GREEN + "Making predictions..." + Style.RESET_ALL, flush=True)
    model_path = args.model_path
    vocab_path = args.vocab_path
    file_to_test = args.file_path

    output_frame = predict(file_to_test, model_path, vocab_path)
    label = output_frame[0][0]
    print(f"The predicted label for the file is: {label}")
    if args.show_output:
        print("\nSorted labels with probability values:")
        for label, value, probability in output_frame:
            print(f"{label:<30} {value:.2f}  {probability:.4f}")
