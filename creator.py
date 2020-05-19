import math
from pprint import pprint
from bs4 import BeautifulSoup
import urllib.request


# manually asks for parameters to create a new hero object
# called by manually_add_heroes
def manual_create_hero():
    name = input("Hero Name and Epithet: ")
    wp_type = input("(Red, Blue, Green, Colorless) (Sword/Axe/Lance/Staff, Tome, Breath, Beast, Dagger, Bow)\n"
                    "Weapon type: ")
    mv_type = input('(Infantry, Flying, Armored, Cavalry)\n'
                    'Movement type: ')
    bst = int(input("BST: "))
    duel_bst = int(input("Duel BST: "))

    print("\nPress enter to say False, write anything to say True")
    if bool(input("Duo? ")):
        duo = True
        legend, grail, season, five = False, False, False, False
    elif bool(input("Legendary? ")):
        legend = True
        duo, grail, season, five = False, False, False, False
    elif bool(input('Grail unit? ')):
        grail = True
        duo, legend, season, five = False, False, False, False
    elif bool(input("Seasonal? ")):
        season = True
        duo, legend, grail, five = False, False, False, False
    elif bool(input("Five star exclusive? ")):
        five = True
        duo, legend, grail, season = False, False, False, False
    else:
        duo, legend, grail, season, five = False, False, False, False, False

    prf = bool(input("Does it have a PRF? "))
    ass = int(input("Assist Cost: "))
    spec = int(input("Special Cost: "))
    a = int(input("A Skill Cost: "))
    b = int(input("B Skill Cost: "))
    c = int(input("C Skill Cost: "))

    return create_max_hero(name, wp_type, mv_type, bst, duel_bst, grail, prf, ass, spec, a, b, c, season, legend, duo, five)


# create a hero object with his max arena setup
def create_max_hero(name: str, wp_type: str, mv_type: str, bst: int, duel_bst: int, grail: int,
                    prf: bool, ass: int, spec: int, a: int, b: int, c: int,
                    season: bool, legend: bool, duo: bool, five: bool):
    healer = wp_type == 'Colorless Staff'
    mv_bst = 170 * ('Infantry' in mv_type or 'Flying' in mv_type)
    hero = {'Name': name, 'WeaponType': wp_type, 'MoveType': mv_type, 'BST': max(bst+3+(not grail), duel_bst, mv_bst),
            'Weapon': 350 + 50*prf, 'Assist': max(400-100*healer, ass), 'Special': max(500-200*healer, spec),
            'A': max(300, a), 'B': max (240, b), 'C': max(300, c),
            'Grail': grail, 'Seasonal': season, 'Legendary': legend, 'Duo': duo, 'FiveStar': five}
    return hero


# formula to calculate arena score for each unit
def score_calc(hero):
    sp_total = hero['Weapon'] + hero['Assist'] + hero['Special'] + hero['A'] + hero['B'] + hero['C'] + 240
    score = (148 + 20 + math.floor(hero['BST']/5) + math.floor(sp_total / 100) + 150) * 2
    return score


# returns column of html file with respective weapon type
def weapon_index(weapon: str):
    value = 6*('Blue' in weapon) + 12*('Green' in weapon) + 18*('Colorless' in weapon)
    value += 1*('Bow' in weapon) + 2*('Dagger' in weapon) + 3*('Tome' in weapon) + 4*('Breath' in weapon) + 5*('Beast' in weapon)
    return value


# automate
# takes bst and other data out of link url, and dumps it into heroesdata.txt
def bst_extractor():
    url = 'https://feheroes.gamepedia.com/Level_40_stats_table'
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    rows = soup.table.findAll('tr')

    heroes = []
    for row in rows[1:]:
        cells = row.findAll('td')
        heroes.append("{}+{}+{}+{}+".format(cells[0].a['title'], cells[2].img['alt'], cells[9].string, cells[3].img['alt']))

    url = 'https://feheroes.gamepedia.com/Hero_skills_table'
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    rows = soup.table.findAll('tr')

    index = 0
    for row in rows[1:]:
        cells = row.findAll('td')
        if len(cells[4].findAll('a')) == 2:
            heroes[index] = heroes[index] + str(1)
        else:
            if '+' in cells[4].findAll('a')[0].string:
                heroes[index] = heroes[index] + str(0)
            else:
                heroes[index] = heroes[index] + str(1)
        print(heroes[index])
        index += 1

    with open('./HTML/heroesdata.txt', 'w', encoding='utf-8') as fp:
        for hero in heroes:
            fp.write(hero + '\n')


