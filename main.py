import os
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageEnhance, ImageTk
import tkinter as tk
from tkinter import Entry, Button, Label, Text
from io import BytesIO


Google_Image = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

u_agnt = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

Image_Folder = 'Images_1'

# Site not to take
exclude_websites = ['http://fresherslive.com/', 'http://pkbnews.in/']

def download_images(data):
    num_images = 2
    log_text.config(state=tk.NORMAL) 

    log_text.insert(tk.END, 'Searching Images....\n')
    log_text.update()

    search_url = Google_Image + 'q=' + data

    response = requests.get(search_url, headers=u_agnt)
    html = response.text

    b_soup = BeautifulSoup(html, 'html.parser')
    results = b_soup.findAll('img', {'class': 'rg_i Q4LuWd'})

    count = 0
    imagelinks = []
    for res in results:
        try:
            link = res['data-src']
            # log_text.insert(tk.END, link + '\n')  
            log_text.update()
            
            if not any(exclude_site in link for exclude_site in exclude_websites):
                imagelinks.append(link)
                count = count + 1
                if (count >= num_images):
                    break

        except KeyError:
            continue

    log_text.insert(tk.END, f'Found {len(imagelinks)} images\nStart downloading...\n')
    log_text.update()

    for i, imagelink in enumerate(imagelinks):
        response = requests.get(imagelink)

        imagename = Image_Folder + '/' + data + str(i + 1) + '.webp'
        with open(imagename, 'wb') as file:
            file.write(response.content)

        # Resize  1200x800
        try:
            img = Image.open(imagename)
            img = img.resize((1200, 800), Image.ANTIALIAS)
            img.save(imagename)
        except Exception as e:
            log_text.insert(tk.END, f"Error resizing image: {e}\n")

    log_text.insert(tk.END, 'Download Completed!\n')
    log_text.config(state=tk.DISABLED)  

def apply_filter(image):

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.3) 
    
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1)  
    
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.2)
    
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2)
    
    return image

def display_images(imagelinks):
    image_frame = tk.Frame(window)
    image_frame.pack()

    for i, imagelink in enumerate(imagelinks):
        response = requests.get(imagelink)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((200, 150), Image.ANTIALIAS)
        
       
        img = apply_filter(img)
        
        photo = ImageTk.PhotoImage(img)  

        image_label = tk.Label(image_frame, image=photo)
        image_label.image = photo
        image_label.grid(row=i // 3, column=i % 3, padx=10, pady=10)


def download_images(data):
    num_images = 2
    log_text.config(state=tk.NORMAL)  

    log_text.insert(tk.END, 'Searching Images....\n')
    log_text.update()

    search_url = Google_Image + 'q=' + data

    response = requests.get(search_url, headers=u_agnt)
    html = response.text

    b_soup = BeautifulSoup(html, 'html.parser')
    results = b_soup.findAll('img', {'class': 'rg_i Q4LuWd'})

    count = 0
    imagelinks = []
    for res in results:
        try:
            link = res['data-src']
            
            log_text.update()
           
            if not any(exclude_site in link for exclude_site in exclude_websites):
                imagelinks.append(link)
                count = count + 1
                if (count >= num_images):
                    break

        except KeyError:
            continue

    log_text.insert(tk.END, f'Found {len(imagelinks)} images\nStart downloading...\n')
    log_text.update()

    for i, imagelink in enumerate(imagelinks):
        response = requests.get(imagelink)

        imagename = Image_Folder + '/' + data + str(i + 1) + '.webp'
        with open(imagename, 'wb') as file:
            file.write(response.content)

        try:
            img = Image.open(imagename)
            
            # Apply the filter
            img = apply_filter(img)
            
            img = img.resize((1200, 800), Image.ANTIALIAS)
            img.save(imagename)
        except Exception as e:
            log_text.insert(tk.END, f"Error processing image: {e}\n")

    log_text.insert(tk.END, 'Download Completed!\n')
    log_text.config(state=tk.DISABLED)  
    return imagelinks 

def on_submit():
    if not os.path.exists(Image_Folder):
        os.mkdir(Image_Folder)

    data = entry.get()
    imagelinks = download_images(data)
    display_images(imagelinks)  



window = tk.Tk()
window.title("Image Downloader")

label = Label(window, text="Enter your search keyword:")
label.pack()

entry = Entry(window)
entry.pack()

button = Button(window, text="Submit", command=on_submit)
button.pack()

log_text = Text(window, wrap=tk.WORD, width=40, height=10)
log_text.pack()
log_text.config(state=tk.DISABLED)

label = Label(window, text="Note: Images will be downloaded in the Images_1 folder")
label.pack()

window.mainloop()
