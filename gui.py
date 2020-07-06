from urllib.request import Request, urlopen
from urllib.parse import quote
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
from io import BytesIO
import tkinter as tk
import requests
import math


def test_function():
    print("Movement: \t", mv_type.get(), "Weapon: \t", wp_color.get() + " " + wp_type.get())
    print("Trait: \t\t", trait.get())
    print("BST: \t\t", bst.get(), "\t\tDuel BST:\t", duel_bst.get())
    print("Weapon: \t", weapon.get(), "\tAssist:\t", assist.get(), "\tSpecial:\t", special.get())
    print("A: \t\t\t", a.get(), "\tB:\t\t\t", b.get(), "\tC:\t\t\t", c.get())
    print()

def weapon_index(weapon: str):
    value = 6*('Blue' in weapon) + 12*('Green' in weapon) + 18*('Colorless' in weapon)
    value += 1*('Bow' in weapon) + 2*('Dagger' in weapon) + 3*('Tome' in weapon) \
                                 + 4*('Breath' in weapon) + 5*('Beast' in weapon)
    return value


def insert_separation(frame):
    sep_label = tk.Label(frame, text=" ")
    sep_label.pack()


# my_urlopen but for gamepedia
# this does not work if url contains weird characters
def gamepedia(hero: str):
    print('https://feheroes.gamepedia.com/' + hero.replace('\n', '').replace(' ', '_'))
    return urlopen(Request('https://feheroes.gamepedia.com/' + quote(hero.replace('\n', '').replace(' ', '_')))).read()


# read heroes' names from newheroes.txt
def get_heroes_from_file():
    with open('HTML/newheroes.txt') as data_file:
        heroes_list = data_file.readlines()
    return heroes_list


