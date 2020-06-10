from urllib.request import Request, urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from pythons.color_print import *
from pprint import pprint

# returns text in yellow
def yellowfy(string: str):
    return '\033[93m' + str(string) + '\033[0m'


# wrapper for urllib.urlopen
def my_urlopen(url: str):
    return urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read()


# my_urlopen but for gamepedia
# this does not work if url contains weird characters
def gamepedia(hero: str):
    return urlopen(Request('https://feheroes.gamepedia.com/' + quote(hero.replace('\n', '')))).read()


# returns 170 if the hero has access to a Duel skill
def has_duel_bst(wp_type: str, mv_type: str):
    return 170 if 'Infantry' in mv_type or ('Flying' in mv_type and 'Colorless' not in wp_type) else 0


# returns the main trait of the hero
def trait_finder(hero):
    traits = ['Duo', 'Legend', 'Grail', 'Season', 'Five']
    for trait in traits:
        if hero[trait]:
            return trait
    return 'Four'


# well, prints hero's info
def print_hero_info(hero):
    table = PrettyTable(['Name', 'Weapon', 'Move', 'BST', 'PRF', 'Assist', 'Special', 'A', 'B', 'C', 'Trait'])

    trait = trait_finder(hero)
    table.add_row([yellowfy(hero['Name']), yellowfy(hero['WeaponType']), yellowfy(hero['MoveType']),
                  yellowfy(hero['BST']), yellowfy(hero['PRF']), yellowfy(hero['Assist']), yellowfy(hero['Special']),
                  yellowfy(hero['A']), yellowfy(hero['B']), yellowfy(hero['C']), yellowfy(trait)])

    print(table)


# extracts the costs of heroes passives and returns them in a list
def passive_cost_extractor(row_list: list):
    costs = {'A': 0, 'B': 0, 'C': 0}

    skill_type_1 = row_list[1].find_all('th')[-1].string
    rowspan_1 = int(row_list[1].find_all('th')[-1]['rowspan'])
    skill_cost_1 = int(row_list[rowspan_1].find_all('td')[3].string)

    costs[skill_type_1] = skill_cost_1

    skill_type_2 = row_list[1+rowspan_1].find_all('th')[-1].string
    rowspan_2 = int(row_list[1+rowspan_1].find_all('th')[-1]['rowspan'])
    skill_cost_2 = int(row_list[rowspan_1+rowspan_2].find_all('td')[3].string)
    costs[skill_type_2] = skill_cost_2

    try:
        skill_type_3 = row_list[1 + rowspan_1 + rowspan_2].find_all('th')[-1].string
        rowspan_3 = int(row_list[1 + rowspan_1 + rowspan_2].find_all('th')[-1]['rowspan'])

        skill_cost_3 = int(row_list[rowspan_1 + rowspan_2 + rowspan_3].find_all('td')[3].string)
        costs[skill_type_3] = skill_cost_3
    except IndexError:
        pass

    return [costs['A'], costs['B'], costs['C']]


# this function extracts the hero's data from gamepedia's page
def hero_web_hunter(hero_name: str):
    soup = BeautifulSoup(gamepedia(hero_name), 'html.parser')

    hero_table_rows = soup.find('table', {'class': 'wikitable hero-infobox'}).tbody.find_all('tr')
    legend, duo, grail, season, five = False, False, False, False, False
    prf, ass, spec, a, b, c = False, 0, 0, 0, 0, 0
    wp_type, mv_type = "", ""
    duel_bst = 0

    name = hero_name.replace('\n', '')

    # remove the alts table because it messes up with the rest of the code
    tables = soup.find_all('table')
    if "You may be looking for:" in str(tables[0]):
        tables.remove(tables[0])
    tables.remove(tables[-1])


    # sum all of the middle values in the stas columns
    bst = sum([int(x.split('/')[1]) for x in [td.string for td in tables[3].tbody.find_all('tr')[-1]][1:-1]])

    for row in hero_table_rows:
        wp_type = row.td.a.string if 'Weapon Type' in str(row) else wp_type
        mv_type = row.td.a.string if 'Move Type' in str(row) else mv_type
        duo = duo or 'Duo' in str(row)
        legend = legend or 'Legendary</a>' in str(row)
        grail = grail or 'Grand Hero Battle' in str(row) or 'Tempest Trials' in str(row)
        season = season or 'Special</a>' in str(row)
        five = five or ('4<img alt="★"' not in str(row) and '5<img alt="★"' in str(
            row)) and not duo and not season and not legend

        duel_bst = max(duel_bst,
                       [int(s) for s in str(row).split() if s.isdigit()][1] if 'Standard Effect 1: Duel' in str(
                           row) else 0, has_duel_bst(wp_type, mv_type))

    # cleaning
    wp_type = wp_type.replace('Sword', 'Red Sword').replace('Lance', 'Blue Lance') \
                     .replace('Axe', 'Green Axe').replace('Staff', 'Colorless Staff')

    # Might = Weapon, Range = Assist, Cooldown = Special, Type = Passives
    for table in tables:
        if 'Might' in str(table.tbody.tr) and 'Range' in str(table.tbody.tr):
            prf = '400' in str(table.tbody.find_all('tr')[-1])

        if 'Range' in str(table.tbody.tr) and 'Might' not in str(table.tbody.tr):
            ass = int(table.tbody.find_all('tr')[-1].find_all('td')[3].string)

        if 'Cooldown' in str(table.tbody.tr):
            spec = int(table.tbody.find_all('tr')[-1].find_all('td')[3].string)

        if 'Type' in str(table.tbody.tr):
            a, b, c = passive_cost_extractor(table.find_all('tr'))

    return {'Name': name, 'WeaponType': wp_type, 'MoveType': mv_type, 'BST': bst, 'Duel_BST': duel_bst,
            'PRF': prf, 'Assist': ass, 'Special': spec, 'A': a, 'B': b, 'C': c,
            'Season': season, 'Legend': legend, 'Duo': duo, 'Grail': grail, 'Five': five}

    # print_hero_info(name, wp_type, mv_type, bst, duel_bst, prf, ass, spec, a, b, c, season, legend, duo, five, grail)