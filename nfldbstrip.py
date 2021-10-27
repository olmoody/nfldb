import requests
import pandas as pd
from bs4 import BeautifulSoup
YEAR=2019
#pp = pprint.PrettyPrinter(indent=4)
data = []
URL = 'https://www.pro-football-reference.com/boxscores/202109120nwe.htm'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
headers = []
header = soup.find(id="div_player_offense")
if header:
    header = header.find_all('tr')[1]
    print(header)
    for items in header:
        try:
            text =items.get_text().rstrip()
            if text:
                headers.append(text)
        except:
            raise "No columns"
    print(headers)



#print(list_header)
teams = ["buf","mia","nwe","nyj","was","nyg","dal","phi","pit","cle","rav","cin","clt","oti","htx","jax","gnb","chi","min","det","nor","tam","atl","car","kan","rai","sdg","den","sea","ram","crd","sfo"]
# # for getting the data
dataFrame = pd.DataFrame(columns = headers)

data = []
#dates = ['202109120']
dates = ['201909050','201909080','201909090','2019090120','201909150','201909160','201909190','201909220','201909230','201909260',
'201909290','201909300','201910030','201910060','201910070','201910100','201910130','201910140','201910170','201910200','201910210',
'201910240','201910270','201910280','201910310','201911030','201911040','201911070','201911100','201911110','201911140','201911170',
'201911180','201911210','201911240','201911250','201911280','201912010','201912020','201912050','201912080','201912090','201912120',
'201912150','201912160','201912210','201912220','201912230','201912290',]
for date in dates:
    for team in teams:
        URL = 'https://www.pro-football-reference.com/boxscores/'+date+team+'.htm'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        players = soup.find(id="div_player_offense")
        if players:
            players = players.find_all(attrs={"data-stat": "player"})
        else:
            continue
        stats = soup.find(id="div_player_offense") #.find_all(attrs={"data-stat": "pass_yds"})
        if stats:
            stats = stats.find_all('td')
        else:
            continue

        game = []
        for items in players:
            try:
                text =items.get_text()
                if text=="Player":
                    continue
                game.append([text])
            except:
                continue
        for i,items in enumerate(stats):
            if i%21==0:
                data.append(game[i//21])
            try:
                game[i//21].append(items.get_text())
            except:
                continue
#print(data)

# Storing the data into Pandas
# DataFrame
dataFrame = pd.DataFrame(data = data, columns = headers)
print(dataFrame)


# Converting Pandas DataFrame
# into CSV file
dataFrame.to_csv('nfldata'+str(YEAR)+'.csv')

#results = soup.find(id='csv_gamelog2020')
#pp.pprint(results)
#print(page)
