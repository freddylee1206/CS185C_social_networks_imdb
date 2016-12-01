import numpy
import pandas 
from imdb import IMDb
imdbapi = IMDb()
seed_movie = '2404435'

nodes = pandas.DataFrame(columns=['id', 'type', 'name', 'edges']) 

def add_movie(movie_id):
    global nodes
    movie = imdbapi.get_movie(movie_id)
    edges = set ([person.getID() for person in (movie['cast'] + movie['director'])])

    newRow = pandas.DataFrame({'id':[movie_id], 'type':['movie'], 'name':[movie.get('title')], 
                        'edges':[edges] })
    nodes = pandas.concat([nodes, newRow])



def add_person(person_id):
    global nodes
    filmography = imdbapi.get_person_filmography(person_id)
    directed_movies= filmography['data']['director'] if 'director' in filmography['data'] else []
    acted_movies= filmography['data']['actor'] if 'actor' in filmography['data'] else []
    name = filmography['data']['name']
    edges = set(directed_movies + acted_movies)
    
    if directed_movies and acted_movies: 
        type='director/actor'
    elif directed_movies:
        type='director'
    elif acted_movies:
        type='actor'
    else:
        type='error'
    
    newRow = pandas.DataFrame({'id':[person_id], 'type':[type], 'name':[name], 
                        'edges':[edges] })
    print newRow
    nodes = pandas.concat([nodes, newRow])

    

add_movie(seed_movie)

all_edges = [edge for list in nodes['edges'] for edge in list]

pending_people = all_edges#.difference(nodes['id'])

for person_id in pending_people[0:10]:
    add_person(person_id)




#print nodes['edges']
#all_edges = set([edge for edges in row for row in nodes[edge]])


print nodes












