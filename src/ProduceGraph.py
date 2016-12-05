import pandas
import seaborn
from matplotlib import pyplot
from networkx import Graph, shortest_path
from networkx.algorithms.bipartite import projected_graph
from networkx.algorithms.centrality import betweenness_centrality
from networkx.algorithms.cluster import clustering
from networkx_viewer import Viewer

WILL_RECALCULATE_GRAPH_PROPERTIES = True

G = Graph()
G.nodes(data=True)
nodes = pandas.read_csv('nodes.csv', index_col='id')
nodes['edges'] = nodes['edges'].apply(lambda string: set(string[5:-2].split(', ')))
people = []

for node_id, (edges, name, node_type, clusteringCoefficient, betweennessCentrality, distance, degree) in nodes.iterrows():
    G.add_node(node_id, attr_dict={
        'id_': node_id,
        'name': name,
        'type_': node_type,
        'edges': edges,
        'clusteringCoefficient': clusteringCoefficient,
        'betweennessCentrality': betweennessCentrality,
        'distanceToFurthestNode': distance,
        'degree': degree
    })
    if node_id[0] == 'p':
        people.append(node_id)
    for edge in edges:
        if len(edge) > 1:
            G.add_edge(node_id, edge)
            G.add_edge(edge, node_id)

pG = projected_graph(G, people)

distances_to_furthest_nodes = dict()
for source, targets_to_paths in shortest_path(pG).iteritems():
    longest_shortest_path_length = 0
    for target, path in targets_to_paths.iteritems():
        longest_shortest_path_length = max([longest_shortest_path_length, len(path)])
        distances_to_furthest_nodes[source] = longest_shortest_path_length

nodes['distanceToFurthestNode'] = pandas.Series(distances_to_furthest_nodes, index=nodes.index)
nodes['clusteringCoefficient'] = pandas.Series(clustering(pG), index=nodes.index)
nodes['betweennessCentrality'] = pandas.Series(betweenness_centrality(pG), index=nodes.index)
nodes['degree'] = pandas.Series(pG.degree(), index=nodes.index)

print "vertices: {}".format(pG.number_of_nodes())
print "edges: {}".format(pG.number_of_edges())
print nodes.nlargest(5, 'clusteringCoefficient')[['clusteringCoefficient', 'name']]
print nodes.nlargest(5, 'betweennessCentrality')[['betweennessCentrality', 'name']]
print nodes.nlargest(5, 'distanceToFurthestNode')[['distanceToFurthestNode', 'name']]
print nodes.nlargest(5, 'degree')[['degree', 'name']]

nodes.to_csv('nodes.csv', encoding='utf-8')

app = Viewer(pG)
app.mainloop()

p_nodes = nodes.loc[~nodes['type'].isin(['error', 'movie'])]
seaborn.FacetGrid(data=p_nodes, hue='type', palette=['red', 'blue', 'green']) \
    .map(pyplot.scatter, 'betweennessCentrality', 'clusteringCoefficient') \
    .add_legend()
pyplot.show()

seaborn.swarmplot(x="type", y="degree", data=p_nodes)
pyplot.show()
