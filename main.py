#Extract Grand Dragon 4D results from check4d.org
#Established since 11th April 2020
import pandas as pd
from datetime import date, timedelta
import asyncio
from playwright.async_api import async_playwright
from typing import List, Dict
import math

# --- Configuration ---
BASE_URL = "https://www.check4d.org/past-results/"
START_DATE = date(2025, 5, 1)
END_DATE = date.today()
EXCEL_FILENAME = "check4d_pastresults_GD4D.xlsx"
PAGE_LOAD_TIMEOUT = 45000
ACTION_TIMEOUT = 15000
DELAY_BETWEEN_REQUESTS = 3.0
COMPANY_NAME = "Grand Dragon 4D"
MAX_CONCURRENT_REQUESTS = 5

async def fetch_results(page, date_str):
    """Fetch results for a specific date."""
    url = f"{BASE_URL}{date_str}#section-cam"
    try:
        await page.goto(url, wait_until='domcontentloaded')
        print(f"  [INFO] Fetched data for {date_str}")
        results = []
        for prefix, count in [("gp", 3), ("gs", 10), ("gc", 10)]:
            for i in range(1, count + 1):
                locator = page.locator(f"#{prefix}{i}")
                if await locator.is_visible(timeout=ACTION_TIMEOUT / 3):
                    text = (await locator.inner_text()).strip()
                    if text.isdigit() and len(text) == 4:
                        results.append(text)
        return [
            {
                "Date": date_str,
                "Number": num,
                **dict(zip(["1st machine", "2nd machine", "3rd machine", "4th machine"], num)),
                "COMPANY_NAME": COMPANY_NAME
            }
            for num in results
        ]
    except Exception as e:
        print(f"  [ERROR] Failed to fetch data for {date_str}: {e}")
        return []

def split_date_range(start_date: date, end_date: date, chunks: int) -> List[tuple]:
    """Split the date range into chunks for parallel processing."""
    total_days = (end_date - start_date).days + 1
    chunk_size = math.ceil(total_days / chunks)
    date_ranges = []
    
    for i in range(0, total_days, chunk_size):
        chunk_start = start_date + timedelta(days=i)
        chunk_end = min(chunk_start + timedelta(days=chunk_size - 1), end_date)
        date_ranges.append((chunk_start, chunk_end))
    
    return date_ranges

async def scrape_chunk(start_date: date, end_date: date) -> List[Dict]:
    """Scrape results for a specific chunk of dates."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_navigation_timeout(PAGE_LOAD_TIMEOUT)
        page.set_default_timeout(ACTION_TIMEOUT)

        chunk_results = []
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            chunk_results.extend(await fetch_results(page, date_str))
            await asyncio.sleep(DELAY_BETWEEN_REQUESTS)
            current_date += timedelta(days=1)

        await browser.close()
        return chunk_results

async def scrape_dates(start_date: date, end_date: date) -> List[Dict]:
    """Scrape results using parallel processing."""
    date_chunks = split_date_range(start_date, end_date, MAX_CONCURRENT_REQUESTS)
    tasks = [scrape_chunk(chunk_start, chunk_end) for chunk_start, chunk_end in date_chunks]
    
    # Run chunks in parallel
    chunk_results = await asyncio.gather(*tasks)
    
    # Flatten results from all chunks
    all_results = []
    for chunk in chunk_results:
        all_results.extend(chunk)
    
    return all_results

def save_to_excel(data, file_name):
    """Save data to an Excel file."""
    if not data:
        print("  [INFO] No data to save.")
        return
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False, engine='openpyxl')
    print(f"  [INFO] Data saved to {file_name}")

async def main():
    print(f"--- Scraping from {START_DATE} to {END_DATE} with {MAX_CONCURRENT_REQUESTS} parallel workers ---")
    results = await scrape_dates(START_DATE, END_DATE)
    save_to_excel(results, EXCEL_FILENAME)
    print("--- Script Finished ---")

if __name__ == "__main__":
    asyncio.run(main())