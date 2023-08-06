import torch_trafo as trafo
import torch


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def test11():
    x = torch.tensor([
        [4, 3, 0, 1, 2],
        [0, 2, 5, 1, 3]
    ]).to(device)
    b, t = x.shape
    n_ids = len(x.unique())  # 6

    # causal mask
    mask = trafo.attn_mask.get('causal', t, device)

    # modeling
    dk = 4
    emb = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dk).to(device)

    mk = 7
    block = trafo.BlockQKV(
        mha_model_dim=mk, kdim=dk, ffn_expansion=1.5).to(device)

    # overwrite params
    for param in emb.parameters():
        param.data[:] = 1
    for param in block.parameters():
        param.data[:] = 1

    y = emb(x)
    assert list(y.shape) == [b, t, dk]

    z = block(y, y, y, mask=mask)
    assert list(z.shape) == [b, t, dk]
    # assert (z == 1).all()


def test12():
    # input data
    x = torch.tensor([
        [4, 3, 0, 1, 2],
        [0, 2, 4, 5, 6]
    ]).to(device)
    b, t = x.shape
    n_ids = len(x.unique())  # 7

    # dimensions
    dk = 4
    dv = 6

    # casual attn mask
    mask = trafo.attn_mask.get('causal', t, device)

    # network layers
    emb_q = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dk).to(device)
    emb_k = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dk).to(device)
    emb_v = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dv).to(device)

    mk = 8
    mv = 9
    norm_method = "scalenorm"
    block = trafo.BlockQKV(
        mha_model_dim=mk,
        kdim=dk,
        vdim=dv,
        mha_output_dim=mv,
        ffn_expansion=1.7,
        bias_qkv=True,
        bias_mhaout=False,
        bias_ffn=True,
        norm_position="pre",
        norm_method=norm_method,
        dropout_attn=0.1,
        dropout_mha=0.1,
        dropout_ffn=0.1
    ).to(device)

    # overwrite params
    for param in emb_q.parameters():
        param.data[:] = 1
    for param in emb_k.parameters():
        param.data[:] = 1
    for param in emb_v.parameters():
        param.data[:] = 1
    for param in block.parameters():
        param.data[:] = 1

    # forward pass
    q = emb_q(x)
    k = emb_k(x)
    v = emb_v(x)
    assert list(q.shape) == [b, t, dk]
    assert list(k.shape) == [b, t, dk]
    assert list(v.shape) == [b, t, dv]

    z = block(query=q, key=k, value=v, mask=mask)
    assert list(z.shape) == [b, t, dk]
    # assert (z == 1).all()

    # check 2
    for name, _ in block.named_parameters():
        assert name in [
            'attention.prj_q.weight', 'attention.prj_q.bias',
            'attention.prj_k.weight', 'attention.prj_k.bias',
            'attention.prj_v.weight', 'attention.prj_v.bias',
            'mha_fc.weight', 'mha_fc.bias',
            # 'norm1.weight', 'norm1.bias', 'norm1.radius',
            'norm1_q.weight', 'norm1_q.bias', 'norm1_q.radius',
            'norm1_k.weight', 'norm1_k.bias', 'norm1_k.radius',
            'norm1_v.weight', 'norm1_v.bias', 'norm1_v.radius',
            'feedforwardnet.0.weight', 'feedforwardnet.0.bias',
            'feedforwardnet.2.weight', 'feedforwardnet.2.bias',
            'norm2.weight', 'norm2.bias', 'norm2.radius']
    # checke projection layer
    assert list(block.attention.prj_q.weight.shape) == [mk, dk]
    assert list(block.attention.prj_k.weight.shape) == [mk, dk]
    assert list(block.attention.prj_v.weight.shape) == [mv, dv]

    assert list(block.attention.prj_q.bias.shape) == [mk]
    assert list(block.attention.prj_k.bias.shape) == [mk]
    assert list(block.attention.prj_v.bias.shape) == [mv]

    assert list(block.mha_fc.weight.shape) == [dk, mv]
    assert block.mha_fc.bias is None

    if norm_method == "scalenorm":
        assert list(block.norm1_q.weight) == [1]
        assert list(block.norm1_k.weight) == [1]
        assert list(block.norm1_v.weight) == [1]
    else:
        # assert list(block.norm1.weight.shape) == [dk]
        # assert list(block.norm1.bias.shape) == [dk]
        assert list(block.norm1_q.weight.shape) == [dk]
        assert list(block.norm1_q.bias.shape) == [dk]
        assert list(block.norm1_k.weight.shape) == [dk]
        assert list(block.norm1_k.bias.shape) == [dk]
        assert list(block.norm1_v.weight.shape) == [dv]
        assert list(block.norm1_v.bias.shape) == [dv]

    assert list(block.feedforwardnet[0].weight.shape) == [int(dk * 1.7), dk]
    assert list(block.feedforwardnet[0].bias.shape) == [int(dk * 1.7)]
    assert list(block.feedforwardnet[2].weight.shape) == [dk, int(dk * 1.7)]
    assert list(block.feedforwardnet[2].bias.shape) == [dk]

    if norm_method == "scalenorm":
        assert list(block.norm2.weight) == [1]
    else:
        assert list(block.norm2.weight.shape) == [dk]
        assert list(block.norm2.bias.shape) == [dk]


def test21():
    x = torch.tensor([
        [4, 3, 0, 1, 2],
        [0, 2, 5, 1, 3]
    ]).to(device)
    b, t = x.shape
    n_ids = len(x.unique())  # 6

    # causal mask
    mask = trafo.attn_mask.get('causal', t, device)

    # modeling
    dk = 4
    emb = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dk).to(device)

    mk = 7
    block = trafo.BlockSource(
        mha_model_dim=mk, kdim=dk, ffn_expansion=1.5).to(device)

    # overwrite params
    for param in emb.parameters():
        param.data[:] = 1
    for param in block.parameters():
        param.data[:] = 1

    y = emb(x)
    assert list(y.shape) == [b, t, dk]

    z = block(y, y, mask=mask)
    assert list(z.shape) == [b, t, dk]
    # assert (z == 1).all()


def test31():
    x = torch.tensor([
        [4, 3, 0, 1, 2],
        [0, 2, 5, 1, 3]
    ]).to(device)
    b, t = x.shape
    n_ids = len(x.unique())  # 6

    # causal mask
    mask = trafo.attn_mask.get('causal', t, device)

    # modeling
    dk = 4
    emb = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dk).to(device)

    mk = 7
    block = trafo.BlockSelf(
        mha_model_dim=mk, kdim=dk, ffn_expansion=1.5).to(device)

    # overwrite params
    for param in emb.parameters():
        param.data[:] = 1
    for param in block.parameters():
        param.data[:] = 1

    y = emb(x)
    assert list(y.shape) == [b, t, dk]

    z = block(y, mask=mask)
    assert list(z.shape) == [b, t, dk]
    # assert (z == 1).all()
