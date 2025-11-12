FROM mcr.microsoft.com/playwright/python:v1.47.0-jammy

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install --with-deps chromium

# Copy source code
COPY crawler/ ./crawler/
COPY transformer/ ./transformer/
COPY data/ ./data/

ENV PYTHONUNBUFFERED=1

CMD ["bash"]
