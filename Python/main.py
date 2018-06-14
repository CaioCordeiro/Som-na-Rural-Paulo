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

ArduinoUnoSerial = serial.Serial('COM4', 9600)

graph = facebook.GraphAPI(access_token="EAACEdEose0cBAKZAlZC9lIKn9P2ny3KIZAHZCGSsJgRTiHfyBChKlJ8ZC5P4vWnnYxpp7j7kNsOjM9UHJkNzVrSENWWBuQN9rAjXn3HqbY6GCvAhoIfshVVwiJa5A8o5RlyaEi89KlR2O6FPQwQOeSZAJ1DLg5SoOoJMulLzOTRixcgUesm3mfM76nB019hv3Y0fgRB2P7agZDZD")
def imgedit(foto): 

    background = Image.open(foto)
    foreground = Image.open("fg.png")
    background.paste(foreground, (0, 0), foreground)
    background.save('editado'+str(counter)+'.jpg')
   
    graph.put_photo(image=open('editado'+str(counter)+'.jpg', 'rb'), message='Look at this cool photo!')

def putText(img, text, location, positive=True):

    font = cv2.FONT_HERSHEY_DUPLEX
    fsize = 2
    colour = (0, 255, 0) if positive else (255, 0, 0)
    if location == 'left_button':
        cv2.putText(img, text, (0, img.shape[0] - 10),
                    font, fsize, colour)
    elif location == 'right_button':
        cv2.putText(
            img, text,
            (int(img.shape[1] - 40*len(text)), int(img.shape[0] - 10)),
            font, fsize, colour)
    elif location == 'centre':
        cv2.putText(
            img, text,
            (int(img.shape[1] / 2 - 20*len(text)), int(img.shape[0] / 2)),
            font, fsize, colour)


if __name__ == '__main__':
    # open webcam and UI
    cap = cv2.VideoCapture(WEBCAM_DEVICE)
    screen = 'Som na Rural'
    cv2.namedWindow(screen, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(screen, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)

    # show webcam and wait for user input
    while True:
        while ArduinoUnoSerial.inWaiting() == 0:
            ret, frame = cap.read()
            img = frame
            img_ui = img.copy()
            putText(img_ui, "TIRAR", 'left_button', True)
            cv2.imshow(screen, img_ui)
            keypress = cv2.waitKey(1)

        if ArduinoUnoSerial.read(1) == b'1':  # serial read 1: take photo
            # take snapshot, wait for user input

            img_ui = img.copy()
            putText(img_ui, "SALVAR", 'left_button', True)
            putText(img_ui, "REPETIR", 'right_button', False)
            cv2.imshow(screen, img_ui)
            keypress = cv2.waitKey(1)
            time.sleep(1)
            # if ArduinoUnoSerial.read(1) == b'1':  # serial read 1: print
            dado_recebido = ArduinoUnoSerial.read(1)
            while(dado_recebido == b'0'):
                dado_recebido = ArduinoUnoSerial.read(1)
                cv2.waitKey(3)

            if dado_recebido == b'1':  # serial read 1: print
                conter = counter+1
                img_ui = img.copy()
                putText(img_ui, "SALVANDO(5)", 'centre', True)
                cv2.imshow(screen, img_ui)
                cv2.waitKey(1)

                datestr = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = os.path.join(
                    os.getcwd(), STORAGE_DIR, datestr + ".jpg")
                cv2.imwrite(filename, img)
               
                imgedit(filename)
                counter = counter + 1


                
              
                for i in range(4, 0, -1):
                    time.sleep(1)
                    img_ui = img.copy()
                    putText(img_ui, "SALVANDO({})".format(i), 'centre', True)
                    cv2.imshow(screen, img_ui)
                    cv2.waitKey(1)

            elif dado_recebido == b'2':
                cv2.waitKey(1)
                continue  # retake

    cv2.waitKey(1)
