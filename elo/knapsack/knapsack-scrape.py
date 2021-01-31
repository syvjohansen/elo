from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd
import time
import json
from pandas.io.json import json_normalize
pd.options.mode.chained_assignment = None

import time
start_time = time.time()





	#return {'id':ids, 'sex':sex}
def fis_team_sprint():
	ids = []
	teams = []
	sex = []
	count = 0
	#start with the men
	startlist_list = ['https://www.fis-ski.com/DB/general/results.html?sectorcode=CC&raceid=36502',
'https://www.fis-ski.com/DB/general/results.html?sectorcode=CC&raceid=38411',
'https://www.fis-ski.com/DB/general/results.html?sectorcode=CC&raceid=36501',
'https://www.fis-ski.com/DB/general/results.html?sectorcode=CC&raceid=38410']
	for a in range(len(startlist_list)):
		startlist = BeautifulSoup(urlopen(startlist_list[a]), 'html.parser')
	#print(startlist)
		names = startlist.find_all('div', {'g-lg-14 g-md-14 g-sm-11 g-xs-10 justify-left bold'})
		body = startlist.find_all('div', {'g-lg-2 g-md-2 g-sm-3 hidden-xs justify-right gray pr-1'})
		print(startlist_list[a])

		for b in range(len(body)):
			#print(body[a].text.strip())
			if(b%3!=0):
				ids.append(int(body[b].text.strip()))
			else:
				team = names[b].text.strip()
				if(a<2):
					team = "m"+team
				else:
					team = "f"+team
				ids.append(team)
			#if(count==0):
			#	sex.append('M')
			#else:
			#	sex.append('L')
		
		

		#print(team)
		count+=1

	print(ids)

	

	#now for the ladies
	
	return ids

def fantasy_team_sprint(startlist):
	name = []
	team_name = []
	team_id = []
	team_price = []
	team_sex = []
	ski_id = []
	price =[]
	sex = []
	#sex = startlist['sex']
	#startlist = startlist['id']
	#print(sex)
	#print(startlist)
	fantasy = 'https://www.fantasyxc.se/api/athletes'
	#soup = BeautifulSoup(urlopen(fantasy), 'html5lib')
	#print(soup)
	with requests.Session() as s:
		r=s.get(fantasy)
		soup = BeautifulSoup(r.content, 'html5lib')
	API_json = json.loads(soup.get_text())
	API_df = pd.DataFrame.from_dict(pd.json_normalize(API_json), orient='columns')

	##Change to locate for increased speed
	for a in range(len(startlist)):
		if(a%3==0):
			
			if(startlist[a].startswith("m")):
				#print(startlist[a])
				country_name = startlist[a]
				country_name = country_name.split("m")
				country_name = country_name[1]
				if(country_name.endswith(" I") or country_name.endswith(" II")):
					pass
				else:
					country_name = country_name + " I"

				nation= API_df.loc[API_df['name']==country_name]
				nation = nation.loc[nation['gender']=='m']
				sex.append('m')
				name.append("Male"+country_name)
				#print(nation)
			else:
				country_name = startlist[a]
				country_name = country_name.split("f")
				country_name = country_name[1]
				if(country_name.endswith(" I") or country_name.endswith(" II")):
					pass
				else:
					country_name = country_name + " I"
				nation= API_df.loc[API_df['name']==country_name]
				nation = nation.loc[nation['gender']=='f']
				sex.append('f')
				name.append("Female" + country_name)
			try:
				ski_id.append(nation['athlete_id'].iloc[0])
				price.append(nation['price'].iloc[0])
				#sex.append(nation['gender'].iloc[0])
			except:
				print(country_name)
				ski_id.append(999999)
				price.append(23096)





		else:

			athlete = API_df.loc[API_df['athlete_id']==startlist[a]]
			
			first_name = []
			last_name = []
			try:
				test_name = (athlete['name'].iloc[0])
			except:
				test_name = "NAME Generic" 
			test_name = test_name.split(" ")
			for word in test_name:
				if word.isupper():
					last_name.append(word)
				else:
					first_name.append(word)
			first_name = ' '.join(first_name)
			last_name = ' '.join(last_name)
			test_name = first_name + " " + last_name


			name.append(test_name)
			try:
				ski_id.append(athlete['athlete_id'].iloc[0])
				price.append(athlete['price'].iloc[0])
				sex.append(athlete['gender'].iloc[0])
			except:
				ski_id.append(999999)
				price.append(999999)
				sex.append('mf')
				#pass
				print(test_name)
		
	d = {'name':name, 'id':ski_id, 'price':price, 'sex':sex}
	fantasy_df = pd.DataFrame(data=d)
	return fantasy_df

