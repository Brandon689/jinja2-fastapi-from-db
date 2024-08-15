from fastapi import FastAPI
from database import DB_NAME
from routers import users
from routers import artists
from routers import albums
from routers import songs
from routers import song_artists
from routers import genres
from routers import song_genres
from routers import playlists
from routers import playlist_songs
from routers import user_library
from routers import user_followers
from routers import artist_followers
from routers import listening_history
from routers import user_recommendations
from routers import podcasts
from routers import podcast_episodes
from routers import podcast_subscriptions
from routers import song_fts
from routers import song_fts_data
from routers import song_fts_idx
from routers import song_fts_content
from routers import song_fts_docsize
from routers import song_fts_config

app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(artists.router)
app.include_router(albums.router)
app.include_router(songs.router)
app.include_router(song_artists.router)
app.include_router(genres.router)
app.include_router(song_genres.router)
app.include_router(playlists.router)
app.include_router(playlist_songs.router)
app.include_router(user_library.router)
app.include_router(user_followers.router)
app.include_router(artist_followers.router)
app.include_router(listening_history.router)
app.include_router(user_recommendations.router)
app.include_router(podcasts.router)
app.include_router(podcast_episodes.router)
app.include_router(podcast_subscriptions.router)
app.include_router(song_fts.router)
app.include_router(song_fts_data.router)
app.include_router(song_fts_idx.router)
app.include_router(song_fts_content.router)
app.include_router(song_fts_docsize.router)
app.include_router(song_fts_config.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)