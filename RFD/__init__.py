from os import path, mkdir, listdir, environ
from shutil import rmtree
from logging import info, warning
from json import dumps, load

# Set Environ for logging
environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'
environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# imports
import cv2