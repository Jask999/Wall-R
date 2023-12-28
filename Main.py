from tkinter import *
from tkinter import font as tkFont
from tkinter import ttk
from PIL import ImageTk,Image
import Algorithm
import requests
import numpy as np
from io import BytesIO
import webbrowser
import time

import praw
from PIL import ImageTk,Image
import math
from io import BytesIO
import ImageMethods


root = Tk()
root.title("Wall-R")
root.geometry("1505x890")
root.resizable(0,0)
root.configure(bg="#121212")
root.iconbitmap("C:/Users/Jaskirat/Downloads/Blue Whale Logo.ico")

imageDataBase = np.load("imageDatabaseTesting.npy", allow_pickle=True)

smallSize = tkFont.Font(size=18)
bigSize = tkFont.Font(size=36)



start = Button(root, text="Start", command=lambda: launch(), height=5, width=25, font=bigSize, bd=0, fg="#c38fff", bg="#1e1e1e", activebackground="#323232", activeforeground="#c294f7")
start.place(x=391, y=300)

restart = Button(root, text="Refresh", height=1, width=20, font=smallSize, bg="#181818", bd=0, activebackground="#282828", fg="#a2a2a2", activeforeground="#b4b4b4", command=lambda: populate_storage())
restart.place(x=608, y=700)


reddit = praw.Reddit(client_id = '4NG_Na51C0BSUMgjt9uV3Q',
                     client_secret = 'abFSjbAxee9NGYkas9-dV66d14_bYA',
                     user_agent= 'prawtutorialv1')


def populate_storage():
    #restart.place_forget()
    #root.update()

    x = 0
    imageDataBase = np.empty((0,7))

    subreddit = reddit.subreddit('wallpaper')
    # creates an instance of a specfic subreddit

    top_posts = subreddit.top(time_filter="month", limit=100)
    #tells what sorting method to use in the subreddit and how many posts to examine

    bar = ttk.Progressbar(root, orient=HORIZONTAL, length=500, mode='determinate')
    bar.pack(pady=155, side=BOTTOM, ipady=8)

    for post in top_posts:
        x = x + 1
        #print(x)

        bar['value'] = x
        root.update_idletasks()


        postUrl = post.url
        postAuthor = post.author
        #print(postUrl)
        if postUrl[-4:-2] == ".p" or postUrl[-4:-2] == ".j":
            #only images & correct file type to be stored (.jpg or .png)

            response = requests.get(postUrl)
            #makes a HTTP request to get the info (image) stored in the link
            #try:
            pil_Img = Image.open(BytesIO(response.content))
            #except:
            #    continue
            domaniantColor = ImageMethods.get_RGB_dominant_color_1(pil_Img)
            LTDratio = ImageMethods.get_light_to_dark_ratio(pil_Img)
            seen = False

            imageData = np.array([[postUrl, postAuthor, domaniantColor[0],
                                   domaniantColor[1], domaniantColor[2], LTDratio, seen]],
                                 dtype="object")
            #print(imageData)
            imageDataBase = np.vstack((imageDataBase, imageData))

    #print(imageDataBase)
    np.save("imageDatabaseTesting.npy", imageDataBase)
    bar.destroy()
    restart.place_forget()



def open_Image(url):# to open image in a tab when clicked                           . Source: https://www.tutorialspoint.com/how-to-create-a-hyperlink-with-a-label-in-tkinter
   webbrowser.open_new_tab(url) # webbrowser library was imported for this

