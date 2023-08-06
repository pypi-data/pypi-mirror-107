import torch_trafo as trafo
import torch


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def test1():
    # ID sequence as input data
    x = torch.tensor([
        [4, 3, 0, 1, 2],
        [0, 2, 5, 1, 3]
    ]).to(device)
    b, t = x.shape  # 2,5
    n_ids = len(x.unique())  # 6

    # embedding layers
    dk = 4
    emb = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dk).to(device)

    # positional embedding
    penc = trafo.positional_encoding(n_seqlen=t, dim=dk, base=100)
    assert list(penc.shape) == [1, t, dk]

    # compute
    y = emb(x) + penc
    assert list(y.shape) == [b, t, dk]
