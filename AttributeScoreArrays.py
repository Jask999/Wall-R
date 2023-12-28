import numpy as np


def initialize_attribute_score_array():
    scoreOfColors1 = np.ones((8,8,8))
    np.save("colorScores.npy", scoreOfColors1)
    print(scoreOfColors1)

    print()

    LTDratioScores = np.ones((21))
    np.save("LTDScores.npy", LTDratioScores)
    print(LTDratioScores)

    print()

    authorScores = np.empty((0,2))
    authorScores = np.append(authorScores, [["asa1", 1]], axis=0) # need to have something in array cuz if array is empty the if statement cant compare (i think), this is just easier and better to do over writing an if statement
    np.save("authorScores.npy", authorScores)


    print(authorScores)

#initialize_attribute_score_array()# THIS IS COMMENTED OUT BECAUSE OF RESET FUNCTION IN ALGORITHM

'''
authorScores = np.load("authorScores.npy", allow_pickle=True)
print(authorScores)

LTS = np.load("LTDScores.npy", allow_pickle=True)
print(LTS)

Color = np.load("colorScores.npy", allow_pickle=True)
print(Color)
'''