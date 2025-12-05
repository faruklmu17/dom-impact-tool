from playwright.sync_api import sync_playwright

def save_dom_snapshot(url: str, path: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(url)

        content = page.content()

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        browser.close()


# BEFORE UI CHANGE
save_dom_snapshot("http://localhost:8000/index.html", "snapshots/dom_v1.html")

# AFTER YOU MODIFY THE HTML, RUN AGAIN:
save_dom_snapshot("http://localhost:8000/index.html", "snapshots/dom_v2.html")
