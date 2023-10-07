import cv2
from cv2 import medianBlur
from cv2 import imwrite
import numpy as np
import PySimpleGUI as sg
from PIL import Image
import os

# Image Processing using CV

# Method to Read Image from the File Location
def read_img(filename):
    img = cv2.imread(filename)
    return img
def cleanup():
    os.remove("cartoon.png")
# Edge Detections
def edge_detection(img, line_wdt, blur):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayBlur = cv2.medianBlur(gray, blur)
    edges = cv2.adaptiveThreshold(
        grayBlur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_wdt, blur)
    return edges

# Running Color Quantisation
def color_quantisation(img, k):
    data = np.float32(img).reshape((-1, 3))
    criteria = (cv2.TermCriteria_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    ret, label, center = cv2.kmeans(
        data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    return result


# Graphical User Interface (GUI)


# Theme Color
sg.theme('DarkBlack')

layout = [[sg.Text('W E L C O M  E - T O - C A R T O O N I F I E R', font=('Arial Bold', 16))],

          [sg.Text('_'*60)],
          [sg.Text('Choose the line width : ', font=('Arial Bold', 12))],
          [sg.Slider(range=(1, 50),
                     default_value=25,
                     size=(20, 15),
                     orientation='horizontal',
                     font=('Helvetica', 12))],
          [sg.Text('Choose the Blur Value : ', font=('Arial Bold', 12))],
          [sg.Slider(range=(1, 15),
                     default_value=7,
                     size=(20, 15),
                     orientation='horizontal',
                     font=('Helvetica', 12))],
          [sg.Text('Choose the Total Colors : ', font=('Arial Bold', 12))],
          [sg.Slider(range=(1, 10),
                     default_value=5,
                     size=(20, 15),
                     orientation='horizontal',
                     font=('Helvetica', 12))],
          [sg.Text('_'*60)],
          [sg.Button('Ok', font=('Arial Bold', 12)), sg.Button('Cancel', font=('Arial Bold', 12))]]

# Create the Window
window = sg.Window('Cartoonifier', layout, element_justification='c', size=(600, 400))


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        # if user closes window or clicks cancel
        break

    line_wdt = int(values[0])
    blur_value = int(values[1])
    totalColors = int(values[2])

    # Get image file location
    filename = sg.popup_get_file('Source File ')

    # Reading image File
    img = read_img(filename)

    # Edge Detections
    edgeImg = edge_detection(img, line_wdt, blur_value)

    # Adding Color Quantisation
    img = color_quantisation(img, totalColors)
    blurred = cv2.bilateralFilter(img, d=7, sigmaColor=200, sigmaSpace=200)

    # Generating Cartoon
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edgeImg)

    # Creating Output
    if event == 'Ok':
        cv2.imwrite('cartoon.png', cartoon)
        image = Image.open('cartoon.png')
        new_image = image.resize((600, 400))
        new_image.save('cartoon.png')
        sg.popup_no_buttons('Image', title='Display image', keep_on_top=True, image='cartoon.png')
        cleanup()
        window.close()

window.close()
