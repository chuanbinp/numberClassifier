from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from collections import Counter

def createExamples():
    numberArrayExamples = open('numArEx.txt','a')
    numbersWeHave = range(0,10) #0-9
    versionsWeHave = range(1,10) #1-9

    for eachNum in numbersWeHave:
        for eachVer in versionsWeHave:
            imgFilePath = 'images/numbers/' + str(eachNum) + '.' + str(eachVer) + '.png'
            ei = Image.open(imgFilePath)
            eiar = np.array(ei)
            eiar1 = str(eiar.tolist())

            lineToWrite = str(eachNum) + '::' + eiar1 + '\n'
            numberArrayExamples.write(lineToWrite)

def threshold(imageArray):
    balanceArray = []
    newArray = imageArray

    for eachRow in imageArray:
        for eachPixel in eachRow:
            avgNum = reduce(lambda x,y: x + y, eachPixel[:3])/len(eachPixel[:3])
            balanceArray.append(avgNum)
    balance = reduce(lambda x,y: x + y, balanceArray)/len(balanceArray)

    for eachRow in newArray:
        for eachPixel in eachRow:
            if reduce(lambda x,y: x + y, eachPixel[:3])/len(eachPixel[:3]) > balance:
                eachPixel[0] = 255
                eachPixel[1] = 255
                eachPixel[2] = 255
                eachPixel[3] = 255
            else:
                eachPixel[0] = 0
                eachPixel[1] = 0
                eachPixel[2] = 0
                eachPixel[3] = 255

    return newArray

def whatNumIsThis(filePath):
    matchedArray = []
    loadExamples = open('numArEx.txt','r').read()
    loadExamples = loadExamples.split('\n')

    i = Image.open(filePath)
    iar = np.array(i)
    iarl = iar.tolist()
    
    for eachRow in iarl:
        for eachPixel in eachRow:
                eachPixel.append(255)
                
    inQuestion = str(iarl)

    for eachExample in loadExamples:
        if len(eachExample) > 3: #omit blank/weird lines
            splitEx = eachExample.split('::')
            currentNum = splitEx[0]
            currentAr = splitEx[1]

            eachPixEx = currentAr.split('],')
            eachPixInQ = inQuestion.split('],')

            x=0

            while x < len(eachPixEx):
                if eachPixEx[x] == eachPixInQ[x]:
                    matchedArray.append(int(currentNum))
                x+=1

    print(matchedArray)            
    x = Counter(matchedArray)        
    print(x)
    
    graphX = []
    graphY = []

    for eachThing in x:
        print (eachThing)
        graphX.append(eachThing)
        print (x[eachThing])
        graphY.append(x[eachThing])
        
    fig = plt.figure()
    ax1 = plt.subplot2grid((4,4), (0,0), rowspan=1, colspan=4)
    ax2 = plt.subplot2grid((4,4), (1,0), rowspan=3, colspan=4)

    ax1.imshow(iar)
    ax2.bar(graphX, graphY, align='center')
    plt.ylim(400)

    xloc = plt.MaxNLocator(12)
    ax2.xaxis.set_major_locator(xloc)
    
    plt.show()

createExamples()
whatNumIsThis('images/test.png')