def display_image():
    global bestImageIndex
    global imageLabel

    bestImageIndex = Algorithm.get_highscore()

    link = imageDataBase[bestImageIndex, 0]

    print(imageDataBase[bestImageIndex, 1])

    response = requests.get(link) #makes a HTTP request to get the info (image) stored in the link

    openImg = Image.open(BytesIO(response.content)) #using the pillow library to open the image
    resized = openImg.resize((1440,810), Image.Resampling.LANCZOS) #uses pillow to resize the image 1280,720   1440,810

    img = ImageTk.PhotoImage(resized)# image is stored in a variable using pillow
    #print(img)


    imageLabel = Label(image=img) # the variable is put into a label from the tkinter library

    imageLabel.image = img # this keeps a refernce to the tkinter object and is needed cause: https://web.archive.org/web/20210508110143/https://web.archive.org/web/20201111190625id_/http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm

    imageLabel.grid(row=0, column=0, columnspan=500, padx=30, pady=10) # label is shoved onto the screen

    imageLabel.bind("<Button-1>", lambda e: #to open image in a tab when clicked
    open_Image(link))

#display_image()



def rating_stars(rating):
    Algorithm.change_scores(rating, bestImageIndex)
    #print(bestImageIndex)
    imageLabel.grid_forget()


    starButtons1.deselect()
    starButtons2.deselect()
    starButtons3.deselect()
    starButtons4.deselect()
    starButtons5.deselect() #TODO remove
    starButtons6.deselect()
    starButtons7.deselect()
    starButtons8.deselect()
    starButtons9.deselect()
    starButtons10.deselect()


    display_image()


rating = IntVar()



def launch():
    global starButtons1
    global starButtons2
    global starButtons3
    global starButtons4
    global starButtons5
    global starButtons6
    global starButtons7
    global starButtons8
    global starButtons9
    global starButtons10

    start.place_forget()
    restart.place_forget()
    display_image()


    for x in range(1, 11):
        """
        starButtons = Radiobutton(root, variable=rating, value=x, bg="black", command=lambda: rating_stars(rating.get()))
        starButtons.grid(row=1,column=245 + x)
        """
        y = str(x)
        starText = Label(root, text=y + "  ", bg="#121212", fg="white").grid(row=2, column=245 + x)

    # ------------------------------- #TODO remove this and uncomment the thing above while also getting rid of the .deselect in the rating stars function

    starButtons1 = Radiobutton(root, variable=rating, value=1, bg="#121212", command=lambda: rating_stars(rating.get()))
    starButtons1.grid(row=1, column=245 + 1)

    starButtons2 = Radiobutton(root, variable=rating, value=2, bg="#121212", command=lambda: rating_stars(rating.get()))
    starButtons2.grid(row=1, column=245 + 2)

    starButtons10 = Radiobutton(root, variable=rating, value=10, bg="#121212", command=lambda: rating_stars(rating.get()))
    starButtons10.grid(row=1, column=245 + 10)

    starButtons3 = Radiobutton(root, variable=rating, value=3, bg="#121212", command=lambda: rating_stars(rating.get()))
    starButtons3.grid(row=1, column=245 + 3)

    starButtons4 = Radiobutton(root, variable=rating, value=4, bg="#121212", command=lambda: rating_stars(rating.get()))
    starButtons4.grid(row=1, column=245 + 4)

    starButtons5 = Radiobutton(root, variable=rating, value=5, bg="#121212", command=lambda: rating_stars(rating.get()))
    starButtons5.grid(row=1, column=245 + 5)

    starButtons6 = Radiobutton(root, variable=rating, value=6, bg="#121212", command=lambda: rating_stars(rating.get()))
    starButtons6.grid(row=1, column=245 + 6)

    starButtons7 = Radiobutton(root, variable=rating, value=7, bg="#121212", command=lambda: rating_stars(rating.get()))
    starButtons7.grid(row=1, column=245 + 7)

    starButtons8 = Radiobutton(root, variable=rating, value=8, bg="#121212", command=lambda: rating_stars(rating.get()))
    starButtons8.grid(row=1, column=245 + 8)

    starButtons9 = Radiobutton(root, variable=rating, value=9, bg="#121212", command=lambda: rating_stars(rating.get()))
    starButtons9.grid(row=1, column=245 + 9)

    # ------------------------




root.mainloop()





