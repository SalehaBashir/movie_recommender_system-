import streamlit as st
import pickle
import requests

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

API_KEY = "b307b2d36534fe19511cb28eab03360f"

# ---------- API Helpers ----------
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    return response.json()

def fetch_cast(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()
    return data.get('cast', [])[:5]

def poster_url(poster_path):
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/500x750?text=No+Poster"

def profile_url(profile_path):
    if profile_path:
        return f"https://image.tmdb.org/t/p/w200{profile_path}"
    return "https://via.placeholder.com/200x200?text=No+Photo"

# ---------- Recommendation Logic ----------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    source_genres = set(movies.iloc[movie_index].genres_list)

    results = []
    for i in movies_list:
        row = movies.iloc[i[0]]
        details = fetch_movie_details(row.movie_id)
        shared = source_genres.intersection(set(row.genres_list))
        reason = "Shares genres: " + ", ".join(list(shared)[:2]) if shared else "Similar theme & story"
        results.append({
            "title": row.title,
            "movie_id": row.movie_id,
            "poster": poster_url(details.get('poster_path')),
            "reason": reason
        })
    return results

# ---------- Page Setup ----------
st.set_page_config(page_title="Movie Recommender", layout="wide")

if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = movies['title'].values[0]

def go_to_detail(title):
    st.session_state.selected_movie = title
    st.session_state.view = 'detail'
    st.rerun()

def go_home():
    st.session_state.view = 'home'
    st.rerun()

# ---------- HOME VIEW ----------
if st.session_state.view == 'home':
    st.title("🎬 Movie Recommender System")
    st.write("Select a movie and get 5 similar recommendations.")

    selected_movie = st.selectbox("Choose a movie:", movies['title'].values)

    if st.button("Recommend"):
        st.session_state.selected_movie = selected_movie

    results = recommend(st.session_state.selected_movie)

    cols = st.columns(5)
    for col, r in zip(cols, results):
        with col:
            st.image(r['poster'], width='stretch')
            st.caption(r['title'])
            st.markdown(f"<span style='font-size:12px; color:gray;'>{r['reason']}</span>", unsafe_allow_html=True)
            if st.button("View details", key=r['title']):
                go_to_detail(r['title'])

# ---------- DETAIL VIEW ----------
elif st.session_state.view == 'detail':
    movie_title = st.session_state.selected_movie
    movie_row = movies[movies['title'] == movie_title].iloc[0]
    movie_id = movie_row.movie_id

    details = fetch_movie_details(movie_id)
    cast = fetch_cast(movie_id)

    if st.button("← Back"):
        go_home()

    left, right = st.columns([1, 2])

    with left:
        st.image(poster_url(details.get('poster_path')), width='stretch')

    with right:
        st.markdown(f"## {details.get('title', movie_title)}")
        st.markdown(f"⭐ **{details.get('vote_average', 'N/A')}** / 10  |  🕒 {details.get('runtime', 'N/A')} min  |  📅 {details.get('release_date', 'N/A')}")
        genres = ", ".join([g['name'] for g in details.get('genres', [])])
        st.markdown(f"**Genres:** {genres}")

        st.markdown("### Synopsis")
        st.write(details.get('overview', 'No synopsis available.'))

        st.markdown("### Cast")
        cast_cols = st.columns(5)
        for c_col, person in zip(cast_cols, cast):
            with c_col:
                st.image(profile_url(person.get('profile_path')), width='stretch')
                st.caption(person.get('name', ''))

    st.markdown("---")
    st.markdown("### More Like This")

    results = recommend(movie_title)
    cols = st.columns(5)
    for col, r in zip(cols, results):
        with col:
            st.image(r['poster'], width='stretch')
            st.caption(r['title'])
            if st.button("View details", key=f"more_{r['title']}"):
                go_to_detail(r['title'])