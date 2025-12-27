FROM mcr.microsoft.com/playwright/python:v1.47.0-jammy

WORKDIR /app

# --- Python deps (cache friendly) ---
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# --- Playwright browsers ---
RUN python -m playwright install --with-deps chromium

# --- App code ---
COPY crawler/ ./crawler/
COPY transformer/ ./transformer/

# --- Runtime data directory (do not COPY if it may not exist in the repo) ---
RUN mkdir -p /app/data

ENV PYTHONUNBUFFERED=1

CMD ["bash"]
