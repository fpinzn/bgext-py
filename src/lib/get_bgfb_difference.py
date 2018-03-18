## Gets the difference of the number pixels classified as either background or foreground
## between frames.

import numpy as np
import cv2
from datetime import datetime

import os, sys

def getRGBWeights ( frame ):
    ## frame.size / 3 to get the number of pixels, not the number of values
    numberOfPixels = frame.size / 3
    RGBValueCount = np.sum(frame, axis=(0,1)) /numberOfPixels
    RGBValues ='R', 'G', 'B'
    return dict(zip(RGBValues, RGBValueCount))

def countFgBgPixels (capture, foregroundBackgroundFilter):
    counter = {}
    frame_number = 0
    ret = True
    while(ret):
        ret, frame = capture.read()
        if not ret:
            break

        fgmask = foregroundBackgroundFilter.apply(frame)
        # cv2.imshow('original',frame)
        # cv2.imshow('fg',fgmask)

        # maskColors are the colors, maskCounts the number of pixels with each column
        maskColors, maskCounts = np.unique(fgmask, return_counts=True)
        maskColorCount = dict(zip(maskColors, maskCounts))

        # add the color values to the dict
        maskColorCount.update(getRGBWeights(frame))

        for k in maskColorCount.keys():
            # if this is the first time a color appears
            if k not in counter:
                counter[k] = np.zeros(frame_number)
                print('new key', k)

            counter[k] = np.append(counter[k], maskColorCount[k])

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        frame_number += 1

    return counter

def write_to_file(data, file_name):
    output_file = open(file_name, 'w')
    output_file.write(str(data))
    output_file.close()

def format_csv(counter):
    file_content = 'frame'

    # this assumes all arrays are the same size
    number_of_frames = counter[list(counter.keys())[0]].size
    for k in counter.keys():
        file_content += ',' + str(k)

    for i in range(number_of_frames):
        file_content += '\n' + str(i)
        for k in counter.keys():
            file_content += ',' + str(counter[k][i])

    return file_content


# Things that might be passed as a param
# videoPath
# outputPath
# history
# varTreshold

def run (videoPath, outputPath, pHistory = 0, pVarTreshold = 8):
    start = datetime.now()

    ## input validation
    if not (os.path.exists(videoPath)):
        print('file', videoPath, 'does not exist')
        sys.exit()

    if (os.access(outputPath, os.W_OK)):
        print('cannot write to', outputPath)
        sys.exit()

    # setup, teardown
    capture = cv2.VideoCapture(videoPath)
    fgbg = cv2.createBackgroundSubtractorMOG2(history = pHistory, varThreshold = pVarTreshold, detectShadows = False)
    # processing
    output = countFgBgPixels(capture, fgbg)
    write_to_file(format_csv(output), outputPath)
    # teardown
    capture.release()
    cv2.destroyAllWindows()

    end = datetime.now()
    print('time taken:', str(end - start))
