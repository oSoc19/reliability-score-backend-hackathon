import json
import statistics



with open('data.json', 'r') as f:
	json_dict = json.load(f)


delay_station = {}
for row in json_dict:
	try:
		delay = row['fields']['delay_dep']
	except KeyError:
		delay = 0
	station = row['fields']['ptcar_lg_nm_nl']
	if station not in delay_station:
		delay_station[station] = []
	delay_station[station].append(delay)


medians = {}
for station in delay_station:
	delays = delay_station[station]
	median = statistics.median(delays)
	medians[station.lower()] = median


medians_json = json.dumps(medians)
with open('median_delays.json', 'w') as f:
	f.write(medians_json)