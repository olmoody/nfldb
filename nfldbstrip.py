import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv
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
    #print(header)
    for items in header:
        try:
            text =items.get_text().rstrip()
            if text:
                headers.append(text)
        except:
            raise "No columns"
    headers.append("gameid")
    print(headers)



with open('NFL DB - Players.csv', mode='r') as infile:
    reader = csv.reader(infile)
    playertoid = {tuple(rows[1].split()[:2]):rows[0] for rows in reader}
#print(playertoid["Nick Foles"])
notfound = {}
newid = len(playertoid.keys())+2
#print(list_header)
teams = ["buf","mia","nwe","nyj","was","nyg","dal","phi","pit","cle","rav","cin","clt","oti","htx","jax","gnb","chi","min","det","nor","tam","atl","car","kan","rai","sdg","den","sea","ram","crd","sfo"]
# # for getting the data
dataFrame = pd.DataFrame(columns = headers)
gameheaders = ["hometeam", "awayteam", "weeknum","date","season"]
data = []
games = []
#dates = ['202109120']
dates = ['201909050','201909080','201909090','201909120','201909150','201909160','201909190','201909220','201909230','201909260',
'201909290','201909300','201910030','201910060','201910070','201910100','201910130','201910140','201910170','201910200','201910210',
'201910240','201910270','201910280','201910310','201911030','201911040','201911070','201911100','201911110','201911140','201911170',
'201911180','201911210','201911240','201911250','201911280','201912010','201912020','201912050','201912080','201912090','201912120',
'201912150','201912160','201912210','201912220','201912230','201912290']
for datenum,date in enumerate(dates):
    for team in teams:
        URL = 'https://www.pro-football-reference.com/boxscores/'+date+team+'.htm'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        game = []
        gameinfo = []

        #gamestattable = gamestattable.find(id="div_team_stats")

        #if gamestattable:
            #awayteam = gamestattable.find_all(attrs={"data-stat": "vis-stat"})
            #hometeam = gamestattable.find_all(attrs={"data-stat": "home-stat"})
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

        teamstable = soup.find(id="div_scoring")
        #print(teamstable)
        teamheader = teamstable.find("thead").find_all("th")
        if teamstable:
            awayteam = teamheader[-2].get_text()
            hometeam = teamheader[-1].get_text()
        else:
            continue
        gameinfo =[hometeam,awayteam,datenum//3+1,date,YEAR]
        games.append(gameinfo)

        #print(hometeam,awayteam)
        for items in players:
            try:
                text =items.get_text()
                if text=="Player":
                    continue
            except:
                continue
            text = tuple(text.split()[:2])
            if text in playertoid:

                playerid = playertoid[text]
            else:
                if text in notfound:
                    playerid = notfound[text][2]
                else:
                    playerid = newid
                    newid +=1
                    notfound[text]=(date,team,playerid)
            game.append([playerid])
        #print(game,stats)
        for i,items in enumerate(stats):
            if i%21==0:
                data.append(game[i//21])
            try:
                game[i//21].append(items.get_text())
            except:
                continue

        for g in game:
            g.append(len(games)-1)
#print(data)

# Storing the data into Pandas
# DataFrame
dataFrame = pd.DataFrame(data = data, columns = headers)
gamedf = pd.DataFrame(data = games,columns= gameheaders)
#print(dataFrame)


# Converting Pandas DataFrame
# into CSV file
print(notfound)
dataFrame.to_csv('nfldata'+str(YEAR)+'.csv')
gamedf.to_csv('nflgamedata'+str(YEAR)+'.csv')

#results = soup.find(id='csv_gamelog2020')
#pp.pprint(results)
#print(page)
