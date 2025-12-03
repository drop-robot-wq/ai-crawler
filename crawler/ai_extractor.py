import json
import requests
from typing import Dict
from .config import OLLAMA_HOST, OLLAMA_MODEL
import re

PROMPT_TEMPLATE = """
	You are a strict JSON extractor for e-commerce products.

	Given the following HTML snippet of an Amazon product card, extract these fields:
	- title (string or null)
	- price (string, numeric only without currency symbol, or null)
	- rating (float 0-5 or null)
	- reviews_count (integer or null)
	- url (string or null)

	Return ONLY valid JSON, no explanation, no markdown, no comments.

	HTML:
	```html
	{html}
"""


def _basic_json_repair(text: str) -> str:
    text = text.strip()

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        return text[start: end + 1]

    # Fallback: just return stripped text
    return text


def extract_product_from_html(html_snippet: str) -> Dict:
    """Call local LLM (Ollama) to extract structured product data from HTML."""
    prompt = PROMPT_TEMPLATE.format(html=html_snippet)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 128
        }
    }

    try:
        resp = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=300)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.ReadTimeout:
        print("Ollama timed out while generating response.")
        return {
            "title": None,
            "price": None,
            "rating": None,
            "reviews_count": None,
            "url": None,
        }
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return {
            "title": None,
            "price": None,
            "rating": None,
            "reviews_count": None,
            "url": None,
        }

    raw_text = data.get("response", "").strip()
    print("This is the raw_text text")
    print(raw_text)
    repaired = _basic_json_repair(raw_text)
    print("This is the repaired text")
    print(repaired)
    # Debug (optional)
    # print("[AIExtractor] Raw LLM output:", raw_text)

    try:
        product = json.loads(repaired)
    except json.JSONDecodeError:
        print("[AIExtractor] JSON decode error, returning empty product.")
        product = {}

    # Ensure all expected keys exist
    normalized = {
        "title": product.get("title"),
        "price": product.get("price"),
        "rating": product.get("rating"),
        "reviews_count": product.get("reviews_count"),
        "url": product.get("url"),
    }
    return normalized
