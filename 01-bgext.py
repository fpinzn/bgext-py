import numpy as np
import cv2
import timeit

cap = cv2.VideoCapture('AT-full-episode.mp4')
# cap = cv2.VideoCapture('AT-20secs.mp4')
fgbg = cv2.createBackgroundSubtractorMOG2()


start = timeit.timeit()

def countColors ():
    counter = {}
    frame_number = 0
    ret = True
    while(ret):
        ret, frame = cap.read()
        fgmask = fgbg.apply(frame)
        # cv2.imshow('original',frame)
        # cv2.imshow('fg',fgmask)

        print('pos', time)

        # uniques are the colors, counts the number of pixels with each column
        uniques, counts = np.unique(fgmask, return_counts=True)
        count_dict = dict(zip(uniques, counts))
        for k in count_dict.keys():
            # if this is the first time a color appears
            if k not in counter:
                counter[k] = np.zeros(frame_number)
                print('new key', k)

            counter[k] = np.append(counter[k], count_dict[k])

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
write_to_file(format_csv(output), '01-full-episode_video-output_file.csv')
end = timeit.timeit()
print(end - start)
print(list(map(lambda k: str(k) + ':' + str(output[k].shape), output.keys())))
