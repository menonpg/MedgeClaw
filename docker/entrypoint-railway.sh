#!/bin/bash
# Railway-compatible entrypoint

# Create required directories
mkdir -p /workspace/data /workspace/outputs /workspace/skills

# Start RStudio Server (internal only)
/init &

# Start JupyterLab on Railway's assigned port
JUPYTER_PORT=${PORT:-8888}

jupyter lab \
    --ip=0.0.0.0 \
    --port="${JUPYTER_PORT}" \
    --no-browser \
    --NotebookApp.token="${JUPYTER_TOKEN:-biomed}" \
    --NotebookApp.base_url="/" \
    --notebook-dir=/workspace/data &

echo "MedgeClaw starting — JupyterLab on port ${JUPYTER_PORT}"
wait
