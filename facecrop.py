#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Quentin Wohlfeil (https://gitlab.com/Quentendo64)
# Created Date: 08.02.2022
# version ='0.2'
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

# ---------------------------------------------------------------------------
# Arguments
# ---------------------------------------------------------------------------

parser = argparse.ArgumentParser(
    prog='facecrop.py',
    description='Automated face detection and out-file cropping',
    epilog='Have fun! And play around with the coordinates')
parser.add_argument('--version', action='version', version='%(prog)s 0.2')

processing = parser.add_argument_group(title='processing')
processing.add_argument('-t',
                        '--takefirst',
                        action='store_true',
                        help="only process the first face in file")
processing.add_argument('-s',
                        '--show',
                        dest='showOutput',
                        action='store_true',
                        help="show the process output")

logs = parser.add_argument_group(title='log configuration')
logs.add_argument('-l', '--log', dest='log',
                  action='store_true', help="write a logfile")
logs.add_argument('-c', '--console', dest='console',
                  action='store_true', help="logging in console")
logs.add_argument('-v', '--verbose', action='store_true',
                  help="increase output verbosity in the logfile")
resizeing = parser.add_argument_group(title='resize the output files')
resizeingMutal = resizeing.add_mutually_exclusive_group()
resizeingMutal.add_argument("-p", "--percentage", type=int, dest='percentage',
                            help="resize the output image size resolution in percentage")
resizeingMutal.add_argument("-f", "--fixed", type=int, nargs=2, dest='px',
                            help='resize the output image size resolution to a fixed px resolution')
cropping = parser.add_argument_group(title='set the cropping coordinates')
cropping.add_argument("x",
                      type=int,
                      default=300,
                      nargs='?',
                      const=1,
                      help="move the X-Axis as pixel (Default: %(default)spx)")
cropping.add_argument("y",
                      type=int,
                      default=300,
                      nargs='?',
                      const=1,
                      help="move the Y-Axis as pixel (Default: %(default)spx)")
cropping.add_argument("w",
                      type=int,
                      default=600,
                      nargs='?',
                      const=1,
                      help="set the Width of crop as pixel (Default: %(default)spx)")
cropping.add_argument("h",
                      type=int,
                      default=600,
                      nargs='?',
                      const=1,
                      help="set the Height of crop as pixel (Default: %(default)spx)")
args = parser.parse_args()

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

if (args.console) or (args.log):
    logFormat = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(threadName)s - %(name)s - %(message)s')

    if (args.verbose):
        loggerConfig = logging.getLogger('').setLevel(logging.DEBUG)
    else:
        loggerConfig = logging.getLogger('').setLevel(logging.INFO)

    logger = logging.getLogger('')
    if (args.console):
        console = logging.StreamHandler()

        console.setFormatter(logFormat)
        logger.addHandler(console)

    if (args.log):
        logfile = logging.FileHandler(
            'facecrop.log', mode='w', encoding="utf-8")
        logfile.setFormatter(logFormat)
        if (args.verbose):
            logfile.setLevel(logging.DEBUG)
        logger.addHandler(logfile)


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

inputDirectory = 'input'
outputDirectory = 'output'
cascadeFile = 'cascade_files/haarcascade_frontalface_alt2.xml'

logging.debug('The Input directory is: ' + inputDirectory)
logging.debug('The Output directory is: ' + outputDirectory)

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------


def return_supported_filetypes(inputDirectory):
    """
    Filter files based on extension. Return: List of supported files
    """
    return [
        "{}/{}".format(dirpath, filename)
        for dirpath, _, filenames in os.walk(inputDirectory)
        for filename in filenames
        if re.match(r'^.*\.(?:jpg|jpeg|png)$', filename)
    ]


def cropFaces(x, y, w, h, file):
    """
    Cropping out based on coordinates. Return: cropped picture
    """
    img = cv2.imread(file)
    logging.debug('Cropping coordinates: X: '+str(x)+'Y: ' +
                  str(y)+'W: ' + str(w)+'H: ' + str(h))
    x = x - args.x
    y = y - args.y
    w = w + args.w
    h = h + args.h
    crop = img[y:y + h, x:x + w]
    return crop


def resizeOutput(picture):
    """
    Resize picture based on pixels or percentage. Return: resized picture
    """
    logging.info('Resizeing Item')
    if (args.percentage):
        logging.debug('Resizeing to: ' + str(args.percentage) +
                      '%' + ' of the original')
        logging.debug('Original Dimensions : ', picture.shape)
        width = int(picture.shape[1] * args.percentage / 100)
        height = int(picture.shape[0] * args.percentage / 100)
        resolution = (width, height)
        resizedImage = cv2.resize(
            picture, resolution, interpolation=cv2.INTER_LINEAR)
        logging.debug('Resized Dimensions : ', resizedImage.shape)
        return resizedImage
    if (args.px):
        logging.debug('Resizeing to: ' + str(args.px[0]) + 'x' + str(args.px[1]))
        logging.debug('Original Dimensions : ', picture.shape)
        resolution = args.px[0], args.px[1]
        resizedImage = cv2.resize(
            picture, resolution, interpolation=cv2.INTER_LINEAR)
        logging.debug('Resized Dimensions : ', resizedImage.shape)
        return resizedImage


def saveOutput(path, file):
    """
    Save file to disk
    """
    logging.info('Saving Item:'+path)
    cv2.imwrite(path, file)
    return file


def showInput():
    """
    Show supported files in input
    """
    for file in return_supported_filetypes(inputDirectory):
        print(file)


def toGrayscale(file):
    """
    Convert picture to grayscale. Return: grayscaled picture
    """
    logging.debug(file + ' to grayscale')
    grayscale = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2GRAY)
    return grayscale


def faceRecognition(file):
    """
    Recognise faces based on cascade files. Return: face coordinates
    """
    logging.debug('Face recognition')
    if(isinstance(file, str)):
        file = cv2.imread(file)
    cv2.CascadeClassifier(cascadeFile)
    coordinates = cv2.CascadeClassifier(
        cascadeFile).detectMultiScale(file, 1.1, 4)
    logging.debug('Found coordinates')
    logging.debug(coordinates)
    return coordinates


def main():
    for file in return_supported_filetypes(inputDirectory):
        fileName = os.path.basename(file).split('.')[0]
        logging.info('Processing Item: ' + file)
        logging.debug('Filename without extension: ' + fileName)
        coordinates = faceRecognition(toGrayscale(file))
        index = 1
        if (args.takefirst):
            logging.debug('--takefist is set - take only 01 of ' +
                          str(f'{len(coordinates):02d}'))
            coordinates = [coordinates[0]]
            logging.debug('Using coordinates: ' + str(coordinates[0]))
        for (x, y, w, h) in coordinates:
            count = f'{index:02d}'
            fullFilePath = outputDirectory + '/' + fileName + '_' + count + '.jpg'
            cropped = cropFaces(x, y, w, h, file)
            if (args.percentage) or (args.px):
                logging.debug('Resize parameter set')
                output = saveOutput(fullFilePath, resizeOutput(cropped))

            else:
                logging.debug('No resizing')
                output = saveOutput(fullFilePath, cropped)

            if(args.showOutput):
                logging.debug('Show Output')
                cv2.imshow(fileName + '_' + count, output)
                if (index == len(coordinates)):
                    print('Press any key in the preview window to exit')
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
            index += 1


# ---------------------------------------------------------------------------
# Here we go - Here the main magic happens
# ---------------------------------------------------------------------------

main()
