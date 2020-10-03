import matplotlib.pyplot as plt
import networkx as nx


def depGraph(schedule, filename):
    G = nx.DiGraph()
    schedule = schedule.split()
    G.add_nodes_from([op[0] for op in schedule])
    for i in range(len(schedule)):
        for j in range(i + 1, len(schedule)):
            if schedule[i][2] == schedule[j][2] and (schedule[i][1] == 'W' or schedule[j][1] == 'W'):
                G.add_edge(schedule[i][0], schedule[j][0])
    nx.draw_networkx(G, with_labels=True, arrows=True)
    if nx.is_directed_acyclic_graph(G):
        print("topoligical sort", nx.topological_sort(G))
    plt.savefig(filename + ".png")
    return nx.is_directed_acyclic_graph(G)


def waitGraph(schedule, filename):
    G = nx.DiGraph()
    schedule = schedule.split()
    G.add_nodes_from([op[0] for op in schedule])
    for i in range(len(schedule)):
        for j in range(i + 1, len(schedule)):
            if G.out_degree(schedule[j][0]) == 0 \
                    and schedule[i][2] == schedule[j][2] \
                    and (schedule[i][1] == 'X' or schedule[j][1] == 'X'):
                G.add_edge(schedule[j][0], schedule[i][0])
                print(schedule[j][0], schedule[i][0])
    nx.draw(G, with_labels=True, arrowstyle='->')
    plt.savefig(filename + ".png")
    return nx.is_directed_acyclic_graph(G)


if __name__ == "__main__":
    # print(waitGraph("1SA 3SA 2XB 4SB 1XC 1SY 2XC 3XB", "1"))
    # print(depGraph("1RB 2RB 3WB 4WB 2RD 3RC 1RC 4WC 4WD 1RA 2WA", "1"))
    # print(depGraph("3RB 2WC 4WA 4WB 2RC 3WB 2RA 2RB 1RA 3RC", '1'))
    # depGraph("1RA 2RA 1RB 2RB 3RA 4RB 1WA 2WB", '2')

    print(waitGraph("3XE 2SE 1XB 1XA 4XA 3SB 2XD 1SD 4SD", '3'))
