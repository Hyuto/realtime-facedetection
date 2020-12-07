from time import sleep
from shutil import rmtree
from os import mkdir, path, listdir
from logging import info, warning
import cv2

def TakePic(LIST_DIR:list, TO_DIR:str, SIZE:int, N_FRAME:int, model):
    """
    Take image and extract all frame that contain faces to generate dataset

    Args:
        LIST_DIR (str)  : List of image directory
        SIZE     (int)  : Image Size
        N_FRAME  (int)  : time for taking
        model           : faceCascade
    """
    mkdir(TO_DIR)
    count = 1
    while count < N_FRAME:
        for item in LIST_DIR:
            image = cv2.imread(item)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = model.detectMultiScale(gray, scaleFactor = 1.1, 
                                        minNeighbors = 5, minSize = (30, 30))
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(image, f"Frame taken {count}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
                img = gray[y:y+h, x:x+w]
                resize = cv2.resize(img, (SIZE, SIZE))
                if count <= N_FRAME:
                    cv2.imwrite(path.join(TO_DIR, f'{count} .jpg'), resize)
                    count += 1
                else:
                    break

def TakeVid(name:str, DIR:str, SIZE:int, N_FRAME:int, model):
    """
    Take video and extract all frame that contain faces to generate dataset

    Args:
        name (str)    : Person name
        DIR (str)     : Directory
        SIZE (int)    : Image Size
        N_FRAME (int) : time for taking
        model         : faceCascade
    """
    cap = cv2.VideoCapture(0)
    count = 1
    while(cap.isOpened()):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = model.detectMultiScale(gray, scaleFactor = 1.1, 
                                       minNeighbors = 5, minSize = (30, 30))

        if cv2.waitKey(1) and count > N_FRAME:
            break

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Frame taken {count}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            img = gray[y:y+h, x:x+w]
            resize = cv2.resize(img, (SIZE, SIZE))
            cv2.imwrite(path.join(DIR, f'{count} .jpg'), resize)
            if count <= N_FRAME:
                count += 1
            else:
                break
        
        cv2.imshow(name, frame)

    cap.release()
    cv2.destroyAllWindows()

def run(CONFIG:dict):
    """
    Run dataset generator

    Args:
        CONFIG (dict): Configuration
    """
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Extracting random person face data
    info("Generating data for random person face..")
    LIST_ITEM_DIR = [path.join(CONFIG['IMAGE_DATA']['RANDOM_FACE_SRC_DATA_DIR'], item) 
                for item in listdir(CONFIG['IMAGE_DATA']['RANDOM_FACE_SRC_DATA_DIR'])]
    TO_DIR = path.join(CONFIG['IMAGE_DATA']['DIR'], "0")
    if path.isdir(TO_DIR):
        rmtree(TO_DIR)
    TakePic(LIST_ITEM_DIR, TO_DIR, CONFIG['IMAGE_DATA']['SIZE'], 
            CONFIG['IMAGE_DATA']['N_FRAME_TAKEN'], faceCascade)
    info("Success generating data for random person face..")

    for item in (CONFIG['PERSONS']):
        info(f'Taking data for {item}..')
        condition = True

        # Look for item dir
        ITEM_DIR = path.join(CONFIG['IMAGE_DATA']['DIR'], item)
        if path.isdir(ITEM_DIR):
            warning(f'Previous dataset for {item} detected')
            warning(f"Do you wan't to delete previous dataset for {item} and take new data?")

            while True:
                USER_INPUT = input("Input [y/n] : ").lower()
                if USER_INPUT in ['y', 'n']:
                    break
                warning('Invalid Input')
            
            if USER_INPUT == 'y':
                warning('Deleting previous dataset')
                rmtree(ITEM_DIR)
            else:
                condition = False
        
        if condition:
            mkdir(ITEM_DIR)

            info(input("Please tap anything if you're ready.."))

            # Take
            TakeVid(item, ITEM_DIR, CONFIG['IMAGE_DATA']['SIZE'], 
                    CONFIG['IMAGE_DATA']['N_FRAME_TAKEN'], faceCascade)

            info(f'Done taking data for {item}')
        sleep(1) 

    info('Completed generating dataset')