def elo_team_sprint(fantasydf):
	wc = [100, 80, 60, 50, 45, 40, 36, 32, 29, 26, 24, 22, 20, 18, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
	wc = [i*2 for i in wc]
	skier_elo = []
	team_elos = []
	
	df = pd.read_pickle("~/ski/elo/python/ski/men/varmen_sprint.pkl")
	ladiesdf = pd.read_pickle("~/ski/elo/python/ski/ladies/varladies_sprint.pkl")
	df = df.append(ladiesdf, ignore_index = True)
	df['name'] = df['name'].str.replace('ø', 'oe')
	df['name'] = df['name'].str.replace('ä', 'ae')
	df['name'] = df['name'].str.replace('æ', 'ae')
	df['name']= df['name'].str.replace('ö', 'oe')
	df['name']= df['name'].str.replace('ü', 'ue')
	df['name']= df['name'].str.replace('å', 'aa')
	df['name'] = df['name'].str.replace('Aleksandr Terentev', 'alexander terentev')
	df['name'] = df['name'].str.replace('Irineu Esteve Altimiras', 'ireneu esteve altimiras')
	df['name'] = df['name'].str.replace('Thomas Hjalmar Westgaard', 'thomas maloney westgaard')
	df['name'] = df['name'].str.replace('Aleksandr Terentev', 'alexander terentev')
	df['name'] = df['name'].str.replace('Lauri Lepistoe', 'lauri lepisto')
	df['name'] = df['name'].str.replace('Philip Bellingham', 'phillip bellingham')
	df['name'] = df['name'].str.replace('Snorri Einarsson', 'snorri eythor einarsson')
	df['name'] = df['name'].str.replace('Krista Paermaekoski', 'krista parmakoski')
	df['name'] = df['name'].str.replace('Jessica Diggins', 'jessie diggins')
	df['name'] = df['name'].str.replace('Patricijia Eiduka', 'patricija eiduka')
	df['name'] = df['name'].str.replace('Katri Lylynperae', 'katri lylynpera')
	df['name'] = df['name'].str.replace('Julia Belger', 'julia preussger')
	df['name'] = df['name'].str.replace('Perttu Hyvaerinen', 'perttu hyvarinen')
	df['name'] = df['name'].str.replace('Kathrine Stewart-Jones', 'katherine stewart-jones')
	df['name'] = df['name'].str.replace('Ailja Iksanova', 'alija iksanova')

	print(fantasydf)
	teamsdf = fantasydf.iloc[::3, :]
	fantasydf = fantasydf[fantasydf.index % 3 !=0]

	#print(fantasydf)

	fantasy_names = fantasydf['name']
	fantasy_names = fantasy_names.str.lower()
	fantasy_names  = fantasy_names.tolist()
	count = 0
	team_elo = 0
	for a in range(len(fantasy_names)):

		skier = df.loc[df['name'].str.lower() == fantasy_names[a]]
		if(len(skier['name'])==0):
			print(fantasy_names[a])
		#print(skier)
		try:
			elo = skier['elo'].iloc[-1]
			team_elo+=elo
			#skier_elo.append(elo)
		#elo = (skier.loc[skier['date']==20210500]['elo'])
		except:
			print(fantasy_names[a])
			team_elo+=1300

		if(a%2==1):
			team_elos.append(team_elo)
			team_elo = 0
			#skier_elo.append(1300)
	print(team_elos)
	teamsdf['elo'] = team_elos
	fantasydf = teamsdf
	mendf = fantasydf.loc[fantasydf['sex']=='m']
	#Edit out these next three and the ladies three for pursuit.  One for actual
	
	mendf = mendf.sort_values(by='elo', ascending=False)
	print(len(mendf))
	#mendf = mendf[:len(mendf)]
	mendf['points'] = wc[:len(mendf)]
	ladiesdf = fantasydf.loc[fantasydf['sex']=='f']
	ladiesdf = ladiesdf.sort_values(by='elo', ascending=False)
	#ladiesdf = ladiesdf[:len(team_elos)]
	ladiesdf['points'] = wc[:len(ladiesdf)]
	mendf['place'] = np.arange(1, len(mendf['name'])+1, 1)
	ladiesdf['place'] = np.arange(1,len(ladiesdf['name'])+1,1)
	fantasydf = mendf
	fantasydf = fantasydf.append(ladiesdf)

	return fantasydf


def fis_relay():
	ids = []
	teams = []
	sex = []
	count = 0
	#start with the men
	startlist_list = ['https://www.fis-ski.com/DB/general/results.html?sectorcode=CC&raceid=36440',
'https://www.fis-ski.com/DB/general/results.html?sectorcode=CC&raceid=36439']
	for a in range(len(startlist_list)):
		startlist = BeautifulSoup(urlopen(startlist_list[a]), 'html.parser')
	#print(startlist)
		names = startlist.find_all('div', {'g-lg-14 g-md-14 g-sm-11 g-xs-10 justify-left bold'})
		body = startlist.find_all('div', {'g-lg-2 g-md-2 g-sm-3 hidden-xs justify-right gray pr-1'})
		print(startlist_list[a])

		for b in range(len(body)):
			#print(body[a].text.strip())
			if(b%5!=0):
				ids.append(int(body[b].text.strip()))
			else:
				team = names[b].text.strip()
				if(a==0):
					team = "m"+team
				else:
					team = "f"+team
				ids.append(team)
			#if(count==0):
			#	sex.append('M')
			#else:
			#	sex.append('L')
		
		

		#print(team)
		count+=1

	print(ids)

	

	#now for the ladies
	
	return ids

def fantasy_relay(startlist):
	name = []
	team_name = []
	team_id = []
	team_price = []
	team_sex = []
	ski_id = []
	price =[]
	sex = []
	#sex = startlist['sex']
	#startlist = startlist['id']
	#print(sex)
	#print(startlist)
	fantasy = 'https://www.fantasyxc.se/api/athletes'
	#soup = BeautifulSoup(urlopen(fantasy), 'html5lib')
	#print(soup)
	with requests.Session() as s:
		r=s.get(fantasy)
		soup = BeautifulSoup(r.content, 'html5lib')
	API_json = json.loads(soup.get_text())
	API_df = pd.DataFrame.from_dict(pd.json_normalize(API_json), orient='columns')

	##Change to locate for increased speed
	for a in range(len(startlist)):
		if(a%5==0):
			
			if(startlist[a].startswith("m")):
				#print(startlist[a])
				country_name = startlist[a]
				country_name = country_name.split("m")
				country_name = country_name[1]
				if(country_name.endswith(" I") or country_name.endswith(" II")):
					pass
				else:
					country_name = country_name + " I"

				nation= API_df.loc[API_df['name']==country_name]
				nation = nation.loc[nation['gender']=='m']
				sex.append('m')
				name.append("Male"+country_name)
				#print(nation)
			else:
				country_name = startlist[a]
				country_name = country_name.split("f")
				country_name = country_name[1]
				if(country_name.endswith(" I") or country_name.endswith(" II")):
					pass
				else:
					country_name = country_name + " I"
				nation= API_df.loc[API_df['name']==country_name]
				nation = nation.loc[nation['gender']=='f']
				sex.append('f')
				name.append("Female" + country_name)
			try:
				ski_id.append(nation['athlete_id'].iloc[0])
				price.append(nation['price'].iloc[0])
				#sex.append(nation['gender'].iloc[0])
			except:
				print(country_name)
				ski_id.append(999999)
				price.append(23096)





		else:

			athlete = API_df.loc[API_df['athlete_id']==startlist[a]]
			
			first_name = []
			last_name = []
			try:
				test_name = (athlete['name'].iloc[0])
			except:
				test_name = "NAME Generic" 
			test_name = test_name.split(" ")
			for word in test_name:
				if word.isupper():
					last_name.append(word)
				else:
					first_name.append(word)
			first_name = ' '.join(first_name)
			last_name = ' '.join(last_name)
			test_name = first_name + " " + last_name


			name.append(test_name)
			try:
				ski_id.append(athlete['athlete_id'].iloc[0])
				price.append(athlete['price'].iloc[0])
				sex.append(athlete['gender'].iloc[0])
			except:
				ski_id.append(999999)
				price.append(999999)
				sex.append('mf')
				#pass
				print(test_name)
		
	d = {'name':name, 'id':ski_id, 'price':price, 'sex':sex}
	fantasy_df = pd.DataFrame(data=d)
	return fantasy_df






def elo_relay(fantasydf):
	wc = [100, 80, 60, 50, 45, 40, 36, 32, 29, 26, 24, 22, 20, 18, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
	wc = [i*2 for i in wc]
	skier_elo = []
	team_elos = []
	
	df = pd.read_pickle("~/ski/elo/python/ski/men/varmen_distance.pkl")
	ladiesdf = pd.read_pickle("~/ski/elo/python/ski/ladies/varladies_distance.pkl")
	df = df.append(ladiesdf, ignore_index = True)
	df['name'] = df['name'].str.replace('ø', 'oe')
	df['name'] = df['name'].str.replace('ä', 'ae')
	df['name'] = df['name'].str.replace('æ', 'ae')
	df['name']= df['name'].str.replace('ö', 'oe')
	df['name']= df['name'].str.replace('ü', 'ue')
	df['name']= df['name'].str.replace('å', 'aa')
	df['name'] = df['name'].str.replace('Aleksandr Terentev', 'alexander terentev')
	df['name'] = df['name'].str.replace('Irineu Esteve Altimiras', 'ireneu esteve altimiras')
	df['name'] = df['name'].str.replace('Thomas Hjalmar Westgaard', 'thomas maloney westgaard')
	df['name'] = df['name'].str.replace('Aleksandr Terentev', 'alexander terentev')
	df['name'] = df['name'].str.replace('Lauri Lepistoe', 'lauri lepisto')
	df['name'] = df['name'].str.replace('Philip Bellingham', 'phillip bellingham')
	df['name'] = df['name'].str.replace('Snorri Einarsson', 'snorri eythor einarsson')
	df['name'] = df['name'].str.replace('Krista Paermaekoski', 'krista parmakoski')
	df['name'] = df['name'].str.replace('Jessica Diggins', 'jessie diggins')
	df['name'] = df['name'].str.replace('Patricijia Eiduka', 'patricija eiduka')
	df['name'] = df['name'].str.replace('Katri Lylynperae', 'katri lylynpera')
	df['name'] = df['name'].str.replace('Julia Belger', 'julia preussger')
	df['name'] = df['name'].str.replace('Perttu Hyvaerinen', 'perttu hyvarinen')
	df['name'] = df['name'].str.replace('Kathrine Stewart-Jones', 'katherine stewart-jones')
	df['name'] = df['name'].str.replace('Ailja Iksanova', 'alija iksanova')

	teamsdf = fantasydf.iloc[::5, :]
	fantasydf = fantasydf[fantasydf.index % 5 !=0]

	#print(fantasydf)

	fantasy_names = fantasydf['name']
	fantasy_names = fantasy_names.str.lower()
	fantasy_names  = fantasy_names.tolist()
	count = 0
	team_elo = 0
	for a in range(len(fantasy_names)):

		skier = df.loc[df['name'].str.lower() == fantasy_names[a]]
		if(len(skier['name'])==0):
			print(fantasy_names[a])
		#print(skier)
		try:
			elo = skier['elo'].iloc[-1]
			team_elo+=elo
			#skier_elo.append(elo)
		#elo = (skier.loc[skier['date']==20210500]['elo'])
		except:
			print(fantasy_names[a])
			team_elo+=1300

		if(a%4==3):
			team_elos.append(team_elo)
			team_elo = 0
			#skier_elo.append(1300)
	print(team_elos)
	teamsdf['elo'] = team_elos
	fantasydf = teamsdf
	mendf = fantasydf.loc[fantasydf['sex']=='m']
	#Edit out these next three and the ladies three for pursuit.  One for actual
	
	#mendf = mendf.sort_values(by='elo', ascending=False)
	print(len(mendf))
	#mendf = mendf[:len(mendf)]
	mendf['points'] = wc[:len(mendf)]
	ladiesdf = fantasydf.loc[fantasydf['sex']=='f']
	#ladiesdf = ladiesdf.sort_values(by='elo', ascending=False)
	#ladiesdf = ladiesdf[:len(team_elos)]
	ladiesdf['points'] = wc[:len(ladiesdf)]
	mendf['place'] = np.arange(1, len(mendf['name'])+1, 1)
	ladiesdf['place'] = np.arange(1,len(ladiesdf['name'])+1,1)
	fantasydf = mendf
	fantasydf = fantasydf.append(ladiesdf)

	return fantasydf

	


def fis():
	ids = []
	sex = []
	count = 0
	#start with the men
	startlist_list = ['https://www.fis-ski.com/DB/general/results.html?sectorcode=CC&raceid=36442',
'https://www.fis-ski.com/DB/general/results.html?sectorcode=CC&raceid=36441']
	for a in startlist_list:
		startlist = BeautifulSoup(urlopen(a), 'html.parser')
	#print(startlist)
		body = startlist.find_all('div', {'class':'pr-1 g-lg-2 g-md-2 g-sm-2 hidden-xs justify-right gray'})
		print(a)

		for b in range(len(body)):
			#print(body[a].text.strip())
			ids.append(int(body[b].text.strip()))
			#if(count==0):
			#	sex.append('M')
			#else:
			#	sex.append('L')
		count+=1

	#now for the ladies
	
	return ids

def fantasy(startlist):
	name = []
	ski_id = []
	price =[]
	sex = []
	#sex = startlist['sex']
	#startlist = startlist['id']
	#print(sex)
	#print(startlist)
	fantasy = 'https://www.fantasyxc.se/api/athletes'
	#soup = BeautifulSoup(urlopen(fantasy), 'html5lib')
	#print(soup)
	with requests.Session() as s:
		r=s.get(fantasy)
		soup = BeautifulSoup(r.content, 'html5lib')
	API_json = json.loads(soup.get_text())
	API_df = pd.DataFrame.from_dict(pd.json_normalize(API_json), orient='columns')

	##Change to locate for increased speed
	for a in range(len(startlist)):
		athlete = API_df.loc[API_df['athlete_id']==startlist[a]]
		
		first_name = []
		last_name = []
		try:
			test_name = (athlete['name'].iloc[0])
		except:
			print(startlist[a])
			continue
		test_name = test_name.split(" ")
		for word in test_name:
			if word.isupper():
				last_name.append(word)
			else:
				first_name.append(word)
		first_name = ' '.join(first_name)
		last_name = ' '.join(last_name)
		test_name = first_name + " " + last_name


		name.append(test_name)
		try:
			ski_id.append(athlete['athlete_id'].iloc[0])
			price.append(athlete['price'].iloc[0])
			sex.append(athlete['gender'].iloc[0])
		except:
			print(test_name)
		
	d = {'name':name, 'id':ski_id, 'price':price, 'sex':sex}
	fantasy_df = pd.DataFrame(data=d)
	return fantasy_df

def pursuit(fantasydf):
	stage = [50, 46, 43, 40, 37, 34, 32, 30, 28, 26, 24, 22, 20, 18, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
	wc = [100, 80, 60, 50, 45, 40, 36, 32, 29, 26, 24, 22, 20, 18, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
	tour = [400, 320, 240, 200, 180, 160, 144, 128, 116, 104, 96, 88, 80, 72, 64, 60, 56, 52, 48, 44, 40, 36, 32, 28, 24, 20,20, 20, 20, 20]

	mendf = fantasydf.loc[fantasydf['sex']=='m']
	mendf = mendf.sort_values(by='elo', ascending=False)
	mendf['pursuit'] = np.arange(1, len(mendf['name'])+1, 1)
	mendf['pursuit'] = .3*mendf['pursuit'] + .7*mendf['place']
	mendf = mendf.sort_values(by='pursuit', ascending=True)
	mendf['pursuit'] = np.arange(1, len(mendf['name'])+1, 1)
	mendf = mendf[:30]
	mendf['points'] = tour

	ladiesdf = fantasydf.loc[fantasydf['sex']=='f']
	ladiesdf = ladiesdf.sort_values(by='elo', ascending=False)
	ladiesdf['pursuit'] = np.arange(1,len(ladiesdf['name'])+1,1)
	ladiesdf['pursuit'] = .3*ladiesdf['pursuit'] + .7*ladiesdf['place']
	ladiesdf = ladiesdf.sort_values(by='pursuit', ascending=True)
	ladiesdf['pursuit'] = np.arange(1,len(ladiesdf['name'])+1,1)
	ladiesdf = ladiesdf[:30]
	ladiesdf['points'] = tour

	fantasydf = mendf
	fantasydf = fantasydf.append(ladiesdf)
	return fantasydf


def elo(fantasydf):
	stage = [50, 46, 43, 40, 37, 34, 32, 30, 28, 26, 24, 22, 20, 18, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
	wc = [100, 80, 60, 50, 45, 40, 36, 32, 29, 26, 24, 22, 20, 18, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
	tour = [400, 320, 240, 200, 180, 160, 144, 128, 116, 104, 96, 88, 80, 72, 64, 60, 56, 52, 48, 44, 40, 36, 32, 28, 24, 20,20, 20, 20, 20]
	mendfs = []
	ladiesdfs = []
	fantasydf.loc[:,'points'] =0
	menpkls = ["~/ski/elo/python/ski/men/varmen_sprint_classic.pkl"]
	#"~/ski/elo/python/ski/men/varmen_15_classic.pkl",
	#"~/ski/elo/python/ski/men/varmen_sprint_classic.pkl"]

	ladiespkls = ["~/ski/elo/python/ski/ladies/varladies_sprint_classic.pkl"]
	#"~/ski/elo/python/ski/ladies/varladies_10_classic.pkl",
	#"~/ski/elo/python/ski/ladies/varladies_sprint_classic.pkl"]

	for a in range(len(menpkls)):
		skier_elo = []
		df = pd.read_pickle(menpkls[a])
		ladiespkl = pd.read_pickle(ladiespkls[a])
		df = df.append(ladiespkl, ignore_index = True)
		df['name'] = df['name'].str.replace('ø', 'oe')
		df['name'] = df['name'].str.replace('Ø', 'oe')
		df['name'] = df['name'].str.replace('ä', 'ae')
		df['name'] = df['name'].str.replace('æ', 'ae')
		df['name']= df['name'].str.replace('ö', 'oe')
		df['name']= df['name'].str.replace('ü', 'ue')
		df['name']= df['name'].str.replace('å', 'aa')
		df['name'] = df['name'].str.replace('Aleksandr Terentev', 'alexander terentev')
		df['name'] = df['name'].str.replace('Irineu Esteve Altimiras', 'ireneu esteve altimiras')
		df['name'] = df['name'].str.replace('Thomas Hjalmar Westgaard', 'thomas maloney westgaard')
		df['name'] = df['name'].str.replace('Aleksandr Terentev', 'alexander terentev')
		df['name'] = df['name'].str.replace('Lauri Lepistoe', 'lauri lepisto')
		df['name'] = df['name'].str.replace('Philip Bellingham', 'phillip bellingham')
		df['name'] = df['name'].str.replace('Snorri Einarsson', 'snorri eythor einarsson')
		df['name'] = df['name'].str.replace('Krista Paermaekoski', 'krista parmakoski')
		df['name'] = df['name'].str.replace('Jessica Diggins', 'jessie diggins')
		df['name'] = df['name'].str.replace('Patricijia Eiduka', 'patricija eiduka')
		df['name'] = df['name'].str.replace('Katri Lylynperae', 'katri lylynpera')
		df['name'] = df['name'].str.replace('Julia Belger', 'julia preussger')
		df['name'] = df['name'].str.replace('Perttu Hyvaerinen', 'perttu hyvarinen')
		df['name'] = df['name'].str.replace('Kathrine Stewart-Jones', 'katherine stewart-jones')
		df['name'] = df['name'].str.replace('Ailja Iksanova', 'alija iksanova')
		#df['name'] = df['name'].str.replace('H', 'ailja iksanova')



		fantasy_names = fantasydf['name']
		fantasy_names = fantasy_names.str.lower()
		fantasy_names  = fantasy_names.tolist()
		#print(fantasy_names)
		for a in range(len(fantasy_names)):
			skier = df.loc[df['name'].str.lower() == fantasy_names[a]]
			if(len(skier['name'])==0):
				print(fantasy_names[a])
			#print(skier)
			try:
				elo = skier['elo'].iloc[-1]
				skier_elo.append(elo)
			#elo = (skier.loc[skier['date']==20210500]['elo'])
			except:
				print(fantasy_names[a])
				skier_elo.append(1300)
			
		fantasydf['elo'] = skier_elo
		mendf = fantasydf.loc[fantasydf['sex']=='m']
		#Edit out these next three and the ladies three for pursuit.  One for actual
		
		mendf = mendf.sort_values(by='elo', ascending=False)
		mendf = mendf.reset_index(drop=True)
		
		#mendf = mendf[:30]
		men_wc_scores = mendf['points'].tolist()
		men_wc_scores = men_wc_scores[:30]
		
		men_wc_scores = np.add(men_wc_scores, wc)
		
		men_wc_scores = pd.Series(men_wc_scores)
		
		mendf.loc[:30, 'points'] = men_wc_scores
		mendfs.append(mendf)
		
		ladiesdf = fantasydf.loc[fantasydf['sex']=='f']
		ladiesdf = ladiesdf.sort_values(by='elo', ascending=False)
		ladiesdf = ladiesdf.reset_index(drop=True)

		ladies_wc_scores = ladiesdf['points'].tolist()
		ladies_wc_scores = ladies_wc_scores[:30]
		ladies_wc_scores = np.add(ladies_wc_scores, wc)
		ladies_wc_scores = pd.Series(ladies_wc_scores)
		ladiesdf.loc[:30, 'points'] = ladies_wc_scores
		ladiesdfs.append(ladiesdf)

	mendf = fantasydf.loc[fantasydf['sex']=='m']
	mendf = mendf.sort_values(by='id')
	mendf = mendf.reset_index(drop=True)
	ladiesdf = fantasydf.loc[fantasydf['sex']=='f']
	ladiesdf = ladiesdf.sort_values(by='id')
	ladiesdf = ladiesdf.reset_index(drop=True)
	

	for a in range(len(mendfs)):
		mendfs[a] = mendfs[a].sort_values(by='id')
		mendfs[a] = mendfs[a].reset_index(drop=True)
		elo_name = "elo"+str(a+1)
		race_name = "race"+str(a+1)
		mendf[elo_name] = mendfs[a]['elo']
		mendf[race_name] = mendfs[a]['points']
		mendf['points'] = mendf['points'] + mendf[race_name]
		ladiesdfs[a] = ladiesdfs[a].sort_values(by='id')
		ladiesdfs[a] = ladiesdfs[a].reset_index(drop=True)
		ladiesdf[elo_name] = ladiesdfs[a]['elo']
		ladiesdf[race_name] = ladiesdfs[a]['points']
		ladiesdf['points'] = ladiesdf['points'] + ladiesdf[race_name]







	
	#ladiesdf = ladiesdf[:30]
	#ladiesdf[:30, 'points'] += wc
	mendf=mendf.sort_values(by='points', ascending=False)
	ladiesdf =ladiesdf.sort_values(by='points', ascending=False)
	mendf = mendf[mendf['points']>0]
	ladiesdf = ladiesdf[ladiesdf['points']>0]
	mendf['place'] = np.arange(1, len(mendf['name'])+1, 1)
	ladiesdf['place'] = np.arange(1,len(ladiesdf['name'])+1,1)
	fantasydf = mendf
	fantasydf = fantasydf.append(ladiesdf)

	return fantasydf
			




	#WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH,
	#	"//div[@class='js-off-canvas-overlay is-overlay-fixed']")))

#startlist = fis()
#startlist = fis_relay()
startlist = fis_team_sprint()

#fantasydf = (fantasy(startlist))
#fantasydf = fantasy_relay(startlist)
fantasydf = fantasy_team_sprint(startlist)
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
 #   print(fantasydf)
#print(fantasydf)
#print(fantasydf)

#fantasydf = elo(fantasydf)
#fantasydf = pursuit(fantasydf)
#fantasydf = elo_relay(fantasydf)
fantasydf = elo_team_sprint(fantasydf)
#print(fantasydf)

fantasydf.to_pickle("~/ski/elo/knapsack/fantasydf_team_sprint.pkl")
fantasydf.to_excel("~/ski/elo/knapsack/fantasydf_team_sprint.xlsx")
print(time.time() - start_time)

