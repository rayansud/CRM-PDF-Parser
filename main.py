
# Import statements for external packages

import unicodedata
import re
from bs4 import BeautifulSoup
from requests import get
from pathlib import Path
import sys
import pdfkit
from tqdm import tqdm
import os
from pyhtml2pdf import converter
from datetime import datetime

# StackExchange-borrowed function that takes in a string and returns a string that is filename safe 
# (no special characters, spaces, etc.)
def slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

headers = {'Accept-Encoding': 'identity'}

# Opens the "CRM_articles.html" file in BeautifulSoup
with open('CRM_articles.html') as fp:
    soup = BeautifulSoup(fp, "html.parser")

# Finds each article-sections in the list of articles
articles = soup.find_all("article", class_="archive-view report research has-image")

#Loops over each article
for article in tqdm(articles):
    #Pulls the article-info div
    article_info = article.find('div',class_="article-info")
    #Pulls the heading from inside the article-info div
    heading = article_info.find('h4',class_="title")
    #Pulls metadata from the article-info div
    meta = article_info.find('div',class_="meta")
    #Pulls the author metadata from the metadata sub-div
    authors = meta.find('div',class_='authors').text
    #Cleans up the author names into LastName-LastName-LastName...
    authors = authors.replace(' and ',',')
    authors = authors.split(',')
    authors = [s.strip() for s in authors]
    authors = [i for i in authors if i]
    authors = [i.split(' ')[-1] for i in authors if i]
    authors = '-'.join(authors)

    #Pulls the publication time metadata from the metadata sub-div
    time = meta.find('time').text
    #Cleans up the publication time into YYYY-MM-DD
    time = datetime.strptime(time,"%A, %B %d, %Y")
    year = time.year
    timestring = time.strftime("%Y.%m.%d")    
    
    #Pulls the link to the article page
    link = heading.find('a')
    #Prepares the filename to save the PDF to
    filename = slugify(heading.text)+".pdf"
    full_namestring = 'downloads/' + str(year) + '/' + timestring + " " + authors + ' ' + filename
    
    #Downloads the html content of the page
    link_html = get(link['href'],headers=headers).content
    #Parses the html content of the page    
    link_html_bs = BeautifulSoup(link_html, "html.parser")
    
    #Uses a "try" statement in case there are any errors and the page doesn't have these components
    try:
        #Removes a bunch of unnecessary components, like popups, newsletters, sidebars, etc. for a clean PDF
        link_html_bs.find('nav', class_="push-nav").decompose()
        link_html_bs.find('section', class_="newsletter newsletter-module full rollup").decompose()
        link_html_bs.find('section', class_="module-secondary feature-more-on").decompose()
        link_html_bs.find('section', class_="related-topics").decompose()
        link_html_bs.find('section', class_="linear-related expandable-list-wrapper").decompose()
        link_html_bs.find('aside', class_="report-sidebar").decompose()
    except:
        print('error')
    #Saves the modified HTML of the article to the "output_tmp.html" file
    with open("output_tmp.html", "w") as file:
        file.write(str(link_html_bs))
    path = os.path.abspath('output_tmp.html')
    #Converts the temporary HTML file to a PDF using pyhtml2pdf package, and saves it
    converter.convert(f'file:///{path}', full_namestring)