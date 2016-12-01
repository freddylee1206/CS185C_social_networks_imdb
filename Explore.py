import pandas
from imdb import IMDb

imdbapi = IMDb()
seed_movie = '2404435'

nodes = pandas.DataFrame(columns=['id', 'type', 'name', 'edges'])


def add_movie(movie_id):
    global nodes
    movie = imdbapi.get_movie(movie_id)
    edges = set([person.getID() for person in (movie['cast'] + movie['director'])])
    newRow = pandas.DataFrame({'id': [movie_id], 'type': ['movie'], 'name': [movie.get('title')], 'edges': [edges]})
    nodes = pandas.concat([nodes, newRow])


def add_person(person_id):
    global nodes
    filmography = imdbapi.get_person_filmography(person_id)
    directed_movies = filmography['data']['director'] if 'director' in filmography['data'] else []
    directed_movies = set([movie.getID() for movie in directed_movies])
    acted_movies = filmography['data']['actor'] if 'actor' in filmography['data'] else []
    acted_movies = set([movie.getID() for movie in acted_movies])
    name = filmography['data']['name']
    edges = directed_movies.union(acted_movies)

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


add_movie(seed_movie)
all_edges = set([edge for edge_list in nodes['edges'] for edge in edge_list])
pending_people = all_edges.difference(nodes['id'])
for node_id in pending_people:
    add_person(node_id)
nodes.to_csv("nodes.csv")
