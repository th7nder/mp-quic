from plot_parser import parse_results, FIBER, LTE
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patheffects as pe

plt.rcParams.update({'lines.linewidth': 1})

def to(t, time, vals):
	if t == -1:
		return time, vals
	return time[time < t], vals[:np.argmax(time >= t)]

def sample(time, vals, step):
	if len(time) % step != 0:
		time = time[:-(len(time) % step)]
		vals = vals[:-(len(vals) % step)]

	return time[::step], np.mean(vals.reshape(-1, step), axis=1)

def plot_srtt_100(t):
	fiber = parse_results('../results/q_fu_1')
	lte = parse_results('../results/q_lu_2')
	mpq = parse_results('../results/mq_u_2')

	plt.figure(figsize=(6, 3))
	f = fiber.paths[FIBER]
	plt.plot(
		*to(t, f.time, f.srtt), 
		color="gold",
		label="Światłowód",
		path_effects=[pe.Stroke(linewidth=1.8, foreground='dimgrey'), pe.Normal()]
	)

	l = lte.paths[LTE]
	plt.plot(
		*to(t, l.time, l.srtt), 
		color="tab:blue",
		label="LTE"
	)
	f =  mpq.paths[FIBER]
	plt.plot(
		*to(t, f.time, f.srtt), 
		color="magenta",
		label="MPQ - Światłowód"
	)
	l = mpq.paths[LTE]
	plt.plot(
		*to(t, l.time, l.srtt), 
		color="tab:green",
		label="MPQ - LTE"
	)

	plt.ylabel('SRTT [ms]')
	plt.xlabel('Czas [s]')
	plt.legend()
	plt.tight_layout()
	plt.savefig('100_srtt', dpi=150)


def plot_inflights_2s50(t):
	fiber = parse_results('../results/2s_q_fu_1')
	lte = parse_results('../results/2s_q_lu_1')
	mpq = parse_results('../results/2s_mq_u_1')


	plt.figure(figsize=(6, 2))
	f =  mpq.paths[FIBER]
	plt.plot(
		*to(t, f.time, f.ifs), 
		color="tab:orange",
		label="MPQ - Światłowód"
	)
	l = mpq.paths[LTE]
	plt.plot(
		*to(t, l.time, l.ifs), 
		color="tab:blue",
		label="MPQ - LTE"
	)


	plt.ylabel('Dane w locie [kB]')
	plt.xlabel('Czas [s]')
	plt.legend()
	plt.tight_layout()
	plt.savefig('2s50_M_inflights', dpi=150)

def plot_thr_2s50_F(t):
	fiber = parse_results('../results/2s_q_fu_1')

	plt.figure(figsize=(6, 2))
	f = fiber.paths[FIBER]
	plt.plot(
		*to(t, f.time, f.throughput), 
		color="tab:orange",
		label="Światłowód"
	)

	plt.ylabel('Przepustowość [Mbps]')
	plt.xlabel('Czas [s]')
	plt.legend()
	plt.tight_layout()
	plt.savefig('2s50_F_throughput')

def plot_thr_2s50(t):
	fiber = parse_results('../results/2s_q_fu_1')
	lte = parse_results('../results/2s_q_lu_1')
	mpq = parse_results('../results/2s_mq_u_1')

	plt.figure(figsize=(6, 2))
	f =  mpq.paths[FIBER]
	plt.plot(
		*to(t, f.time, f.throughput), 
		color="tab:orange",
		label="MPQ - Światłowód"
	)
	l = mpq.paths[LTE]
	plt.plot(
		*to(t, l.time, l.throughput), 
		color="tab:blue",
		label="MPQ - LTE"
	)

	plt.ylabel('Przepustowość [Mbps]')
	plt.xlabel('Czas [s]')
	plt.legend()
	plt.tight_layout()
	plt.savefig('2s50_M_throughput')


def plot_thr_100(t):
	fiber = parse_results('../results/q_fu_1')
	lte = parse_results('../results/q_lu_2')
	mpq = parse_results('../results/mq_u_2')

	plt.figure(figsize=(6, 3))
	f = fiber.paths[FIBER]
	plt.plot(
		*to(t, f.time, f.throughput), 
		color="tab:orange",
		label="Światłowód"
	)
	l = lte.paths[LTE]
	plt.plot(
		*to(t, l.time, l.throughput), 
		color="tab:blue",
		label="LTE"
	)

	f =  mpq.paths[FIBER]
	plt.plot(
		*to(t, f.time, f.throughput), 
		color="tab:red",
		label="MPQ - Światłowód"
	)
	l = mpq.paths[LTE]
	plt.plot(
		*to(t, l.time, l.throughput), 
		color="tab:green",
		label="MPQ - LTE"
	)

	plt.ylabel('Przepustowość [Mbps]')
	plt.xlabel('Czas [s]')
	plt.yticks([0, 30, 60, 90, 120, 150, 180])
	plt.legend(loc="upper right")
	plt.tight_layout()
	# plt.show()
	plt.savefig('100_throughput', dpi=150)

def plot_inflights_100(t):
	fiber = parse_results('../results/q_fu_1')
	lte = parse_results('../results/q_lu_2')
	mpq = parse_results('../results/mq_u_2')


	plt.figure(figsize=(6, 3))
	f = fiber.paths[FIBER]
	plt.plot(
		*to(t, f.time, f.ifs), 
		color="tab:orange",
		label="Światłowód"
	)
	l = lte.paths[LTE]
	plt.plot(
		*to(t, l.time, l.ifs), 
		color="tab:blue",
		label="LTE"
	)

	f =  mpq.paths[FIBER]
	plt.plot(
		*to(t, f.time, f.ifs), 
		color="tab:red",
		label="MPQ - Światłowód"
	)
	l = mpq.paths[LTE]
	plt.plot(
		*to(t, l.time, l.ifs), 
		color="tab:green",
		label="MPQ - LTE"
	)


	plt.ylabel('Dane w locie [kB]')
	plt.xlabel('Czas [s]')
	plt.legend()
	plt.tight_layout()
	plt.savefig('100_inflight', dpi=150)

plot_inflights_100(10)
plot_srtt_100(10.0)
plot_thr_100(10.0)

plot_thr_2s50(-1)
plot_thr_2s50_F(-1)
plot_inflights_2s50(-1)