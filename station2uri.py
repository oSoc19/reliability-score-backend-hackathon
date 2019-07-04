import json


def toURI(station):
	uri = station_uris_dict[station]
	return uri


with open('station_uris.json', 'r') as f:
	station_uris_dict = json.load(f)

with open('median_delays.json', 'r') as f:
	median_dict = json.load(f)


median_delays_uri = {}
for station in median_dict:
	try:
		uri = toURI(station)
	except:
		uri = 'NO-URI'
	median_delays_uri[uri] = median_dict[station]


with open('median_delays_uri.json', 'w') as f:
	f.write(json.dumps(median_delays_uri))