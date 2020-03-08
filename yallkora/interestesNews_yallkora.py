#! python3
# mainNews_yallkora.py - Finding All interested_Area_news & its direct links in "https://www.yallkora.com"
# and make an excel file with all these data.


import requests
from bs4 import BeautifulSoup
import pandas as pd

# Get the Page text as html string
page_content = requests.get('https://www.yallakora.com').text

# Parse the hole html string as a beautifulsoup object
soup = BeautifulSoup(page_content, 'lxml')

# Find The area of the html you want to web scraping (interestedArticles)
interestedArticles = soup.find('section', class_='interestedArticles')  # find return a string
headlinesDiv = interestedArticles.find_all('li', class_='item')         # find_all return a list of all item.

# Create empty lists to append the data
links_headlines = []
headlines = []
num = []

# Loop through all lists "li" to get the paragraph <p> & links "href"
for i in range(len(headlinesDiv)):
    # Get the number of list
    num.append(i + 1)
    # Get headlines <p>
    headlines.append(headlinesDiv[i].p.text.strip())
    # Get links "href"
    for a in headlinesDiv[i].find_all('a', href=True):
        links_headlines.append('https://www.yallakora.com/' + a['href'])


# Make data frame with pandas module to save data
yallkora_file = pd.DataFrame({
    'ترتيب الاخبار الحالي': num,
    'عناوين الأخبار': headlines,
    'لينك الخبر علي الموقع (تحويل مباشر)': links_headlines
})

''' I install "openpyxl" library before this step to make an excel sheet with pandas'''
# Create an excel file
yallkora_file.to_excel('yallkoraInterestedArticles.xlsx')
