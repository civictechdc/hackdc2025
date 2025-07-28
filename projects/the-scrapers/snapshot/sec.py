import requests
import re
import sys
import json

from bs4 import BeautifulSoup

# Author: Misha Vinokur.

# Goal:
# Scrape the SEC website and atempt to get data into a format that mirrulations can use. 

# Full list can be found: 
# https://www.sec.gov/rules-regulations/rulemaking-activity
# Single Rule: https://www.sec.gov/rules-regulations/2025/06/s7-11-23#34-103320final
# comments for single rule: https://www.sec.gov/comments/s7-11-23/s71123.htm

# How to use:
# Run the command sec.py [url]

# Notes for future developer
# The SEC website blocks many common scrapers, the way we went about this was to use sequence of
# CURL commands to access the website. 

# Test here is can we scrape a single rule comment page. 
# url = "https://www.sec.gov/rules-regulations/2025/06/s7-11-23#34-103320final"

url = sys.argv[1]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.sec.gov/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

# Note, we do this because sec.gov blocks most common scrape tools. 
try:
    response = requests.get(url, headers=headers, timeout=15)
    html = response.text
    http_code = response.status_code
    print(f"HTTP {http_code}")

except requests.RequestException as e:
    print(f"Request failed: {e}")

soup = BeautifulSoup(html, "html.parser")

# Get Docket ID. 
# We get this via RegEx from the url path e.g. https://www.sec.gov/rules-regulations/2025/06/s7-11-23#34-103320final
match = re.search(r"/(s7-\d+-\d+)", url, re.IGNORECASE)
docket_id = "id:", match.group(1)

# Get docket title:
# We get this from the h1 value
docket_title = "title:", soup.find("h1").text.strip()

# The links are found in the <table> tag;
table = soup.find("table")
links = table.find_all("a");
file_links = "links:", [a['href'] for a in links if a.has_attr('href')]

# This is the output of a single docket comment value
data = [docket_id, docket_title, file_links];

# Output as JSON
print(json.dumps(data));
