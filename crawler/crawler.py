import json
from .config import TARGET_URL, RAW_JSON_PATH, PRODUCT_LIMIT
from .fetcher import fetch_page_html
from .parser import parse_best_sellers


def run_crawler():
    print("[Crawler] Start")
    html = fetch_page_html(TARGET_URL)

    print("[Crawler] Parsing and extracting top 5 products with AI...")
    products = parse_best_sellers(html, limit=PRODUCT_LIMIT)

    print(f"[Crawler] Extracted {len(products)} products.")
    RAW_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RAW_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"[Crawler] Saved JSON → {RAW_JSON_PATH}")
    print("[Crawler] Done.")


if __name__ == "__main__":
    run_crawler()
