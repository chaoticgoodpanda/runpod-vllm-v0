"""Patch Qwen3VLTextConfig to add tie_word_embeddings attribute."""
import inspect
from transformers.models.qwen3_vl import configuration_qwen3_vl as mod

filepath = inspect.getfile(mod)
print(f"Patching: {filepath}")

with open(filepath, "r") as f:
    content = f.read()

if "tie_word_embeddings" in content:
    print("Already has tie_word_embeddings, skipping")
else:
    content = content.replace(
        "attention_dropout: float",
        "tie_word_embeddings=False,\n        attention_dropout: float",
    )
    content = content.replace(
        "self.attention_dropout = attention_dropout",
        "self.attention_dropout = attention_dropout\n        self.tie_word_embeddings = tie_word_embeddings",
    )
    with open(filepath, "w") as f:
        f.write(content)
    print("Patched successfully")
