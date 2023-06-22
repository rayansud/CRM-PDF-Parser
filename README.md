# CRM PDF Scraper

This program pulls all published articles on the CRM Brookings website as a clean PDF.

## Instructions for use

1. Install Python 3.9 or above, and make sure you have Google Chrome installed
2. Download and unzip this repo
3. Navigate to the downloaded folder in your terminal
4. Install all required packages with the command `pip install requirement.txt`
5. Go to `https://www.brookings.edu/center/center-on-regulation-and-markets/page/2/` and click "Show More" at the bottom for as long as you like, until it shows all the articles you need
6. Save the webpage as `CRM_articles.html`
7. Run the script by running `python main.py` in your terminal
8. The PDFs will download over some time, to the `downloads` folder, arranged by year, author, and title
