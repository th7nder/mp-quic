import numpy as np
import matplotlib.pyplot as plt
import csv

def clamp_time(time):
	s = time[0]
	for i in range(len(time)):
		time[i] -= s




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

def plot_delays(filename, paths, ax, fromTime, toTime, slg, show_labels):
	# ax.set_title('Opóźnienie odbioru vs. czas wysłania')
	# ax.set_xlabel('Czas wysłania [s]')
	if show_labels:
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

	print(streams)

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
		print(f"Delay max: {max(delays)}")
		
		clamp_time(times)
		r = find_times(times, fromTime, toTime)
		ax.plot(times[r[0]:r[1]], delays[r[0]:r[1]], label=slg[stream], color=scolors[stream])

	# ax.legend()

def plot_rtts(filename, paths, ax4, fromTime, toTime, slg, show_labels):
	# ax4.set_title('RTT vs. czas wysłania')
	ax4.set_xlabel('Czas wysłania [s]')
	if show_labels:
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

	for stream in sorted(streams):
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

	# ax4.legend()


def plot_mp2(filename, savefile, title, fromTime, toTime, slg, show_labels=False):
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
	fig, ((ax4), (ax5)) = plt.subplots(2, 1, figsize=((7, 4)))
	# fig.suptitle(title)
	plot_delays(filename, paths, ax4, fromTime, toTime, slg, show_labels)
	plot_rtts(filename, paths, ax5, fromTime, toTime, slg, show_labels)

	plt.setp(ax4.get_xticklabels(), visible=False)

	plt.rcParams.update({'lines.linewidth':0.6})
	plt.tight_layout()
	plt.savefig(savefile)

def plot_mp(filename, savefile, title, fromTime, toTime, slg, show_labels=False):
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
	fig, ((ax1), (ax2), (ax3), (ax4), (ax5)) = plt.subplots(5, 1, figsize=((3, 8)))
	# fig.suptitle(title)
	plot_delays(filename, paths, ax4, fromTime, toTime, slg, show_labels)
	plot_rtts(filename, paths, ax5, fromTime, toTime, slg, show_labels)
	if show_labels:
		# plot_inflights(ax4, filename, paths)
		# ax1.set_title('Dane w locie vs. czas')
		# ax1.set_xlabel('Czas [s]')
		ax1.set_ylabel('Dane w locie [kB]')
		# ax2.set_title('SRTT vs. czas')
		# ax2.set_xlabel('Czas [s]')
		ax2.set_ylabel('SRTT [ms]')

		# ax3.set_title('Przepustowość vs. czas')
		# ax3.set_xlabel('Czas [s]')
		ax3.set_ylabel('Tput [Mbps]')

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
			loss = int(row[8])
			packets = int(row[6])
			if int(srtt) == 0:
				throughput = 0
			else: 
				throughput = (int(inFlight) * 8) / (int(srtt) / 1000 / 1000)
			thr.append(throughput / 1000 / 1000)

		if sum(inFlights) < 1000:
			continue

		if p == "3":
			color = "orange"
			l = "Światłowód"
		elif p == "0" and rows[0][3][0] == "8":
			l = "Światłowód"
			color = "orange"
		else:
			l = "LTE"
			color = "dodgerblue"
		print(l, 'Tput', sum(thr) / len(thr), thr[-1])
		print(l, 'In-flight', sum(inFlights) / len(inFlights))
		print(l, 'SRTT', sum(srtts) / len(srtts))
		print(l, 'Loss', loss / packets * 100)

		clamp_time(t)
		r = find_times(t, fromTime, toTime)
		ax1.plot(t[r[0]:r[1]], inFlights[r[0]:r[1]], label=l, color=color)
		# ax1.plot(t[r[0]:r[1]], cwnds[r[0]:r[1]], label=f"{l} - okno przeciążenia")
		ax2.plot(t[r[0]:r[1]], srtts[r[0]:r[1]], label=l, color=color)
		ax3.plot(t[r[0]:r[1]], thr[r[0]:r[1]], label=l, color=color)

	# ax1.legend()
	# ax2.legend()
	# ax3.legend()
	# plt.show()
	# plt.subplots_adjust(hspace=0.3)
	plt.setp(ax1.get_xticklabels(), visible=False)
	plt.setp(ax2.get_xticklabels(), visible=False)
	plt.setp(ax3.get_xticklabels(), visible=False)
	plt.setp(ax4.get_xticklabels(), visible=False)

	plt.rcParams.update({'lines.linewidth':0.6})
	plt.tight_layout()
	plt.savefig(savefile)


# plot_mp('../results/mq_t_game', 'mq_t_game.png', '1. MPQUIC | 5MB upload + different, 4 streams throttled (.31); 13:28, 5.12.2020', 5, 7)

slg = {
	"3": "Strumień pliku 100MB",
}

