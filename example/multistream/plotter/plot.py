import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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


def plot_delays_bar(filename, ax, fromTime, toTime, label, show_labels):
	# ax.set_title('Opóźnienie odbioru vs. czas wysłania')
	# ax.set_xlabel('Czas wysłania [s]')
	if show_labels:
		ax.set_ylabel('Opóź. odbioru [ms]')

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

	previous = None
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
		print(f"Avg delay s - {stream}", sum(delays) / len(delays))
		
		clamp_time(times)
		r = find_times(times, fromTime, toTime)

		curr = np.array(delays[r[0]:r[1]])
		times = np.array(times[r[0]:r[1]])
		sampling = len(curr) // 500
		if len(curr) % sampling != 0:
			curr = curr[:-(len(curr) % sampling)]
			times = times[:-(len(times) % sampling)]

		print(len(curr))
		print(len(times))
		curr = np.mean(curr.reshape(-1, sampling), axis=1)
		times = times[::sampling]

		if previous != None:
			ax.step(times, curr, label=slg[stream], color=scolors[stream])
		else:
			ax.step(times, curr, label=slg[stream], color=scolors[stream])
		previous = delays

	return streams


def plot_delays_diff(filename, ax, fromTime, toTime, label, color, show_labels):
	if show_labels:
		ax.set_ylabel('Opóź. odbioru [ms]')

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

	previous = None
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
		print(f"Avg delay s - {stream}", sum(delays) / len(delays))
		
		clamp_time(times)
		r = find_times(times, fromTime, toTime)

		curr = np.array(delays[r[0]:r[1]])
		times = np.array(times[r[0]:r[1]])
		sampling = len(curr) // 150
		if len(curr) % sampling != 0:
			curr = curr[:-(len(curr) % sampling)]
			times = times[:-(len(times) % sampling)]

		print(len(curr))
		print(len(times))
		curr = np.mean(curr.reshape(-1, sampling), axis=1)
		times = times[::sampling]

		if previous != None:
			ax.step(times, curr, label=label, color=color)
		else:
			ax.step(times, curr, label=label, color=color)
		previous = delays

	return streams


def plot_delays(filename, paths, ax, fromTime, toTime, slg, show_labels):
	if show_labels:
		ax.set_ylabel('Opóź. odbioru [ms]')

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
		print(f"Avg delay s - {stream}", sum(delays) / len(delays))
		
		clamp_time(times)
		r = find_times(times, fromTime, toTime)
		ax.plot(times[r[0]:r[1]], delays[r[0]:r[1]], label=slg[stream], color=scolors[stream])

	return streams

def plot_single_delay_combined(filenames, savefile, fromTime, toTime, slg, show_labels=False, ticks=[], size=(6, 2)):
	_, ((ax1)) = plt.subplots(1, 1, figsize=size)
	colors = [
		"orange",
		"dodgerblue",
		"green"
	]
	labels = [
		"Światłowód",
		"LTE",
		"Wielościeżkowa",
	]
	for idx, filename in enumerate(filenames):
		plot_delays_diff(filename, ax1, fromTime, toTime, labels[idx], colors[idx], show_labels=True)

	if len(ticks) > 0:
		ax1.yaxis.set_ticks(ticks)

	ax1.legend()
	plt.rcParams.update({'lines.linewidth': 1})
	plt.tight_layout()
	plt.savefig(savefile, dpi=150)
	plt.close()


