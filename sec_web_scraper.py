# General purpose web scraper
# Originally created for Civic Tech DC hackathon to scrape SEC documents
# Can be adapted for various web scraping tasks

import requests
from bs4 import BeautifulSoup
import time
import argparse
import json
from typing import Dict, List, Optional


class WebScraper:
    """
    A general-purpose web scraper that can extract content from any website
    using CSS selectors with configurable rate limiting and headers.
    """
    
    def __init__(self, delay: float = 1.0, custom_headers: Optional[Dict] = None):
        """
        Initialize the web scraper with optional configuration.
        
        Args:
            delay: Time to wait between requests (seconds)
            custom_headers: Custom HTTP headers to use
        """
        self.delay = delay
        # Default headers that work well for most websites
        self.headers = custom_headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def scrape(self, url: str, selectors: List[str], extract_all: bool = False) -> Dict:
        """
        Scrape content from a URL using the provided CSS selectors.
        
        Args:
            url: The URL to scrape
            selectors: List of CSS selectors to extract content
            extract_all: If True, extract all matching elements; if False, just the first
            
        Returns:
            Dictionary mapping selectors to extracted content
        """
        # Rate limiting to be respectful to target servers
        time.sleep(self.delay)
        
        # Fetch the webpage
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        results = {}
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                if extract_all:
                    # Extract text from all matching elements
                    results[selector] = [elem.get_text(strip=True) for elem in elements]
                else:
                    # Extract text from first matching element only
                    results[selector] = elements[0].get_text(strip=True)
            else:
                results[selector] = None
        
        return results


def main():
    """
    Command-line interface for the web scraper.
    Allows users to specify URL, selectors, and output format.
    """
    parser = argparse.ArgumentParser(description='General purpose web scraper')
    parser.add_argument('url', help='URL to scrape')
    parser.add_argument('--selectors', '-s', nargs='+', default=['h1'], 
                       help='CSS selectors to extract (default: h1)')
    parser.add_argument('--delay', '-d', type=float, default=1.0,
                       help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--all', '-a', action='store_true',
                       help='Extract all matching elements (default: first only)')
    parser.add_argument('--json', '-j', action='store_true',
                       help='Output results as JSON')
    
    args = parser.parse_args()
    
    # Create scraper instance with specified delay
    scraper = WebScraper(delay=args.delay)
    
    # Perform the scraping
    results = scraper.scrape(args.url, args.selectors, args.all)
    
    # Output results in requested format
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for selector, content in results.items():
            if content:
                if isinstance(content, list):
                    print(f"{selector}: {len(content)} items found")
                    for i, item in enumerate(content, 1):
                        print(f"  {i}. {item}")
                else:
                    print(f"{selector}: {content}")
            else:
                print(f"{selector}: Not found")


# Example usage for SEC documents (original use case)
def scrape_sec_document():
    """Example function showing how to use the scraper for SEC documents."""
    scraper = WebScraper(delay=1.0)
    results = scraper.scrape(
        "https://www.sec.gov/rules-regulations/2025/03/s7-16-22",
        ["h1", ".summary", "p"]
    )
    return results


if __name__ == "__main__":
    main()
