import numpy as np
#import ImageInfo
import math

import AttributeScoreArrays # remove when done

def reset():
    ImageInfo.populate_storage()  # REMOVEEEE MAYBE TODO here look
    #AttributeScoreArrays.initialize_attribute_score_array()
#reset()

imageDataBase = np.load("imageDatabaseTesting.npy", allow_pickle=True)
#print(imageDataBase)
def update():
    for x in range (len(imageDataBase)):
        imageDataBase[x,6] = False
    np.save("imageDatabaseTesting.npy", imageDataBase)
    AttributeScoreArrays.initialize_attribute_score_array()
#update()

#print(imageDataBase)


#ImageInfo.populate_storage() #keep here when done


colorScores = np.load("colorScores.npy", allow_pickle=True)

#colorScores[0,1,1] = 2 # [depth, row, column]

color = np.array([255, 81, 37])

def RGB_to_index (color):

    R = color[0]
    G = color[1]
    B = color[2]

    intervals = 256/8

    RIndex = R/intervals
    RIndex = math.floor(RIndex)

    GIndex = G/intervals
    GIndex = math.floor(GIndex)

    BIndex = B/intervals
    BIndex = math.floor(BIndex)

    return RIndex, GIndex, BIndex

"""
#colorIndex = RGB_to_index(color)

#print(colorIndex)


#colorScores[RGB_to_index(mostDomaniantColor)] = 2

#print(colorScores[colorIndex])
"""


LTDratioScores = np.load("LTDScores.npy", allow_pickle=True) #TODO just a todo to make sure i remember: its 21 becuase the 21st index keeps track of the score of images where LTDratio is over 1


LTDRATIO = 0.58


def LTDratio_to_index(LTDRATIO):
    interval = 1/10

    LTDIndex = LTDRATIO/interval

    if LTDIndex >= 20:
        LTDIndex = 20
    else:
        LTDIndex = math.floor(LTDIndex)

    return LTDIndex

"""
ratioIndex = LTDratio_to_index(LTDRATIO)

print(ratioIndex)
"""


authorScores = np.load("authorScores.npy", allow_pickle=True)

author = "PlayerInk"


# i use this inside the for loop and for some reason if the variable was not referneced inside the function doing thats illegal

def author_to_index(author):
    global authorScores

    counter = 0
    authorIndex = 0


    for i in range (len(authorScores[:,1]) + 1):
        if authorScores[i,0] != author:
            counter = counter + 1

            if counter == len(authorScores[:,1]):
                authorScores = np.append(authorScores, [[author, 1]], axis=0)
                np.save("authorScores.npy", authorScores)
        else:
            authorIndex = i
            break

    return authorIndex

"""
AuthorIndex = author_to_index(author)

print(AuthorIndex)

print(authorScores)
"""



""""""""""""""""""""""
"""""""""""""""""""""

def score_adder (rating):
    adder = -17.565+6.633*rating+-0.864*rating**2+0.048 * rating**3
    adder=round(adder)
    return adder




rating = 10 # make it whole numbers

fakeBestImageIndex = 0

#print("\nColor Scores:")
#print(colorScores)
#print("\nAuthor Scores:")
#print(authorScores)
#print("\nLTD ratio Score::")
#print(LTDratioScores)


