import json
from playwright.sync_api import sync_playwright
from datetime import datetime
import re

def lambda_scraper():
    """ 
    Scrapes e-commerce product data and stores in s3
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Scrape Amazon best sellers (public data)
        page.goto('https://www.amazon.com/best-sellers-books-Amazon/zgbs/books', timeout=60000)
        page.wait_for_selector('ol.a-ordered-list', timeout=15000)

        print("Page loaded:", page.title())
        
        products = []
        items = page.query_selector_all('ol.a-ordered-list li')
        print(f"Found {len(items)} product items")

        for item in items[:50]:
            try:

                asin_el = item.query_selector('div[data-asin]')
                if not asin_el:
                    continue  # skip placeholders, ads, etc.
                
                asin = asin_el.get_attribute('data-asin')
                
                title_el = item.query_selector('a span, div > a > span')
                rank_el = item.query_selector('span.zg-bdg-text')

                title = title_el.inner_text().strip() if title_el else "N/A"
                rank = rank_el.inner_text().strip() if rank_el else "N/A"
            

                li_text = item.inner_text()  # full text of this <li>
                match = re.search(r'\$\d+(?:\.\d{1,2})?', li_text)  # matches $22.38, $35.00 etc.
                price = match.group(0) if match else "N/A"
            
            
                products.append({
                    'product_id': hash(title),
                    'title': title,
                    'price': price,
                    'rank': rank,
                    'scraped_at': datetime.now().isoformat(),
                    'source': 'amazon_bestsellers'
                })
            except Exception as e:
                print(f"Error parsing item: {e}")
                continue

        browser.close


    # Save results to local JSON file
    with open(
        'amazon_bestsellers.json', "w", encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)


    print(f"Scraping complete. Saved {len(products)} items to amazon_bestsellers.json ")

if __name__ == "__main__":
    lambda_scraper()
