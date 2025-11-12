import json
import requests
from typing import Dict
from .config import OLLAMA_HOST, OLLAMA_MODEL

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

def extract_product_from_html(html_snippet: str) -> Dict:
	"""Call local LLM (Ollama) to extract structured product data from HTML."""
	prompt = PROMPT_TEMPLATE.format(html=html_snippet)

	payload = {
	    "model": OLLAMA_MODEL,
	    "prompt": prompt,
	    "stream": False,
	}

	resp = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=120)
	resp.raise_for_status()
	data = resp.json()

	raw_text = data.get("response", "").strip()
	# Debug (optional)
	# print("[AIExtractor] Raw LLM output:", raw_text)

	try:
	    product = json.loads(raw_text)
	except json.JSONDecodeError:
	    print("[AIExtractor] JSON decode error, returning empty product.")
	    product = {
	        "title": None,
	        "price": None,
	        "rating": None,
	        "reviews_count": None,
	        "url": None,
	    }

	# Ensure all expected keys exist
	for key in ["title", "price", "rating", "reviews_count", "url"]:
	    product.setdefault(key, None)

	return product
