import numpy as np
import matplotlib.pyplot as plt
import csv

def clamp_time(time):
	s = time[0]
	for i in range(len(time)):
		time[i] -= s
	
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

	fig, ((ax1), (ax2), (ax3)) = plt.subplots(3, 1, figsize=((40, 16)))
	fig.suptitle(title)
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


# plot('../results/fiber.csv', 'quic_fiber.png', 'QUIC | Fiber over Wi-Fi 5GHz, 170/60Mbps, 100MB upload, 1 stream, unthrottled')
# plot('../results/lte.csv', 'quic_lte.png', 'QUIC | LTE over Ethernet, 60/30Mbps, 100MB upload, 1 stream, unthrottled')

# plot_mp('../results/multipath_unthrottled.csv', 'mpquic.png', 'MPQUIC | 100 MB upload, 1 stream, unthrottled')
# plot_mp('../results/multipath_1.csv', 'mpquic_1.png', 'MPQUIC | 100 MB upload, 1 stream, unthrottled')
# plot_mp('../results/multipath_2.csv', 'mpquic_2.png', 'MPQUIC | 100 MB upload, 1 stream, unthrottled')
# plot_mp('../results/multipath_3.csv', 'mpquic_3.png', 'MPQUIC | 1GB upload, 1 stream, unthrottled')
plot_mp('../results/mq_u_1.csv', 'mq_u_1.png', 'MPQUIC | 400 MB upload, 1 stream, UNTHROTTLED (.78)')
plot_mp('../results/mq_u_2.csv', 'mq_u_2.png', 'MPQUIC | 800 MB upload, 1 stream, UNTHROTTLED (.78)')


# plot_mp('../results/q_t_1.csv', 'q_t_1.png', 'QUIC | 10 MB upload, THROTTLED')

# plot_mp('../results/mp_t_2.csv', 'mp_t_2.png', 'MPQUIC | 400 MB upload, 1 stream, THROTTLED')
# plot_mp('../results/mp_t_3.csv', 'mp_t_3.png', 'MPQUIC | 400 MB upload, 1 stream, THROTTLED')
# plot_mp('../results/mp_t_4.csv', 'mp_t_4.png', 'MPQUIC | 400 MB upload, 1 stream, THROTTLED')
# plot_mp('../results/mp_t_5.csv', 'mp_t_5.png', 'MPQUIC | 400 MB upload, 1 stream, THROTTLED')

# plot_mp('../results/mp_u_1.csv', 'mp_u_1.png', 'MPQUIC | 400 MB upload, 1 stream, unthrottled')
# plot_mp('../results/mp_u_2.csv', 'mp_u_2.png', 'MPQUIC | 400 MB upload, 1 stream, unthrottled')
# plot_mp('../results/mp_u_3.csv', 'mp_u_3.png', 'MPQUIC | 400 MB upload, 1 stream, unthrottled')
# plot_mp('../results/mp_u_4.csv', 'mp_u_4.png', 'MPQUIC | 400 MB upload, 1 stream, unthrottled')
# plot_mp('../results/mp_u_5.csv', 'mp_u_5.png', 'MPQUIC | 400 MB upload, 1 stream, unthrottled')
