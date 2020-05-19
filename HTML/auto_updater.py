from urllib.request import Request, urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from pprint import pprint

# wrapper for urllib.urlopen
def my_urlopen(url: str):
    return urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read()

def gamepedia(hero: str):
    return urlopen(Request('https://feheroes.gamepedia.com/' + quote(hero))).read()


# get heroes list from file newheroes.txt
with open('./HTML/newheroes.txt') as data_file:
    heroes_list = data_file.readlines()


# TODO for each hero
# name wp_type mv_type bst duel_bst grail prf ass spec a b c season legend duo five
# xxxx
for hero in heroes_list:
    # TODO for each hero

    # name wp_type mv_type bst duel_bst grail prf ass spec a b c season legend duo five
    soup = BeautifulSoup(gamepedia(hero), 'html.parser')

    name = hero
    hero_table_rows = soup.find('table', {'class': 'wikitable hero-infobox'}).tbody.find_all('tr')

    #pprint(hero_table_rows)

    wp_type = ""
    for row in hero_table_rows:
        wp_type = row if 'Weapon Type' in str(row) else 0
        print(wp_type)

    #pprint(wp_type)


#soup = BeautifulSoup(gamepress(heroes_hrefs[0]), 'html.parser')

#soup = BeautifulSoup(my_urlopen('https://gamepress.gg/feheroes/hero/legendary-chrom'), 'html.parser')

# name = soup.find('table', {'id': 'hero-details-table'}).tr.th.find('span').string.split(' ')[-1] + soup.find('table', {'id': 'hero-details-table'}).tr.th.find_all('span')[1].string.replace(' - ', ': ')
# mv_type = soup.find('div', {'class': 'taxonomy-term vocabulary-movement'}).h2.a.div.string
# wp_type = soup.find('div', {'class': 'taxonomy-term vocabulary-attribute'}).h2.a.div.string
# bst = int(soup.find_all('span', {'class': 'max-stats-number'})[0].string)
# prf = '400' in soup.find_all('div', {'id': 'weapon-skills'})[0].tbody.find_all('tr')[-1].find_all('td')[1].string
#
# try:
#     ass = int(soup.find_all('div', {'id': 'command-skills'})[0].tbody.find_all('tr')[-1].find_all('td')[2].string)
# except IndexError:
#     ass = 0
#
# try:
#     spec = int(soup.find_all('div', {'id': 'special-skills'})[0].tbody.find_all('tr')[-1].find_all('td')[1].string)
# except IndexError:
#     spec = 0
#
# a, b, c = 0, 0, 0
# passive_rows = soup.find('div', {'id': 'passive-skills'}).div.div.div.table.tbody.find_all('tr')
# for row in passive_rows:
#     tds = row.find_all('td')
#     pprint(tds[1])
#     a = int(tds[1].string) if 'A' in tds[2].div.string else a
#     b = int(tds[1].string) if 'B' in tds[2].div.string else b
#     c = int(tds[1].string) if 'C' in tds[2].div.string else c
#
# pprint(a)
# print(b)
# print(c)









#GAMEPRESS DATA IS FUCKING WRONG, DONT USE IT PLS