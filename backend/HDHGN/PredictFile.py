import torch
import ast

from models.HDHGN import HDHGN
from MyDataset import HDHGData
from utilities.vocab import Vocab
from utilities.utils import pre_walk_tree

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
    return label

if __name__ == '__main__':
    model_path = "work_dir/HDHGN/HDHGN.pt"
    vocab_path = "data/vocab4ast.json"
    file_to_test = "data/additional/file_to_test.py"
    print("Making predictions...")
    label = predict(file_to_test, model_path, vocab_path)
    print(f"The predicted label for the file is: {label}")
