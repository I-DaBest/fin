.. moVstudiocode documentation master file, created by
   sphinx-quickstart on Tue Nov 25 07:05:18 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

moVstudiocode documentation
===========================

Documentation goes here
Movie recommendation code 
-This code gives out reccomendations for a movie
=====

Change the movie_ids_to_query and movie_id to a certain number to find the movie for that movie id, and it will find similar movies


All movies come from The Movie Database (tmdb)

Movie recommendation code 

This code gives out reccomendations for a movie

Change the movie_ids_to_query and movie_id to a certain number to find the movie for that movie id, and it will find similar movies

All movies come from The Movie Database (tmdb)

Ratings are based on vote average- the average rating from users on the site

Can add multiple movie ids to find listings for multiple movies

##Functions:

async main - finds the movies and displays their titles, ids, and ratings as a list



"""
moVstudiocode.py
====================================
This code gives out movie reccomendations

| Author: Katherine
| Date: 2025 Novermber 30
"""

import asyncio
from tmdb import route, schema
from dacite import from_dict
import requests
import json
import matplotlib.pyplot as plt
import networkx as nx

async def main():
    """
    Gets the movies from the online movie database and finds similar movies
    Parameters
    ----------
    movie_ids_to_query: list[int]
        the id of the movie you want recommendations for
        
    Returns
    ----------
    movie_similarity_data: dict
        the title and id of movies considered similar to the chosen movie, used for making the graph
    """

    base = route.Base()
    base.key = "4ec39598d34ba6c46351241dcf930713" #The API key to access the movie database
    movie_ids_to_query = [777] #the movie you want to use

    movie_id = 777
    URL = f"https://api.themoviedb.org/3/movie/{movie_id}/similar"

    params = {
    'api_key': "4ec39598d34ba6c46351241dcf930713",
    'language': 'en-US',
    'page': 1
    }

    response = requests.get(URL, params=params)
    movie_similarity_data = {}

    for movie_id in movie_ids_to_query:
        # Fetch movie title
        movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        details_response = requests.get(movie_details_url, params=params)
        
        movie_title = "Unknown"
        if details_response.status_code == 200:
            movie_details = details_response.json()
            movie_title = movie_details.get('title', 'Unknown')
            movie_rating = movie_details.get('vote_average')
        else:
            print(f"Error fetching details for movie ID {movie_id}: {details_response.status_code}")
            continue

        # Fetch similar movies
        similar_response = requests.get(URL, params=params)

        if similar_response.status_code == 200:
            data = similar_response.json()
            similar_movies_list = [
                {'id': m['id'], 'title': m['title'], 'rating': m['vote_average']} for m in data['results']
            ]
            movie_similarity_data[movie_id] = {
                "title": movie_title,
                "similar_movies": similar_movies_list,
                "vote_average": movie_rating
                
            }
        else:
            print(f"Error fetching similar movies for movie ID {movie_id}: {similar_response.status_code}")

    if response.status_code == 200:
        
        data = response.json()
        movie = movie_id
        print(f"The movie you chose is: {movie_title}")
        print(f"Similar movies to {movie_title}:")
        for movie in data['results']:
            print(f"* {movie['title']} (ID: {movie['id']}) Rating:{movie['vote_average']}")
    else:
        print(f"Error: {response.status_code}")

    return movie_similarity_data


if __name__ == "__main__":
    """
    This part of the code runs the main function and builds a graph with the data collected
    
    Parameters
    ----------
    collected data: dict
        data collected from the main function about movie titles and ids
    """
    print("Finding similar movies")

    # Run the async function and get the result
    collected_data = asyncio.run(main())

    # This is where the collected data is availible

    # Build the NetworkX graph
    graph = nx.Graph()

    for movie_id, data in collected_data.items():
        title = data['title']
        graph.add_node(movie_id, title=title)

        for sim in data['similar_movies']:
            sim_id = sim['id']
            sim_title = sim['title']

            if not graph.has_node(sim_id):
                graph.add_node(sim_id, title=sim_title)

            # You can add weights later if you want (e.g., similarity score)
            graph.add_edge(movie_id, sim_id)

    print(f"\nGraph of all the recommended movies:")
    print(f"Number of nodes: {graph.number_of_nodes()}")
    print(f"Number of edges: {graph.number_of_edges()}")

    # Visualize
    plt.figure(figsize=(16, 12))
    pos = nx.spring_layout(graph, k=0.5, iterations=50)  # better layout

    nx.draw_networkx(
        graph,
        pos=pos,
        with_labels=True,
        labels={n: f"{n}\n{d['title']}" for n, d in graph.nodes(data=True)},
        node_size=2000,
        node_color='red',
        font_size=9,
        font_weight='light',
        edge_color='gray',
        alpha=0.9
    )

    plt.title('Movie Similarity Network (TMDB Similar Movies)', size=18)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


.. automodule:: moVstudiocode
   :members: Katherine, Semcneil
   :undoc-members:
   :show-inheritance:

.. toctree::
   :maxdepth: 2
   :caption: Contents:


