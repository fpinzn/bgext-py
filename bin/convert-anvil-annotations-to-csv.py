from colorama import init
init()

from colorama import Fore, Back, Style
import sys, os
import argparse

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src/lib')
import anvil2frames

def getArgs () :
    parser = argparse.ArgumentParser(description = 'Convert from an anvil annotation file to a csv with a list of frames.')
    parser.add_argument('anvilFile', help='path of the anvil annotation xml file')
    parser.add_argument('--fr', dest = 'frameRate', help='frame rate of the annotated video')
    parser.add_argument('-o', dest = 'outputPath', help='path of the output csv file')
    return parser.parse_args()


def run () :
    args = getArgs()
    print(Fore.BLUE,
        'anvil file: ', args.anvilFile,
        'frame rate: ', args.frameRate,
        'output path: ', args.outputPath,
        Style.RESET_ALL)
    anvil2frames.convert_anvil_file_to_annotation_csv_frames_given_frame_rate_and_save_to_file(args.anvilFile, args.frameRate, args.outputPath)

run()
