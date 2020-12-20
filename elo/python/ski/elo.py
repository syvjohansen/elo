import pandas as pd

xlsx = pd.ExcelFile('~/ski/elo/excel365/all.xlsx')
ladiesdf = pd.read_excel(xlsx, sheet_name="Ladies", header=None)
mendf = pd.read_excel(xlsx, "Men", header=None)
ladiesdf.columns = ['date', 'city', 'country', 'level', 'sex', 'distance', 'discipline', 'place', 'name', 'nation']
mendf.columns = ['date', 'city', 'country', 'level', 'sex', 'distance', 'discipline', 'place', 'name', 'nation']


#ladies_places = list(int(ladiesdf['place']))
lady_seasons = []
for a in range(len(ladiesdf['date'])):
	date = str(ladiesdf['date'][a])
	year = date[0:4]
	day = date[4:8]
	if(day>'0500'):
		season = int(year)+1
	else:
		season = int(year)
	lady_seasons.append(season)

ladiesdf['seasons'] = lady_seasons



ladies_race = []
race = 1

for a in range(len(ladiesdf['place'])):
	if (a==1):
		ladies_race.append(race)
		continue
	if (lady_seasons[a]!=lady_seasons[a-1]):
		race=1
		ladies_race.append(race)
	elif(ladiesdf['date'][a]!=ladiesdf['date'][a-1]):
		race+=1
		ladies_race.append(race)
	elif(str(ladiesdf['place'][a])=='1'):
		if(str(ladiesdf['place'][a-1])>'1'):
			race+=1
			ladies_race.append(race)
		else:
			ladies_race.append(race)
	else:
		ladies_race.append(race)
print(len(ladies_race))
print(len(ladiesdf['place']))


ladiesdf['race'] = ladies_race
print(ladiesdf['race'])


print(ladiesdf.head())
print(mendf.head())