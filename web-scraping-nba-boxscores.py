from selenium import webdriver
from bs4 import BeautifulSoup as soup 
import pandas as pd


def get_boxscores(szn):
    season = szn
    d = webdriver.Chrome('C:/Windows/System32/chromedriver_win32/chromedriver')
    d.get('https://www.nba.com/stats/teams/boxscores-traditional/?Season={}&SeasonType=Regular%20Season&sort=MIN&dir=1'.format(season))
    d.set_window_position(0, 0)
    d.set_window_size(100000, 200000)
    d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    d.find_element_by_xpath('/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[1]/div/div/select/option[1]').click()
    #d.get('https://www.nba.com/stats/teams/boxscores-traditional/?Season=2015-16&SeasonType=Regular%20Season&sort=MIN&dir=1')
    #s=soup(d.page_source, 'html.parser').find('nba-stat-table', {'class': 'stats-table-next'}).find('div', {'class':'stats-table-pagination__inner'}).find('div', {'class': 'stats-table-pagination__info'}).find('select', {'class':'stats-table-pagination__select'}).find('option', {'label': 'All'})

    s = soup(d.page_source, 'html.parser').find('div', {'class':'nba-stat-table'})


    #headers, [_, *data] = [i.text for i in s.find_all('th')], [[i.text for i in b.find_all('td')] for b in s.find_all('tr')]
    #final_data = [i for i in data if len(i) > 1]
    #final_data


    #table = browser.find_element_by_class_name


    #print([s["data-pages"] for s in soup.select("select.catalogPagination_dropdown") if s.has_attr("data-pages")])


    header = [i.text for i in s.find_all('tr')[0].find_all('th')]
    #index 
    tbody= s.find('tbody')
    df = pd.DataFrame(columns = header)
    rows = tbody.find_all('tr')
    for row in rows: 
        tds = row.find_all('td')
        if len(tds) >1:
            df = df.append(pd.Series([td.text for td in tds], index=header),ignore_index=True)

    df.to_csv('C:/Users/sathw/OneDrive/Desktop/KMeans-Clustering-NBA-Teams/data/totals_{}.csv'.format(season), index=False)


seasons = ['2014-15','2015-16','2016-17','2017-18','2018-19']
for szn in seasons:
    get_boxscores(szn)