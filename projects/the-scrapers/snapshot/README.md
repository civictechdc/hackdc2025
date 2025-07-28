This is the web scraping team's work for the Civic Tech DC hackathon.

We each tried different approaches to scraping the SEC and FEC websites
- File sec_web_scraper.py is a scraper built with AI LLM
- File FCCScraping.py is an API interpreter using the FCC API 
- File sec.py is a basic file where you can type in the sec rule comment page and it will output the docket ID and description. via command python3 `sec.py [url]`


# FCCScraping.py
* Given a range of proceeding creation dates, pull all proceedings within that range to process
* Obtain the Docket # and # of Filings under each proceeding
* Iterate through each of the Filings within each proceeding and obtain:
  * Every document link attached to a Filing
  * The comment text associated with the Filing

# Sec.py
## The use of these files for mirrulations.
Scrape SEC rule comments (Updated Code) - https://github.com/Cromian/sec-comments