# creates the HTML tag given a hero object
def create_tag(hero):
    name = hero['Name']
    soup = BeautifulSoup('', 'html.parser')
    clean_name = name.replace(':', '').replace(' ', '_').replace("'", '').replace('ç', 'c').replace('"', '')\
        .replace('í', 'i').replace('á', 'a').replace('é', 'e')
    path = 'HTML/assets/45px-' + clean_name + '_Face_FC.webp.png'
    tag = soup.new_tag('img', title=name, alt=name, src=path, decoding="async", width="40", height="40")

    regfive = True
    fourstar = True

    tag['data-move'] = hero['MoveType']
    if hero['Grail']:
        regfive = False
        fourstar = False
        tag['data-grail'] = 'true'
    if hero['Seasonal']:
        regfive = False
        fourstar = False
        tag['data-season'] = 'true'
    if hero['Legendary']:
        regfive = False
        fourstar = False
        tag['data-legend'] = 'true'
    if hero['Duo']:
        regfive = False
        fourstar = False
        tag['data-duo'] = 'true'
    if not hero['FiveStar'] and not regfive and fourstar:
        tag['data-four'] = 'true'
    elif regfive:
        tag['data-five'] = 'true'
    # print(tag)
    return tag


# automate
# insert a tag into a specified position
def htlm_insert(soup: BeautifulSoup, file_row: str):
    name, mv_type, bst, wp_type, prf = file_row.split('+')
    herobj = create_max_hero(name, wp_type, mv_type, 0, int(bst), 0, bool(prf), 0, 0, 0, 0, 0, False, False, False, False)
    score = score_calc(herobj)

    row_index = 0
    rows = soup.findAll('tr')
    for i in range(len(rows)):
        if str(score) in rows[i].th.string:
            row_index = i

    tag = create_tag(name)
    soup.findAll('tr')[row_index].findAll('td')[weapon_index(wp_type)].append(tag)
    return soup


# automate
# the great first fill of the html file, used only for mass insert
def hyper_fill():
    with open('./HTML/heroesdata.txt', encoding='utf-8') as fp:
        heroes = fp.readlines()

    with open ('maxscoretable.html') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')

    for hero in heroes:
        soup = htlm_insert(soup, hero)

    with open ('maxscoretable.html', 'w', encoding='utf-8') as html_file:
        html_file.write(soup.prettify())


# automate
# inserts the given tag inside the html code
def html_manual_insert(score, wp_type, tag):
    with open ('maxscoretable.html') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')

    row_index = 0
    rows = soup.findAll('tr')
    for i in range(len(rows)):
        if str(score) in rows[i].th.string:
            row_index = i

    soup.findAll('tr')[row_index].findAll('td')[weapon_index(wp_type)].append(tag)

    with open ('maxscoretable.html', 'w', encoding='utf-8') as html_file:
        html_file.write(soup.prettify())


    # cleaning the html page
    with open('./maxscoretable.html', encoding='utf-8') as fp:
        html = fp.read()

    with open('./maxscoretable.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html.replace('<td>\n               </td>', '<td></td>'))

    return


# main function, the one to call
# function to call if you wanna manually add a hero into the html file
def manually_add_heroes():
    hero = manual_create_hero()
    score = score_calc(hero)
    tag = create_tag(hero)

    print('\n\n{} scores {} : {}'.format(hero['Name'], score, tag))

    response = input('(Y/N) Automatically add? ').upper()
    if 'Y' in response:
        html_manual_insert(score, hero['WeaponType'], tag)
    return


# temporary function to manually add a tag to all heroes already inserted into the html file
def correct_heroes():
    with open('maxscoretable.html') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')

    with open('./HTML/heroesdata.txt') as data_file:
        data = data_file.readlines()

    images = soup.findAll('img')

    for i in range(len(images)):
        attrs = images[i].attrs
        if 'data-season' in attrs:

            if 'data-five' in attrs:
                del images[i]['data-five']

    with open ('maxscoretable.html', 'w', encoding='utf-8') as html_file:
        html_file.write(soup.prettify())


manually_add_heroes()