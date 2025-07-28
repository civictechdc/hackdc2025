import requests
import json

urlProceeding = 'https://publicapi.fcc.gov/ecfs/proceedings'
urlFiling = 'https://publicapi.fcc.gov/ecfs/filings'
# Free API Key can be signed for here: https://www.fcc.gov/ecfs/help/public_api
api_key = "HqtoNwrICfhxiKr9hDHVELP5P6s3ex13SKqbJbJd"
# Parameter for pulling proceedings from a specific date range. Format is [gte]StartDate[lte]EndDate
proceedingCreated = "[gte]2000-01-01[lte]2025-07-26"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "x-api-key": api_key
}

paramProceeding ={
    "api_key" : api_key,
    "date_proceeding_created" : proceedingCreated   
}

r = requests.get(urlProceeding, headers=headers, params=paramProceeding)
if r.status_code == 200:
    print("Request Successful")
    dataList = r.json()
    formatted_json = json.dumps(dataList, indent=4, sort_keys=True)
    # Uncomment next line to print formatted JSON for debugging
    # print(formatted_json)

    # Save each proceeding in data request
    proceedings = dataList.get("proceeding", [])
    # print(f"Total Proceedings Found: {len(proceedings)}")

    # Only grab proceedings that have a public comment (filing)
    filtered_proceedings = [
        p for p in proceedings if "total_filing_count" in p
    ]
    # Iterate through each proceeding to grab it's proceeding code 
    for p in filtered_proceedings:
        # Grab the Docket Name
        savedName = p.get("name")
        numComments = p.get("total_filing_count")
        paramFiling = {
            "api_key" : api_key,
            "proceedings.name" : savedName
        }
        # print(savedName)
        rfile = requests.get(urlFiling, headers=headers, params=paramFiling)
        fileData = rfile.json()
        formatted_filejson = json.dumps(fileData, indent=4, sort_keys=True)
        # print(formatted_filejson)

        # Grab the filings within the proceeding specified
        filings = fileData.get("filing",[])
        # For each filing, grab any documents or comments
        for filing in filings:
            # Grab the comments
                # TO DO: Parse filings to grab the comment text
            # Grab any pdfs or downloadable documents
            docs = filing.get("documents",[])
            for d in docs:
                document_source_link = d.get("src",[])
                # TO DO: Download document using the document source link
            formatted_filingsjson = json.dumps(filings, indent=4, sort_keys=True)
else:
    print(f"Error {r.status_code}: {r.text}")