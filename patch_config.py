"""Patch vLLM's qwen3_vl.py to safely access tie_word_embeddings.

The root cause: vLLM accesses config.tie_word_embeddings directly on
Qwen3VLTextConfig. Even though transformers 4.57+ has this parameter in
__init__, the V1 engine subprocess may load configs differently, losing
the attribute. Fix: patch vLLM's source to use getattr with a default.
"""
import glob
import os
import re

# Find vLLM's qwen3*.py files — qwen3_vl.py imports Qwen3ForCausalLM from qwen3.py,
# which also accesses config.tie_word_embeddings in load_weights()
vllm_paths = glob.glob("/usr/local/lib/python*/dist-packages/vllm/model_executor/models/qwen3*.py")

for path in vllm_paths:
    print(f"Patching vLLM: {path}")
    with open(path, "r") as f:
        content = f.read()

    # Replace all bare config.tie_word_embeddings with getattr(config, 'tie_word_embeddings', False)
    original = content
    content = re.sub(
        r'(\w+)\.tie_word_embeddings',
        r"getattr(\1, 'tie_word_embeddings', False)",
        content,
    )

    if content != original:
        with open(path, "w") as f:
            f.write(content)
        count = original.count('.tie_word_embeddings')
        print(f"  Replaced {count} occurrences of .tie_word_embeddings with safe getattr")
    else:
        print("  No .tie_word_embeddings references found")

if not vllm_paths:
    print("WARNING: No vLLM qwen3_vl.py found!")
