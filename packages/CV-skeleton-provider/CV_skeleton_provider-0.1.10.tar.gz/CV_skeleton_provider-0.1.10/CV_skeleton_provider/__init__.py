import argparse
import cv2
import time
import imutils
import math
import numpy as np
import sys,os

from spcase.SPimage import forImage
from spcase.SPvideo import forVideo
from utils.formatter import str2bool
from utils.formatter import fileformat


from utils.formatter import optionChecker
from utils.preprocessor import preBack
from utils.preprocessor import preGray
from utils.preprocessor import preGamma
from utils.preprocessor import preBlackProportion
