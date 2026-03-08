FROM runpod/worker-v1-vllm:v2.14.0

# Fix: vLLM's qwen3_vl.py accesses config.tie_word_embeddings on
# Qwen3VLTextConfig, but the bundled transformers version is missing it.
# Patch the config class on disk so it propagates to V1 engine subprocesses.
RUN python3 -c "
import transformers, inspect, os

# Find the config file
from transformers.models.qwen3_vl import configuration_qwen3_vl as mod
filepath = inspect.getfile(mod)
print(f'Patching: {filepath}')

with open(filepath, 'r') as f:
    content = f.read()

# Check if already patched
if 'tie_word_embeddings' in content:
    print('Already has tie_word_embeddings, skipping')
else:
    # Add tie_word_embeddings=False param and self.tie_word_embeddings assignment
    # Find the __init__ of Qwen3VLTextConfig and add the param
    content = content.replace(
        'attention_dropout: float',
        'tie_word_embeddings=False,\n        attention_dropout: float'
    )
    # Add the self assignment after the last self.* = * in __init__
    content = content.replace(
        'self.attention_dropout = attention_dropout',
        'self.attention_dropout = attention_dropout\n        self.tie_word_embeddings = tie_word_embeddings'
    )
    with open(filepath, 'w') as f:
        f.write(content)
    print('Patched successfully')
"
