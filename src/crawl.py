# src/crawl.py (JS-capable crawler)
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse
import os, time

BASE_URL = "https://aibitsoft.com"
OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

visited = set()

def crawl(url, depth=0, max_depth=3):
    if url in visited or not url.startswith(BASE_URL) or depth > max_depth:
        return
    visited.add(url)

    print(f"[+] Crawling: {url}")
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        time.sleep(2)
        html = page.content()
        text = page.inner_text("body")
        browser.close()

    fname = os.path.join(OUTPUT_DIR, f"{len(visited)}.txt")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"URL: {url}\n\n{text}")

    links = []
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        new_url = urljoin(url, a["href"])
        if urlparse(new_url).netloc == urlparse(BASE_URL).netloc:
            links.append(new_url)

    for link in links:
        crawl(link, depth + 1, max_depth)

if __name__ == "__main__":
    crawl(BASE_URL)
    print("[✔] Crawling complete.")
