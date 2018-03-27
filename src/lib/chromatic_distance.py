## Gets the euclidean distance between frames
OUTPUT_FOLDER = 'out/chromatic-distance/'

import numpy as np
import cv2
from datetime import datetime

import os, sys
import util
from scipy.spatial import distance

def preProcessFrame(frame, frameNumber):
    lowerResoFrame = cv2.pyrDown(cv2.pyrDown(frame))
    cv2.imwrite(OUTPUT_FOLDER + str(frameNumber) + '.png', lowerResoFrame)
    return lowerResoFrame.reshape(lowerResoFrame.shape[0] * lowerResoFrame.shape[1] * lowerResoFrame.shape[2])

def calcDistances (capture):
    distances = np.array([])
    previousFrame = np.array([])
    frameNumber = 0
    ret = True
    while(ret):
        ret, frame = capture.read()
        if not ret:
            break

        reshapedFrame = preProcessFrame(frame, frameNumber)
        if previousFrame.size > 0:
            currentDistance = int(np.linalg.norm(reshapedFrame - previousFrame))
            print(frameNumber, currentDistance)
            distances = np.append(distances, currentDistance)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        frameNumber += 1
        previousFrame = np.copy(reshapedFrame)
    return {'distances': distances}


def run (videoPath):
    start = datetime.now()
    outputPath = OUTPUT_FOLDER + os.path.basename(videoPath) + '-diffs.csv'

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
