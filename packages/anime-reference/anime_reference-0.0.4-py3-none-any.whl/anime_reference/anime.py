from requests import get
from bs4 import BeautifulSoup
import pandas as pd 
try:
    from constants import *
    from utils import *
except:
    from anime_reference.constants import *
    from anime_reference.utils import *

def get_summary(title, episode_name):
    title_lower = title.lower()
    anime = anime_object(title_lower)
    try:
        return anime.summary(episode_name)
    except AttributeError:
        return None

def get_episode_names(title):
    title_lower = title.lower()
    anime = anime_object(title_lower)
    try:
        return anime.episode_names
    except AttributeError:
        return None
    
def get_episodes(title):
    title = title.lower()
    anime = anime_object(title)
    try:
        return anime.episodes
    except AttributeError:
        return None

def get_movie_names(title):
    return None

def get_movies(title):
    return None

def get_synopsis(title):
    return None

def get_anime_titles():
    return None
