from typing import List, Dict
from bs4 import BeautifulSoup
from .ai_extractor import extract_product_from_html


def parse_best_sellers(html: str, limit: int = 5) -> List[Dict]:
    """
    Parse HTML and extract top N product entries using AI-based extraction.

    We only use BeautifulSoup to locate individual product cards,
    and delegate field extraction to the LLM.
    """
    soup = BeautifulSoup(html, "lxml")

    print("Hello World !")

    # This selector may need adjustment depending on Amazon layout.
    # Commonly best-seller or listing cards have data-asin attribute.
    product_cards = soup.select("div[data-asin]")

    if not product_cards:
        print("[Parser] No product cards found with data-asin selector, "
              "you may need to adjust CSS selectors.")
        return []

    products: List[Dict] = []

    for idx, card in enumerate(product_cards[:limit]):
        print(f"[Parser] Processing product card {idx+1}...")
        html_snippet = str(card)
        product = extract_product_from_html(html_snippet)
        products.append(product)

    return products
