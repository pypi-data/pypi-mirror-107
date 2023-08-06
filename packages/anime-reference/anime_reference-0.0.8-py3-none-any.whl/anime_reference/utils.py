from re import search
from bs4 import BeautifulSoup

def clean_str_list(str_list):
    clean_list = []
    for string in str_list:
        result = search('"(.*)"', string)
        clean_list.append(result.group(1).strip())
    return clean_list

def format_episode_links(prefix_url, links):
    return [prefix_url+search('a href="(.*)" ', string).group(1) for string in links]

def clean_text(text):
    text = search(" <p>(.*)\n</p>", text).group(1)
    text = text.replace("<p>", "")
    text = text.replace("</p>", "")
    text = text.replace("  ", " ")
    text = text.replace(".,", ".")
    text = str(text).replace("\\", "")
    soup = BeautifulSoup(text, "html.parser")
    tags = list(map(str, soup.find_all("a")))
    for tag in tags:
        result = search('title="(.*)"', tag)
        text = text.replace(tag, result.group(1))
    return text
