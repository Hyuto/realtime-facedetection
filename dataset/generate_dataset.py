from time import sleep
from shutil import rmtree
from os import mkdir, path
from logging import info, warning
import cv2

def TakePic(name:str, DIR:str, SIZE:int, N_FRAME:int, model, src = 0):
    """
    Take all frame of to generate dataset

    Args:
        name (str)   : Person name
        DIR (str)    : Directory
        SIZE (int)   : Image Size
        N_FRAME(int) : time for taking
        model        : faceCascade
        src          : frame source. Default = 0 [webcam]
    """
    cap = cv2.VideoCapture(src)
    count = 1
    while(cap.isOpened()):
        ret, frame = cap.read()
        if (src != 0 and count <= 1) or src == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = model.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )

        if cv2.waitKey(1) and count > N_FRAME:
            break

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Frame taken {count}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            img = gray[y:y+h, x:x+w]
            resize = cv2.resize(img, (SIZE, SIZE))
            if count <= N_FRAME:
                cv2.imwrite(path.join(DIR, f'{count} .jpg'), resize)
                count += 1
        
        if src == 0:
            cv2.imshow(name, frame)

    cap.release()
    cv2.destroyAllWindows()

def run(config:dict, DIR:str):
    """
    Run dataset generator

    Args:
        config (dict): Configuration
        DIR (str): Dataset folder directory
    """
    if not path.isdir(DIR):
        warning('Image data directory not found')
        info(f'Making new directory for {path.basename(DIR)}')
        mkdir(DIR)
    
    count = set()
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    for item in (["0"] + config['PERSONS']):
        info(f'Taking data for {item}..')
        
        # Look for item dir
        ITEM_DIR = path.join(DIR, item)
        if path.isdir(ITEM_DIR):
            warning(f'Previous dataset for {item} detected')
            warning('Deleting previous dataset')
            rmtree(ITEM_DIR)
        mkdir(ITEM_DIR)

        if item != "0":
            info(input("Please tap anything if you're ready.."))

            # Take
            TakePic(item, ITEM_DIR, config['IMG_SIZE'], config['N_FRAME'], faceCascade)

            info(f'Done taking data for {item}')
            sleep(1)
        else: # Extracting random person face data
            info("Generating data for random person face..")
            TakePic(item, ITEM_DIR, config['IMG_SIZE'], config['N_FRAME'], 
                    faceCascade, src = path.join(DIR, "../random-people.jpeg"))
            info("Success generating data for random person face..")

    info('Completed generating dataset')