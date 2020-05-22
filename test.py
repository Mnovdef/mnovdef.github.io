from bs4 import BeautifulSoup

# removes weird characters from heroes name to create path to image
def clean_hero_name(hero_name: str):
    return hero_name.replace(':', '').replace(' ', '_').replace("'", '')\
                    .replace('ç', 'c').replace('"', '').replace('í', 'i')\
                    .replace('á', 'a').replace('é', 'e')


# creates html tag
def create_tag(hero):
    name = hero['Name']
    soup = BeautifulSoup('', 'html.parser')
    path = 'HTML/assets/45px-' + clean_hero_name(name) + '_Face_FC.webp.png'
    tag = soup.new_tag('img', title=name, alt=name, src=path, decoding="async", width="40", height="40")

    tag_strings = ['data-duo', 'data-legend', 'data-grail', 'data-season', 'data-five']
    hero_params = [hero['Duo'], hero['Legendary'], hero['Grail'], hero['Season'], hero['Five']]

    for attribute, bool_value in dict(zip(tag_strings, hero_params)).items():
        if bool_value:
            tag[attribute] = 'true'

    if True not in hero_params:
        tag['data-four'] = 'true'

    tag['data-move'] = hero['MoveType']
    return tag



hero = {'Duo': False, 'Legendary': False, 'Grail': False, 'Season': False, 'Five':False, 'Name': 'Pietro', 'MoveType': 'A Piedi'}

print(create_tag(hero))
