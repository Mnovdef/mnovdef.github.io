from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
from pprint import pprint

def my_urlopen(url: str):
    return urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read()

def passive_cost_extractor(row_list: list):
    skills = []
    try:
        try:
            rowspan_1 = int(row_list[1].find_all('td')[-1]['rowspan'])
        except:
            return
        tds = row_list[rowspan_1].find_all('td')
        print('\tFound ', tds[0].a.img['src'])
        skills.append([tds[0].a.img['src'], int(str(tds[4])[4])])

        rowspan_2 = int(row_list[1+rowspan_1].find_all('td')[-1]['rowspan'])
        tds = row_list[rowspan_1 + rowspan_2].find_all('td')
        print('\tFound ', tds[0].a.img['src'])
        skills.append([tds[0].a.img['src'], int(str(tds[4])[4])])

        try:
            rowspan_3 = int(row_list[1 + rowspan_2].find_all('td')[-1]['rowspan'])
        except:
            rowspan_3 = 1
        tds = row_list[rowspan_1 + rowspan_2 + rowspan_3].find_all('td')
        print('\tFound ', tds[0].a.img['src'])
        skills.append([tds[0].a.img['src'], int(str(tds[4])[4])])
    except IndexError:
        pass

    return skills

def preleva_tutte_le_img_tag_da_html():
    with open('../maxscoretable.html') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')

    table = soup.find_all('table', {'class': 'heroes_table'})[0]
    rows = table.find_all('tr')[1:]

    with open('../heroes_data.txt', 'w', encoding='utf-8') as file:
        for row in rows:
            score = int(row.th.string)
            tds = row.find_all('td')
            for td in tds:
                images = td.find_all('img')
                for image in images:
                    hero_string = ''
                    for data in [image['alt'], image['src'], score, tds.index(td), image['data-move']]:
                        hero_string += str(data) + ' # '

                    for data in ['data-duo', 'data-legend', 'data-grail', 'data-season', 'data-five', 'data-four']:
                        try:
                            check = image[data]
                            hero_string += (data)
                        except KeyError:
                            continue

                    file.write(hero_string + '\n')

def print_four_star_passives():
    url = 'https://feheroes.gamepedia.com/Hero_availability_chart'
    soup = BeautifulSoup(my_urlopen(url), 'html.parser')

    rows = soup.find('table', {'class': 'wikitable unsortable'}).tbody.find_all('tr')[2:]
    columns = [row.find_all('td')[2:6] for row in rows]
    a_list = [b for c in [item for sublist in [[td.find_all('a') for td in listina] for listina in columns]
                          for item in sublist] for b in c]
    a_list = [[a['href'], a['title']] for a in a_list]


    skills = []
    # TODO remove [0]
    for hero in a_list:
        url = 'https://feheroes.gamepedia.com' + hero[0]
        soup = BeautifulSoup(my_urlopen(url), 'html.parser')
        passiveTable = soup.find_all('table', {'class': 'wikitable default unsortable skills-table'})[-1]

        print('Doing: ', hero[1])
        skills.append(passive_cost_extractor(passiveTable.find_all('tr')))

    pprint(skills)
    # skills = [item for sublist in skills for item in sublist]

    skills.remove(None)
    with open('HTML/temp.txt', 'w', encoding='utf-8') as html_file:
        for hero in skills:
            for skill in hero:
                print(skill[0])
                skill_name = skill[0].split('/')[7]
                img_location = './HTML/passives/' + skill_name
                urlretrieve(skill[0], img_location)

                img = soup.new_tag('img', src=img_location, alt=skill_name, width=30)
                html_file.write('<td>{}</td>\n'.format(img))

    # pprint(skills)
