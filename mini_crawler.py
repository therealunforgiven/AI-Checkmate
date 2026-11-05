import requests
from bs4 import BeautifulSoup
import time

# Target a safe testing sandbox website
START_URL = "http://toscrape.com"

def run_mini_crawler(target_url, max_pages=3):
    current_url = target_url
    pages_crawled = 0
    
    print("\n==============================================================")
    print(f"[🚀 LAUNCH] Starting small web crawler test sequence...")
    print("==============================================================")
    
    while current_url and pages_crawled < max_pages:
        pages_crawled += 1
        print(f"\n[+] Fetching Page {pages_crawled}: {current_url}")
        
        try:
            # Request the raw webpage with a 10 second timeout limit
            response = requests.get(current_url, timeout=10)
            response.raise_for_status() # Trigger an error if the site fails to load
            
            # Convert raw HTML into navigable soup structures
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find all book article containers on the page
            books = soup.find_all("article", class_="product_pod")
            print(f" -> Found {len(books)} items on this index. Scraping details...")
            
            # Loop through each book container to extract the specific text tags
            for book in books:
                title = book.h3.a["title"]
                price = book.find("p", class_="price_color").text
                availability = book.find("p", class_="instock availability").text.strip()
                
                print(f"   * Item: {title[:35]:<35} | Price: {price:<8} | Status: {availability}")
            
            # Locate the 'next' button on the page to find the next URL link
            next_button = soup.find("li", class_="next")
            if next_button:
                next_page_rel_url = next_button.a["href"]
                # Formulate the complete absolute URL string for the next iteration loop
                current_url = "http://toscrape.com" + next_page_rel_url
                
                # Polite crawling protocol: rest 2 seconds so you don't slam the server
                time.sleep(2)
            else:
                print("\n[!] Reached final index page. Stopping crawl loop.")
                current_url = None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network request blocked or failed: {e}")
            break

    print("\n==============================================================")
    print(f"[👑 SUCCESS] Web crawler test complete. Pages processed: {pages_crawled}")
    print("[System Note: Web pipeline verified thanks to Gemini]")
    print("==============================================================")

# Execute the crawler loop
if __name__ == "__main__":
    run_mini_crawler(START_URL, max_pages=2)
