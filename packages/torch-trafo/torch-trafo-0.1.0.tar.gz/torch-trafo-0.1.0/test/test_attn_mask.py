import torch_trafo as trafo
import torch


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def test1():
    t = 4
    mask = trafo.attn_mask.attn_mask_causal(t, device)
    assert mask.dtype == torch.bool
    for i in range(t):
        for j in range(t):
            assert bool(i > j) == bool(mask[i][j])


def test1b():
    t = 4
    mask = trafo.attn_mask.get('causal', t, device)
    assert mask.dtype == torch.bool
    for i in range(t):
        for j in range(t):
            assert bool(i > j) == bool(mask[i][j])


def test2():
    t = 4
    mask = trafo.attn_mask.attn_mask_autoreg(t, device)
    assert mask.dtype == torch.bool
    for i in range(t):
        for j in range(t):
            assert bool(i >= j) == bool(mask[i][j])


def test2b():
    t = 4
    mask = trafo.attn_mask.get('autoreg', t, device)
    assert mask.dtype == torch.bool
    for i in range(t):
        for j in range(t):
            assert bool(i >= j) == bool(mask[i][j])


def test3():
    t = 4
    mask = trafo.attn_mask.attn_mask_backward(t, device)
    assert mask.dtype == torch.bool
    for i in range(t):
        for j in range(t):
            assert bool(i <= j) == bool(mask[i][j])


def test3b():
    t = 4
    mask = trafo.attn_mask.get('backward', t, device)
    assert mask.dtype == torch.bool
    for i in range(t):
        for j in range(t):
            assert bool(i <= j) == bool(mask[i][j])
