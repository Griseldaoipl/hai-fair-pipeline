# Dockerfile — reproducible environment for the FAIR HAI surveillance pipeline
# Pins Python 3.11 and all dependencies so that `run_all.py` executes in a
# byte-identical environment on any host (see manuscript, Reproducibility).
#
# Build:  docker build -t hai-fair-pipeline .
# Run:    docker run --rm hai-fair-pipeline          # executes run_all.py

FROM python:3.11.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=0 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install pinned dependencies first (leverages Docker layer caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the pipeline, data, codebook, and validation assets
COPY . .

# Reproduce all results by default (deterministic; fixed seeds, see README)
CMD ["python", "run_all.py"]
