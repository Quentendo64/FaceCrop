#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Quentin Wohlfeil (https://gitlab.com/Quentendo64)
# Created Date: 08.02.2022
# version ='0.1'
# ---------------------------------------------------------------------------
""" Automatically crop faces out of pictures based on OpenCV """
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import cv2
import logging
import argparse
import re
import os
parser = argparse.ArgumentParser(
    description="Use --takefirst for only process first face in file")
parser.add_argument('-t', '--takefirst',  action='store_true',
                    help="Only process the first face in file")
parser.add_argument('-l', '--log',  action='store_true',
                    help="Write a logfile")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Increase output verbosity in the logfile")
parser.add_argument("x", type=int, default=300, nargs='?',
                    const=1, help="Move the X-Axis as pixel")
parser.add_argument("y", type=int, default=300, nargs='?',
                    const=1, help="Move the Y-Axis as pixel")
parser.add_argument("w", type=int, default=600, nargs='?',
                    const=1, help="Set the Width of crop as pixel")
parser.add_argument("h", type=int, default=600, nargs='?',
                    const=1, help="Set the Height of crop as pixel")
args = parser.parse_args()
if (args.log == True):
    if (args.verbose == True):
        logging.basicConfig(filename='facecrop.log', level=logging.DEBUG)
    else:
        logging.basicConfig(filename='facecrop.log', level=logging.INFO)
inputDirectory = 'input'
outputDirectory = 'output'
logging.debug('The Input directory is: ' + inputDirectory)
logging.debug('The Output directory is: ' + outputDirectory)


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------


def return_supported_filetypes(inputDirectory):
    return ["{}/{}".format(dirpath, filename) for dirpath, _, filenames in os.walk(inputDirectory) for filename in filenames if re.match(r'^.*\.(?:jpg|jpeg|png)$', filename)]


def processSingle(faces):
    """
    This function will only take the first face and save it as file.
    """
    index = 1
    for (x, y, w, h) in faces:
        if(index == 1):
            count = f'{index:02d}'
            logging.debug('Count is: ' + count)
            logging.debug('INTCount is: ')
            logging.debug(index)
            logging.info('Processing Face: ' + count + ' of ' + file)
            x = x - args.x
            y = y - args.y
            w = w + args.w
            h = h + args.h
            logging.debug('Cropping coordinates:')
            logging.debug('x:')
            logging.debug(x)
            logging.debug('y')
            logging.debug(y)
            logging.debug('w')
            logging.debug(w)
            logging.debug('h')
            logging.debug(h)
            crop = img[y:y + h, x:x + w]
            logging.info(outputDirectory + '/' +
                         fileName + '_' + count + '.jpg')
            cv2.imwrite(outputDirectory + '/' + fileName + '.jpg', crop)
            index += 1
            logging.debug(index)


def processAll(faces):
    """
    This function will take all faces and save it as file.
    """
    index = 1
    for (x, y, w, h) in faces:
        count = f'{index:02d}'
        logging.debug('Count is: ' + count)
        logging.debug('INTCount is: ')
        logging.debug(index)
        logging.info('Processing Face: ' + count + ' of ' + file)
        x = x - args.x
        y = y - args.y
        w = w + args.w
        h = h + args.h
        logging.debug('Cropping coordinates:')
        logging.debug('x:')
        logging.debug(x)
        logging.debug('y')
        logging.debug(y)
        logging.debug('w')
        logging.debug(w)
        logging.debug('h')
        logging.debug(h)
        crop = img[y:y + h, x:x + w]
        logging.info(outputDirectory + '/' + fileName + '_' + count + '.jpg')
        cv2.imwrite(outputDirectory + '/' + fileName +
                    '_' + count + '.jpg', crop)
        index += 1
        logging.debug(index)


for file in return_supported_filetypes(inputDirectory):
    print(file)


# ---------------------------------------------------------------------------
# Here we go
# ---------------------------------------------------------------------------

for file in return_supported_filetypes(inputDirectory):
    fileName = os.path.basename(file).split('.')[0]
    logging.info('Processing Item: ' + file)
    logging.debug('Filename without extension: ' + fileName)
    img = cv2.imread(file)
    face_cascade = cv2.CascadeClassifier(
        'cascade_files/haarcascade_frontalface_alt2.xml')
    logging.debug('Convert File to grayscale')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    logging.debug('Face Coordinates: ')
    logging.debug(faces)
    faceCount = len(faces)
    logging.debug('Detected Faces: ')
    logging.debug(faceCount)

    if (faceCount > 1):
        if (args.takefirst == True):
            logging.debug(
                '--takefirst / -t is active -- will only process first face in file: ' + file)
            processSingle(faces)
        else:
            processAll(faces)
    else:
        processSingle(faces)
