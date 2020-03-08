#! python3
# mainNews_yallkora.py - Finding All main_news & its direct links in "https://www.yallkora.com"
# and make an excel file with all these data.

# libraries for the project are: beautifulsoup4, requests, pandas, lxml
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Get the Page text as html string
page_content = requests.get('https://www.yallakora.com').text

# Parse the page_content as a beautiful soup object with "lxml" parser
soup = BeautifulSoup(page_content, 'lxml')

# Find The area of the html you want to web scraping (featuredArea)
featuredArea = soup.find('section', class_='featuredArea')     # find return a string
headlinesDiv = featuredArea.find_all('div', class_='desc')     # find_all return a list of all item.

# Create empty lists to append the data
link_headlines = []
headlines = []
num = []

# Loop through all lists "li" to get the paragraph <p> & links "href"
for i in range(len(headlinesDiv)):
    # Get number of the headline
    num.append(i + 1)
    # Get <p>
    headlines.append(headlinesDiv[i].p.text.strip())
    # Get links "href"
    links = featuredArea.find_all('a', class_='link')
    link_headlines.append('https://www.yallakora.com/' + links[i]['href'])

# Make data frame with pandas module to save data
yallkora_headlines = pd.DataFrame({
    'الترتيب': num,
    'عناوين الأخبار': headlines,
    'لينك الخبر علي موقع يلاكورة ( تحويل مباشر )': link_headlines
})

''' I install "openpyxl" library before this step
    to make an excel sheet with pandas'''
# Create an excel file
yallkora_headlines.to_excel('yallkora_links&headlines.xlsx')
