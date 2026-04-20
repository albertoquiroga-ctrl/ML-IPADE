from playwright.sync_api import sync_playwright
import os, sys

html = os.path.abspath('store10_analysis.html')
pdf  = os.path.abspath('store10_analysis.pdf')
url  = 'file:///' + html.replace('\\', '/')

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url, wait_until='load')
    page.pdf(
        path=pdf,
        format='A4',
        print_background=True,
        margin={'top': '15mm', 'bottom': '15mm', 'left': '12mm', 'right': '12mm'},
    )
    browser.close()

print('OK ->', pdf, os.path.getsize(pdf), 'bytes')
