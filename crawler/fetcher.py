from playwright.sync_api import sync_playwright


def fetch_page_html(url: str, headless: bool = True) -> str:
    """Fetch rendered HTML from the given URL using Playwright."""
    print(f"[Fetcher] Loading URL: {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)
        # scroll to trigger lazy loading
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)
        html = page.content()
        browser.close()
    print("[Fetcher] Page loaded, HTML captured.")
    return html
