import numpy as np
import cv2
import timeit

cap = cv2.VideoCapture('AT-full-episode.mp4')
# cap = cv2.VideoCapture('AT-20secs.mp4')
fgbg = cv2.createBackgroundSubtractorMOG2(100, 16, False)
font = cv2.FONT_HERSHEY_PLAIN

TRESHOLD = 40000
start = timeit.timeit()


def writeDerivative (img, derivative):
    cv2.putText(img, str(derivative),(10,400), font, 1,(255,0,0), 2, cv2.LINE_AA)

def extractScenes ():
    historicCount = {}
    frameNumber = 0
    frameNumberOfLastCut = 0
    ret = True
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    sceneWriter = cv2.VideoWriter('out2/0-0.mp4',fourcc, 23.98, (720,404))
    sceneMaskWriter = cv2.VideoWriter('out2/0-0-mask.mp4',fourcc, 23.98, (720,404))

    while(ret):
        ret, frame = cap.read()
        frameMask = fgbg.apply(frame)


        # cv2.imshow('original',frame)
        # cv2.imshow('fg',frameMask)

        # values are the colors, counts the number of pixels with each column
        values, counts = np.unique(frameMask, return_counts=True)
        countPerValue = dict(zip(values, counts))
        for k in countPerValue.keys():
            # if this is the first time a color appears
            if k not in historicCount:
                historicCount[k] = np.zeros(frameNumber)
                print('new key', k)

            historicCount[k] = np.append(historicCount[k], countPerValue[k])

        if 0 in historicCount:
            diff255 =(historicCount[0][frameNumber] - historicCount[0][frameNumber-1])
            framesSinceLastCut = frameNumber - frameNumberOfLastCut
            if diff255 > TRESHOLD and framesSinceLastCut > 10:
                sceneWriter.release()
                sceneWriter = cv2.VideoWriter('out2/' + str(frameNumber) + '-0.mp4',fourcc, 23.98, (720,404))

                sceneMaskWriter.release()
                sceneMaskWriter = cv2.VideoWriter('out2/' + str(frameNumber) + '-0-mask.mp4',fourcc, 23.98, (720,404))

                frameNumberOfLastCut = frameNumber

            writeDerivative(frame, diff255)
            sceneWriter.write(frame)

            rgbMask = cv2.cvtColor(frameMask, cv2.COLOR_GRAY2BGR)
            writeDerivative(rgbMask, diff255)
            sceneMaskWriter.write(rgbMask)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        frameNumber += 1

    cap.release()
    cv2.destroyAllWindows()
    return historicCount

extractScenes()
end = timeit.timeit()
print(end - start)
