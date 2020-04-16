import networkx as nx
import matplotlib.pyplot as plt

def depGraph(schedule, filename):
	G = nx.DiGraph()
	schedule = schedule.split()
	G.add_nodes_from([op[0] for op in schedule])
	for i in range(len(schedule)):
		for j in range(i + 1, len(schedule)):
			if schedule[i][2] == schedule[j][2] and (schedule[i][1] == 'W' or schedule[j][1] == 'W'):
				G.add_edge(schedule[i][0], schedule[j][0])
	nx.draw(G, with_labels=True)
	plt.savefig(filename + ".png")
	return nx.is_directed_acyclic_graph(G)


def waitGraph(schedule, filename):
	G = nx.DiGraph()
	schedule = schedule.split()
	G.add_nodes_from([op[0] for op in schedule])
	for i in range(len(schedule)):
		for j in range(i + 1, len(schedule)):
			if G.out_degree(schedule[j][0]) == 0\
					and schedule[i][2] == schedule[j][2]\
					and (schedule[i][1] == 'X' or schedule[j][1] == 'X'):
				G.add_edge(schedule[j][0], schedule[i][0])
	nx.draw(G, with_labels=True)
	plt.savefig(filename + ".png")
	return nx.is_directed_acyclic_graph(G)


# print(depGraph("3RC 1RA 1WA 1RB 2WB 2RC 2WC 2WA 3WD", '1'))
# depGraph("1RA 2RA 1RB 2RB 3RA 4RB 1WA 2WB", '2')

print(waitGraph("1SA 1SD 2XB 1SB 3SD 3SC 2XC 4XB 3XA", '3'))
