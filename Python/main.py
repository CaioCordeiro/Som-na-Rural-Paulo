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
ArduinoUnoSerial = serial.Serial('COM4', 9600)
foreground = Image.open("filtro-640x480.png")

graph = facebook.GraphAPI(
    access_token="EAACEdEose0cBAKgmn9ZB0Ke8BbmZB0JtYyI0WynjfLXrWA4g5TZCapREmhTkrwG87Nw8gVwaue8Ykrj5UvjgBwYsZATBvfO4xI3kVeK4Qj2PNjHnoJg3GX59DLA7dA1wSvOHL5IEALLxsX6rd5Q6jsU4kV6ZCPgkT4V8Sc6jZBoW9ZCEj8HVeZA8ZAt2uuYhOGxF27kUQcyxn9VVMZCjghczhA")


def imgedit(foto):

    background = Image.open(foto)
    foreground = Image.open("filtro-640x480.png")
    background.paste(foreground, (0, 0), foreground)
    datestr = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    background.save('./storage/'+datestr+'.jpg')
    return ('./storage/'+datestr+'.jpg')

def imgeditintpreview(foto):

    background = Image.open(foto)
    foreground = Image.open("filtro-640x480.png")
    background.paste(foreground, (0, 0), foreground)
    background.save('temp.jpg')
    return ('temp.jpg')

def imgeditint1(foto):

    background = Image.open(foto)
    foreground = Image.open("TELA3.png")
    background.paste(foreground, (0, 0), foreground)
    background.save('temp.jpg')
    return ('temp.jpg')


def imgeditint2(foto):

    background = Image.open(foto)
    foreground = Image.open("TELA4.png")
    background.paste(foreground, (0, 0), foreground)
    background.save('temp.jpg')
    return ('temp.jpg')

def imgeditint3(foto):

    background = Image.open(foto)
    foreground = Image.open("TELA5.png")
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
        img2 = cv2.imread('TELA1.png')
        while ArduinoUnoSerial.inWaiting() == 0:
            ret, frame = cap.read()
            img = frame
            img_ui = img.copy()
            # para espelhar a imagem so descomentar
            # img = cv2.flip(img, 1)
            blended = cv2.addWeighted(img, 0.9 , img2, 0.2, 1.9)
            cv2.imshow(screen, blended)
            keypress = cv2.waitKey(1)
        # TELA 0

        if ArduinoUnoSerial.read(1) == b'1':  # serial read 1: take photo
            # TELA 1 - DELAY DE CONTAGEM + SORRIA
            print("tela 1")
            imgsorria = cv2.imread('TELA2.png')
            while x > 0:
                milli_sec = int(round(time.time() * 1000))
                while(int(round(time.time() * 1000)) - milli_sec < 500):
                    ret, frame = cap.read()
                    img = frame
                    img_ui = img.copy()
                    blended = cv2.addWeighted(img, 0.9 , imgsorria, 0.2, 1.9)
                    putText(blended, str(x), 'centre', True)
                    cv2.imshow(screen, blended)
                    keypress = cv2.waitKey(1)
                milli_sec = int(round(time.time() * 1000))
                while(int(round(time.time() * 1000)) - milli_sec < 150):
                    ret, frame = cap.read()
                    img = frame
                    img_ui = img.copy()
                    blended = cv2.addWeighted(img, 0.9 , imgsorria, 0.2, 1.9)
                    cv2.imshow(screen, blended)
                    keypress = cv2.waitKey(1)
                x = x - 1
            # TELA 1 - DELAY DE CONTAGEM + SORRIA
            x = 5

            milli_sec = int(round(time.time() * 1000))
            while(int(round(time.time() * 1000)) - milli_sec < 1000):
                img = frame
                img_ui = img.copy()
                filename = os.path.join(
                    os.getcwd(), STORAGE_DIR, "temp.jpg")
                cv2.imwrite(filename, img)
                img_readed = cv2.imread(imgeditintpreview(filename))

                cv2.imshow(screen, img_readed)
                keypress = cv2.waitKey(1)

            # TELA 2
            dado_recebido = ArduinoUnoSerial.read(1)
            while(dado_recebido != b'1' and dado_recebido != b'2'):
                dado_recebido = ArduinoUnoSerial.read(1)
                print("tela 2")
                img2 = cv2.imread('interface1-640x480.png')
                img = frame
                img_ui = img.copy()
                filename = os.path.join(
                    os.getcwd(), STORAGE_DIR, "temp.jpg")
                cv2.imwrite(filename, img)
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
                
                while int(round(time.time() * 1000)) - milli_sec < 5000:
                    img2 = cv2.imread('interface3-640x480.png')
                    img = frame
                    img_ui = img.copy()
                    img_readed = cv2.imread(imgeditint3(filename))
                    cv2.imshow(screen, img_readed)
                    keypress = cv2.waitKey(1)
                    dado_recebido = ArduinoUnoSerial.read(1)

            else:
                continue

            # TELA 4

    cv2.waitKey(1)
