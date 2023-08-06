from re import search
try:
    from constants import *
    from Naruto import *
except:
    from anime_reference.constants import *
    from anime_reference.Naruto import *

def anime_object(title):
    if title in NARUTO.keys():
        return Naruto(title)
    else:
        print(f"Title {title} is not a valid title.")
        return None
    
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