# changes the image on the GUI
def change_image(image_url):
    global img_label
    response = requests.get(image_url)

    img = Image.open(BytesIO(response.content))
    img = img.resize((300, 400), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    img_label.configure(image=img)
    img_label.image = img


# reads the next hero from file, then changes Name and Image in the GUI
heroes_index = 0
def read_next_hero():
    global heroes_index
    global heroes_list

    soup = BeautifulSoup(gamepedia(heroes_list[heroes_index]), 'html.parser')

    tables = soup.find_all('table')
    if "You may be looking for:" in str(tables[0]):
        tables.remove(tables[0])

    # change hero title
    hero_name_entry.delete(0, len(hero_name_entry.get()))
    hero_name_entry.insert(0, heroes_list[heroes_index])

    # change hero image
    image_url = tables[1].td.div.a.img['src']
    change_image(image_url)

    heroes_index += 1

    bst.delete(0, "end")
    duel_bst.delete(0, "end")
    text_box.delete(0.0, "end")
    score_entry.delete(0, "end")

    return


# well, calculates score giver a hero
def score_calc(hero):
    sp_total = hero['PRF'] + hero['Assist'] + hero['Special'] + hero['A'] + hero['B'] + hero['C'] + 240
    score = (148 + 20 + math.floor(hero['BST']/5) + math.floor(sp_total / 100) + 150) * 2
    return score


# creates the html tag to insert and prints it into textFrame
def create_tag():
    # score calculation
    global bst, duel_bst, current_tag, current_wp, current_score
    try:
        bst_value = max(int(bst.get())+3+int((trait.get() != 'grail')), int(duel_bst.get()))
    except ValueError:
        text_box.delete(0.0, "end")
        text_box.insert(0.0, "My Friend, something is messed up in the BST region")
        return

    text_box.delete(0.0, "end")
    sp_total = int(weapon.get()) + int(assist.get()) + int(special.get()) + \
               int(a.get()) + int(b.get()) + int(c.get()) + 240

    score = (148 + 20 + math.floor(bst_value / 5) + math.floor(sp_total / 100) + 150) * 2

    score_entry.delete(0, "end")
    score_entry.insert(0, score)

    # tag creation
    name = hero_name_entry.get().replace('\n', "")
    soup = BeautifulSoup('', 'html.parser')
    path = 'HTML/assets/45px-' + name.replace(" ", '_').replace(':', '').replace("'", '') + '_Face_FC.webp.png'
    tag = soup.new_tag('img', title=name, alt=name, src=path, decoding="async", width="40", height="40")

    tag['data-move'] = mv_type.get()
    tag['data-' + trait.get()] = "true"

    text_box.delete(0.0, "end")
    text_box.insert(0.0, tag)

    current_tag = tag
    current_score = score
    current_wp = wp_color.get() + " " + wp_type.get()
    return tag


# inserts current_tag into html file
def html_insert():
    global current_tag, current_wp, current_score

    with open('maxscoretable.html') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')

    rows = soup.find('table', {'class': 'heroes_table'}).findAll('tr')

    row_index = 0
    for i in range(1, len(rows)):
        if str(current_score) in rows[i].th.string:
            row_index = i

    rows[row_index].findAll('td')[weapon_index(current_wp)].append(current_tag)

    with open('maxscoretable.html', 'w', encoding='utf-8') as html_file:
        html_file.write(soup.prettify())

    print(hero_name_entry.get().replace("\n", ''), " added into HTML file.")
    return





window = tk.Tk()

# HERO NAME LABEL
hero_name_entry = tk.Entry(window, font=("Arial", 22), justify=tk.CENTER)
# hero_name_entry.insert(0, hero_name)
hero_name_entry.pack(side=tk.TOP)

# ============== TOP FRAME ==============
# contains left and right frames
top_frame = tk.Frame(window)
top_frame.pack()


# ============== LEFT FRAME ==============
# contains the hero image, that's it
left_frame = tk.Frame(top_frame)
left_frame.pack(side=tk.LEFT)


# IMAGE LABEL
image_url = "https://gamepedia.cursecdn.com/feheroes_gamepedia_en/thumb/3/3b/"\
            + "Selena_Sandbar_Fluorspar_Face.webp/340px-Selena_Sandbar_Fluorspar_Face.webp.png"
response = requests.get(image_url)

img = Image.open(BytesIO(response.content))
img = img.resize((300, 400), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)

img_label = tk.Label(left_frame, image=img, border=2)
img_label.pack()


# ============== RIGHT FRAME ==============
# contains aaaaaall of the hero informations
right_frame = tk.Frame(top_frame)
right_frame.pack(side=tk.RIGHT)

# test_button = tk.Button(right_frame, text="Test", command=test_function)
# test_button.pack()


# MOVEMENT FRAME
mv_frame = tk.Frame(right_frame)
mv_frame.pack()

mv_label = tk.Label(mv_frame, text="Movement Type:", font=("", 9, "bold"))
mv_label.pack(side=tk.LEFT)
mv_type = tk.StringVar(value="Infantry")

mv_check1 = tk.Radiobutton(mv_frame, text="Infantry", variable=mv_type, value="Infantry")
mv_check2 = tk.Radiobutton(mv_frame, text="Flying",  variable=mv_type, value="Flying")
mv_check3 = tk.Radiobutton(mv_frame, text="Cavalry", variable=mv_type, value="Cavalry")
mv_check4 = tk.Radiobutton(mv_frame, text="Armored", variable=mv_type, value="Armored")
mv_check4.pack(side=tk.RIGHT)
mv_check3.pack(side=tk.RIGHT)
mv_check2.pack(side=tk.RIGHT)
mv_check1.pack(side=tk.RIGHT)

insert_separation(right_frame)

# WEAPON FRAME
wp_frame = tk.Frame(right_frame)
wp_frameL = tk.Frame(wp_frame)
wp_frameR = tk.Frame(wp_frame)
wp_frame1 = tk.Frame(wp_frameR)
wp_frame2 = tk.Frame(wp_frameR)

wp_frame.pack()
wp_frameL.pack(side=tk.LEFT)
wp_frameR.pack(side=tk.RIGHT)
wp_frame1.pack()
wp_frame2.pack()

wp_label = tk.Label(wp_frame, text="Weapon Type:", font=("", 9, 'bold'))
wp_label.pack(side=tk.LEFT)

wp_color = tk.StringVar(value="Red")
wp_type = tk.StringVar(value="Sword")
wp_checkcol1 = tk.Radiobutton(wp_frame1, variable=wp_color, text="Red", value="Red")
wp_checkcol2 = tk.Radiobutton(wp_frame1, variable=wp_color, text="Blue", value="Blue")
wp_checkcol3 = tk.Radiobutton(wp_frame1, variable=wp_color, text="Green", value="Green")
wp_checkcol4 = tk.Radiobutton(wp_frame1, variable=wp_color, text="Colorless", value="Colorless")
wp_checkcol4.pack(side=tk.RIGHT)
wp_checkcol3.pack(side=tk.RIGHT)
wp_checkcol2.pack(side=tk.RIGHT)
wp_checkcol1.pack(side=tk.RIGHT)

wp_checktype1 = tk.Radiobutton(wp_frame2, variable=wp_type, text="Sword", value="Sword")
wp_checktype2 = tk.Radiobutton(wp_frame2, variable=wp_type, text="Bow", value="Bow")
wp_checktype3 = tk.Radiobutton(wp_frame2, variable=wp_type, text="Dagger", value="Dagger")
wp_checktype4 = tk.Radiobutton(wp_frame2, variable=wp_type, text="Beast", value="Beast")
wp_checktype5 = tk.Radiobutton(wp_frame2, variable=wp_type, text="Tome", value="Tome")
wp_checktype6 = tk.Radiobutton(wp_frame2, variable=wp_type, text="Breath", value="Breath")
wp_checktype6.pack(side=tk.RIGHT)
wp_checktype5.pack(side=tk.RIGHT)
wp_checktype4.pack(side=tk.RIGHT)
wp_checktype3.pack(side=tk.RIGHT)
wp_checktype2.pack(side=tk.RIGHT)
wp_checktype1.pack(side=tk.RIGHT)

insert_separation(right_frame)

# TYPE FRAME
trait_frame = tk.Frame(right_frame)
trait_frame.pack()

trait_label = tk.Label(trait_frame, text="Trait Type:", font=("", 9, "bold")).pack(side=tk.LEFT)
trait = tk.StringVar(value="duo")

trait_check1 = tk.Radiobutton(trait_frame, variable=trait, text="Duo", value="duo")
trait_check2 = tk.Radiobutton(trait_frame, variable=trait, text="Legendary", value="legend")
trait_check3 = tk.Radiobutton(trait_frame, variable=trait, text="Grail", value="grail")
trait_check4 = tk.Radiobutton(trait_frame, variable=trait, text="Seasonal", value="season")
trait_check5 = tk.Radiobutton(trait_frame, variable=trait, text="Five Star", value="five")
trait_check6 = tk.Radiobutton(trait_frame, variable=trait, text="Four Star", value="four")
trait_check6.pack(side=tk.RIGHT)
trait_check5.pack(side=tk.RIGHT)
trait_check4.pack(side=tk.RIGHT)
trait_check3.pack(side=tk.RIGHT)
trait_check2.pack(side=tk.RIGHT)
trait_check1.pack(side=tk.RIGHT)

insert_separation(right_frame)

# BST FRAME
bst_frame = tk.Frame(right_frame)
bst_frame.pack()

bst_label = tk.Label(bst_frame, text="BST:   ", font=("", 9, "bold"))
duel_bst = tk.Entry(bst_frame, justify=tk.CENTER)
bst_label.pack(side=tk.LEFT)
duel_bst.pack(side=tk.RIGHT)

duel_bst_label = tk.Label(bst_frame, text="                Duel BST:   ", font=("", 9, "bold"))
bst = tk.Entry(bst_frame, justify=tk.CENTER)
duel_bst_label.pack(side=tk.RIGHT)
bst.pack(side=tk.RIGHT)

insert_separation(right_frame)

# WEAPON FRAME
weapon_frame = tk.Frame(right_frame)
weapon_frame.pack()

weapon_label = tk.Label(weapon_frame, text="Weapon Type:", font=("", 9, "bold")).pack(side=tk.LEFT)
weapon = tk.IntVar(value="350")

weapon_check1 = tk.Radiobutton(weapon_frame, variable=weapon, text="No PRF", value="350")
weapon_check2 = tk.Radiobutton(weapon_frame, variable=weapon, text="PRF",    value="400")
weapon_check2.pack(side=tk.RIGHT)
weapon_check1.pack(side=tk.RIGHT)


# ASSIST FRAME
assist_frame = tk.Frame(right_frame)
assist_frame.pack()

assist_label = tk.Label(assist_frame, text="Assist Cost:", font=("", 9, "bold")).pack(side=tk.LEFT)
assist = tk.IntVar(value="400")

assist_check1 = tk.Radiobutton(assist_frame, variable=assist, text="Special",   value="500")
assist_check2 = tk.Radiobutton(assist_frame, variable=assist, text="Rally Up+", value="400")
assist_check3 = tk.Radiobutton(assist_frame, variable=assist, text="Restore+",  value="300")
assist_check3.pack(side=tk.RIGHT)
assist_check2.pack(side=tk.RIGHT)
assist_check1.pack(side=tk.RIGHT)


# SPECIAL FRAME
special_frame = tk.Frame(right_frame)
special_frame.pack()

special_label = tk.Label(special_frame, text="Special Cost:", font=("", 9, "bold")).pack(side=tk.LEFT)
special = tk.IntVar(value="500")

special_check1 = tk.Radiobutton(special_frame, variable=special, text="Aether", value="500")
special_check2 = tk.Radiobutton(special_frame, variable=special, text="Balm+", value="300")
special_check2.pack(side=tk.RIGHT)
special_check1.pack(side=tk.RIGHT)


# A FRAME
a_frame = tk.Frame(right_frame)
a_frame.pack()

a_label = tk.Label(a_frame, text="A Passive Cost:", font=("", 9, "bold")).pack(side=tk.LEFT)
a = tk.IntVar(value="300")

a_check1 = tk.Radiobutton(a_frame, variable=a, text="350 SP", value="350")
a_check2 = tk.Radiobutton(a_frame, variable=a, text="300 SP", value="300")
a_check2.pack(side=tk.RIGHT)
a_check1.pack(side=tk.RIGHT)


# B FRAME
b_frame = tk.Frame(right_frame)
b_frame.pack()

b_label = tk.Label(b_frame, text="B Passive Cost:", font=("", 9, "bold")).pack(side=tk.LEFT)
b = tk.IntVar(value="240")

b_check1 = tk.Radiobutton(b_frame, variable=b, text="300 SP", value="300")
b_check2 = tk.Radiobutton(b_frame, variable=b, text="240 SP", value="240")
b_check2.pack(side=tk.RIGHT)
b_check1.pack(side=tk.RIGHT)


# C FRAME
c_frame = tk.Frame(right_frame)
c_frame.pack()

c_label = tk.Label(c_frame, text="C Passive Cost:", font=("", 9, "bold")).pack(side=tk.LEFT)
c = tk.IntVar(value="300")

c_check1 = tk.Radiobutton(c_frame, variable=c, text="300 SP", value="300")
c_check1.pack(side=tk.RIGHT)

insert_separation(window)


# BIG TEXTBOX
text_frame = tk.Frame(window, background="blue")
text_frame.pack(side=tk.BOTTOM)

text_box = tk.Text(height=2, wrap=tk.WORD)
text_box.pack(fill=tk.X)

insert_separation(window)


# ============== BOTTOM FRAME ==============
# contains action buttons
bottom_frame = tk.Frame(window)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Read Next Hero from File, Create Tag, Insert in HTML
read_button = tk.Button(bottom_frame,   text="Read next Hero",   command=read_next_hero)
create_button = tk.Button(bottom_frame, text="Create Tag",       command=create_tag)
insert_button = tk.Button(bottom_frame, text="Insert into HTML", command=html_insert)
score_label = tk.Label(bottom_frame, text="Score:    ")
score_entry = tk.Entry(bottom_frame, justify=tk.CENTER)
score_label.pack(side=tk.LEFT)
score_entry.pack(side=tk.LEFT)
read_button.pack(side=tk.RIGHT, padx=5)
insert_button.pack(side=tk.RIGHT, padx=5)
create_button.pack(side=tk.RIGHT, padx=5)


heroes_list = get_heroes_from_file()
current_tag = ""
current_score = 0
current_wp = ""

window.mainloop()








