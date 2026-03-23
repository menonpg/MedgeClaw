# Biomed OpenClaw - Analysis Environment
# Base: rocker/rstudio includes R + RStudio Server
FROM rocker/rstudio:4.3.3

LABEL maintainer="xjtulyc"
LABEL description="Biomedical analysis environment for OpenClaw + Claude Code"

# ── System dependencies ──────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv curl git \
    libcurl4-openssl-dev libssl-dev libxml2-dev \
    libfontconfig1-dev libharfbuzz-dev libfribidi-dev \
    libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev \
    libgit2-dev libssh2-1-dev \
    nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# ── Python: uv package manager ───────────────────────────────────────────────
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# ── Python: biomed packages ───────────────────────────────────────────────────
RUN pip3 install --no-cache-dir \
    jupyterlab \
    scanpy anndata scvi-tools \
    biopython \
    pydeseq2 \
    lifelines \
    nibabel pydicom \
    pandas numpy scipy \
    matplotlib seaborn plotly \
    scikit-learn \
    networkx \
    uv

# ── R: Bioconductor + CRAN packages ──────────────────────────────────────────
RUN Rscript -e "install.packages('BiocManager', repos='https://cloud.r-project.org')"

RUN Rscript -e "BiocManager::install(c( \
    'DESeq2', 'edgeR', 'limma', \
    'clusterProfiler', 'enrichplot', \
    'Seurat', 'SingleCellExperiment', \
    'GSVA', 'fgsea', \
    'AnnotationHub', 'org.Hs.eg.db' \
), ask=FALSE)"

RUN Rscript -e "install.packages(c( \
    'survival', 'survminer', \
    'ggplot2', 'ggpubr', 'patchwork', \
    'pheatmap', 'ComplexHeatmap', \
    'corrplot', 'VennDiagram', \
    'renv', 'here', 'tidyverse' \
), repos='https://cloud.r-project.org')"

# ── Claude Code ───────────────────────────────────────────────────────────────
RUN npm install -g @anthropic-ai/claude-code

# ── Ports ─────────────────────────────────────────────────────────────────────
# 8787 = RStudio Server
# 8888 = JupyterLab
EXPOSE 8787 8888

# ── Entrypoint ────────────────────────────────────────────────────────────────
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]

# ── Railway entrypoint ────────────────────────────────────────────────────────
COPY docker/entrypoint-railway.sh /entrypoint-railway.sh
RUN chmod +x /entrypoint-railway.sh
EXPOSE 8787
EXPOSE 8888

# ── K-Dense Scientific Skills (inline clone — Railway doesn't support submodules) ──
RUN mkdir -p /workspace/skills && \
    git clone --depth=1 https://github.com/K-Dense-AI/claude-scientific-skills.git \
    /workspace/skills/scientific 2>/dev/null || echo "K-Dense skills unavailable, continuing"

WORKDIR /workspace
