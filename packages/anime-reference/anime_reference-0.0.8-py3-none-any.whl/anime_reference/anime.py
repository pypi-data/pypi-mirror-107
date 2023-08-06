try:
    from anime_reference.Naruto import Naruto
    from anime_reference.constants import *
except:
    from Naruto import Naruto
    from constants import *

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

def anime_object(title):
    if title in NARUTO.keys():
        return Naruto(title)
    else:
        print(f"Title {title} is not a valid title.")
        return None
if __name__ == "__main__":
    print(get_summary("naruto", "Enter: Naruto Uzumaki!"))
    print(get_episodes("naruto"))
    print(get_episode_names("naruto"))
