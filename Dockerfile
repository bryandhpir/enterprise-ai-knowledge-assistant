
FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/home/appuser/.cache/huggingface

# Dependencies for Python ML libraries
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

# Create an unprivileged user
RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p /app/data/chroma \
    && chown -R appuser:appuser /app /home/appuser

# Copy application source
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
