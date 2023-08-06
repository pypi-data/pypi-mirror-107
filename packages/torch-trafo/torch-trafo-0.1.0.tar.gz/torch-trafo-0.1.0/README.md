[![PyPI version](https://badge.fury.io/py/torch-trafo.svg)](https://badge.fury.io/py/torch-trafo)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/ulf1/torch-trafo.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ulf1/torch-trafo/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ulf1/torch-trafo.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ulf1/torch-trafo/context:python)
[![torch-trafo](https://snyk.io/advisor/python/torch-trafo/badge.svg)](https://snyk.io/advisor/python/torch-trafo)


# torch-trafo
PyTorch implementation of transformer layers.

## Introduction

### Motivation
The purposes of this repository [torch-trafo](https://pypi.org/project/torch-trafo) is to code the Transformer-Modell from scratch, i.e. it exists for educational reasons. 


### Data Format Conventions
All classes are "batch first", i.e. inputs, outputs, values, queries and keys have the tensor dimension `[batch_size, seq_len, dim]`.

### Folders Structure
The folders are organized as follows:

```
|- torch_trafo
    |- attention.py     Multi-Head Attention
    |- block.py         Transformer Block
    |- stack.py         Encoder, Decoder
    |- tasks.py         Standard models from literature, e.g. MLM, NMT
|- tasks-to-learn       Demo Jupyter Notebooks to show how to train standard models
|- experimental         Jupyter notebooks as technical reports on new models
```

### Modules and Classes
We implemented three types of classes mainly to avoid unnecessary copying of input variables.

- `*Self` classes: If all three input variables (query, keys, value) are just copies of the same single input variable (e.g. an input sequence) then it is called "Simple Self-Attention". For example, the BERT language model, or the Encoder in [seminal Transformer paper](https://arxiv.org/abs/1706.03762) are using just one type of input sequence. For educational purposes, the formulas of the "Simple Self-Attention" are easier to comprehend.
- `*Source` classes: A "Source Transformer" has two inputs. One input is used as keys as well as values (i.e. the database), and the second input are the queries. An examples is the decoder in the [seminal Transformer paper](https://arxiv.org/abs/1706.03762).
- `*QKV` classes: In theory, an attention mechanism can have three distinct input variables. 


| Module | Description | 1 Input <br> `query == key == value` <br> (Self-Attn. Tr.) | 2 Inputs <br> `query != key == value` <br> (Source-Attn. Tr.) | 3 Inputs <br> `query != key != value` |
|:------:|:------:|:-------:|:--------:|:--------:|
| `attention.py` | Multi-Head Attention | `MhaSelf` | `MhaSource` | `MhaQKV` |
| `block.py` | Transformer Block w. MHA & FFN | `BlockSelf` | `BlockSource` | `BlockQKV` |
| `stack.py` | Stacked Transformer Blocks | `StackSelf` | `StackSource` | `StackQKV` |

The modules are basically different onions shells.
A transformer **stack** consists of multiple transformer **blocks**, 
which in turn consist of a multi-head **attention** mechanism and a FNN.

### List of classes and functions
- `trafo.Mha*` (attention.py): The Multihead-Attention (MHA) layer
- `trafo.Block*` (block.py): The TransformerBlock of MHA layer and FFN layer
- `trafo.Stack*` (stack.py): Multiple blocks stacked, e.g. DecoderStack, EncoderStack


## Usage

### MHA with Causal Mask

```py
import torch_trafo as trafo
import torch
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Dataset
x = torch.tensor([
    [4, 3, 0, 1, 2],
    [0, 2, 5, 1, 3]
]).to(device)
batch_size, n_seqlen = x.shape  
n_ids = len(x.unique())  # Number of IDs in your VOCAB

# Settings
kdim = 4               # Num. of features in `query` and `key`
model_dim = 8 * kdim   # dimension of the projection layers `prj_q` and `prj_k`

# Modeling
emb = torch.nn.Embedding(num_embeddings=n_ids, embedding_dim=kdim).to(device)
penc = trafo.positional_encoding(seqlen=n_seqlen, dim=kdim, base=100)
att = trafo.MhaQKV(model_dim=model_dim, kdim=kdim).to(device)

# Causal mask
# The causal mask is optional and requires the sequence length (`n_seqlen`)
#  what is unknown when `trafo.MhaQKV` is instantiated
attn_mask = trafo.attn_mask_causal(n_seqlen, device)

# Forward Pass
y = emb(x) + penc
z = att(query=y, key=y, value=y, mask=attn_mask)
```

### Visualize the attention matrix of an training example

```py
trained_attn_layer = ...
A = trafo.get_attention_matrix(trained_attn_layer, query=x, key=x, value=x)
```


### Project Y to another feature dimension or sequence length
In the [seminal Transformer paper](https://arxiv.org/abs/1706.03762) the MHA has a final output layer to concat the heads.
Our implementation of MHA has not implemented it.
It's also not implemented in the `Block*` classes because I suspect that the FFN can serve the same purposes as the dropped linear layer between MHA and FFN.

Reduce the feature dimension (b, t, d1) -> (b, t, d2)
```
Y = att(...)
fc = torch.nn.Linear(mv, do, bias=True)
out = fc(Y)
ffn layer ...
```

Reduce the sequence length (b, t1, d) -> (b, t2, d)
```
Y = att(...)
cnn = torch.nn.CNN(mv, do, bias=True)
out = cnn(Y)
ffn layer ...
```



## Appendix

### Installation
The `torch-trafo` [git repo](http://github.com/ulf1/torch-trafo) is available as [PyPi package](https://pypi.org/project/torch-trafo)

```
pip install torch-trafo
pip install git+ssh://git@github.com/ulf1/torch-trafo.git
```

### Install a virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
pip install -r requirements-demo.txt --no-cache-dir
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

### Python commands

* Jupyter for the examples: `jupyter lab`
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `PYTHONPATH=. pytest`

Publish

```sh
pandoc README.md --from markdown --to rst -s -o README.rst
python setup.py sdist 
twine upload -r pypi dist/*
```

### Clean up 

```
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```


### Support
Please [open an issue](https://github.com/ulf1/torch-trafo/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/torch-trafo/compare/).