def change_scores (rating, bestImageIndex):
    adder = score_adder(rating)



    RGBvalue = imageDataBase[bestImageIndex, 2] # retreives the images RGB value from the correct row and column
    RGBIndexes = RGB_to_index(RGBvalue) # converts the RGB value of the image into the index of the score array

    colorScores[RGBIndexes] = colorScores[RGBIndexes] + adder


    RGBvalue2 = imageDataBase[bestImageIndex, 3]  # This is the same thing as above but for the second most domaniant color
    RGBIndexes2 = RGB_to_index(RGBvalue2)

    colorScores[RGBIndexes2] = colorScores[RGBIndexes2] + math.floor(adder/1.1) # Here Instead of just adding, adder. This is done to reduce the influence for the second most domaniant color to the scores
    #score impacts:
    # 1 = -10, 2 = -6, 3 = -3,4 = -1, 5 = 0, 6 = 0, 7 = 2, 8 = 3, 9 = 6, 10 = 9 everything has an impact of one less execept a one star which has an impact of 2 less


    RGBvalue3 = imageDataBase[bestImageIndex, 4] # Now for 3rd most domaniant color
    RGBIndexes3 = RGB_to_index(RGBvalue3)

    colorScores[RGBIndexes3] = colorScores[RGBIndexes3] + math.floor(adder/1.3)
    #Score Impacts of /1.3:
    # 1 = -9, 2 = -5, 3 = -3, 4 = -1, 5 = 0, 6 = 0, 7 = 2, 8 = 3, 9 = 5, 10 = 7
    np.save("colorScores.npy", colorScores)


    LTDratio = imageDataBase[bestImageIndex, 5]
    LTDIndex = LTDratio_to_index(LTDratio)

    LTDratioScores[LTDIndex] = LTDratioScores[LTDIndex] + adder
    np.save("LTDScores.npy", LTDratioScores)


    authorValue = imageDataBase[bestImageIndex, 1]
    authorIndex = author_to_index(authorValue)

    authorScores[authorIndex, 1] = int(authorScores[authorIndex, 1]) + adder
    np.save("authorScores.npy", authorScores)


    print("\n\n\n\n\n"
          "     ------------------------------------------------        "
          " \n\n\n\n\n ")

    #print(colorScores)
    #print(authorScores)
    #print(LTDratioScores)


#print(colorScores)
#print(LTDratioScores)
#print(authorScores)

#change_scores(rating, fakeBestImageIndex)

#print(colorScores)
#print(LTDratioScores)
#print(authorScores)


def populate_final_scores():
    score = np.array([])
    for x in range (len(imageDataBase)):
        scoringImage = imageDataBase[x,:]
        for y in range (1,6):

            if y == 1:
                author = scoringImage[y]
                indexAuthor = author_to_index(author) #still need this becasue it will add the author to the list if its a new author
                authorScore = authorScores[indexAuthor,1]

            if y == 2:
                color1 = scoringImage[y]
                indexColor1 =  RGB_to_index(color1)
                color1Score = colorScores[indexColor1]

            if y == 3:
                color2 = scoringImage[y]
                indexcolor2 = RGB_to_index(color2)
                color2Score = colorScores[indexcolor2]

            if y == 4:
                color3 = scoringImage[y]
                indexcolor3 = RGB_to_index(color3)
                color3Score = colorScores[indexcolor3]

            if y == 5:
                LTD = scoringImage[y]
                indexLTD = LTDratio_to_index(LTD)
                LTDscore = LTDratioScores[indexLTD]


        finalScore = round(((color1Score + color2Score + color3Score)/3)) + int(authorScore)+ LTDscore # Do i need the int, the 4th image was actually from asa1 #TODO make it divide by 3
        score = np.append(score, finalScore)

    #print(score)
    return score


#populate_final_scores()

def get_highscore ():
    score = populate_final_scores()
    #This 1D "score" array contains the score for each image
    #in the same order that it was retrevied and stored in the ImageDatabase array
    scoreLength = len(score) # length of the "score" array
    sortedScore = np.arange((scoreLength))
    #.arange method creates an array of 0,1,2,3... until the length of "score"

    for x in range(scoreLength - 1):
        # This is now the modified selection sort algorithm, which sorts "score"
        # whenever a swap is made in "score" the same swap is made in "sortedScore"
        # This keeps track of the original indexes of the values from "score" array
        maxIndex = x
        for y in range(x + 1, scoreLength):
            if score[maxIndex] < score[y]:
                maxIndex = y
        if maxIndex != x:
            temp = score[maxIndex]
            score[maxIndex] = score[x]
            score[x] = temp # swap is made for "score"

            temp = sortedScore[maxIndex]
            sortedScore[maxIndex] = sortedScore[x]
            sortedScore[x] = temp # same swap is made for "sortedScore"

    # Once "score" is sorted, "sortedScore" will be also sorted such that:
    # "sortedScore" has the indexes of sorted "score" values in desending order



    for i in range (0,scoreLength):
        x = sortedScore[i]

        if imageDataBase[x, 6] == False:
            bestImageIndex = x
            imageDataBase[x, 6] = True
            np.save("imageDatabaseTesting.npy", imageDataBase)
            break
        else:
            bestImageIndex = None
    return bestImageIndex

#best = get_highscore()
#print(best)

#print(imageDataBase)

