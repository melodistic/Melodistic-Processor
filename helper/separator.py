import getopt
import os
import shutil
import sys
from spleeter.separator import Separator

def separate(audio, filename):
    separator = Separator('spleeter:2stems')
    separator.separate_to_file(audio, 'instrumental/')
    os.rename('instrumental/'+filename.split('.')[0]+'/accompaniment.wav', 'instrumental/'+filename)
    shutil.rmtree('instrumental/'+filename.split('.')[0])
    os.remove(filename)

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:],"f:",["filename="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-f", "--filename"):
            filename = arg
            separate(filename, filename.split('/')[-1])
            sys.exit(0)
