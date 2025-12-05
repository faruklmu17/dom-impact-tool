from playwright.sync_api import Playwright, sync_playwright

def test_login_button_visible(playwright: Playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/index.html")  # however you serve it
    assert page.locator("[data-test='login-button']").is_visible()
    browser.close()


def test_email_and_password_fields(playwright: Playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/index.html")
    assert page.locator("[data-test='email-input']").is_visible()
    assert page.locator("[data-test='password-input']").is_visible()
    browser.close()
