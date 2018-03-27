## Counts color per frame
FILE_PREFIX = 'color-count-per-frame'

import numpy as np
import cv2
from datetime import datetime
import time

import os, sys
import util
def flatten_pixels(frame):
    ## Asserts is rgb shaped
    assert frame.shape[2] == 3
    return frame.reshape(frame.shape[0] * frame.shape[1], 3)

def get_hex_from_decimal_bgr(bgr):
    # found in https://stackoverflow.com/questions/3380726/converting-a-rgb-color-tuple-to-a-six-digit-code-in-python
    return '%02x%02x%02x' % (bgr[2],bgr[1],bgr[0])

def get_pixel_count_per_color_in_frame ( frame ):
    flattened_pixels= flatten_pixels(frame)
    decimalColors, pixelCount = np.unique(flattened_pixels, return_counts=True, axis=0)
    hexColors = list(map(get_hex_from_decimal_bgr, decimalColors))
    pixelCountPerColor = dict(zip(hexColors, pixelCount))
    assert len(flattened_pixels) == sum(pixelCount)
    # pixelCountPerColor = sorted(pixelCountPerColor, key=lambda k: pixelCountPerColor[k][0])

    return pixelCountPerColor

def count_colors (capture):
    counter = {}
    frame_number = 0
    ret = True
    while(ret):
        start = time.time()
        ret, frame = capture.read()
        if not ret:
            break

        currentFramePixelsPerColorCount = get_pixel_count_per_color_in_frame(frame)

        cv2.imshow('original',frame)
        util.write_to_file(str(currentFramePixelsPerColorCount), 'out/countrgb' +'-'+str(frame_number))
        # for k in currentFrameCount.keys():
        #     # if this is the first time a color appears
        #     if k not in counter:
        #         counter[k] = np.array(np.zeros(frame_number))
        #         # print('new key', k)

            # counter[k] = np.append(counter[k], currentFrameCount[k])
        k = cv2.waitKey(30) & 0xFF
        if k == 27:
            break

        frame_number += 1
        end = time.time()
        print(frame_number,', time: ', end - start)

    return counter


def run (videoPath, outputPath):
    start = datetime.now()

    if not (os.path.exists(videoPath)):
        print('file', videoPath, 'does not exist')
        sys.exit()

    if (os.access(outputPath, os.W_OK)):
        print('cannot write to', outputPath)
        sys.exit()

    capture = cv2.VideoCapture(videoPath)
    output = count_colors(capture)

    capture.release()
    cv2.destroyAllWindows()

    end = datetime.now()
    print('time taken:', str(end - start))
