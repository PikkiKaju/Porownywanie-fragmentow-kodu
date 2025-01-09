import torch
import torch.nn as nn
import torch.nn.functional as F
import torch_geometric
from torch_geometric.nn import HeteroLinear, MLP
from torch_geometric.utils import softmax
from torch_scatter import scatter_add

from models.layers import HeteroEmbedding, HDHGConv

class HDHGN(nn.Module):
    """
    Heterogeneous Directed Hypergraph Network (HDHGN) model.
    """
    def __init__(self, num_types: int, vocab_sizes: dict, edge_vocab_size: int, embed_size: int, dim_size: int, 
                 num_layers: int, num_edge_heads: int, num_node_heads: int, num_heads: int, feed_sizes: list, 
                 dropout_rate: float):
        """
        Initialize the HDHGN model.

        Args:
            num_types (int): Number of node types.
            vocab_sizes (dict): Vocabulary sizes for each node type.
            edge_vocab_size (int): Vocabulary size for edge types.
            embed_size (int): Embedding size.
            dim_size (int): Dimension size.
            num_layers (int): Number of layers.
            num_edge_heads (int): Number of edge heads.
            num_node_heads (int): Number of node heads.
            num_heads (int): Number of attention heads.
            feed_sizes (list): Sizes of the feed-forward layers.
            dropout_rate (float): Dropout rate.
        """
        super(HDHGN, self).__init__()
        self.num_types = num_types
        self.vocab_sizes = vocab_sizes
        self.edge_vocab_size = edge_vocab_size
        self.embed_size = embed_size
        self.dim_size = dim_size
        self.num_layers = num_layers
        self.num_edge_heads = num_edge_heads
        self.num_node_heads = num_node_heads
        self.num_heads = num_heads
        self.feed_sizes = feed_sizes
        self.dropout_rate = dropout_rate

        self.embedding = HeteroEmbedding(self.num_types, self.vocab_sizes, self.embed_size)
        self.hetero_linear = HeteroLinear(self.embed_size, self.dim_size, self.num_types)
        self.edge_embedding = nn.Embedding(self.edge_vocab_size, self.embed_size, padding_idx=0)

        self.HPHG = nn.ModuleList(
            [HDHGConv(self.dim_size, self.num_edge_heads, self.num_node_heads) for i in
             range(self.num_layers)])
        self.attn = nn.Parameter(
            torch.Tensor(1, self.num_heads, self.dim_size // self.num_heads))
        self.mlp = MLP(self.feed_sizes, act="elu", dropout=self.dropout_rate, norm="batch_norm")

        self.reset_parameters()

    def reset_parameters(self):
        """
        Reset the parameters of the model.
        """
        nn.init.xavier_uniform_(self.attn)

    def forward(self, x: torch.Tensor, types: torch.Tensor, edge_types: torch.Tensor, 
                edge_in_out_indexs: torch.Tensor, edge_in_out_head_tail: torch.Tensor, batch: torch.Tensor):
        """
        Forward pass of the model.

        Args:
            x (torch.Tensor): Node features.
            types (torch.Tensor): Node types.
            edge_types (torch.Tensor): Edge types.
            edge_in_out_indexs (torch.Tensor): Edge in-out indices.
            edge_in_out_head_tail (torch.Tensor): Edge head-tail indices.
            batch (torch.Tensor): Batch indices.

        Returns:
            torch.Tensor: Output of the model.
        """
        # x, types [num_nodes] edge_types [num_edges] edge_in_out_indexs [2, num_nodeedges]
        x = self.embedding(x, types)
        # x [num_nodes, embed_size]
        x = self.hetero_linear(x, types)
        # x [num_nodes, dim_size]
        edge_attr = self.edge_embedding(edge_types)
        # edge_attr [num_edges, dim_size]
        for i in range(self.num_layers):
            x = self.HPHG[i](x, edge_attr, edge_in_out_indexs, edge_in_out_head_tail, batch)

        x = x.reshape(-1, self.num_heads, self.dim_size // self.num_heads)
        attn = (self.attn * x).sum(dim=-1)
        # attn [num_nodes, num_heads]
        attn_score = softmax(attn, batch)
        attn_score = attn_score.unsqueeze(-1)
        # attn_score [num_nodes, num_heads, 1]
        x = x * attn_score
        v = scatter_add(x, batch, 0)
        # v [batch_size, num_heads, head_size]
        v = v.reshape(-1, self.dim_size)
        # v [batch_size, dim_size]
        out = self.mlp(v)
        # out [batch_size, label_size]
        
        return out
