#!/bin/bash
# Railway-compatible entrypoint
# JupyterLab on $PORT (Railway public URL)
# RStudio Server on internal port 8787

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

# Health check endpoint (simple Python HTTP server on same port? No — jupyter serves it)
echo "MedgeClaw analysis environment starting..."
echo "JupyterLab: port ${JUPYTER_PORT}"
echo "RStudio Server: port 8787 (internal)"

wait