def plot_single(tp, filename, savefile, title, fromTime, toTime, slg, show_labels=False, ticks=[], yLabel=True, legend=False, delayBar=False, size=(6, 2)):
	rows = []
	with open(filename + '/main.csv') as f:
		c = csv.reader(f)
		for row in c:
			rows.append(row)

	paths = set()
	for row in rows:
		path = row[1]
		paths.add(path)

	fig, ((ax1)) = plt.subplots(1, 1, figsize=size)
	if show_labels:
		if yLabel:
			if tp == 'inFlights':
				ax1.set_ylabel('Dane w locie [kB]')
			elif tp == 'thr':
				ax1.set_ylabel('Przepustowość [Mbps]')
			elif tp == 'delays':
				ax1.set_ylabel('Opóź. odbioru [ms]')
			else:
				ax1.set_ylabel('SRTT [ms]')
		ax1.set_xlabel('Czas [s]')
	
	streams = None
	if tp == 'delays':
		if delayBar:
			streams = plot_delays_bar(filename, ax1, fromTime, toTime, slg, show_labels)
		else:
			streams = plot_delays(filename, paths, ax1, fromTime, toTime, slg, show_labels)
	else:
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

			print(l, 'SRTT', sum(srtts) / len(srtts))
			

			clamp_time(t)
			r = find_times(t, fromTime, toTime)
			if tp == 'inFlights':
				ax1.plot(t[r[0]:r[1]], inFlights[r[0]:r[1]], label=l, color=color)
			elif tp == 'thr':
				ax1.plot(t[r[0]:r[1]], thr[r[0]:r[1]], label=l, color=color)
			else:
				ax1.plot(t[r[0]:r[1]], srtts[r[0]:r[1]], label=l, color=color)


	if len(ticks) > 0:
		ax1.yaxis.set_ticks(ticks)

	if legend and streams is not None and len(streams) > 1: 
		ax1.legend()
	elif legend and streams is None:
		ax1.legend()

	plt.rcParams.update({'lines.linewidth': 1})
	plt.tight_layout()
	plt.savefig(savefile, dpi=150)
	plt.close()


slg = {
	"3": "Strumień pliku 100MB",
}


plot_single_delay_combined(['../results/q_fu_1', '../results/q_lu_2', '../results/mq_u_2'], '100_combined.png', 0, 10, slg, show_labels=True, size=((6, 3)))

slg = {
	"3": "Strumień 1 pliku 50MB",
	"5": "Strumień 2 pliku 50MB",
}


plot_single('delays', '../results/2s_q_fu_1', '2s50_F_delays.png', '', 0, -1, slg, show_labels=True, delayBar=True, legend=True)
plot_single('delays', '../results/2s_q_lu_1', '2s50_L_delays.png', '', 0, -1, slg, show_labels=True, delayBar=True, legend=True)
plot_single('delays', '../results/2s_mq_u_1', '2s50_M_delays.png', '', 0, -1, slg, show_labels=True, delayBar=True, legend=True)


slg = {
	"3": "Strumień 1 pliku 50MB",
	"5": "Strumień 13kB co 0.1s",
}

plot_single('srtt', '../results/2sr_q_fu_2', '2sr_F_srtt.png', '', 0, 5, slg, show_labels=True)
plot_single('srtt', '../results/2sr_mq_u_1', '2sr_M_srtt.png', '', 0, 5, slg, show_labels=True, legend=True)

plot_single('delays', '../results/2sr_q_fu_2', '2sr_F_delays.png', '', 0, 5, slg, show_labels=True, legend=True, delayBar=True)
plot_single('delays', '../results/2sr_mq_u_1', '2sr_M_delays.png', '', 0, 5, slg, show_labels=True, legend=True,  delayBar=True)

plot_single('srtt', '../results/2sr_mq_u_1', '2sr_M_srtt.png', '', 0, 13, slg, show_labels=True, legend=True, ticks=[0, 50, 100, 150])
plot_single('delays', '../results/2sr_mq_u_1', '2sr_M_delays.png', '', 0, 13, slg, show_labels=True, legend=True,  delayBar=True, ticks=[0, 60, 120, 180, 240, 300])

plot_single('srtt', '../results/2sp_mq_u_1', '2sp_M_srtt.png', '', 0, 13, slg, show_labels=True, legend=True, ticks=[0, 50, 100, 150])
plot_single('delays', '../results/2sp_mq_u_1', '2sp_M_delays.png', '', 0, 13, slg, show_labels=True, legend=True,  delayBar=True, ticks=[0, 60, 120, 180, 240, 300])
