import numpy as np
import matplotlib.pyplot as plt
import csv

def clamp_time(time):
	s = time[0]
	for i in range(len(time)):
		time[i] -= s
	

def plot(filename, savefile, title):
	t = []
	inFlights = []
	srtts = []
	with open(filename) as f:
		c = csv.reader(f)
		for row in c:
			time = row[0]
			inFlight = row[4]
			srtt = row[5]
			t.append(int(time) / 1000 / 1000 / 1000 )
			inFlights.append(int(inFlight) / 1024)
			srtts.append(int(srtt) / 1000)

	clamp_time(t)
	fig, ((ax1), (ax2)) = plt.subplots(2, 1, figsize=((20, 12)))
	ax1.plot(t, inFlights)
	ax1.set_title('in-flight vs. time')
	ax1.set_xlabel('time [s]')
	ax1.set_ylabel('in-flight [kB]')

	ax2.plot(t, srtts)
	ax2.set_title('SRTT vs. time')
	ax2.set_xlabel('time [s]')
	ax2.set_ylabel('SRTT [ms]')
	fig.suptitle(title)
	plt.savefig(savefile)

def plot_mp(filename, savefile, title):
	rows = []
	with open(filename) as f:
		c = csv.reader(f)
		for row in c:
			rows.append(row)

	paths = set()
	for row in rows:
		path = row[1]
		paths.add(path)

	fig, ((ax1), (ax2)) = plt.subplots(2, 1, figsize=((20, 12)))
	fig.suptitle(title)
	ax1.set_title('in-flight vs. time')
	ax1.set_xlabel('time [s]')
	ax1.set_ylabel('in-flight [kB]')
	ax2.set_title('SRTT vs. time')
	ax2.set_xlabel('time [s]')
	ax2.set_ylabel('SRTT [ms]')

	for p in paths:
		t = []
		inFlights = []
		srtts = []
		for row in rows:
			path = row[1]
			if path != p:
				continue
			time = row[0]
			inFlight = row[4]
			srtt = row[5]
			ip = row[3]
			t.append(int(time) / 1000 / 1000 / 1000)
			inFlights.append(int(inFlight) / 1024)
			srtts.append(int(srtt) / 1000)
	
		if sum(inFlights) < 10:
			continue
		if ip[0] == "8":
			l = "Fiber over WiFi 5Ghz 170/60Mbps"
		else:
			l = "LTE over Ethernet 60/30Mbps"
		clamp_time(t)
		ax1.plot(t, inFlights, label=l)
		ax2.plot(t, srtts, label=l)

	ax1.legend()
	ax2.legend()
	plt.savefig(savefile)


plot('../results/fiber.csv', 'quic_fiber.png', 'QUIC | Fiber over Wi-Fi 5GHz, 170/60Mbps, 100MB upload, 1 stream, unthrottled')
plot('../results/lte.csv', 'quic_lte.png', 'QUIC | LTE over Ethernet, 60/30Mbps, 100MB upload, 1 stream, unthrottled')

plot_mp('../results/multipath.csv', 'mpquic.png', 'MPQUIC | 100 MB upload, 1 stream, unthrottled')
