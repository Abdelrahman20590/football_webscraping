from bs4 import BeautifulSoup
import requests
from pandas import DataFrame


class Yallkora:
    '''
        This is a Web Scraping Yallkora Website:
                 1- matches_results(): To get the match result of that date - format (month/day/year).
                 2- save_images(): To save the recent news images at the site.
                 3- main_news(): To save the recent main news & its links.
        All save as an excel file
        '''

    # Get the Yallkora main page "res -->  Class Variable"
    res = requests.get("https://www.yallakora.com/")
    try:
        res.raise_for_status()
    except Exception as exc:
        print("There was a problem: {}".format(exc))

    @staticmethod
    def matches_results(date=None):
        """take date argument if you want matches results for specific day,
           if no date has given : you will get the current day matches results.
        """
        # Get the exact url that contains the user results date.
        if not date:
            url = 'https://www.yallakora.com/Match-Center/'
        else:
            dt = f'?date={date}#days'
            url = 'https://www.yallakora.com/Match-Center/' + dt

        # Get the Page text as html string by requests module
        page = requests.get(url)
        try:
            page.raise_for_status()
        except Exception as exc:
            print('There was a problem: {}'.format(exc))

        # Create empty lists for store data
        total_teamsA, total_teamsB, league_list, time_list, week_list, tv_list = [], [], [], [], [], []
        score_teamA, score_teamB = [], []

        # Parse the page_content as a beautiful soup object with "lxml" parser
        soup = BeautifulSoup(page.text, 'lxml')
        # Specify the area of html which has the matches for every football tournament
        tournments = soup.select('.mtchObjContainer')
        # Specify the area of html which has the title of the tournament ( this is a list of item for each tournament )
        leagueTitle = soup.select('.ttl')

        #  make a loop for every tournament in the page.
        for i in range(len(tournments)):
            # Extract the Area of each tournament matches with looping through all tournaments
            itemMatch = tournments[i].find_all('li', class_='item matchObj mix done')
            if not itemMatch:
                itemMatch = tournments[i].find_all('li', class_='item matchObj mix soon')
            # Extract the league title
            theLeague = leagueTitle[i].h2.text.strip()
            league_list.append(theLeague)

            # Creating lists for saving teamA & team B
            teamA, teamB = [], []

            # Looping through every match at each tournament
            for y in range(len(itemMatch)):
                # Extract each team name from the match item
                teamName = itemMatch[y].select('.teamName')
                a = teamName[0].text.strip()
                b = teamName[1].text.strip()
                teamA.append(a)
                teamB.append(b)
                total_teamsA.append(a)
                total_teamsB.append(b)

                # Extract match time for each match of the tournament
                time_match = itemMatch[y].select('.matchTime')[0].text.strip()
                time_list.append(time_match)

                # Extract match Week number of the tournament
                weekNumber = itemMatch[y].select('.week')[0].text.strip()
                week_list.append(weekNumber)

                # Extract TV Channels
                tvChannel = itemMatch[y].find('div', class_='tv icon-tv').text.strip()
                tv_list.append(tvChannel)

                # Extract match result as teamsA score list & teamsB score list
                scoreA = itemMatch[y].select('.result')
                score_teamA.append(scoreA[0].text.strip())
                score_teamB.append(scoreA[1].text.strip())

        # Formate Match playboard
        match_board = [total_teamsA[i] + "  " + score_teamA[i] + " : " + score_teamB[i] + "  " + total_teamsB[i]
                       for i in range(len(total_teamsA))]

        pd = DataFrame({"Match Board": match_board, "Match Time": time_list, "TV Channel": tv_list})
        return pd.to_excel("matchResults2.xlsx")

    @classmethod
    def main_news(cls):
        # Make an beautiful soup object
        yall_soup = BeautifulSoup(cls.res.text, 'lxml')

        headlines = yall_soup.find_all('div', class_='desc')
        links = yall_soup.find_all('a', class_='link')

        # Saving Only 6 Main news headlines & its links
        linksList = ['https://www.yallakora.com/' + links[i]['href'].split("%")[0] for i in range(len(links)) if i < 6]
        headlinesList = [headlines[i].text.strip() for i in range(len(headlines)) if i < 6]

        # Saving to an excel sheet
        pd = DataFrame({"HeadLines": headlinesList, "Link": linksList})
        pd.to_excel("scraping2.xlsx")

    @classmethod
    def save_images(cls):
        # Make an beautiful soup object
        yall_soup = BeautifulSoup(cls.res.text, 'lxml')

        # searching for every image by CSS class named "imageCntnr"
        img_center = yall_soup.select('.imageCntnr')  # [0].find("img")['data-src']

        # make a list for img url and alternate text for each if it is exists
        img_url = [img.find("img")['data-src'].replace("\\", "/") for img in img_center]
        img_alt = [img.find('img')['alt'] for img in img_center]

        for i, url in enumerate(img_url):
            # Get url of an image
            img_res = requests.get(url)
            print(f"Image number {i + 1} copied!")

            # saving every image with unique index name
            with open(f'imgs/YallImage{i}.jpg', 'wb') as f:
                for chunk in img_res.iter_content(100_000):
                    f.write(chunk)
        print('ok')


if __name__ == "__main__":
    scraper = Yallkora()

    """ I Choose this date because there aren't any football matches right now"""
    scraper.matches_results('3/8/2020')

    """ Saving All Images of Main Page to a imgs folder at our directory"""
    scraper.save_images()

    """Saving 6 Main Recent Headlines of Main Page """
    scraper.main_news()
