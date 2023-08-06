__version__ = '0.1.0'

# Layers
from .layers.attention import (MhaQKV, MhaSource, MhaSelf,
                               positional_encoding, get_attention_matrix)
from .layers.block import (BlockQKV, BlockSource, BlockSelf)
from .layers.stack import (StackQKV, StackSource, StackSelf)

# Utility functions as submodules (explicit import required)
from .utils import attn_mask
from .utils import activations
from .utils import weightprops
from .utils import losses

# Tasks to learn as submodules (explicit import required)
# e.g. loss functions, training wrapper, etc. for ...
from .tasks import mlm  # Masked LM training

# Data loader
from .tasks import char
