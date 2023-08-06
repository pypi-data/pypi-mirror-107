import torch_trafo as trafo
import torch


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def test01():
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

    # attention layer
    mk = 7  # hidden neurons of the projection layers prj_q and prj_k
    mv = 8  # hidden neurons of the projection layer prj_v; Is the output dim
    att = trafo.MhaQKV(
        model_dim=mk, kdim=dk, output_dim=mv).to(device)

    # overwrite params
    for name, param in emb.named_parameters():
        param.data[:] = 1
    for name, param in att.named_parameters():
        param.data[:] = 1

    # forward pass
    y = emb(x)
    assert list(y.shape) == [b, t, dk]
    z = att(query=y, key=y, value=y)
    assert list(z.shape) == [b, t, mv]
    assert (z == 4).all()

    # check model
    for name, param in att.named_parameters():
        assert name in [
            'prj_q.weight', 'prj_k.weight', 'prj_v.weight']
    # check projection layer
    assert list(att.prj_q.weight.shape) == [mk, dk]
    assert list(att.prj_k.weight.shape) == [mk, dk]
    assert list(att.prj_v.weight.shape) == [mv, dk]


def test02():
    # ID sequence as input data
    x = torch.tensor([
        [4, 3, 0, 1, 2],
        [0, 2, 5, 1, 3]
    ]).to(device)
    b, t = x.shape  # 2,5
    n_ids = len(x.unique())  # 6

    # embedding layers
    dk = 4
    emb_k = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dk).to(device)
    emb_q = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dk).to(device)
    dv = 3
    emb_v = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dv).to(device)

    # attention layer
    mk = 7  # hidden neurons of the projection layers prj_q and prj_k
    mv = 8  # hidden neurons of the projection layer prj_v; Is the output dim
    att = trafo.MhaQKV(
        model_dim=mk, kdim=dk, output_dim=mv, vdim=dv).to(device)

    # overwrite params
    for name, param in emb_q.named_parameters():
        param.data[:] = 1
    for name, param in emb_k.named_parameters():
        param.data[:] = 1
    for name, param in emb_v.named_parameters():
        param.data[:] = 1
    for name, param in att.named_parameters():
        param.data[:] = 1

    # forward pass
    q = emb_q(x)
    k = emb_k(x)
    v = emb_v(x)
    assert list(q.shape) == [b, t, dk]
    assert list(k.shape) == [b, t, dk]
    assert list(v.shape) == [b, t, dv]

    z = att(query=q, key=k, value=v)
    assert list(z.shape) == [b, t, mv]
    assert (z == 3).all()

    # check model
    for name, param in att.named_parameters():
        assert name in [
            'prj_q.weight', 'prj_k.weight', 'prj_v.weight']
    # check projection layer
    assert list(att.prj_q.weight.shape) == [mk, dk]
    assert list(att.prj_k.weight.shape) == [mk, dk]
    assert list(att.prj_v.weight.shape) == [mv, dv]

    # causal mask
    mask = trafo.attn_mask.get('causal', t)
    z2 = att(query=q, key=k, value=v, mask=mask)
    assert list(z2.shape) == [b, t, mv]
    assert (z2 == 3).all()


def test03():
    # ID sequence as input data
    x = torch.tensor([
        [4, 3, 0, 1, 2],
        [0, 2, 5, 1, 3]
    ]).to(device)
    b, t = x.shape  # 2,5
    n_ids = len(x.unique())  # 6

    # embedding layers
    dk = 4
    emb_k = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dk).to(device)
    emb_q = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dk).to(device)
    dv = 3
    emb_v = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dv).to(device)

    # attention layer
    mk = 7  # hidden neurons of the projection layers prj_q and prj_k
    mv = 8  # hidden neurons of the projection layer prj_v; Is the output dim
    bias_qkv = True
    dropout_attn = 0.0
    att = trafo.MhaQKV(
        model_dim=mk, kdim=dk, output_dim=mv, vdim=dv,
        bias_qkv=bias_qkv, dropout_attn=dropout_attn).to(device)

    # overwrite params
    for name, param in emb_q.named_parameters():
        param.data[:] = 1
    for name, param in emb_k.named_parameters():
        param.data[:] = 1
    for name, param in emb_v.named_parameters():
        param.data[:] = 1
    for name, param in att.named_parameters():
        param.data[:] = 1

    # forward pass
    q = emb_q(x)
    k = emb_k(x)
    v = emb_v(x)
    assert list(q.shape) == [b, t, dk]
    assert list(k.shape) == [b, t, dk]
    assert list(v.shape) == [b, t, dv]

    z = att(query=q, key=k, value=v)
    assert list(z.shape) == [b, t, mv]
    assert (z == 4).all()

    # check model
    for name, param in att.named_parameters():
        assert name in [
            'prj_q.weight', 'prj_k.weight', 'prj_v.weight',
            'prj_q.bias', 'prj_k.bias', 'prj_v.bias']
    # check projection layer
    assert list(att.prj_q.weight.shape) == [mk, dk]
    assert list(att.prj_k.weight.shape) == [mk, dk]
    assert list(att.prj_v.weight.shape) == [mv, dv]

    assert list(att.prj_q.bias.shape) == [mk]
    assert list(att.prj_k.bias.shape) == [mk]
    assert list(att.prj_v.bias.shape) == [mv]


