import urllib.request, json

sayfa = "https://data.ijf.org/api/get_json?access_token=&params[action]=competition.contests&params[__ust]=&params[id_competition]={0}&params[id_weight]={1}&params[empty]=true"
competition = 0

while competition < 1575:
	competition += 1
	flag = 0
	print(100*"*")
	while flag < 14:
		flag += 1
		vericek= sayfa.format(competition, flag)
		print(vericek)
		with urllib.request.urlopen(vericek) as url:
			data = json.loads(url.read().decode())
			veri = json.dumps(data, indent=2)
			
			for contest in data['contests']:
				print(contest['fight_no'], contest['id_fight'], contest['round_name'], contest['person_white'], contest['person_blue'], contest['ippon_b'], contest['waza_b'], contest['yuko_b'], contest['penalty_b'], contest['ippon_w'], contest['waza_w'], contest['yuko_w'], contest['penalty_w'])
