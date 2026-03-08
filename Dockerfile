FROM runpod/worker-v1-vllm:v2.14.0

# Fix: vLLM's qwen3_vl.py accesses config.tie_word_embeddings on
# Qwen3VLTextConfig, but Qwen's config.json only has it at the top level
# (not in text_config). The entrypoint monkey-patches the class to default
# the attribute to False before vLLM loads.
COPY entrypoint.py /entrypoint.py
CMD ["python3", "/entrypoint.py"]
