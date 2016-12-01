import pandas
import networkx as nx
from networkx_viewer import Viewer

G = nx.MultiGraph()
G.nodes(data=True)
nodes = pandas.read_csv('nodes.csv')
nodes['edges'] = nodes['edges'].apply(lambda string: set([e[1:-1] for e in string[5:-2].split(', ')]))

for index, (_, edges, id_, name, type_) in nodes.iterrows():
    G.add_node(id_, attr_dict={
        'id_': id_,
        'name': name,
        'type_': type_,
        'edges': edges,
        'index': index,
    })
    for edge in edges:
        G.add_edge(id_, edge)

app = Viewer(G)
app.mainloop()
