import socket
import urllib.request, json
import pandas as pd

# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)

sayfa = "https://data.ijf.org/api/get_json?access_token=&params[action]=competition.results&params[__ust]=&params[id_competition]={0}"
competition = 1575

while competition > 999:
	competition -= 1
	print(100*"*", "\n")

	vericek= sayfa.format(competition)
	print(vericek)
	
	with urllib.request.urlopen(vericek) as url:
		data = json.loads(url.read().decode())
		veri = data['totals']
			
		my_df = pd.DataFrame(veri)
		my_df.to_csv('result-data.csv', mode='a', index=False, header=False)