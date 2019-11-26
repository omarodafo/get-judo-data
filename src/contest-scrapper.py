import socket
import urllib.request, json
import pandas as pd
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
			finished_competition.append(competition['id_competition'])
		
	return finished_competition



# For adding date and time to filename 
get_datetime = datetime.now()
get_datetime = (get_datetime.strftime('%d-%m-%Y__%H-%M'))

data_url = "https://data.ijf.org/api/get_json?access_token=&params[action]=competition.contests&params[__ust]=&params[id_competition]={0}&params[id_weight]={1}&params[empty]=true"
with alive_bar(len(get_latest_events())) as bar:
	for competition_id in get_latest_events():
		competition = competition_id
		weight_id = 0

		while weight_id < 14:
			weight_id += 1
			target_url = data_url.format(competition, weight_id)
			with urllib.request.urlopen(target_url) as url:
				data = json.loads(url.read().decode())
				data_pd = data['contests']
				
			dataframe = pd.DataFrame(data_pd)
			dataframe.to_csv('contests-data-{}.csv'.format(get_datetime), mode='a', index=False, header=False)
		bar()