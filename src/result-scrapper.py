import socket
import urllib.request, json
import pandas as pd
from pandas.io.json import json_normalize    
from alive_progress import alive_bar
from datetime import datetime

# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)


def get_latest_events():
	events_url = "https://data.ijf.org/api/get_json?access_token=&params[action]=competition.get_list&params[__ust]=&params[year]=&params[month]=&params[rank_group]=&params[sort]=-1"

	with urllib.request.urlopen(events_url) as url:
		data = json.loads(url.read().decode())

	finished_competition = []
	for competition in data:
		has_result = (competition['has_results'])
		if (has_result != "0"):
			finished_competition.append(int(competition['id_competition']))
		
	finished_competition.sort(reverse=True)
	return finished_competition


data_url = "https://data.ijf.org/api/get_json?access_token=&params[action]=competition.results&params[__ust]=&params[id_competition]={0}"

with alive_bar(len(get_latest_events())) as bar:
	
	for competition_id in get_latest_events():
		target_url = data_url.format(competition_id)
		
		with urllib.request.urlopen(target_url) as url:
			data = json.loads(url.read().decode())
			get_gender = data['by_categories'].keys()

			for i in get_gender:
				int(i)

				if str(i) == '1':
					male_weight = json_normalize(data['by_categories'], record_path=['1']).values

					for j in male_weight:
						j = int(j)
						normalize_data = json_normalize(data['by_categories'], record_path=['1',str(j),'persons'])
						dataframe = pd.DataFrame(normalize_data)
						dataframe.to_csv('result-data.csv', mode='a', index=False, header=False)
				else:
					female_weight = json_normalize(data['by_categories'], record_path=['2']).values
					
					for j in female_weight:
						j = int(j)
						normalize_data = json_normalize(data['by_categories'], record_path=['2',str(j),'persons'])
						dataframe = pd.DataFrame(normalize_data)
						dataframe.to_csv('result-data.csv', mode='a', index=False, header=False)
		bar()