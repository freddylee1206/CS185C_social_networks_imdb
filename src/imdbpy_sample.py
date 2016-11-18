from imdb import IMDb
imdbapi = IMDb()

# print the director(s) of a movie
the_matrix = imdbapi.get_movie('0133093')
print the_matrix['director']
print the_matrix['cast']

p = imdbapi.get_person_filmography('0905154')
print(p)

# search for a person
for person in imdbapi.search_person('Mel Gibson'):
    print person.personID, person['name']
