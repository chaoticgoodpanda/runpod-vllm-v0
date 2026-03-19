# runpod-vllm-v0 — Custom vLLM Docker Image for Qwen3-VL

A custom Docker image that patches a vLLM bug affecting Qwen3-VL model inference on RunPod serverless. Used as the base image for the MMDS LoRA scorer endpoint.

**Docker image:** `ghcr.io/chaoticgoodpanda/runpod-vllm-v0:v2.14.0-v0engine`
**GitHub:** `chaoticgoodpanda/runpod-vllm-v0`

## The Bug

vLLM's `qwen3_vl.py` (and `qwen3.py`) access `config.tie_word_embeddings` directly. When running under vLLM's V1 engine in subprocess mode, the `Qwen3VLTextConfig` object can lose this attribute during serialization. This causes an `AttributeError` crash during model loading.

## The Fix

`patch_config.py` runs at Docker build time and patches all `qwen3*.py` files in the vLLM installation:

```python
# Before (crashes):
config.tie_word_embeddings

# After (safe):
getattr(config, 'tie_word_embeddings', False)
```

## Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Based on `runpod/worker-v1-vllm:v2.14.0`, applies patch |
| `patch_config.py` | Python script that regex-replaces all `.tie_word_embeddings` accesses |

## Build & Push

```bash
# Login to ghcr.io
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Build
docker build -t ghcr.io/chaoticgoodpanda/runpod-vllm-v0:v2.14.0-v0engine .

# Push
docker push ghcr.io/chaoticgoodpanda/runpod-vllm-v0:v2.14.0-v0engine
```

## RunPod Template Configuration

When creating/updating a RunPod serverless endpoint using this image:

| Setting | Value |
|---------|-------|
| Docker image | `ghcr.io/chaoticgoodpanda/runpod-vllm-v0:v2.14.0-v0engine` |
| Model | `mtl278/mmds-design-scorer-merged-v12-1` |
| `HUGGING_FACE_HUB_TOKEN` | HuggingFace token (NOT `HF_TOKEN`) |
| `DTYPE` | `half` (NOT `bfloat16` — RunPod worker doesn't recognize it) |
| GPU | AMPERE_80 (A100 80GB) |
| Idle timeout | 1800 seconds |

## Important Notes

- **ghcr.io package visibility is separate from repo visibility.** Making the repo public does NOT make the Docker image public. Set package visibility independently in GitHub's web UI (Packages > Package Settings).
- **Template updates don't refresh running workers.** After pushing a new image, you must delete and recreate the RunPod endpoint for changes to take effect.
- **Commits must be pushed before building.** GitHub Actions builds from remote HEAD. Local-only commits won't be in the image.
