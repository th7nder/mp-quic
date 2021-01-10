import csv
import numpy as np


FIBER = "Światłowód"
LTE = "LTE"


class Result:
	def __init__(self, paths, streams):
		self.paths = paths
		self.streams = streams

class Path:
	def __init__(self, t, ifs, srtt, throughput):
		self.time = t - t[0]
		self.ifs = ifs
		self.srtt = srtt
		self.throughput = throughput

class Stream:
	def __init__(self, t, delays):
		self.t = t
		self.delays = delays 

def parse_streams(filename):
	rows = []
	with open(filename + '/delays.csv') as f:
		c = csv.reader(f)
		for row in c:
			rows.append(row)

	streams = set()
	for row in rows:
		stream = row[0]
		# skip crypto stream
		if stream == "1":
			continue 
		streams.add(stream)


	streams_data = {}
	for stream in sorted(streams):
		pds = []
		for row in rows:
			s = row[0]
			if stream != s:
				continue

			pn = int(row[1])
			sentTime = int(row[2]) / 1000 / 1000 / 1000
			delay = int(row[3])
			if delay != -1:
				# nanoseconds
				delay /= 1000 * 1000
			pds.append((sentTime, delay, pn))
		pds.sort(key=lambda k: k[0])
		times = list(map(lambda x: x[0], pds))
		delays = list(map(lambda x: x[1], pds))
		streams_data[stream] = Stream(np.array(times), np.array(delays))
	
	return streams

def parse_results(filename):
	rows = []
	with open(filename + '/main.csv') as f:
		c = csv.reader(f)
		for row in c:
			rows.append(row)

	paths = set()
	for row in rows:
		path = row[1]
		paths.add(path)

	path_data = {}
	for p in paths:
		t = []
		inFlights = []
		srtts = []
		thr = []
		for row in rows:
			path = row[1]
			if path != p:
				continue
			time = row[0]
			inFlight = row[4]
			srtt = row[5]
			t.append(int(time) / 1000 / 1000 / 1000)
			inFlights.append(int(inFlight) / 1000)
			srtts.append(int(srtt) / 1000)
			if int(srtt) == 0:
				throughput = 0
			else: 
				throughput = (int(inFlight) * 8) / (int(srtt) / 1000 / 1000)
			thr.append(throughput / 1000 / 1000)

			if row[3][0] == "8":
				l = FIBER
			else:
				l = LTE

		if sum(inFlights) < 1000:
			continue

		# print(paths)
		# print(rows[0][3])
		# if rows[0][3][0] == "8":
		# 	l = FIBER
		# else:
		# 	l = LTE
		# if p == "3":
		# 	l = FIBER
		# elif p == "0" and rows[0][3][0] == "8":
		# 	l = FIBER
		# else:
		# 	l = LTE

		path_data[l] = Path(np.array(t), np.array(inFlights), np.array(srtts), np.array(thr))

	streams_data = parse_streams(filename)
	return Result(path_data, streams_data)