"""
def test04():
    # ID sequence as input data
    x = torch.tensor([
        [4, 3, 0, 1, 2],
        [0, 2, 5, 1, 3]
    ]).to(device)
    b, t = x.shape  # 2,5
    n_ids = len(x.unique())  # 6

    # embedding layers
    dk = 4
    emb_k = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dk).to(device)
    emb_q = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dk).to(device)
    dv = 3
    emb_v = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dv).to(device)

    # attention layer
    mk = 8
    bias_qkv = True
    att1 = trafo.MhaQKV(
        model_dim=mk, kdim=dk, vdim=dv,
        bias_qkv=bias_qkv).to(device)
    # pytorch MHA
    att2 = torch.nn.MultiheadAttention(
        embed_dim=mk, num_heads=mk // dk, kdim=dk, vdim=dv,
        bias=bias_qkv).to(device)

    # forward pass
    q = emb_q(x)
    k = emb_k(x)
    v = emb_v(x)
    assert list(q.shape) == [b, t, dk]
    assert list(k.shape) == [b, t, dk]
    assert list(v.shape) == [b, t, dv]

    z1 = att1(query=q, key=k, value=v)
    z2 = att2(
        query=q.transpose(0, 1),
        key=k.transpose(0, 1),
        value=v.transpose(0, 1))
    assert z1.tolist() == z2[0].tolist()

    assert list(z1.shape) == [b, t, mk]
    assert list(z2.shape) == [b, t, mk]
"""


def test13():
    # ID sequence as input data
    x = torch.tensor([
        [4, 3, 0, 1, 2],
        [0, 2, 5, 1, 3]
    ]).to(device)
    b, t = x.shape  # 2,5
    n_ids = len(x.unique())  # 6

    # embedding layers
    dk = 4
    emb_kv = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dk).to(device)
    emb_q = torch.nn.Embedding(
        num_embeddings=n_ids, embedding_dim=dk).to(device)

    # attention layer
    mk = 7  # hidden neurons of the projection layers prj_q and prj_k
    mv = 8  # hidden neurons of the projection layer prj_v; Is the output dim
    bias_qkv = True
    dropout_attn = 0.0
    att = trafo.MhaSource(
        model_dim=mk, kdim=dk, output_dim=mv,
        bias_qkv=bias_qkv, dropout_attn=dropout_attn).to(device)

    # overwrite params
    for name, param in emb_q.named_parameters():
        param.data[:] = 1
    for name, param in emb_kv.named_parameters():
        param.data[:] = 1
    for name, param in att.named_parameters():
        param.data[:] = 1

    # forward pass
    q = emb_q(x)
    kv = emb_kv(x)
    assert list(q.shape) == [b, t, dk]
    assert list(kv.shape) == [b, t, dk]

    z = att(query=q, x=kv)
    assert list(z.shape) == [b, t, mv]
    assert (z == 5).all()

    # check model
    for name, param in att.named_parameters():
        assert name in [
            'prj_q.weight', 'prj_k.weight', 'prj_v.weight',
            'prj_q.bias', 'prj_k.bias', 'prj_v.bias']
    # check projection layer
    assert list(att.prj_q.weight.shape) == [mk, dk]
    assert list(att.prj_k.weight.shape) == [mk, dk]
    assert list(att.prj_v.weight.shape) == [mv, dk]

    assert list(att.prj_q.bias.shape) == [mk]
    assert list(att.prj_k.bias.shape) == [mk]
    assert list(att.prj_v.bias.shape) == [mv]

    # causal mask
    mask = trafo.attn_mask.get('causal', t)
    z2 = att(query=q, x=kv, mask=mask)
    assert list(z2.shape) == [b, t, mv]
    assert (z2 == 5).all()


def test23():
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

    # attention layer
    mk = 7  # hidden neurons of the projection layers prj_q and prj_k
    mv = 8  # hidden neurons of the projection layer prj_v; Is the output dim
    bias_qkv = True
    dropout_attn = 0.0
    att = trafo.MhaSelf(
        model_dim=mk, kdim=dk, output_dim=mv,
        bias_qkv=bias_qkv, dropout_attn=dropout_attn).to(device)

    # overwrite params
    for name, param in emb.named_parameters():
        param.data[:] = 1
    for name, param in att.named_parameters():
        param.data[:] = 1

    # forward pass
    y = emb(x)
    assert list(y.shape) == [b, t, dk]

    z = att(y)
    assert list(z.shape) == [b, t, mv]
    assert (z == 5).all()

    # check model
    for name, param in att.named_parameters():
        assert name in [
            'prj_q.weight', 'prj_k.weight', 'prj_v.weight',
            'prj_q.bias', 'prj_k.bias', 'prj_v.bias']
    # check projection layer
    assert list(att.prj_q.weight.shape) == [mk, dk]
    assert list(att.prj_k.weight.shape) == [mk, dk]
    assert list(att.prj_v.weight.shape) == [mv, dk]

    assert list(att.prj_q.bias.shape) == [mk]
    assert list(att.prj_k.bias.shape) == [mk]
    assert list(att.prj_v.bias.shape) == [mv]

    # causal mask
    mask = trafo.attn_mask.get('causal', t)
    z2 = att(y, mask=mask)
    assert list(z2.shape) == [b, t, mv]
    assert (z2 == 5).all()
