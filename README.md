# Movie Recommender System

A small content-based movie recommender built from the TMDB 5000 movie metadata dataset. The project includes a Gradio web app and the notebook used to prepare the movie data and calculate movie similarity.

## How it works

The notebook combines each movie's overview, genres, keywords, first three cast members, and director into a text field. It stems the words, creates a bag-of-words representation with `CountVectorizer` (up to 5,000 features, excluding English stop words), then calculates pairwise cosine similarity. Given a selected title, the app returns the five most similar movies and attempts to retrieve their posters from TMDB.

## Project files

- `app.py` — Gradio interface, recommendation lookup, and poster requests.
- `movir_recomender_system.ipynb` — data preparation and similarity-generation workflow.
- `movie_dict.pkl` — serialized movie table used by the app.
- `similarity.pkl` — serialized pairwise similarity matrix required by the app. This file is not currently present in the repository, so the app will not start until it is generated (see below).
- `requirements.txt` — dependencies for the web app.

## Requirements

- Python 3.9 or newer
- Packages listed in `requirements.txt`
- A TMDB API key for poster lookup (optional; poster requests use a built-in fallback key if `TMDB_API_KEY` is unset, and unavailable posters show a placeholder)

Install the app dependencies in a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Generate the similarity data

The notebook downloads the TMDB 5000 dataset through KaggleHub and writes `movie_dict.pkl` and `similarity.pkl` in its current working directory. To reproduce those files, install the notebook's additional dependencies and run the notebook from the project directory:

```bash
python -m pip install kagglehub nltk scikit-learn jupyter
jupyter notebook movir_recomender_system.ipynb
```

Run the notebook cells in order through the final serialization cells. KaggleHub may require Kaggle access/configuration to download the dataset. Ensure the generated `similarity.pkl` is next to `app.py`; it must use the same movie ordering as `movie_dict.pkl`.

## Run the app

Set `TMDB_API_KEY` to your own TMDB API key to use poster lookup, then start the server:

```bash
export TMDB_API_KEY="your-tmdb-api-key"
python app.py
```

Open <http://localhost:7860>. The app binds to `0.0.0.0`; set `PORT` to change its listening port, for example `PORT=8000 python app.py`.

## Recommendation and poster behavior

The selected movie is matched by title, its similarity scores are sorted, and the highest-scoring result is skipped because it is the selected movie itself. The next five titles are returned. Poster images are fetched from TMDB's movie endpoint and displayed from its image CDN. If a request fails or the movie has no poster path, the app displays a placeholder image.

## Notes

- The similarity matrix is dense and covers the full movie collection; it can consume substantial memory when regenerated.
- `movie_dict.pkl` and `similarity.pkl` are Python pickle files. Only load pickle files from sources you trust.
- The dataset and poster metadata are provided by TMDB; follow their applicable terms when using or redistributing them.
