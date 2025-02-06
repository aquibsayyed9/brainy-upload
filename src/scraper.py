import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

AUTHORS = {
    "marcus_aurelius": "https://www.brainyquote.com/authors/marcus-aurelius-quotes",
    "seneca": "https://www.brainyquote.com/authors/lucius-annaeus-seneca-quotes",
    "plato": "https://www.brainyquote.com/authors/plato-quotes",
    "socrates": "https://www.brainyquote.com/authors/socrates-quotes",
    "aristotle": "https://www.brainyquote.com/authors/aristotle-quotes",
    "einstein": "https://www.brainyquote.com/authors/albert-einstein-quotes",
    "mlk_jr": "https://www.brainyquote.com/authors/martin-luther-king-jr-quotes",
    "abdul_kalam": "https://www.brainyquote.com/authors/a-p-j-abdul-kalam-quotes",
    "gandhi": "https://www.brainyquote.com/authors/mahatma-gandhi-quotes",
    "jung": "https://www.brainyquote.com/authors/carl-jung-quotes"
}

def get_random_quote():
    """Fetches a random quote using Selenium to bypass bot detection."""
    author = random.choice(list(AUTHORS.keys()))
    url = AUTHORS[author]

    print(f"Fetching quotes from {author.replace('_', ' ').title()}...")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--window-size=1920,1080')
    # Add user agent to appear more like a regular browser
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.binary_location = '/usr/bin/chromium'

    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        
        # Print page source for debugging
        print("Page source length:", len(driver.page_source))
        print("Current URL:", driver.current_url)
        
        # Wait up to 10 seconds for quotes to load
        wait = WebDriverWait(driver, 10)
        quote_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".grid-item .b-qt"))
        )
        
        # Try different selectors if the first one fails
        if not quote_elements:
            quote_elements = driver.find_elements(By.CSS_SELECTOR, ".clearfix .b-qt")
        
        print(f"Found {len(quote_elements)} quote elements")
        
        quotes = []
        for element in quote_elements:
            try:
                quote_text = element.text.strip()
                if quote_text:
                    quotes.append(quote_text)
            except Exception as e:
                print(f"Error extracting quote text: {e}")
                continue
        
        print(f"Successfully extracted {len(quotes)} quotes")
        
        if not quotes:
            print("No quotes found. Trying alternative method...")
            # Try getting quotes by XPath as a fallback
            quote_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'grid-item')]//a[@title='view quote']")
            quotes = [q.text.strip() for q in quote_elements if q.text.strip()]

        if not quotes:
            print(f"No quotes found for {author} after all attempts.")
            return None, None
            
        selected_quote = random.choice(quotes)
        print(f"Selected quote: {selected_quote[:50]}...")
        return author.replace('_', ' ').title(), selected_quote

    except Exception as e:
        print(f"Error fetching quotes: {e}")
        print("Page source excerpt:")
        try:
            print(driver.page_source[:1000])
        except:
            print("Could not print page source")
        return None, None
        
    finally:
        driver.quit()