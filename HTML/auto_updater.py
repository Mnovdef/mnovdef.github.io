from urllib.request import Request, urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from pprint import pprint

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


# well, prints hero's info
def print_hero_info(name, wp_type, mv_type, bst, duel_bst, prf, ass, spec, a, b, c, season, legend, duo, five, grail):
    print('name: {}'.format(name))
    print('wp_type: {}'.format(wp_type))
    print('mv_type: {}'.format(mv_type))
    print('bst: {}'.format(bst))
    print('duel_bst: {}'.format(duel_bst))
    print('prf: {}'.format(prf))
    print('ass: {}'.format(ass))
    print('spec: {}'.format(spec))
    print('a: {}'.format(a))
    print('b: {}'.format(b))
    print('c: {}'.format(c))
    print('duo: {}'.format(duo))
    print('legend: {}'.format(legend))
    print('grail: {}'.format(grail))
    print('season: {}'.format(season))
    print('five: {}'.format(five))
    print()


# extracts the costs of heroes passives and returns them in a list
def passive_cost_extractor(row_list: list):
    costs = {'A': 0, 'B': 0, 'C': 0}

    skill_type_1 = row_list[1].find_all('td')[-1].string
    rowspan_1 = int(row_list[1].find_all('td')[-1]['rowspan'])
    skill_cost_1 = int(row_list[rowspan_1].find_all('td')[3].string)

    costs[skill_type_1] = skill_cost_1

    skill_type_2 = row_list[1+rowspan_1].find_all('td')[-1].string
    rowspan_2 = int(row_list[1+rowspan_1].find_all('td')[-1]['rowspan'])
    skill_cost_2 = int(row_list[rowspan_1+rowspan_2].find_all('td')[3].string)
    costs[skill_type_2] = skill_cost_2

    try:
        skill_type_3 = row_list[1 + rowspan_1 + rowspan_2].find_all('td')[-1].string
        rowspan_3 = int(row_list[1 + rowspan_1 + rowspan_2].find_all('td')[-1]['rowspan'])

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
    bst = sum(
        [int(x.split('/')[1]) for x in [td.string for td in soup.find_all('table')[4].tbody.find_all('tr')[-1]][1:-1]])

    for row in hero_table_rows:
        wp_type = row.td.a.string if 'Weapon Type' in str(row) else wp_type
        mv_type = row.td.a.string if 'Move Type' in str(row) else mv_type
        duo = duo or 'Duo' in str(row)
        legend = legend or 'Legendary' in str(row)
        grail = grail or 'Grand Hero Battle' in str(row) or 'Tempest Trials' in str(row)
        season = season or 'Focus —' in str(row) and not duo and not legend
        five = five or ('4<img alt="★"' not in str(row) and '5<img alt="★"' in str(
            row)) and not duo and not season and not legend

        duel_bst = max(duel_bst,
                       [int(s) for s in str(row).split() if s.isdigit()][1] if 'Standard Effect 1: Duel' in str(
                           row) else 0, has_duel_bst(wp_type, mv_type))

    # cleaning
    wp_type = wp_type.replace('Sword', 'Red Sword').replace('Lance', 'Blue Lance') \
        .replace('Axe', 'Green Axe').replace('Staff', 'Colorless Staff')

    # Might = Weapon, Range = Assist, Cooldown = Special, Type = Passives
    tables = soup.find_all('table', {'class': 'wikitable default unsortable skills-table'})
    for table in tables:
        if 'Might' in table.tbody.tr.find_all('th')[1].string:
            prf = '400' in str(table.tbody.find_all('tr')[-1])

        if 'Range' in table.tbody.tr.find_all('th')[1].string:
            ass = int(table.tbody.find_all('tr')[-1].find_all('td')[3].string)

        if 'Cooldown' in table.tbody.tr.find_all('th')[1].string:
            spec = int(table.tbody.find_all('tr')[-1].find_all('td')[3].string)

        if 'Type' in table.tbody.tr.find_all('th')[-1].string:
            a, b, c = passive_cost_extractor(table.find_all('tr'))

    return [name, wp_type, mv_type, bst, duel_bst, grail, prf, ass, spec, a, b, c, season, legend, duo, five]

    # print_hero_info(name, wp_type, mv_type, bst, duel_bst, prf, ass, spec, a, b, c, season, legend, duo, five, grail)
