from playwright.sync_api import sync_playwright
import pandas as pd
import time

def fetch_rr_numbers_fois(rake_names, session_cookie, output_file="rake_rr_numbers.xlsx"):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=800)  # slow_mo to see actions
        context = browser.new_context()

        # Inject your FOIS session cookie
        context.add_cookies([{
            "name": "JSESSIONID",
            "value": session_cookie,
            "domain": "www.fois.indianrail.gov.in",
            "path": "/",
            "httpOnly": True,
            "secure": True
        }])

        page = context.new_page()
        # Open FOIS Rake search page
        page.goto("https://www.fois.indianrail.gov.in/ecbs/RouterServlet")

        for rake in rake_names:
            try:
                # 1️⃣ Enter rake name in search box
                search_box = page.locator("input[type='search']")
                search_box.fill("")  # clear previous search
                search_box.type(rake)
                time.sleep(2)  # wait for table row to appear

                # 2️⃣ Check if the row exists
                row_locator = page.locator(f"tr:has-text('{rake}')")
                if row_locator.count() == 0:
                    print(f"No row found for {rake}, skipping")
                    continue

                # 3️⃣ Click Load Name link in that row
                load_link = row_locator.locator("a[id^='LoadName']").first
                load_link.click()

                # 4️⃣ Wait for dialog and collect RR numbers
                page.wait_for_selector("div.modal-body a", timeout=5000)
                rr_links = page.locator("div.modal-body a")
                rr_count = rr_links.count()

                if rr_count == 1:
                    rr_number = rr_links.first.inner_text().strip()
                    results.append({"Rake Name": rake, "RR Number": rr_number})
                    print(f"{rake} → {rr_number}")
                else:
                    print(f"{rake} has no RR or multiple RR, skipping")

                # 5️⃣ Close dialog safely (Escape key)
                page.keyboard.press("Escape")
                time.sleep(1)

            except Exception as e:
                print(f"Error fetching {rake}: {e}")
                continue

        # Close browser
        browser.close()

    # Save results to Excel
    if results:
        df = pd.DataFrame(results)
        df.to_excel(output_file, index=False)
        print(f"\n✅ RR Numbers saved to {output_file}")
    else:
        print("No RR numbers found to save.")


# ------------------------
# Example usage
rake_names = ["PM-50156", "YARADA-R-606", "PRGTITP478"]  # Replace with your list
session_cookie = "YOUR_JSESSIONID_VALUE"  # Replace with your FOIS session cookie

fetch_rr_numbers_fois(rake_names, session_cookie)
