from requests import get
from bs4 import BeautifulSoup
import pandas as pd
try:
    from constants import *
    from utils import clean_str_list, format_episode_links, clean_text
except:
    from anime_reference.constants import *
    from anime_reference.utils import clean_str_list, format_episode_links, clean_text
    
class Naruto:
    def __init__(self, title):
        self.title = title
        self._check_title()
        return None

    def _check_title(self):
        if self.title not in NARUTO.keys():
            print(f"Anime \"{title}\" is not a valid anime title.")
            # TODO: Add a helper function that asks "Did you mean (title)?"
            return None
        
    def _check_episode_name(self, episode_name):
        if episode_name not in self.episode_names:
            print(f"Episode \"{episode_name}\" is not a valid {self.title} episode name.")
            # TODO: Add a helper function that asks "Did you mean (episode name)?"
            return None
        
    def _get_link(self):
        return NARUTO[self.title]

    @property
    def _episode_link_dict(self):
        link = self._get_link() # link for the all epsiodes of the different naruto shows
        response = get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = list(map(str, soup.find_all('a')))
            if self.title == "naruto":
                start_index = links.index('<a href="/wiki/Enter:_Naruto_Uzumaki!" title="Enter: Naruto Uzumaki!">Enter: Naruto Uzumaki!</a>')
                end_index = links.index('<a href="/wiki/Departure_(episode)" title="Departure (episode)">Departure </a>')
                links = links[start_index:end_index+1]
                links = format_episode_links("https://naruto.fandom.com", links)
                return dict(zip(self.episode_names, links))
            elif self.title == "naruto shippuden":
                start_index = links.index('<a href="/wiki/Homecoming_(episode)" title="Homecoming (episode)">Homecoming </a>')
                end_index = links.index('<a href="/wiki/The_Message" title="The Message">The Message</a>')
                links = links[start_index:end_index+1]
                links = format_episode_links("https://naruto.fandom.com", links)
                return dict(zip(self.episode_names, links))
            elif self.title == "boruto":
                start_index = links.index('<a href="/wiki/Boruto_Uzumaki!!_(episode)" title="Boruto Uzumaki!! (episode)">Boruto Uzumaki!! </a>')
                end_index = links.index('<a href="/wiki/Becoming_a_Student" title="Becoming a Student">Becoming a Student</a>')
                links = links[start_index:end_index+1]
                links = format_episode_links("https://naruto.fandom.com", links)
                return dict(zip(self.episode_names, links))
        else:
            print(f"Bad response, status code: {response.status_code}")
            return None

    def _get_episode_link(self, episode_name):
        self._check_episode_name(episode_name)
        try:
            return self._episode_link_dict[episode_name]
        except KeyError:
            return None
    
    def get_episodes(self):
        link = self._get_link()
        try:
            response = get(link)
        except:
            return None
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table')
            if self.title == "naruto":
                df = pd.read_html(str(tables))[0]
            elif self.title == "naruto shippuden":
                df = pd.read_html(str(tables))[1]
            elif self.title == "boruto":
                df = pd.read_html(str(tables))[2]
            return df
        else:
            print(f"Bad response, status code: {response.status_code}")
            return None
   
    def summary(self, episode_name):
        link = self._get_episode_link(episode_name)
        try:
            response = get(link)
        except:
            return None
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            texts = clean_text(str(soup.find_all('p')))
            return texts
        else:
            print(f"Bad response, status code: {response.status_code}")
            return None
    
    @property
    def episode_names(self):
        return clean_str_list(list(self.get_episodes()['Episode Title']))

    @property
    def episodes(self):
        return len(self.get_episodes())
