import numpy as np
import cv2
import timeit
import os

OUTPUT_FOLDER = 'out/scene-writer/chromatic-distance/'
TRESHOLD = 9000

# expects a video file and a csv


def extractScenes (capture, cutFunction):
    frameNumber = 0
    frameNumberOfLastCut = 0
    ret = True
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    sceneWriter = cv2.VideoWriter(OUTPUT_FOLDER + '0.mp4', fourcc, 23.98, (720,404))

    while(ret):
        ret, frame = capture.read()
        recentlyCut = (frameNumber - frameNumberOfLastCut) < 3
        if cutFunction(frameNumber) and not recentlyCut:
            sceneWriter.release()
            sceneWriter = cv2.VideoWriter(OUTPUT_FOLDER + str(frameNumber) + '.mp4',fourcc, 23.98, (720,404))
            frameNumberOfLastCut = frameNumber
        else:
            sceneWriter.write(frame)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        frameNumber += 1

    capture.release()
    cv2.destroyAllWindows()

def generateCutFunction(frameValues):
    return lambda frameNumber: frameValues[frameNumber] > TRESHOLD

def getFromCSVFrameValues(filePath):
    file = open(filePath, 'r')
    lines = file.read().split('\n')
    return list(map(lambda l: float(l.split(',')[1]), lines[1:]))


def run(videoPath, csvFilePath):
    start = timeit.timeit()

    if not (os.path.exists(videoPath)):
        print('file', videoPath, 'does not exist')
        sys.exit()
    if not (os.path.exists(csvFilePath)):
        print('file', csvFilePath, 'does not exist')
        sys.exit()

    cutFunction = generateCutFunction(getFromCSVFrameValues(csvFilePath))

    capture = cv2.VideoCapture(videoPath)
    extractScenes(capture, cutFunction)

    end = timeit.timeit()
    print(end - start)
