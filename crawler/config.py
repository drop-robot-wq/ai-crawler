import os
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

TARGET_URL = os.getenv("TARGET_URL", "https://www.amazon.com/Best-Sellers/zgbs")

DATA_DIR = BASE_DIR / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"

DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
RAW_JSON_PATH = DATA_RAW_DIR / f"products_{TIMESTAMP}.json"
CSV_PATH = DATA_PROCESSED_DIR / f"products_{TIMESTAMP}.csv"

# AI config
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")
PRODUCT_LIMIT = int(os.getenv("PRODUCT_LIMIT", "1"))
