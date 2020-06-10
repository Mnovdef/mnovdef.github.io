from bs4 import BeautifulSoup
import pythons.auto_updater
import math


# ===============================================================
# ====================== SUPPORT FUNCTIONS ======================
# ===============================================================

# cleans the <td>s inside maxscoretable.html
def code_cleaner():
    with open('maxscoretable.html', encoding='utf-8') as fp:
        html = fp.read()

    with open('maxscoretable.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html.replace('<td>\n               </td>', '<td></td>')
                        .replace('<td>\n      </td>', '<td></td>'))

    print('Page Cleaned')


# removes weird characters from heroes name to create path to image
def clean_hero_name(hero_name: str):
    return hero_name.replace(':', '').replace(' ', '_').replace("'", '') \
        .replace('ç', 'c').replace('"', '').replace('í', 'i') \
        .replace('á', 'a').replace('é', 'e')


# formula to calculate arena score for each unit
def score_calc(hero):
    sp_total = hero['PRF'] + hero['Assist'] + hero['Special'] + hero['A'] + hero['B'] + hero['C'] + 240
    score = (148 + 20 + math.floor(hero['BST']/5) + math.floor(sp_total / 100) + 150) * 2
    return score


# returns column of html file with respective weapon type
def weapon_index(weapon: str):
    value = 6*('Blue' in weapon) + 12*('Green' in weapon) + 18*('Colorless' in weapon)
    value += 1*('Bow' in weapon) + 2*('Dagger' in weapon) + 3*('Tome' in weapon) \
                                 + 4*('Breath' in weapon) + 5*('Beast' in weapon)
    return value


# creates the HTML tag given a hero object
def create_tag(hero):
    name = hero['Name']
    soup = BeautifulSoup('', 'html.parser')
    path = 'HTML/assets/45px-' + clean_hero_name(name) + '_Face_FC.webp.png'
    tag = soup.new_tag('img', title=name, alt=name, src=path, decoding="async", width="40", height="40")

    tag_strings = ['data-duo', 'data-legend', 'data-grail', 'data-season', 'data-five']
    hero_params = [hero['Duo'], hero['Legend'], hero['Grail'], hero['Season'], hero['Five']]

    # creates a dict with the couple (tag-attribute, bool_value) and adds it to the tag if bool_value = True
    for attribute, bool_value in dict(zip(tag_strings, hero_params)).items():
        if bool_value:
            tag[attribute] = 'true'

    # if True is not in hero_params, it is a 4star available hero
    if True not in hero_params:
        tag['data-four'] = 'true'

    tag['data-move'] = hero['MoveType']
    return tag


# ================================================================
# ======================== MAIN FUNCTIONS ========================
# ================================================================

# manually asks for parameters to create a new hero object
# called by manually_add_heroes
def get_hero_data_from_input():
    name = input("Hero Name and Epithet: ")
    wp_type = input("(Red, Blue, Green, Colorless) (Sword/Axe/Lance/Staff, Tome, Breath, Beast, Dagger, Bow)\n"
                    "Weapon type: ")
    mv_type = input('(Infantry, Flying, Armored, Cavalry)\nMovement type: ')
    bst = int(input("BST: "))
    duel_bst = int(input("Duel BST: "))

    print("\nPress enter to say False, write anything to say True")

    values = [False] * 5
    strings = ["Duo? ", "Legendary? ", "Grail unit? ", "Seasonal? ", "Five star exclusive? "]
    for index in range(5):
        values[index] = bool(input(strings[index]))
        if values[index]:
            break

    duo, legend, grail, season, five = values

    prf = bool(input("Does it have a PRF? "))
    ass = int(input("Assist Cost: "))
    spec = int(input("Special Cost: "))
    a = int(input("A Skill Cost: "))
    b = int(input("B Skill Cost: "))
    c = int(input("C Skill Cost: "))

    hero_params ={'Name': name, 'WeaponType': wp_type, 'MoveType': mv_type,
                  'BST': bst, 'Duel_BST': duel_bst,
                  'PRF': prf, 'Assist': ass, 'Special': spec, 'A': a, 'B': b, 'C': c,
                  'Duo': duo, 'Legend': legend, 'Grail': grail, 'Season': season, 'Five': five}

    return create_max_hero(hero_params)


# create a hero object with his max arena setup
def create_max_hero(hero: dict):
    healer = hero['WeaponType'] == 'Colorless Staff'
    mv_bst = 170 * ('Infantry' in hero['MoveType'] or 'Flying' in hero['MoveType'])

    max_hero = {'Name': hero['Name'], 'WeaponType': hero['WeaponType'], 'MoveType': hero['MoveType'],
                'BST': max(hero['BST']+3+(not hero['Grail']), hero['Duel_BST'], mv_bst),
                'PRF': 350 + 50*hero['PRF'], 'Assist': max(400-100*healer, hero['Assist']),
                'Special': max(500-200*healer, hero['Special']),
                'A': max(300, hero['A']), 'B': max (240, hero['B']), 'C': max(300, hero['C']),
                'Duo': hero['Duo'], 'Legend': hero['Legend'], 'Grail': hero['Grail'],
                'Season': hero['Season'], 'Five': hero['Five']}
    return max_hero


# automate
# inserts the given tag inside the html code
def insert_tag_into_html(score, wp_type, tag):
    with open ('maxscoretable.html') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')

    rows = soup.find('table', {'class': 'heroes_table'}).findAll('tr')

    row_index = 0
    for i in range(len(rows)):
        if str(score) in rows[i].th.string:
            row_index = i

    rows[row_index].findAll('td')[weapon_index(wp_type)].append(tag)

    with open ('maxscoretable.html', 'w', encoding='utf-8') as html_file:
        html_file.write(soup.prettify())

    code_cleaner()
    return


# main function, the one to call
# function to call if you wanna manually add a hero into the html file
def manually_add_heroes():
    hero = get_hero_data_from_input()
    score = score_calc(hero)
    tag = create_tag(hero)

    print('\n\n{} scores {} : {}'.format(hero['Name'], score, tag))

    response = input('(Y/N) Automatically add? ').upper()
    if 'Y' in response:
        insert_tag_into_html(score, hero['WeaponType'], tag)
    return


# automatedscript to generate and insert tags into HTML
# put heroes names into newheroes.html before running and watch it go
def auto_create_from_file():
    with open('HTML/newheroes.txt') as data_file:
        heroes_list = data_file.readlines()

    for listed_hero in heroes_list:
        hero_params = pythons.auto_updater.hero_web_hunter(listed_hero)
        hero = create_max_hero(hero_params)
        score = score_calc(hero)
        tag = create_tag(hero)

        print('**{}** scores **{}** points.\n{}'.format(hero['Name'], score, tag))
        pythons.auto_updater.print_hero_info(hero)

        response = input('(Y/N) Automatically add? ').upper()
        if 'Y' in response:
            insert_tag_into_html(score, hero['WeaponType'], tag)

    return

# code_cleaner()
auto_create_from_file()

# manually_add_heroes()