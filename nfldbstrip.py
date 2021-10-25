import requests
import pandas as pd
from bs4 import BeautifulSoup
YEAR=2020
#pp = pprint.PrettyPrinter(indent=4)
data = []
URL = 'https://www.pro-football-reference.com/boxscores/202109120nwe.htm'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
header = soup.find(id="div_player_offense").find_all('tr')[1]
headers = []
for items in header:
    try:
        headers.append(items.get_text())
    except:
        continue
print(headers)

#print(list_header)
# teams = ["buf","mia","nwe","nyj","was","nyg","dal","phi","pit","cle","rav","cin","clt","oti","htx","jax","gnb","chi","min","det","nor","tam","atl","car","kan","rai","sdg","den","sea","ram","crd","sfo"]
# # for getting the data
dataFrame = pd.DataFrame(columns = headers)

data = []
URL = 'https://www.pro-football-reference.com/boxscores/202109120nwe.htm'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
players = soup.find(id="div_player_offense").find_all(attrs={"data-stat": "player"})
stats = soup.find(id="div_player_offense").find_all('td') #.find_all(attrs={"data-stat": "pass_yds"})
list_header = []
lheader1 = []
for items in players:
    try:
        text =items.get_text()
        if text=="Player":
            continue
        lheader1.append([text])
    except:
        continue
for i,items in enumerate(stats):
    if i%21==0:
        list_header.append(lheader1[i//21])
    try:
        lheader1[i//21].append(items.get_text())
    except:
        continue
print(lheader1)
# print(len(teams))
# for team in teams:
#     print(team)
#     URL = 'https://www.pro-football-reference.com/boxscores/'+date+'/'+team+'/'
#     page = requests.get(URL)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     HTML_data = soup.find(id="gamelog"+str(YEAR)).find_all("tr")[2:]
#
#     for element in HTML_data:
#         sub_data = [team]
#         for sub_element in element:
#             try:
#                 sub_data.append(sub_element.get_text())
#             except:
#                 continue
#         data.append(sub_data)
#
#     # Storing the data into Pandas
#     # DataFrame
#     dataFramenew = pd.DataFrame(data = data, columns = list_header)
#     dataFramenew.append(dataFrame)
#     #print(dataFrame)
# # Converting Pandas DataFrame
# # into CSV file
# dataFramenew.to_csv('nfldata'+str(YEAR)+'.csv')

#results = soup.find(id='csv_gamelog2020')
#pp.pprint(results)
#print(page)
