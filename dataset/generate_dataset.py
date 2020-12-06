from time import sleep
from shutil import rmtree
from os import mkdir, path
import cv2, logging

def TakePic(name:str, DIR:str, SIZE:int, N_FRAME:int, model):
    """
    Take all frame of to generate dataset

    Args:
        name (str)   : Person name
        DIR (str)    : Directory
        SIZE (int)   : Image Size
        N_FRAME(int) : time for taking
        model        : faceCascade
    """
    cap = cv2.VideoCapture(0)
    count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = model.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if cv2.waitKey(1) and count >= N_FRAME:
            break

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Frame taken {count}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            img = gray[y:y+h, x:x+w]
            resize = cv2.resize(img, (SIZE, SIZE))
            cv2.imwrite(path.join(DIR, f'{count} .jpg'), resize)
            count += 1
        
        cv2.imshow(name, frame)

    cap.release()
    cv2.destroyAllWindows()

def run(config:dict, DIR:str):
    """
    Run dataset generator

    Args:
        items (list): all person names
        DIR (str): Dataset folder directory
        SIZE (int): Image size
    """
    count = set()
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    for i, item in enumerate(config['persons']):
        logging.info(f'Taking data for {item}..')
        
        # Look for item dir
        ITEM_DIR = path.join(DIR, item)
        if path.isdir(ITEM_DIR):
            logging.warning(f'Previous dataset for {item} detected')
            logging.warning('Deleting previous dataset')
            rmtree(ITEM_DIR)
        mkdir(ITEM_DIR)

        logging.info(input("Please tap anything if you're ready.."))

        # Take
        TakePic(item, ITEM_DIR, config['IMG_SIZE'], config['n_frame'], faceCascade)

        logging.info(f'Done taking data for {item}')
        sleep(1)

    logging.info('Completed generating dataset')