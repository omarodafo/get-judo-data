import socket
import urllib.request, json
import pandas as pd

# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)

sayfa = "https://data.ijf.org/api/get_json?access_token=&params[action]=competition.contests&params[__ust]=&params[id_competition]={0}&params[id_weight]={1}&params[empty]=true"
competition = 999

while competition < 1575:
	competition += 1
	flag = 0
	print(100*"*", "\n")
	while flag < 14:
		flag += 1
		vericek= sayfa.format(competition, flag)
		print(vericek)
		with urllib.request.urlopen(vericek) as url:
			data = json.loads(url.read().decode())
			veri = data['contests']
			
		my_df = pd.DataFrame(veri)
		my_df.to_csv('data.csv', mode='a', index=False, header=False)