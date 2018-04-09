from colorama import init
init()

from colorama import Fore, Back, Style
import sys, os
import argparse

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src/lib')
import get_bgfb_difference
import get_rgb_difference
import get_count_per_color_per_frame
import chromatic_distance
import scene_writer

def getArgs () :
    parser = argparse.ArgumentParser(description = 'Extract statistics about relative background-foreground change.')
    parser.add_argument('-v', dest = 'videoPath', help='path of the video to analyze')
    parser.add_argument('-o', dest = 'outputPath', help='path of the output csv file')
    parser.add_argument('--history', dest = 'history', type = int, help='history of the fgbg filter')
    parser.add_argument('--treshold', dest = 'treshold', type = int, help='treshold of the fgbg filter')
    parser.add_argument('--rgb', dest = 'rgb', type = bool, default = False, const = True, nargs='?', help='rgb analysis')

    subparser = parser.add_subparsers(dest="subparser")
    sceneExtractorSubParser = subparser.add_parser('extract')
    sceneExtractorSubParser.add_argument('-v', dest = 'videoPath', help='path of the video to extract scenes from')
    sceneExtractorSubParser.add_argument('-c', dest = 'csvPath', help='path of the csv file with values per frame (ex. chromatic change)')
    sceneExtractorSubParser.add_argument('-t', dest = 'treshold', help='treshold to consider a frame a scene cut file with values per frame (ex. chromatic change)')

    chromaticDistanceSubparser = subparser.add_parser('chromatic-distance')
    chromaticDistanceSubparser.add_argument('-v', dest = 'videoPath', help='path of the video to extract scenes from')
    chromaticDistanceSubparser.add_argument('--rgb', dest = 'rgb', type = bool, default = False, const = True, nargs='?', help='rgb analysis')

    colorCounterSubparser = subparser.add_parser('color-counter')
    colorCounterSubparser.add_argument('-v', dest = 'videoPath', help='path of the video for which the numbers of pixels of each color, for each frame will be counted')


    return parser.parse_args()


def run () :
    args = getArgs()

    print(args)
    print(Fore.BLUE,
        'running with -> videoPath:', args.videoPath, 'outputPath:', args.outputPath,
        'history:', args.history, 'treshold:', args.treshold, 'rgb analysis:', args.rgb, Style.RESET_ALL)

    if args.subparser == 'extract':
        scene_writer.run(args.videoPath, args.csvPath, args.treshold)

    if args.subparser == 'chromatic-distance':
        chromatic_distance.run(args.videoPath, args.rgb)

    if args.subparser == 'color-counter':
        get_count_per_color_per_frame.run(args.videoPath)

    else:
        get_bgfb_difference.run(args.videoPath, args.outputPath, args.history, args.treshold)

run()
