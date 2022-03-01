# FaceCrop

Automatically crop faces out of pictures bunch of pictures.

## Installation:
- _Tested with Python **3.9.7** on MacOS Montery_
- _Tested with Python **3.10.2** on Windows 11 21H2_
- _Tested with Python **3.10.0** on Ubuntu 21.10_ 
```
pip3 install -r requirements.txt
```

## HowToUse:
1. Insert your **source** pictures in the **input** folder (Processing: .jpg .jpeg .png)
2. Run the Python script (See command below)
3. Check the results in the **output** folder
4. Nothing else...
5. Maybe play with positional arguments and move x-/y-axis (See example 4)

## Script Arguments
```
usage: facecrop.py [-h] [--version] [-t] [-s] [-l] [-c] [-v] [-p PERCENTAGE | -f PX PX] [x] [y] [w] [h]

Automated face detection and out-file cropping

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

processing:
  -t, --takefirst       only process the first face in file
  -s, --show            show the process output

log configuration:
  -l, --log             write a logfile
  -c, --console         logging in console
  -v, --verbose         increase output verbosity in the logfile

resize the output files:
  -p PERCENTAGE, --percentage PERCENTAGE
                        resize the output image size resolution in percentage
  -f PX PX, --fixed PX PX
                        resize the output image size resolution to a fixed px resolution

set the cropping coordinates:
  x                     move the X-Axis as pixel (Default: 300px)
  y                     move the Y-Axis as pixel (Default: 300px)
  w                     set the Width of crop as pixel (Default: 600px)
  h                     set the Height of crop as pixel (Default: 600px)

Have fun! And play around with the coordinates
  ```
##### Process only first face find in a picture
When you know that there is only one person on the source picture.
You should use this mode - otherwise false/positives will also be saved.
```
python3 facecrop.py --takefirst
```
##### Process all faces find in picture
Running this mode on single person pictures results sometimes in additional false/positive cropped pictures.
```
python3 facecrop.py
```
##### Process all faces find in picture and show output
Running with --show will open the output as preview
```
python3 facecrop.py --show
```
## Example 01:
Photo by <a href="https://unsplash.com/@brokenlenscap?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Ben Parker</a> on <a href="https://unsplash.com/s/photos/people?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
#### **Command**:
```
python3 facecrop.py --takefirst
```
#### Input:
![example01-input.jpg](EXAMPLE/example01-input.jpg)
#### Output:
![example01-output.jpg](EXAMPLE/example01-output.jpg)

## Example 02:
Photo by <a href="https://unsplash.com/@rafaelladiniz?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Rafaella Mendes Diniz</a> on <a href="https://unsplash.com/s/photos/people?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
#### **Command**:
```
python3 facecrop.py --takefirst
```
#### Input:
![example02-input.jpg](EXAMPLE/example02-input.jpg)
#### Output:
![example02-output.jpg](EXAMPLE/example02-output.jpg)

## Example 03:
Photo by <a href="https://unsplash.com/@ankit_raj19?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Ankit Rajbhandari</a> on <a href="https://unsplash.com/s/photos/group-photo?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
#### **Command**:
```
python3 facecrop.py
```
#### Input:
![example03-input.jpg](EXAMPLE/example03-input.jpg)
#### Output:
![example03-output.jpg](EXAMPLE/example03-output_01.jpg)
![example03-output.jpg](EXAMPLE/example03-output_02.jpg)
![example03-output.jpg](EXAMPLE/example03-output_03.jpg)
![example03-output.jpg](EXAMPLE/example03-output_04.jpg)
## Example 04:
Photo by <a href="https://unsplash.com/@brokenlenscap?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Ben Parker</a> on <a href="https://unsplash.com/s/photos/people?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
#### **Command**:
```
python3 facecrop.py --takefirst 500 400 0 700
```
#### Input:
![example01-input.jpg](EXAMPLE/example01-input.jpg)
#### Output:
![example04-output.jpg](EXAMPLE/example04-output.jpg)

## Example 05:
Photo by <a href="https://unsplash.com/@rafaelladiniz?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Rafaella Mendes Diniz</a> on <a href="https://unsplash.com/s/photos/people?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
#### **Command**:
```
python3 facecrop.py --takefirst --fixed 100 100
```
#### Input:
![example02-input.jpg](EXAMPLE/example02-input.jpg)
#### Output:
![example05-output.jpg](EXAMPLE/example05-output.jpg)