import cv2
import os
import sys
import time
import datetime
import serial
import facebook
from PIL import Image
import numpy

counter = 0
WEBCAM_DEVICE = 0
STORAGE_DIR = 'storage'
x = 5
ArduinoUnoSerial = serial.Serial('/dev/ttyACM0', 9600)
foreground = Image.open("filtro.png")

graph = facebook.GraphAPI(
    access_token="EAACEdEose0cBAAKvdHizf1bGQaY6vCdAf9rZCt04ORSxffCXzGZCRkkr3ElIyBZAmNy0KrNV9lNe53RGIxlvrvZBQsqk9eSymYW8KZB6KMbhRmFCaHWTol7qaaU2i1CL1wZC2Xga1khAevjOqCAXwxcrsBkfstsZABeL6lHjWghdipqVZCUAPBhNaZAeBQwNIiwd89mKU4qDmEQZDZD")


def imgedit(foto):

    background = Image.open(foto)
    foreground = Image.open("filtro.png")
    background.paste(foreground, (0, 0), foreground)
    background.save('editado'+str(counter)+'.jpg')
    return ('editado'+str(counter)+'.jpg')


def imgeditint1(foto):

    background = Image.open(foto)
    foreground = Image.open("interface1-640x480.png")
    background.paste(foreground, (0, 0), foreground)
    background.save('editado'+str(counter)+'.jpg')
    return ('editado'+str(counter)+'.jpg')


def imgeditint2(foto):

    background = Image.open(foto)
    foreground = Image.open("interface2-640x480.png")
    background.paste(foreground, (0, 0), foreground)
    background.save('editado'+str(counter)+'.jpg')
    return ('editado'+str(counter)+'.jpg')

def imgeditint3(foto):

    background = Image.open(foto)
    foreground = Image.open("interface3-640x480.png")
    background.paste(foreground, (0, 0), foreground)
    background.save('temp.jpg')
    return ('temp.jpg')

def screenEdit(screen):

    background = Image.open(screen)
    foreground = Image.open("filtro.png")
    background.paste(foreground, (0, 0), foreground)
    return background


def putText(img, text, location, positive=True):

    font = cv2.FONT_HERSHEY_SIMPLEX
    fsize = 5
    colour = (0, 255, 0) if positive else (0, 0, 255)
    if location == 'left_button':
        cv2.putText(img, text, (0, img.shape[0] - 10),
                    font, fsize, colour)
    elif location == 'right_button':
        cv2.putText(
            img, text,
            (int(img.shape[1] - 60*len(text)), int(img.shape[0] - 10)),
            font, fsize, colour)
    elif location == 'centre':
        cv2.putText(
            img, text,
            (int(img.shape[1] / 2 - 60*len(text)), int(img.shape[0] / 2)),
            font, fsize, colour, 4)


if __name__ == '__main__':
    # open webcam and UI
    cap = cv2.VideoCapture(WEBCAM_DEVICE)
    screen = 'Som na Rural'
    cv2.namedWindow(screen, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(screen, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)

    # show webcam and wait for user input
    while True:

        # TELA 0
        img2 = cv2.imread('interface0-640x480.png')
        while ArduinoUnoSerial.inWaiting() == 0:
            ret, frame = cap.read()
            img = frame
            img_ui = img.copy()
            # para espelhar a imagem so descomentar
            # img = cv2.flip(img, 1)
            blended = cv2.addWeighted(img, 0.8, img2, 0.5, 1)
            cv2.imshow(screen, blended)
            keypress = cv2.waitKey(1)
        # TELA 0

        if ArduinoUnoSerial.read(1) == b'1':  # serial read 1: take photo
            # TELA 1 - DELAY DE CONTAGEM + SORRIA
            print("tela 1")
            while x > 0:
                milli_sec = int(round(time.time() * 1000))
                while(int(round(time.time() * 1000)) - milli_sec < 1000):
                    ret, frame = cap.read()
                    img = frame
                    img_ui = img.copy()
                    putText(img_ui, str(x), 'centre', True)
                    cv2.imshow(screen, img_ui)
                    keypress = cv2.waitKey(1)
                milli_sec = int(round(time.time() * 1000))
                while(int(round(time.time() * 1000)) - milli_sec < 500):
                    ret, frame = cap.read()
                    img = frame
                    img_ui = img.copy()
                    cv2.imshow(screen, img_ui)
                    keypress = cv2.waitKey(1)
                x = x - 1
            # TELA 1 - DELAY DE CONTAGEM + SORRIA
            x = 5

            # TELA 2
            dado_recebido = ArduinoUnoSerial.read(1)
            while(dado_recebido != b'1' and dado_recebido != b'2'):
                dado_recebido = ArduinoUnoSerial.read(1)
                print("tela 2")
                img2 = cv2.imread('interface1-640x480.png')
                img = frame
                img_ui = img.copy()
                blended = cv2.addWeighted(img, 0.8, img2, 0.5, 1)
                filename = os.path.join(
                    os.getcwd(), STORAGE_DIR, "temp.jpg")
                cv2.imwrite(filename, img)
                imgedit(filename)
                img_readed = cv2.imread(imgeditint1(filename))

                cv2.imshow(screen, img_readed)
                keypress = cv2.waitKey(1)
            # TELA 2

            # TELA 3
            if dado_recebido == b'1':
                cv2.waitKey(1)
                print("tela 3")

                dado_recebido = ArduinoUnoSerial.read(1)
                while(dado_recebido == b'1' and dado_recebido == b'2'):
                    cv2.waitKey(1)
                    dado_recebido = ArduinoUnoSerial.read(1)

                while dado_recebido != b'1' and dado_recebido != b'2':
                    img2 = cv2.imread('interface2-640x480.png')
                    img = frame
                    img_ui = img.copy()
                    filename = os.path.join(
                        os.getcwd(), STORAGE_DIR, "temp.jpg")
                    cv2.imwrite(filename, img)
                    imgedit(filename)
                    img_readed = cv2.imread(imgeditint2(filename))
                    cv2.imshow(screen, img_readed)
                    keypress = cv2.waitKey(1)
                    dado_recebido = ArduinoUnoSerial.read(1)

            else:
                print("foi no else")
                continue
            # TELA 3

            # TELA 4
            if dado_recebido == b'1':
                cv2.waitKey(1)
                print("tela 4")

                dado_recebido = ArduinoUnoSerial.read(1)
                while(dado_recebido == b'1' and dado_recebido == b'2'):
                    cv2.waitKey(1)
                    dado_recebido = ArduinoUnoSerial.read(1)

                milli_sec = int(round(time.time() * 1000))
                
                img = frame
                filename = os.path.join(
                    os.getcwd(), STORAGE_DIR, "temp.jpg")
                cv2.imwrite(filename, img)
                imgedit(filename)
                
                while int(round(time.time() * 1000)) - milli_sec < 2000:
                    img2 = cv2.imread('interface3-640x480.png')
                    img = frame
                    img_ui = img.copy()
                    blended = cv2.addWeighted(img, 0.8, img2, 0.5, 1)
                    img_readed = cv2.imread(imgeditint3(filename))
                    cv2.imshow(screen, img_readed)
                    keypress = cv2.waitKey(1)
                    dado_recebido = ArduinoUnoSerial.read(1)

            else:
                continue

            # TELA 4

    cv2.waitKey(1)
