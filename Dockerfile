FROM runpod/worker-v1-vllm:v2.14.0

# Fix: Qwen3-VL crashes with "Qwen3VLTextConfig has no attribute
# tie_word_embeddings" because the bundled transformers is too old.
# Upgrade to latest transformers which has the complete Qwen3-VL config.
RUN pip install --no-cache-dir --upgrade transformers
