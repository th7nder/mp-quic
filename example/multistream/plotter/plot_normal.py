from plot_parser import parse_results, FIBER, LTE
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

plt.rcParams.update({'lines.linewidth': 1})

def to(t, time, vals):
	return time[time < t], vals[:np.argmax(time >= t)]



def plot_srtt_100(t):
	fiber = parse_results('../results/q_fu_1')
	lte = parse_results('../results/q_lu_2')
	mpq = parse_results('../results/mq_u_2')

	plt.figure(figsize=(6, 3))
	f = fiber.paths[FIBER]
	plt.plot(
		*to(t, f.time, f.srtt), 
		color="tab:orange",
		label="Światłowód"
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
		color="tab:red",
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
	plt.legend()
	plt.tight_layout()
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
	# plt.show()

plot_inflights_100(10)
plot_srtt_100(10.0)
plot_thr_100(10.0)
