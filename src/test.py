import asyncio
import json
import nest_asyncio
import requests
import networkx as nx
import matplotlib.pyplot as plt
#Run "pip3 install nest_asyncio" in the terminal to install nest_asyncio 
nest_asyncio.apply()

# === Your existing main() and other functions here ===
async def main(movie_ids_to_query):
    api_key = "4ec39598d34ba6c46351241dcf930713"
    movie_similarity_data = {}

    for movie_id in movie_ids_to_query:
        # Fetch movie title
        movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {'api_key': api_key, 'language': 'en-US'}
        details_response = requests.get(movie_details_url, params=params)
        
        movie_title = "Unknown"
        if details_response.status_code == 200:
            movie_details = details_response.json()
            movie_title = movie_details.get('title', 'Unknown')
        else:
            print(f"Error fetching details for movie ID {movie_id}: {details_response.status_code}")
            continue

        # Fetch similar movies
        similar_movies_url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar"
        similar_response = requests.get(similar_movies_url, params=params)

        if similar_response.status_code == 200:
            data = similar_response.json()
            similar_movies_list = [
                {'id': m['id'], 'title': m['title']} for m in data['results']
                #(f"* m['title']} (ID: {m['id']})")
                #(f"* {movie['title']} (ID: {movie['id']})")
            ]
            movie_similarity_data[movie_id] = {
                "title": movie_title,
                "similar_movies": similar_movies_list
                
            }
        else:
            print(f"Error fetching similar movies for movie ID {movie_id}: {similar_response.status_code}")

    return movie_similarity_data


async def run_analysis():
    print("Fetching recommended movies based on your liked films...\n")

    movie_ids_to_query = [777] #the movie you want to use
    collected_data = await main(movie_ids_to_query)
   
    
    print("\nCollected Movie Similarity Data:")
    #print(f'{json.dumps(collected_data)}', end='\n')
    for movie_ids_to_query in collected_data:
        #print(json.dumps(collected_data, indent=0))
        print(json.dumps(collected_data, indent=0))

    return collected_data  # ← Important: return it!


if __name__ == "__main__":
    # Run the async function and get the result
    collected_data = asyncio.run(run_analysis())

    # -----------------------------
    # This is where the collected data is availible
    # -----------------------------

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

    print(f"\nGraph built!")
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