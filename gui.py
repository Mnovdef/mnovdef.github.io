import tkinter as tk
from PIL import ImageTk, Image
from io import BytesIO
import requests

window = tk.Tk()
# window.geometry("550x300+300+150")
# window.resizable(width=True, height=True)


# ============== HERO NAME LABEL ==============
# gets hero name from given url, and puts it into a label
hero_name = "Selena: La Sgualdrena"
hero_name_label = tk.Label(window, text=hero_name, font=("Arial", 22))

hero_name_label.pack()




# ============== IMAGE LABEL ==============
# get the image from site, and load it into an image object
image_url = "https://gamepedia.cursecdn.com/feheroes_gamepedia_en/thumb/3/3b/Selena_Sandbar_Fluorspar_Face.webp/340px-Selena_Sandbar_Fluorspar_Face.webp.png"
response = requests.get(image_url)
img = Image.open(BytesIO(response.content))
img = img.resize((300, 400), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)

# create the image panel
img_label = tk.Label(window, image=img)
img_label.pack()


window.mainloop()