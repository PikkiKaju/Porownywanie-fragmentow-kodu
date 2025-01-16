import argparse
import torch
import ast

from models.HDHGN import HDHGN
from MyDataset import HDHGData
from utilities.vocab import Vocab
from utilities.utils import pre_walk_tree


# Initialize argument parser
parser = argparse.ArgumentParser()

# Adding optional arguments
parser.add_argument("-mp", "--model_path", help = "Path to the pre-trained model", type = str, default = "work_dir/HDHGN/HDHGN.pt")
parser.add_argument("-vp", "--vocab_path", help = "Path to the vocabulary file", type = str, default = "data/vocab4ast.json")
parser.add_argument("-fp", "--file_path", help = "Path to the file to be predicted", type = str, default = "data/additional/file_to_test.py")


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
        print(f"Model output: {output}")
        prediction = torch.argmax(output, dim=-1)
        print(f"Prediction index: {prediction}")
    
    # Decode prediction
    label = vocab.vocab["labels"].id2word[prediction.item()]
    probabilities = torch.nn.functional.softmax(output, dim=-1)
    return output, probabilities, label

if __name__ == '__main__':
    model_path = args.model_path
    vocab_path = args.vocab_path
    file_to_test = args.file_path
    print("Making predictions...")
    output, probabilities, label = predict(file_to_test, model_path, vocab_path)
    print(f"The output for the file is: {output}")
    print(f"The probabilities for each label are: {probabilities}")
    print(f"The predicted label for the file is: {label}")
