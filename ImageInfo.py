#I merged this into Main to make the progress bar
import praw
from PIL import ImageTk,Image
import math
import requests
from io import BytesIO
import numpy as np
import ImageMethods




#creates an instance of reddit class
reddit = praw.Reddit(client_id = '4NG_Na51C0BSUMgjt9uV3Q',
                     client_secret = 'abFSjbAxee9NGYkas9-dV66d14_bYA',
                     user_agent= 'prawtutorialv1')


def populate_storage():
    x = 0
    imageDataBase = np.empty((0,7))

    subreddit = reddit.subreddit('wallpaper')
    # creates an instance of a specfic subreddit

    top_posts = subreddit.top(time_filter="month", limit=100)
    #tells what sorting method to use in the subreddit and how many posts to examine

    for post in top_posts:
        x = x + 1
        print(x)


        postUrl = post.url
        postAuthor = post.author
        print(postUrl)
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

            imageDataBase = np.vstack((imageDataBase, imageData))

    print(imageDataBase)
    np.save("imageDatabaseTesting.npy", imageDataBase)

#populate_storage()



#Storage = populate_storage()
#print(Storage)

#ORRRR
#populate_storage()
#Storage = return_storage()
#print(Storage)


