import pandas as pd
import numpy as np

ladiesdf = pd.read_pickle("~/ski/elo/python/ski/ladiesdf.pkl")

mendf = pd.read_pickle("~/ski/elo/python/ski/mendf.pkl")

import numpy as np
K=1

def EA (pelos ,place):
	players = len(pelos)
	ra = pelos[place - 1]
	QA = 10**(ra/400) 
	QA = np.repeat(QA, players - 1)

	rb = np.delete(np.array(pelos), place - 1)
	QB = 10**(rb/400)
	EA = QA / (QA + QB)
	return EA

def SA (pelos,place):
	players = len(pelos)
	return (place - 1)*[0] + (players-place)*[1]


def lady_elo():
	ladiesdf = pd.DataFrame()
	name_pool = []
	seasons = pd.unique(ladiesdf['season'])
	#for season in range(len(seasons)):
	for season in range(1):
		seasondf = ladiesdf.loc[ladiesdf['season']==seasons[season]]
		races = pd.unique(seasondf['race'])
		for race in range(len(races)):
			pelo_list = []
			elo_list = []
			racedf = seasondf.loc[seasondf['race']==races[race]]
			racedf.reset_index(inplace=True, drop=True)
			for a in range(len(racedf['name'])):
				if (racedf['name'][a] not in name_pool):
					name_pool.append(racedf['name'][a])
					pelo_list.append(1300)
				else:
					#print("yo")
					#Get the vet skiers line
					vetskier = ladieselodf.loc[ladieselodf['name']==racedf['name'][a]]
					pelo_list.append(vetskier['elo'].iloc[-1])


				#else we have to find them and see if they are the same person
				#else we have to find their last elo in ladieselodf
			racedf['pelo'] = pelo_list
			for b in range(len(pelo_list)):
				print(pelo_list[b])
				place = b+1
				print(pelo_list[place-1] + K*(sum(SA(pelo, place)) - sum(EA(pelo,place))))


print(lady_elo())