## Gets the euclidean distance between frames
OUTPUT_FOLDER = 'out/chromatic-distance/'

import numpy as np
import cv2
from datetime import datetime

import os, sys
import util
from scipy.spatial import distance

allHueValues = np.array([])

def getDistanceRGB(currentFrameLowerRes, previousFrameLowerRes):
    diffenceVector = (currentFrameLowerRes - previousFrameLowerRes).flatten()
    return int(np.linalg.norm(diffenceVector))

def getHSVFrame(lowerResoFrame):
    return cv2.cvtColor(lowerResoFrame, cv2.COLOR_BGR2HSV)

def getDistanceHSV(currentFrameLowerRes, previousFrameLowerRes, useHueOnly = True):
    # The Hue component is a circle so %180 is needed to calculate the correct distance between 2 hues
    currentHues = currentFrameLowerRes[:, :, 0]
    previousHues = previousFrameLowerRes[:, :, 0]

    flatHueDifference = ((currentHues - previousHues) % 180).flatten()

    if useHueOnly:
        differenceVector = flatHueDifference
    else:
        currentSV = currentFrameLowerRes[:, :, [1,2]]
        previousSV = previousFrameLowerRes[:, :, [1,2]]
        assert currentHues.shape == previousHues.shape
        assert currentSV.shape == previousSV.shape

        flatSvDifference = (currentSV - previousSV).flatten()

        differenceVector = np.concatenate((flatHueDifference, flatSvDifference))

    return int(np.linalg.norm(differenceVector))


def calcDistances (capture, useRgb):
    distances = np.array([])
    previousFrame = np.array([])
    frameNumber = 0
    ret = True
    while(ret):
        ret, frame = capture.read()
        if not ret:
            break

        lowerResoFrame = cv2.pyrDown(cv2.pyrDown(frame))

        if previousFrame.size > 0:
            if useRgb:
                currentDistance = getDistanceRGB(lowerResoFrame, previousFrame)
            else:
                lowerResoFrame = getHSVFrame(lowerResoFrame)
                currentDistance = getDistanceHSV(lowerResoFrame, previousFrame)

            print(frameNumber, currentDistance)
            distances = np.append(distances, currentDistance)
        elif not useRgb:
            lowerResoFrame = getHSVFrame(lowerResoFrame)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        frameNumber += 1
        previousFrame = np.copy(lowerResoFrame)

    return {'distances': distances}


def run (videoPath, useRgb):
    start = datetime.now()
    outputPath = OUTPUT_FOLDER + os.path.basename(videoPath) + '-diffs-h.csv'

    if not (os.path.exists(videoPath)):
        print('file', videoPath, 'does not exist')
        sys.exit()

    if (os.access(outputPath, os.W_OK)):
        print('cannot write to', outputPath)
        sys.exit()

    capture = cv2.VideoCapture(videoPath)
    output = util.calc_diffs(calcDistances(capture, useRgb))

    capture.release()
    cv2.destroyAllWindows()

    util.write_to_file(util.format_csv(output), outputPath)
    end = datetime.now()
    print('time taken:', str(end - start))
