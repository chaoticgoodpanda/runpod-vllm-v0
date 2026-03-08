"""Wrapper entrypoint that patches Qwen3VLTextConfig before vLLM loads.

vLLM's qwen3_vl.py:1192 accesses config.tie_word_embeddings on Qwen3VLTextConfig,
but Qwen's config.json only has tie_word_embeddings at the top level (not in text_config).
This monkey-patches the class to default the attribute to False.
"""
import importlib

# Patch Qwen3VLTextConfig before anything imports vLLM's model code
try:
    mod = importlib.import_module("transformers.models.qwen3_vl.configuration_qwen3_vl")
    Cls = getattr(mod, "Qwen3VLTextConfig", None)
    if Cls is not None:
        _orig_init = Cls.__init__

        def _patched_init(self, *args, **kwargs):
            _orig_init(self, *args, **kwargs)
            if not hasattr(self, "tie_word_embeddings"):
                self.tie_word_embeddings = False

        Cls.__init__ = _patched_init
        print("[patch] Qwen3VLTextConfig patched: tie_word_embeddings defaults to False")
except Exception as e:
    print(f"[patch] Could not patch Qwen3VLTextConfig: {e}")

# Run the original handler
exec(open("/src/handler.py").read())
