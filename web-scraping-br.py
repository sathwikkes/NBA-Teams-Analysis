from bs4 import BeautifulSoup, Comment 
import requests 
import pandas as pd
import json


def scrape_data(y):
    year = y
    url = "https://www.basketball-reference.com/leagues/NBA_{}.html".format(year)
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.content, 'lxml')
    # https://stackoverflow.com/questions/55198103/scraping-difficult-table <- genius
    placeholder = soup.select_one('#all_team-stats-base .placeholder')
    placeholder2 = soup.select_one('#all_team-stats-per_game .placeholder')
    comment = next(elem for elem in placeholder.next_siblings if isinstance(elem, Comment))
    comment2 = next(elem for elem in placeholder2.next_siblings if isinstance(elem, Comment))
    table_soup = BeautifulSoup(comment, 'lxml')
    table_soup2 = BeautifulSoup(comment2, 'lxml')

    header = [i.text for i in table_soup.find_all('tr')[0].find_all('th')]
    header2 = [i.text for i in table_soup2.find_all('tr')[0].find_all('th')]
    header = header[1:]
    header2 = header2[1:]

    df = pd.DataFrame(columns = header)
    df2 = pd.DataFrame(columns = header2)

    rows = table_soup.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        if tds:
            df = df.append(pd.Series([td.text for td in tds], index=header),ignore_index=True)

    rows2 = table_soup2.find_all('tr')
    for row in rows2:
        td = row.find_all('td')
        if td:
            df2 = df2.append(pd.Series([ts.text for ts in td], index = header2), ignore_index=True)

    df.columns = ['Team', 'G', 'MP-Total', 'FGM-Total', 'FGA-Total', 'FG%-Total', '3PM-Total', '3PA-Total', '3P%-Total', 
                '2PM-Total', '2PA-Total', '2P%-Total', 'FTM-Total', 'FTA-Total', 'FT%-Total', 'ORB-Total', 'DRB-Total', 
                'TRB-Total', 'AST-Total', 'STL-Total', 'BLK-Total', 'TOV-Total', 'PF-Total', 'PTS-Total']
    df2.columns =  ['Team2', 'G2','MP-PG', 'FGM-PG', 'FGA-PG', 'FG%-PG', '3PM-PG', '3PA-PG', '3P%-PG', 
                '2PM-PG', '2PA-PG', '2P%-PG', 'FTM-PG', 'FTA-PG', 'FT%-PG', 'ORB-PG', 'DRB-PG', 
                'TRB-PG', 'AST-PG', 'STL-PG', 'BLK-PG', 'TOV-PG', 'PF-PG', 'PTS-PG']
    result = [df, df2]
    blah = pd.concat(result, axis=1)
    print(blah.head())

    blah.to_csv('C:/Users/sathw/OneDrive/Desktop/KMeans-Clustering-NBA-Teams/data/totals_{}.csv'.format(year), index=False)


years = [2015,2016,2017,2018,2019]
for year in years:
    scrape_data(year)