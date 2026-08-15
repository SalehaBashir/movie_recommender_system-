# Movie Recommender System

This is a content-based movie recommendation app I built while learning ML — you pick a movie and it suggests 5 similar ones based on genre, cast, and plot similarity.

I followed a tutorial to learn the core approach (vectorizing movie tags and using cosine similarity), but wanted to actually build something usable instead of just running it in a notebook, so I added:

- Real posters and movie info pulled from TMDB instead of just printing titles
- A note on each recommendation showing why it was picked (shared genres)
- A proper page for each movie with synopsis, cast, rating etc.
- The ability to click into a recommended movie and keep browsing from there

## How it works

The dataset (TMDB 5000 movies) gets cleaned up and each movie's genres, cast, keywords, and overview get combined into one text field. That gets vectorized and compared using cosine similarity, so movies with similar "tags" end up close to each other. When you pick a movie, it just returns the 5 closest ones.

Posters, ratings, and cast details aren't stored anywhere — they're fetched from TMDB every time so the info stays current.

## Stack

Python + Pandas + scikit-learn for the ML part, Streamlit for the frontend, TMDB API for movie data.

One annoying bit: the similarity matrix ended up being 176MB, way over GitHub's file limit, so it's hosted on Google Drive and the app downloads it automatically the first time it runs.

## Running it

```bash
git clone https://github.com/SalehaBashir/movie_recommender_system-.git
cd movie_recommender_system-
pip install -r requirements.txt
streamlit run app.py
```

You'll need a free TMDB API key from themoviedb.org/settings/api, add it in app.py.

First run will take a bit longer since it has to pull similarity.pkl from Drive.

## Live demo

https://q9tpkmnfatp3hfkbayafba.streamlit.app