import numpy as np
import matplotlib.pyplot as plt
import csv

def clamp_time(time):
	s = time[0]
	for i in range(len(time)):
		time[i] -= s


slg = {
	"3": "100MB upload",
	"5": "5. 0.3-0.7s, 1,5-5kB",
	"7": "7. 0.5-0.8s, 20-250B",
	"9": "9. 0.1s, 100B",
}

scolors = {
	"3": "g",
	"5": "r",
	"7": "b",
	"9": "m",
}

def find_times(times, f, to):
	start = -1
	end = -1
	for idx, t in enumerate(times):
		if start == -1 and t > f:
			start = idx 
		if to != -1 and end == -1 and t > to:
			end = idx

	return (start, end)

def plot_delays(filename, paths, ax, fromTime, toTime):
	ax.set_title('Opóźnienie odbioru vs. czas wysłania')
	ax.set_xlabel('Czas wysłania [s]')
	ax.set_ylabel('Opóźnienie odbioru [ms]')

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
		ax.plot(times[r[0]:r[1]], delays[r[0]:r[1]], label=slg[stream], color=scolors[stream])

	ax.legend()

def plot_rtts(filename, paths, ax4, fromTime, toTime):
	ax4.set_title('RTT vs. czas wysłania')
	ax4.set_xlabel('Czas wysłania [s]')
	ax4.set_ylabel('RTT [ms]')

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
		ax4.plot(times[r[0]:r[1]], delays[r[0]:r[1]], label=slg[stream], color=scolors[stream])

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
	ax1.set_title('Dane w locie vs. czas')
	ax1.set_xlabel('Czas [s]')
	ax1.set_ylabel('Dane w locie [kB]')
	ax2.set_title('SRTT vs. czas')
	ax2.set_xlabel('Czas [s]')
	ax2.set_ylabel('SRTT [ms]')

	ax3.set_title('Przepustowość vs. czas')
	ax3.set_xlabel('Czas [s]')
	ax3.set_ylabel('Przepustowść [Mbps]')

	for p in paths:
		t = []
		inFlights = []
		srtts = []
		thr = []
		cwnds = []
		for row in rows:
			path = row[1]
			if path != p:
				continue
			time = row[0]
			inFlight = row[4]
			srtt = row[5]
			cwnd = row[9]
			t.append(int(time) / 1000 / 1000 / 1000)
			inFlights.append(int(inFlight) / 1000)
			cwnds.append(int(cwnd) / 1000)
			srtts.append(int(srtt) / 1000)
			if int(srtt) == 0:
				throughput = 0
			else: 
				throughput = (int(inFlight) * 8) / (int(srtt) / 1000 / 1000)
			thr.append(throughput / 1000 / 1000)

		if sum(inFlights) < 1000:
			continue

		if p == "3":
			l = "Światłowód"
		elif p == "0" and rows[0][3][0] == "8":
			l = "Światłowód"
		else:
			l = "LTE"
		print(sum(thr) / len(thr))
		clamp_time(t)
		r = find_times(t, fromTime, toTime)
		ax1.plot(t[r[0]:r[1]], inFlights[r[0]:r[1]], label=l)
		ax1.plot(t[r[0]:r[1]], cwnds[r[0]:r[1]], label=f"{l} - okno przeciążenia")
		ax2.plot(t[r[0]:r[1]], srtts[r[0]:r[1]], label=l)
		ax3.plot(t[r[0]:r[1]], thr[r[0]:r[1]], label=l)

	ax1.legend()
	ax2.legend()
	ax3.legend()
	# plt.show()
	plt.savefig(savefile)

# plot_mp('../results/mq_t_game', 'mq_t_game.png', '1. MPQUIC | 5MB upload + different, 4 streams throttled (.31); 13:28, 5.12.2020', 5, 7)


plot_mp('../results/mq_u_1', '3_mq_u_1.png', '3. MPQUIC | 1 strumień, wysyłanie pliku 100MB, nietłumiony', 0, -1)
plot_mp('../results/q_fu_1', '1_q_fu_1.png', '1. QUIC Światłowód | 1 strumień, wysyłanie pliku 100MB, nietłumiony', 0, -1)
plot_mp('../results/q_lu_1', '2_q_lu_1.png', '2. QUIC LTE  | 1 strumień, wysyłanie pliku 100MB, nietłumiony', 0, -1)

plot_mp('../results/q_ft_1', '4_q_ft_1.png', '4. QUIC Światłowód | 1 strumień, wysyłanie pliku 5MB, tłumiony | wykres ucięty, 0-4s', 0, 4)
plot_mp('../results/q_lt_1', '5_q_lt_1.png', '5. QUIC LTE | 1 strumień, wysyłanie pliku 5MB, tłumiony | wykres ucięty, 0-4s', 0, 4)


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


# plot_mp('../results/2_mq_t_1', '2_mq_t_1.png', '10. MPQUIC | 2 streams, 5MB per stream; throttled (.31); 00:32, 15.12.2020', 0, -1)
# plot_mp('../results/2_mq_t_2', '2_mq_t_2.png', '11. MPQUIC | 2 streams, 5MB per stream; throttled (.31); 00:33, 23.11.2020')
# plot_mp('../results/2_mq_t_3', '2_mq_t_3.png', '12. MPQUIC | 2 streams, 5MB per stream; throttled (.31); 00:33, 23.11.2020')
# plot_mp('../results/2_mq_t_4', '2_mq_t_4.png', '13. MPQUIC | 2 streams, 5MB per stream; throttled (.31); 11:23, 25.11.2020')









