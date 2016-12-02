import pandas
from imdb import IMDb


imdbapi = IMDb()
seed_movie = 'm2404435'

nodes = pandas.DataFrame(columns=['id', 'type', 'name', 'edges'])


def add_movie(movie_id, final=False):
    global nodes
    movie = imdbapi.get_movie(movie_id[1:])
    edges = set(['p' + person.getID() for person in (movie['cast'] + movie['director'])]) if not final else set()
    newRow = pandas.DataFrame({'id': [movie_id], 'type': ['movie'], 'name': [movie.get('title')], 'edges': [edges]})
    nodes = pandas.concat([nodes, newRow])


def add_person(person_id, final=False):
    global nodes
    filmography = imdbapi.get_person_filmography(person_id[1:])
    directed_movies = filmography['data']['director'] if 'director' in filmography['data'] else []
    directed_movies = set(['m' + movie.getID() for movie in directed_movies])
    acted_movies = filmography['data']['actor'] if 'actor' in filmography['data'] else []
    acted_movies = set(['m' + movie.getID() for movie in acted_movies])
    name = filmography['data']['name']
    edges = directed_movies.union(acted_movies) if final else set()

    if directed_movies and acted_movies:
        node_type = 'director/actor'
    elif directed_movies:
        node_type = 'director'
    elif acted_movies:
        node_type = 'actor'
    else:
        node_type = 'error'

    newRow = pandas.DataFrame({'id': [person_id], 'type': [node_type], 'name': [name], 'edges': [edges]})
    nodes = pandas.concat([nodes, newRow])


def expand_graph(final=False):
    all_edges = set([destination_node for edge_list in nodes['edges'] for destination_node in edge_list])
    dangling_edges = all_edges.difference(nodes['id'])
    for node_id in dangling_edges:
        if node_id[0] is 'p':
            add_person(node_id, final=final)
        elif node_id[1] is 'm':
            add_movie(node_id, final=final)
        else:
            raise Exception("mistagged node_id {}".format(node_id))


add_movie(seed_movie)
expand_graph()
expand_graph(final=True)
nodes.to_csv("nodes.csv")
print "fin."
