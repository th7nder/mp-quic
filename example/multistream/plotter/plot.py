import numpy as np
import matplotlib.pyplot as plt
import csv

def clamp_time(time):
	s = time[0]
	for i in range(len(time)):
		time[i] -= s


slg = {
	"3": "3. 5MB upload",
	"5": "5. 0.3-0.7s, 1,5-5kB",
	"7": "7. 0.5-0.8s, 20-250B",
	"9": "9. 0.1s, 100B",
}

def find_times(times, f, to):
	start = -1
	end = -1
	for idx, t in enumerate(times):
		if start == -1 and t > f:
			start = idx 
		if end == -1 and t > to:
			end = idx

	return (start, end)

def plot_delays(filename, paths, ax, fromTime, toTime):
	ax.set_title('sent time vs. delay to receive (from oldest unacked)')
	ax.set_xlabel('sent time [s]')
	ax.set_ylabel('delay [ms]')

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

	for stream in streams:
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
		print(f"Delay max: {max(delays)}")
		
		clamp_time(times)
		r = find_times(times, fromTime, toTime)
		ax.plot(times[r[0]:r[1]], delays[r[0]:r[1]], label=slg[stream], marker='o')

	ax.legend()

def plot_rtts(filename, paths, ax4, fromTime, toTime):
	ax4.set_title('sent time vs. delay to receive (from sent time)')
	ax4.set_xlabel('sent time [s]')
	ax4.set_ylabel('delay [ms]')

	rows = []
	with open(filename + '/rtt.csv') as f:
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

	for stream in streams:
		pds = []
		for row in rows:
			s = row[0]
			if stream != s:
				continue
			if len(row) != 4:
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
		print(f"RTT max: {max(delays)}")
		
		clamp_time(times)
		r = find_times(times, fromTime, toTime)
		ax4.plot(times[r[0]:r[1]], delays[r[0]:r[1]], label=slg[stream])

	ax4.legend()


def plot_mp(filename, savefile, title, fromTime, toTime):
	rows = []
	with open(filename + '/main.csv') as f:
		c = csv.reader(f)
		for row in c:
			rows.append(row)

	paths = set()
	for row in rows:
		path = row[1]
		paths.add(path)

	print(paths)
	fig, ((ax1), (ax2), (ax3), (ax4), (ax5)) = plt.subplots(5, 1, figsize=((40, 31)))
	fig.suptitle(title)
	plot_delays(filename, paths, ax4, fromTime, toTime)
	plot_rtts(filename, paths, ax5, fromTime, toTime)
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
		r = find_times(t, fromTime, toTime)
		ax1.plot(t[r[0]:r[1]], inFlights[r[0]:r[1]], label=l)
		ax2.plot(t[r[0]:r[1]], srtts[r[0]:r[1]], label=l)
		ax3.plot(t[r[0]:r[1]], thr[r[0]:r[1]], label=l)

	ax1.legend()
	ax2.legend()
	ax3.legend()
	plt.show()
	# plt.savefig(savefile)

plot_mp('../results/mq_t_game', 'mq_t_game.png', '1. MPQUIC | 5MB upload + different, 4 streams throttled (.78); 13:28, 5.12.2020', 4.5, 6.5)


# plot_mp('../results/mq_u_1', 'mq_u_1.png', '1. MPQUIC | 50MB upload, 1 stream UNTHROTTLED (.78); 00:41, 23.11.2020')
# plot_mp('../results/mq_u_2', 'mq_u_2.png', '2. MPQUIC | 50MB upload, 1 stream UNTHROTTLED (.78); 00:41, 23.11.2020')
# plot_mp('../results/mq_u_3', 'mq_u_3.png', '3. MPQUIC | 50MB upload, 1 stream UNTHROTTLED (.78); 00:41, 23.11.2020')
# plot_mp('../results/mq_u_4', 'mq_u_4.png', '44. MPQUIC | 50MB upload, 1 stream UNTHROTTLED (.78); 16:34, 25.11.2020')
# plot_mp('../results/mq_u_5', 'mq_u_5.png', '44. MPQUIC | 50MB upload, 1 stream UNTHROTTLED (.78); 16:34, 25.11.2020')



# plot_mp('../results/mq_t_1', 'mq_t_1.png', '4. MPQUIC | 50MB upload, 1 stream UNTHROTTLED (.78); 00:41, 23.11.2020')
# plot_mp('../results/mq_t_2', 'mq_t_2.png', '5. MPQUIC | 50MB upload, 1 stream UNTHROTTLED (.78); 00:41, 23.11.2020')
# plot_mp('../results/mq_t_3', 'mq_t_3.png', '6. MPQUIC | 50MB upload, 1 stream UNTHROTTLED (.78); 00:41, 23.11.2020')


# plot_mp('../results/2_mq_u_1', '2_mq_u_1.png', '7. MPQUIC | 2 streams, 50MB per stream UNTHROTTLED (.78); 00:20, 23.11.2020')
# plot_mp('../results/2_mq_u_2', '2_mq_u_2.png', '8. MPQUIC | 2 streams, 50MB per stream UNTHROTTLED (.78); 00:20, 23.11.2020')
# plot_mp('../results/2_mq_u_3', '2_mq_u_3.png', '9. MPQUIC | 2 streams, 50MB per stream UNTHROTTLED (.78); 00:20, 23.11.2020')
# plot_mp('../results/2_mq_u_4', '2_mq_u_4.png', '9. MPQUIC | 2 streams, 50MB per stream UNTHROTTLED (.78); 11:27, 25.11.2020')


# plot_mp('../results/2_mq_t_1', '2_mq_t_1.png', '10. MPQUIC | 2 streams, 5MB per stream; throttled (.31); 00:32, 23.11.2020')
# plot_mp('../results/2_mq_t_2', '2_mq_t_2.png', '11. MPQUIC | 2 streams, 5MB per stream; throttled (.31); 00:33, 23.11.2020')
# plot_mp('../results/2_mq_t_3', '2_mq_t_3.png', '12. MPQUIC | 2 streams, 5MB per stream; throttled (.31); 00:33, 23.11.2020')
# plot_mp('../results/2_mq_t_4', '2_mq_t_4.png', '13. MPQUIC | 2 streams, 5MB per stream; throttled (.31); 11:23, 25.11.2020')









