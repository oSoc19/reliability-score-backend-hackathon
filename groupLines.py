import json
import csv
import re


def filter(station):
	station = station.lower()							# Covert to lowercase
	station = re.sub(r'\d', '', station)				# Remove numbers
	station = re.sub(r'\/.*', '', station)
	station = station.rstrip()							# Strip whitespaces from start/ending
	station = station.replace('\'', '\\\'')
	return station



with open('data.json', 'r') as f:
	json_dict = json.load(f)

stations_json = []
for row in json_dict:
	station = filter(row['fields']['ptcar_lg_nm_nl'])
	if station not in stations_json:
		stations_json.append(station)


with open('stations.csv', 'r', newline='') as f:
	reader = csv.reader(f, delimiter=',')
	stations_csv = []
	csv_uris = {}
	for row in reader:
		station = filter(row[1])
		uri = row[0]
		if station not in stations_csv:
			stations_csv.append(station)
			csv_uris[station] = uri


uris = {}
for station in stations_json:
	if filter(station) in csv_uris.keys():
		uris[station] = csv_uris[filter(station)]
	else:
		uris[station] = 'NO URI FOUND'




matches = 0
doesntmatch = []
for station in stations_json:
	if station in stations_csv:
		matches += 1
	else:
		doesntmatch.append(station)
print(f'{matches}/{len(stations_json)}')


print(doesntmatch)
print(len(doesntmatch))


with open('station_uris_2.json', 'w') as f:
	f.write(str(uris))