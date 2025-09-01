from playwright.sync_api import sync_playwright
import pandas as pd
import time

# ---------------------------
# Rake names list (add all your rake names here)
rake_names = [
    "PM-50156","YARADA-R-606","PRGTITP478","TPDDU1401-","YARADA-R-641",
    "VIRAT-41","VIRAT-55","TPDDU1430-","NKJ-LION-160750","SRIVALI-V-154",
    "PRGTITP379-R-48","TPDDU1295-","DELTA4102--","YARADA-V-646","KOTA---YDCC196",
    # ... add all remaining rake names ...
]

# FOIS session cookie
session_cookie = "YOUR_JSESSIONID_VALUE"

# ---------------------------
def fetch_rr_numbers_fois(rake_names, session_cookie, output_file="rake_rr_numbers.xlsx"):
    results = []

    with sync_playwright() as p:
        # Use headless=True for Codespaces / server; False to see browser actions locally
        browser = p.chromium.launch(headless=True, slow_mo=0)
        context = browser.new_context()

        # Add FOIS session cookie
        context.add_cookies([{
            "name": "JSESSIONID",
            "value": session_cookie,
            "domain": "www.fois.indianrail.gov.in",
            "path": "/",
            "httpOnly": True,
            "secure": True
        }])

        page = context.new_page()
        page.goto("https://www.fois.indianrail.gov.in/ecbs/RouterServlet")

        for rake in rake_names:
            try:
                # Clear & type rake in search box
                search_box = page.locator("input[type='search']")
                search_box.fill(""_
