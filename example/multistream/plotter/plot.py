import numpy as np
import matplotlib.pyplot as plt
import csv

def clamp_time(time):
	s = time[0]
	for i in range(len(time)):
		time[i] -= s

def plot_rtts(filename, paths, ax4):
	ax4.set_title('packet number vs. time to ack')
	ax4.set_xlabel('packet number')
	ax4.set_ylabel('time to ACK')

	rows = []
	with open(filename + '/rtt.csv') as f:
		c = csv.reader(f)
		for row in c:
			rows.append(row)

	for p in paths:
		packets = []
		delays = []
		for row in rows:
			path = row[0]
			if path != p:
				continue

			pn = int(row[1])
			delay = int(row[2]) / 1000
			packets.append(pn)
			delays.append(delay)

		if p == "3":
			l = "Fiber over WiFi 5Ghz 170/60Mbps"
		else:
			l = "LTE over Ethernet 60/30Mbps"

		ax4.plot(packets, delays, label=l)

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
	plot_rtts(filename, paths, ax4)
	# plot_inflights(ax4, filename, paths)
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
# plot_mp('../results/mq_u_2', 'mq_u_2.png', 'MPQUIC | 400 MB upload, 1 stream, UNTHROTTLED (.78); 14:55, 16.11.2020')

# plot_mp('../results/mq_t_1', 'mq_t_1.png', 'MPQUIC | 10 MB upload, 1 stream, throttled (.31); 14:26, 17.11.2020')

plot_mp('../results/mq_u_3', 'mq_u_3.png', 'MPQUIC | 400 MB upload, 1 stream localhost; 03:31, 20.11.2020')






