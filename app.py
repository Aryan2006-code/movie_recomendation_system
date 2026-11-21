from pathlib import Path
import os
import pickle

import gradio as gr
import pandas as pd
import requests

BASE_DIR = Path(__file__).resolve().parent

with (BASE_DIR / "movie_dict.pkl").open("rb") as file:
    movies = pd.DataFrame(pickle.load(file))

with (BASE_DIR / "similarity.pkl").open("rb") as file:
    similarity = pickle.load(file)

movie_titles = movies["title"].tolist()

def fetch_poster(movie_id):
    """Return a TMDB poster URL, or a visible fallback when one is unavailable."""
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}",
            params={
                "api_key": os.environ.get(
                    "TMDB_API_KEY", "8265bd1679663a7ea12ac168da84d2e8"
                ),
                "language": "en-US",
            },
            timeout=10,
        )
        response.raise_for_status()
        poster_path = response.json().get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except (requests.RequestException, ValueError):
        pass

    return "https://placehold.co/500x750?text=Poster+Unavailable"

def recommend(movie: str):
    if not movie:
        return []

    movie_index = movies.index[movies["title"] == movie][0]
    distances = similarity[movie_index]

    nearest_movies = sorted(
        enumerate(distances), key=lambda item: item[1], reverse=True
    )[1:6]
    recommendations = []

    for movie_index, _ in nearest_movies:
        recommended_movie = movies.iloc[movie_index]
        movie_id = recommended_movie["movie_id"]
        title = recommended_movie["title"]
        recommendations.append((fetch_poster(movie_id), title))
    return recommendations


with gr.Blocks(title="Movie Recommender System") as demo:
    gr.Markdown("# Movie Recommender System")
    gr.Markdown("Choose a movie to get five recommendations with posters.")

    movie_input = gr.Dropdown(
        choices=movie_titles,
        label="Choose a movie",
        value=movie_titles[0] if movie_titles else None,
    )
    recommend_button = gr.Button("Recommend", variant="primary")
    recommendations = gr.Gallery(
        label="Recommended movies",
        columns=5,
        rows=1,
        object_fit="contain",
        height=360,
    )

    recommend_button.click(recommend, inputs=movie_input, outputs=recommendations)


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", "7860")),
    )
