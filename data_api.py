
import requests
import json
# import sys
# sys.setExecutionLimit(100000000)
def get_movies_from_tastedive (movie_name):
    '''This function takes in a movie as a parameter and returns a list of 5 movies similar to the movie using the Taste Dive APi'''
    baseurl= 'https://tastedive.com/api/similar'
    params_dict={}
    params_dict['q']= movie_name
    params_dict['type']= 'movies'
    params_dict['limit']= '5'
    same=requests.get(baseurl, params=params_dict)

    return same.json()


def extract_movie_titles(data):
    '''This function takes a list of JSON formatted data returned from the get_movies_from_tastedive function and
    extracts the movie titles of the similar movies'''
    movie_titles=[]
    for item in data['Similar']['Results']:
        movie_titles.append(item['Name'])
    return movie_titles



def get_related_titles(movie_list):
    '''This function takes a list of movies as an input and for every movie, returns a list of 5 similar movies (Only the title of the movies are returned) '''
    #If one movie is returned twice in the related movies list, they are only added once. To remove any repititions
    final_list=[]
    #Contains a list of lists of 5 similar movie titles for every movie in the movie list
    relatedlist=[]
    for elem in movie_list:
        relatedlist.append(extract_movie_titles(get_movies_from_tastedive(elem)))
    for item in relatedlist:
        for name in item:
            if name not in final_list:
                final_list.append(name)
    return final_list

def get_movie_data(movie_title):
    '''This function returns some information about a movie including the movie rating various rating sites using the OMDB API'''
    baseurl='http://www.omdbapi.com/'
    params_dict={}
    #The API_KEY here has been altered slightly to prevent unwanted use. If needed for testing, you can request for mine
    params_dict['apikey']= '33e0b99w'
    params_dict['t']= movie_title
    params_dict['r']= 'json'
    resp = requests.get(baseurl,params_dict)
    #print(resp.url)
    return resp.json()

def get_movie_rating(movie_info):
    '''This function takes a dictionary containing some JSON data about a movie and returns integer of the rotten tomatoes rating.
    If there is no rotten Tomatoes rating then 0 is returned'''
    for rating in movie_info['Ratings']:
        if rating['Source']=='Rotten Tomatoes':
            rott_rate = int(rating['Value'].rstrip('%'))
            break
        else:
            rott_rate=0
    return rott_rate

def get_sorted_recommendations(lst):
    '''This function takes a list of movies and returns a list of movies related to the movies in the list entered. The returned lists
    of movies is sorted based on their rotten tomatoes rating in the descending order'''
#Output produces a list of movies titles related to the movies in the list passed into the function
    output= get_related_titles(lst)
    #print(output)
    #This dictionary assigns rotten tomatoes rating to every movie name in the output which is a list of related movies to the movie list that was passed into the funcion
    dic_names={}
    for name in output:
        dic_names[name]=get_movie_rating(get_movie_data(name))

#Rott list contains a sorted list of tuples for each related movie in descending order.
    rott_list= sorted(dic_names.items(), key = lambda tup:(tup[1],tup[0]), reverse= True )
    #print(rott_list)
#fin_list conatins a list of just the movie titles in descending order. i.e the related movie with the highest rotten tomatoes rating comes first
    fin_list=[]
    for tup in rott_list:
        fin_list.append(tup[0])

        #print(tup[0])
    return fin_list



print(get_sorted_recommendations(['Deadpool','Friday']))
