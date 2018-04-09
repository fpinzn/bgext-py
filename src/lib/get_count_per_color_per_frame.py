## Counts color per frame
OUTPUT_FOLDER = 'out/count-color-frames/'

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
    return pixelCountPerColor

def format_json (dictionary):
    result = '['
    for color in dictionary:
        result += '{"color":"' + str(color) + '","count":' + str(dictionary[color]) + '},'
    # result[:-1] to remove the trailling comma
    result = result[:-1] + ']'
    return result

def count_colors (capture, videoPath):
    counter = {}
    frame_number = 0
    ret = True
    while(ret):
        start = time.time()
        ret, frame = capture.read()
        if not ret:
            break

        currentFramePixelsPerColorCount = get_pixel_count_per_color_in_frame(frame)
        filePath = OUTPUT_FOLDER + os.path.basename(videoPath) + '-' + str(frame_number)
        util.write_to_file(format_json(currentFramePixelsPerColorCount), filePath + '.json')
        # show the frames
        # cv2.imshow('original',frame)
        cv2.imwrite(filePath + '.png', frame)

        k = cv2.waitKey(30) & 0xFF
        if k == 27:
            break

        frame_number += 1
        end = time.time()
        print(frame_number,', time: ', end - start)

    return counter


def run (videoPath):
    start = datetime.now()

    if not (os.path.exists(videoPath)):
        print('file', videoPath, 'does not exist')
        sys.exit()


    capture = cv2.VideoCapture(videoPath)
    output = count_colors(capture, videoPath)

    capture.release()
    cv2.destroyAllWindows()

    end = datetime.now()
    print('time taken:', str(end - start))
