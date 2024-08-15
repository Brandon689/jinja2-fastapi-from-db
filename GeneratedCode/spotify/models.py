from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class UsersBase(BaseModel):
    username: str
    email: str
    password_hash: str
    date_of_birth: datetime
    country: str
    premium_status: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    

class UsersCreate(UsersBase):
    pass

class Users(UsersBase):
    user_id: int

class ArtistsBase(BaseModel):
    name: str
    bio: Optional[str] = None
    country: Optional[str] = None
    formed_year: Optional[int] = None
    website: Optional[str] = None
    

class ArtistsCreate(ArtistsBase):
    pass

class Artists(ArtistsBase):
    artist_id: int

class AlbumsBase(BaseModel):
    title: str
    artist_id: int
    release_date: datetime
    genre: Optional[str] = None
    label: Optional[str] = None
    

class AlbumsCreate(AlbumsBase):
    pass

class Albums(AlbumsBase):
    album_id: int

class SongsBase(BaseModel):
    title: str
    album_id: Optional[int] = None
    duration: int
    track_number: Optional[int] = None
    explicit: bool
    lyrics: Optional[str] = None
    audio_file_path: str
    

class SongsCreate(SongsBase):
    pass

class Songs(SongsBase):
    song_id: int

class Song_artistsBase(BaseModel):
    artist_id: Optional[int] = None
    role: str
    

class Song_artistsCreate(Song_artistsBase):
    pass

class Song_artists(Song_artistsBase):
    song_id: int

class GenresBase(BaseModel):
    name: str
    

class GenresCreate(GenresBase):
    pass

class Genres(GenresBase):
    genre_id: int

class Song_genresBase(BaseModel):
    genre_id: Optional[int] = None
    

class Song_genresCreate(Song_genresBase):
    pass

class Song_genres(Song_genresBase):
    song_id: int

class PlaylistsBase(BaseModel):
    name: str
    user_id: int
    description: Optional[str] = None
    is_public: bool
    created_at: datetime
    updated_at: datetime
    

class PlaylistsCreate(PlaylistsBase):
    pass

class Playlists(PlaylistsBase):
    playlist_id: int

class Playlist_songsBase(BaseModel):
    song_id: Optional[int] = None
    position: int
    added_at: datetime
    

class Playlist_songsCreate(Playlist_songsBase):
    pass

class Playlist_songs(Playlist_songsBase):
    playlist_id: int

class User_libraryBase(BaseModel):
    item_type: str
    item_id: int
    added_at: datetime
    

class User_libraryCreate(User_libraryBase):
    pass

class User_library(User_libraryBase):
    user_id: int

class User_followersBase(BaseModel):
    followed_id: Optional[int] = None
    followed_at: datetime
    

class User_followersCreate(User_followersBase):
    pass

class User_followers(User_followersBase):
    follower_id: int

class Artist_followersBase(BaseModel):
    artist_id: Optional[int] = None
    followed_at: datetime
    

class Artist_followersCreate(Artist_followersBase):
    pass

class Artist_followers(Artist_followersBase):
    user_id: int

class Listening_historyBase(BaseModel):
    user_id: int
    song_id: int
    listened_at: datetime
    duration_listened: int
    

class Listening_historyCreate(Listening_historyBase):
    pass

class Listening_history(Listening_historyBase):
    history_id: int

class User_recommendationsBase(BaseModel):
    user_id: int
    item_type: str
    item_id: int
    score: float
    generated_at: datetime
    

class User_recommendationsCreate(User_recommendationsBase):
    pass

class User_recommendations(User_recommendationsBase):
    recommendation_id: int

class PodcastsBase(BaseModel):
    title: str
    description: Optional[str] = None
    publisher: str
    language: str
    rss_feed_url: str
    

class PodcastsCreate(PodcastsBase):
    pass

class Podcasts(PodcastsBase):
    podcast_id: int

class Podcast_episodesBase(BaseModel):
    podcast_id: int
    title: str
    description: Optional[str] = None
    duration: int
    release_date: datetime
    audio_file_path: str
    

class Podcast_episodesCreate(Podcast_episodesBase):
    pass

class Podcast_episodes(Podcast_episodesBase):
    episode_id: int

class Podcast_subscriptionsBase(BaseModel):
    podcast_id: Optional[int] = None
    subscribed_at: datetime
    

class Podcast_subscriptionsCreate(Podcast_subscriptionsBase):
    pass

class Podcast_subscriptions(Podcast_subscriptionsBase):
    user_id: int

class Song_ftsBase(BaseModel):
    title: Optional[str] = None
    artist_name: Optional[str] = None
    album_title: Optional[str] = None
    

class Song_ftsCreate(Song_ftsBase):
    pass

class Song_fts(Song_ftsBase):
    id: int

class Song_fts_dataBase(BaseModel):
    block: Optional[bytes] = None
    

class Song_fts_dataCreate(Song_fts_dataBase):
    pass

class Song_fts_data(Song_fts_dataBase):
    id: int

class Song_fts_idxBase(BaseModel):
    term: str
    pgno: Optional[str] = None
    

class Song_fts_idxCreate(Song_fts_idxBase):
    pass

class Song_fts_idx(Song_fts_idxBase):
    segid: int

class Song_fts_contentBase(BaseModel):
    c0: Optional[str] = None
    c1: Optional[str] = None
    c2: Optional[str] = None
    

class Song_fts_contentCreate(Song_fts_contentBase):
    pass

class Song_fts_content(Song_fts_contentBase):
    id: int

class Song_fts_docsizeBase(BaseModel):
    sz: Optional[bytes] = None
    

class Song_fts_docsizeCreate(Song_fts_docsizeBase):
    pass

class Song_fts_docsize(Song_fts_docsizeBase):
    id: int

class Song_fts_configBase(BaseModel):
    v: Optional[str] = None
    

class Song_fts_configCreate(Song_fts_configBase):
    pass

class Song_fts_config(Song_fts_configBase):
    k: int

