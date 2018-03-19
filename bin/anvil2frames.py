from colorama import init
init()

from colorama import Fore, Back, Style
import sys, os
import argparse
import anvil2frames

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src/lib')
# import anvil2frames

def getArgs () :
    parser = argparse.ArgumentParser(description = 'Convert from an anvil annotation file to a csv with a list of frames.')
    parser.add_argument('anvilFile', help='path of the anvil annotation xml file')
    parser.add_argument('--fr', dest = 'frameRate', help='frame rate of the annotated video')
    return parser.parse_args()


def run () :
    args = getArgs()
    print(args)
    print(Fore.BLUE,
        'anvil file: ', args.anvilFile,
        'frame rate: ', args.frameRate,
        Style.RESET_ALL)

run()
