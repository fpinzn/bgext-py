import numpy as np
import cv2
import timeit

cap = cv2.VideoCapture('AT-full-episode.mp4')
# cap = cv2.VideoCapture('AT-20secs.mp4')
fgbg = cv2.createBackgroundSubtractorMOG2(100, 16, False)


start = timeit.timeit()
def getRGBWeights ( frame ):
    numberOfPixels = frame.size
    RGBValueCount = np.sum(frame, axis=(0,1)) /numberOfPixels
    RGBValues ='R', 'G', 'B'
    # print(frame)
    # print(dict(zip(RGBValues, RGBValueCount)))
    return dict(zip(RGBValues, RGBValueCount))

def countColors ():
    counter = {}
    frame_number = 0
    ret = True
    while(ret):
        ret, frame = cap.read()
        if not ret:
            break
        fgmask = fgbg.apply(frame)
        # cv2.imshow('original',frame)
        # cv2.imshow('fg',fgmask)

        # maskValues are the colors, maskCounts the number of pixels with each column
        maskValues, maskCounts = np.unique(fgmask, return_counts=True)
        maskValueCounts = dict(zip(maskValues, maskCounts))

        # getRGBWeights(frame)
        maskValueCounts.update(getRGBWeights(frame))

        for k in maskValueCounts.keys():
            # if this is the first time a color appears
            if k not in counter:
                counter[k] = np.zeros(frame_number)
                print('new key', k)

            counter[k] = np.append(counter[k], maskValueCounts[k])

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        frame_number += 1

    cap.release()
    cv2.destroyAllWindows()
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



output = countColors()
write_to_file(format_csv(output), '01-full-video-output-file-with-rgb.csv')
end = timeit.timeit()
print(end - start)
print(list(map(lambda k: str(k) + ':' + str(output[k].shape), output.keys())))
