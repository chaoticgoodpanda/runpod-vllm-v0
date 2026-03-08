FROM runpod/worker-v1-vllm:v2.14.0

# Fix: vLLM's qwen3_vl.py accesses config.tie_word_embeddings directly,
# but V1 engine subprocesses lose the attribute from Qwen3VLTextConfig.
# Patch vLLM source to use getattr() with safe default.
COPY patch_config.py /tmp/patch_config.py
RUN python3 /tmp/patch_config.py && rm /tmp/patch_config.py
