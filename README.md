# AI-Enhanced Amazon Top 5 Crawler (Local Prototype)

This is a small, local prototype of an **AI-enhanced web crawler + transformer**:

- Uses **Playwright** to fetch an Amazon Best Sellers page.
- Uses a **local LLM (Ollama + Llama 3)** to extract structured product data from HTML.
- Saves the **top 5 products** as JSON.
- Transforms the JSON into a clean **CSV** file.

This is the first brick of a larger **AI web crawler + Product Intelligence Database (PIDB)** project.

---

## 1. Architecture (Prototype Scope)

```text
Playwright Crawler → HTML
                   → Parser (BeautifulSoup: find product blocks)
                   → AI Extractor (Ollama Llama3: HTML → JSON objects)
                   → data/raw/products_<timestamp>.json
                   → Transformer (Pandas: JSON → CSV)
                   → data/processed/products_<timestamp>.csv
