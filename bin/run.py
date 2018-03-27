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

def getArgs () :
    parser = argparse.ArgumentParser(description = 'Extract statistics about relative background-foreground change.')
    parser.add_argument('-v', dest = 'videoPath', help='path of the video to analyze')
    parser.add_argument('-o', dest = 'outputPath', help='path of the output csv file')
    parser.add_argument('--history', dest = 'history', type = int, help='history of the fgbg filter')
    parser.add_argument('--treshold', dest = 'treshold', type = int, help='treshold of the fgbg filter')
    parser.add_argument('--rgb', dest = 'rgb', type = bool, default = False, const = True, nargs='?', help='rgb analysis')
    return parser.parse_args()


def run () :
    args = getArgs()

    print(Fore.BLUE,
        'running with -> videoPath:', args.videoPath, 'outputPath:', args.outputPath,
        'history:', args.history, 'treshold:', args.treshold, 'rgb analysis:', args.rgb, Style.RESET_ALL)

    if args.rgb:
        ## get_rgb_difference.run(args.videoPath, args.outputPath, args.history, args.treshold)
        # get_count_per_color_per_frame.run(args.videoPath)
        chromatic_distance.run(args.videoPath)
    else:
        get_bgfb_difference.run(args.videoPath, args.outputPath, args.history, args.treshold)

run()
