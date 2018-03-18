## Gets the difference of the RGB avg values between frames.

import numpy as np
import cv2
from datetime import datetime

import os, sys
import util

def getRGBWeights ( frame ):
    ## frame.size / 3 to get the number of pixels, not the number of values
    numberOfPixels = frame.size / 3
    RGBValueCount = np.sum(frame, axis=(0,1)) /numberOfPixels
    RGBValues ='R', 'G', 'B'
    # print(frame)
    # print(dict(zip(RGBValues, RGBValueCount)))
    return dict(zip(RGBValues, RGBValueCount))

def countColors (capture):
    counter = {}
    frame_number = 0
    ret = True
    while(ret):
        ret, frame = capture.read()
        if not ret:
            break

        # add the color values to the dict
        colorAverages = getRGBWeights(frame)

        for k in colorAverages.keys():
            # if this is the first time a color appears
            if k not in counter:
                counter[k] = np.zeros(frame_number)
                print('new key', k)
            counter[k] = np.append(counter[k], colorAverages[k])

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        frame_number += 1

    return counter


def run (videoPath, outputPath, pHistory = 0, pVarTreshold = 8):
    start = datetime.now()

    if not (os.path.exists(videoPath)):
        print('file', videoPath, 'does not exist')
        sys.exit()

    if (os.access(outputPath, os.W_OK)):
        print('cannot write to', outputPath)
        sys.exit()

    capture = cv2.VideoCapture(videoPath)

    output = countColors(capture)
    rgb_diffs = util.prefix_dict_keys(util.calc_diffs(output), 'diff')
    output.update(rgb_diffs)

    capture.release()
    cv2.destroyAllWindows()

    util.write_to_file(util.format_csv(output), outputPath)
    end = datetime.now()
    print('time taken:', str(end - start))
