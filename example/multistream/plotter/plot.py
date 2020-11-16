import numpy as np
import matplotlib.pyplot as plt
import csv

def clamp_time(time):
	s = time[0]
	for i in range(len(time)):
		time[i] -= s

def plot_inflights(ax4, filename, paths):
	ax4.set_title('in-flight vs. time')
	ax4.set_xlabel('time [s]')
	ax4.set_ylabel('in-flight [kB]')

	rows = []
	streams = set()
	with open(filename + '/str_aggr.csv') as f:
		c = csv.reader(f)
		for row in c:
			rows.append(row)
			streams.add(row[1])

	for s in streams:
		t = []
		inFlights = []
		for row in rows:
			stream = row[1]
			if stream != s:
				continue
			time = row[0]
			inFlight = int(row[2]) / 1000 
			t.append(int(time) / 1000 / 1000 / 1000)
			inFlights.append(inFlight)
		clamp_time(t)
		ax4.plot(t, inFlights, label=f"Stream {s} | Aggregated ")

	rows = []
	with open(filename + '/str_per_int.csv') as f: 
		c = csv.reader(f)
		for row in c:
			rows.append(row)

	
	for p in paths:
		for s in streams:
			t = []
			inFlights = []
			for row in rows:
				stream = row[1]
				path = row[2]
				if path != p or stream != s:
					continue
				time = row[0]
				inFlight = int(row[3]) / 1000 
				t.append(int(time) / 1000 / 1000 / 1000)
				inFlights.append(inFlight)
			clamp_time(t)
			print(f"Haha: {len(t)}")
			ax4.plot(t, inFlights, label=f"Stream {s} | Path {p}")

	ax4.legend()

def plot_mp(filename, savefile, title):
	rows = []
	with open(filename + '/main.csv') as f:
		c = csv.reader(f)
		for row in c:
			rows.append(row)

	paths = set()
	for row in rows:
		path = row[1]
		if path == "0":
			continue
		paths.add(path)

	fig, ((ax1), (ax2), (ax3), (ax4)) = plt.subplots(4, 1, figsize=((40, 25)))
	fig.suptitle(title)
	plot_inflights(ax4, filename, paths)
	ax1.set_title('in-flight vs. time')
	ax1.set_xlabel('time [s]')
	ax1.set_ylabel('in-flight [kB]')
	ax2.set_title('SRTT vs. time')
	ax2.set_xlabel('time [s]')
	ax2.set_ylabel('SRTT [ms]')

	ax3.set_title('Throughput vs. time')
	ax3.set_xlabel('time [s]')
	ax3.set_ylabel('Throughput [Mbps]')

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

		if sum(inFlights) < 1000:
			continue

		if p == "3":
			l = "Fiber over WiFi 5Ghz 170/60Mbps"
		else:
			l = "LTE over Ethernet 60/30Mbps"
		print(sum(thr) / len(thr))
		clamp_time(t)
		ax1.plot(t, inFlights, label=l)
		ax2.plot(t, srtts, label=l)
		ax3.plot(t, thr, label=l)

	ax1.legend()
	ax2.legend()
	ax3.legend()
	plt.savefig(savefile)


# plot_mp('../results/mq_u_1', 'mq_u_1.png', 'MPQUIC | 400 MB upload, 1 stream, UNTHROTTLED (.78)')
plot_mp('../results/mq_u_2', 'mq_u_2.png', 'MPQUIC | 400 MB upload, 1 stream, UNTHROTTLED (.78)')



