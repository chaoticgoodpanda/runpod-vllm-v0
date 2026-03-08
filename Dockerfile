FROM runpod/worker-v1-vllm:v2.14.0

# Fix: vLLM's qwen3_vl.py accesses config.tie_word_embeddings on
# Qwen3VLTextConfig, but the bundled transformers version is missing it.
# Patch the config class on disk so it propagates to V1 engine subprocesses.
COPY patch_config.py /tmp/patch_config.py
RUN python3 /tmp/patch_config.py && rm /tmp/patch_config.py
