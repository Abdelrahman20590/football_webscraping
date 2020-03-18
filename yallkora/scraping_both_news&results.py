import requests
from bs4 import BeautifulSoup
import pprint


def get_html(date=None):
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
        print('There was a problem: %s' % (exc))

    return page.text


class YallkoraScrapper:
    def __init__(self, date=None):
        self.date = date

    '''
    This is a class for Web Scraping Yallkora Website:
             1- match_result(): To get the match result of that date.
             2- recent_news(): To get the recent news at the site right now.
    '''

    # TODO: METHOD FOR EXTRACT MATCHES RESULTS
    def match_results(self):
        # Store Data Dictionary.
        data_dict = {}

        # Create empty lists for store data
        total_teamsA, total_teamsB, league_list, time_list, week_list, tv_list = [], [], [], [], [], []
        score_teamA, score_teamB = [], []

        # Get the Page Content as a String Html.
        page_content = get_html(self.date)

        # Parse the page_content as a beautiful soup object with "lxml" parser
        soup = BeautifulSoup(page_content, 'lxml')

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
        # print(match_board[0])


        # data_dict['Teams A List'] = total_teamsA
        # data_dict['Teams B List'] = total_teamsB
        data_dict['Match Board'] = match_board
        data_dict['Tournament or League Names'] = league_list
        data_dict['Match Time'] = time_list
        data_dict['Week or Round'] = week_list
        data_dict['TV channel'] = tv_list



        pprint.pprint(data_dict)

    # TODO: METHOD FOR EXTRACT RECENT HEADLINES & MOST IMPORTANT ARTICLE.
    def recent_news(self):
        pass


""" I Choose this date because there aren't any matches now"""
if __name__ == "__main__":
    YallkoraScrapper('3/8/2020').match_results()


