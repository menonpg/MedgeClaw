#!/bin/bash
# Railway entrypoint — JupyterLab only (RStudio requires s6-overlay, not Railway-compatible)
set -e

mkdir -p /workspace/data /workspace/outputs /workspace/skills

echo "Starting JupyterLab on port ${PORT:-8888}..."

exec jupyter lab \
    --ip=0.0.0.0 \
    --port="${PORT:-8888}" \
    --no-browser \
    --ServerApp.token="${JUPYTER_TOKEN:-biomed}" \
    --ServerApp.allow_origin="*" \
    --notebook-dir=/workspace/data
