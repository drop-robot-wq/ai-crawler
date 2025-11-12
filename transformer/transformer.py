import json
from pathlib import Path

import pandas as pd

from crawler.config import DATA_RAW_DIR, CSV_PATH


def get_latest_json() -> Path:
    json_files = sorted(DATA_RAW_DIR.glob("products_*.json"))
    if not json_files:
        raise FileNotFoundError("No JSON product files found in data/raw/")
    return json_files[-1]


def transform_json_to_csv():
    latest_json = get_latest_json()
    print(f"[Transformer] Using JSON: {latest_json}")

    with open(latest_json, "r", encoding="utf-8") as f:
        products = json.load(f)

    df = pd.DataFrame(products)

    # Basic cleanup
    if "price" in df.columns:
        df["price"] = (
            df["price"]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
        )
        df["price"] = pd.to_numeric(df["price"], errors="coerce")

    if "rating" in df.columns:
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    if "reviews_count" in df.columns:
        df["reviews_count"] = pd.to_numeric(df["reviews_count"], errors="coerce")

    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CSV_PATH, index=False)
    print(f"[Transformer] Saved CSV → {CSV_PATH}")
    print("[Transformer] Done.")


if __name__ == "__main__":
    transform_json_to_csv()
