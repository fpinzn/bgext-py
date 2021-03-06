import numpy as np
import cv2
import timeit
import os

OUTPUT_FOLDER = 'out/scene-writer/chromatic-distance/'

# expects a video file and a csv


def extractScenes (capture, cutFunction):
    frameNumber = 0
    frameNumberOfLastCut = 0
    ret = True
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))   # float
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) # float

    sceneWriter = cv2.VideoWriter(OUTPUT_FOLDER + '0.mp4', fourcc, 23.98, (width,height))

    while(ret):
        ret, frame = capture.read()
        recentlyCut = (frameNumber - frameNumberOfLastCut) < 3
        if cutFunction(frameNumber) and not recentlyCut:
            sceneWriter.release()
            sceneWriter = cv2.VideoWriter(OUTPUT_FOLDER + str(frameNumber) + '.mp4',fourcc, 23.98, (width,height))
            frameNumberOfLastCut = frameNumber
        else:
            sceneWriter.write(frame)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        frameNumber += 1

    capture.release()
    cv2.destroyAllWindows()

def generateCutFunction(frameValues, treshold):
    return lambda frameNumber: frameValues[frameNumber] > treshold

def getFromCSVFrameValues(filePath):
    file = open(filePath, 'r')
    lines = file.read().split('\n')
    return list(map(lambda l: float(l.split(',')[1]), lines[1:]))


def run(videoPath, csvFilePath, treshold = 9000):
    start = timeit.timeit()

    if not (os.path.exists(videoPath)):
        print('file', videoPath, 'does not exist')
        sys.exit()
    if not (os.path.exists(csvFilePath)):
        print('file', csvFilePath, 'does not exist')
        sys.exit()

    cutFunction = generateCutFunction(getFromCSVFrameValues(csvFilePath), int(treshold))

    capture = cv2.VideoCapture(videoPath)
    extractScenes(capture, cutFunction)

    end = timeit.timeit()
    print(end - start)
