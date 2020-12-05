from time import time, sleep
from shutil import rmtree
from os import mkdir, path
import cv2, logging

def TakePic(name:str, DIR:str, SIZE:int):
    """
    Take all frame of to generate dataset

    Args:
        name (str): Person name
        DIR (str): Directory
        SIZE (int): Image Size
    """
    START = time()
    cap = cv2.VideoCapture(0)
    count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        cv2.imshow(name, frame)

        if cv2.waitKey(1) and int(time() - START) >= 10:
            break

        resize = cv2.resize(frame, (SIZE, SIZE))
        cv2.imwrite(path.join(DIR, f'{count} .jpg'), resize)
        count += 1

    cap.release()
    cv2.destroyAllWindows()

def run(items:list, DIR:str, SIZE:int):
    """
    Run dataset generator

    Args:
        items (list): all person names
        DIR (str): Dataset folder directory
        SIZE (int): Image size
    """
    for item in items:
        logging.info(f'Taking data for {item}..')
        
        DIR = path.join(DIR, item)
        if path.isdir(DIR):
            logging.warning(f'Previous dataset for {item} detected')
            logging.warning('Deleting previous dataset')
            rmtree(DIR)
        mkdir(DIR)

        logging.info(input("Please tap anything if you're ready.."))

        TakePic(item, DIR, SIZE)
        logging.info(f'Done taking data for {item}')
        sleep(1)

    logging.info('Completed generating dataset')