## Gets the euclidean distance between frames
OUTPUT_FOLDER = 'out/chromatic-distance/'
HSV_COLOR_SPACE = True

import numpy as np
import cv2
from datetime import datetime

import os, sys
import util
from scipy.spatial import distance

allHueValues = np.array([])

def getDistanceRGB(lowerResoFrame, previousFrame):
    reshapedFrame =  lowerResoFrame.reshape(lowerResoFrame.shape[0] * lowerResoFrame.shape[1] * lowerResoFrame.shape[2])
    return int(np.linalg.norm(reshapedFrame - previousFrame))

def getDownsampledHue(lowerResoFrame):
    hsvLowerResoFrame = cv2.cvtColor(lowerResoFrame, cv2.COLOR_BGR2HSV)
    hueValues = hsvLowerResoFrame[:,:,0]
    reshapedHueValues = hueValues.reshape(1, hueValues.size)
    assert reshapedHueValues.size == hsvLowerResoFrame.shape[0] * hsvLowerResoFrame.shape[1]
    return reshapedHueValues

def getDistanceHSV(lowerResoFrameHues, previousFrameHues):
    # The Hue component is a circle so %180 is needed to calculate the correct distance between 2 hues
    return int(np.linalg.norm((lowerResoFrameHues - previousFrameHues) % 180))


def calcDistances (capture):
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
            if HSV_COLOR_SPACE:
                lowerResoFrame = getDownsampledHue(lowerResoFrame)
                currentDistance = getDistanceHSV(lowerResoFrame, previousFrame)
            else:
                currentDistance = getDistanceRGB(lowerResoFrame, previousFrame)

            print(frameNumber, currentDistance)
            distances = np.append(distances, currentDistance)
        elif HSV_COLOR_SPACE:
            lowerResoFrame = getDownsampledHue(lowerResoFrame)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        frameNumber += 1
        previousFrame = np.copy(lowerResoFrame)

    return {'distances': distances}


def run (videoPath):
    start = datetime.now()
    outputPath = OUTPUT_FOLDER + os.path.basename(videoPath) + '-diffs-hsv.csv'

    if not (os.path.exists(videoPath)):
        print('file', videoPath, 'does not exist')
        sys.exit()

    if (os.access(outputPath, os.W_OK)):
        print('cannot write to', outputPath)
        sys.exit()

    capture = cv2.VideoCapture(videoPath)
    output = util.calc_diffs(calcDistances(capture))

    capture.release()
    cv2.destroyAllWindows()

    util.write_to_file(util.format_csv(output), outputPath)
    end = datetime.now()
    print('time taken:', str(end - start))
