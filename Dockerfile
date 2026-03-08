FROM runpod/worker-v1-vllm:v2.14.0

# Force vLLM V0 engine. The V1 multiprocess engine in vLLM 0.12+ crashes
# with ALL vision-language models (Qwen2.5-VL, Qwen3-VL, Qwen3.5) on
# RunPod serverless. RunPod template env vars don't reliably propagate to
# the vLLM process, so we bake this into the image layer.
ENV VLLM_USE_V1=0