# plot_mp('../results/mq_u_1', 'morn_u_3_mq_1.png', '3. MPQUIC | 1 strumień, wysyłanie pliku 100MB, nietłumiony', 0, -1, slg, show_labels=False)
# plot_mp('../results/mq_u_2', 'u_3_mq_2.png', '3.1. MPQUIC | 1 strumień, wysyłanie pliku 100MB, nietłumiony', 0, -1, slg),
# plot_mp('../results/q_fu_1', 'u_2_q_f_1.png', '1. QUIC Światłowód | 1 strumień, wysyłanie pliku 100MB, nietłumiony', 0,-1, slg, show_labels=True),
# plot_mp('../results/q_lu_1', 'morn_u_2_q_l_1.png', '2. QUIC LTE  | 1 strumień, wysyłanie pliku 100MB, nietłumiony', 0, -1)
# plot_mp('../results/q_lu_2', 'u_2_q_l_2.png', '2.1. QUIC LTE  | 1 strumień, wysyłanie pliku 100MB, nietłumiony', 0, -1, slg),

# plot_mp2('../results/mq_u_2', 'uZ_3_mq_2.png', '3.1. MPQUIC | 1 strumień, wysyłanie pliku 100MB, nietłumiony', 16, 18, slg, show_labels=True),


slg = {
	"3": "Strumień pliku 50MB",
	"5": "Strumień pliku 50MB",
}

# 2s 50MB
# plot_mp('../results/2s_q_fu_1', 'u_7_2s_q_f_1.png', '7. QUIC Fiber | 2 strumienie, wysyłanie 2 plików 50MB, nietłumiony', 0, -1, slg, show_labels=True)
# plot_mp('../results/2s_q_lu_1', 'u_6_2s_q_l_1.png', '6. QUIC LTE | 2 strumienie, wysyłanie 2 plików 50MB, nietłumiony', 0, -1, slg)
# plot_mp('../results/2s_mq_u_1', 'u_8_2s_mq_1.png', '8. MPQUIC | 2 strumienie, wysyłanie 2 plików 50MB, nietłumiony', 0, -1, slg)

# plot_mp2('../results/2s_q_lu_1', 'uZ_6_2s_q_l_1.png', '6. QUIC LTE | 2 strumienie, wysyłanie 2 plików 50MB, nietłumiony', 16, 18, slg, show_labels=True)
# plot_mp2('../results/2s_mq_u_1', 'uZ_8_2s_mq_1.png', '8. MPQUIC | 2 strumienie, wysyłanie 2 plików 50MB, nietłumiony', 16, 18, slg, show_labels=True)

## plot_mp('../results/2s_mq_u_2', 'u_8_2s_mq_2.png', '8. MPQUIC | 2 strumienie, wysyłanie 2 plików 50MB, nietłumiony', 0, -1, slg)
## plot_mp2('../results/2s_mq_u_2', 'uZ_8_2s_mq_2.png', '8. MPQUIC | 2 strumienie, wysyłanie 2 plików 50MB, nietłumiony', 12, 13, slg)

# 2SR 50 + mouse

plot_mp('../results/2sr_q_lu_1', 'u_12_2sr_q_l_1.png', '12. QUIC LTE | 2 strumienie, wysyłanie 1 pliku 50MB oraz 10kB co 0.2s, nietłumiony', 0, -1, slg)
# plot_mp('../results/2sr_q_fu_1', 'u_13_2sr_q_f_1.png', '13. QUIC Fiber | 2 strumienie, wysyłanie 1 pliku 50MB oraz 10kB co 0.2s', 0, -1, slg, show_labels=True)
plot_mp('../results/2sr_q_fu_2', 'u_13_2sr_q_f_2.png', '13. QUIC Fiber | 2 strumienie, wysyłanie 1 pliku 50MB oraz 10kB co 0.2s', 0, -1, slg, show_labels=True)
plot_mp('../results/2sr_mq_u_1', 'u_14_2sr_mq_1.png', '14. MPQUIC  | 2 strumienie, wysyłanie 1 pliku 50MB oraz 10kB co 0.2s', 0, -1, slg)

# 2 SP 50 + mouse

# plot_mp('../results/2sp_q_lu_1', 'u_9_2sp_q_l_1.png', '9. QUIC (priorytet strumień 2) LTE | 2 strumienie, wysyłanie 1 pliku 50MB oraz 10kB co 0.2s, nietłumiony', 0, -1, slg)
# plot_mp('../results/2sp_q_fu_1', 'u_10_2sp_q_f_1.png', '10. QUIC Fiber (priorytet strumień 2) | 2 strumienie, wysyłanie 1 pliku 50MB oraz 10kB co 0.2s', 0, -1, slg, show_labels=True)
# plot_mp('../results/2sp_mq_u_1', 'u_11_2sp_mq_1.png', '11. MPQUIC (priorytet strumień 2) | 2 strumienie, wysyłanie 1 pliku 50MB oraz 10kB co 0.2s', 0, -1, slg)






