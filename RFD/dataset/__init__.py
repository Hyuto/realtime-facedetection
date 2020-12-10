from time import sleep
from .take import *
from .. import rmtree
from .. import path, listdir, mkdir
from .. import info, warning

def run(CONFIG:dict):
    """
    Run dataset generator

    Args:
        CONFIG (dict): Configuration
    """

    # Extracting random person face data
    info("Generating data for random person face..")
    LIST_ITEM_DIR = [path.join(CONFIG['IMAGE_DATA']['RANDOM_FACE_SRC_DATA_DIR'], item) 
                for item in listdir(CONFIG['IMAGE_DATA']['RANDOM_FACE_SRC_DATA_DIR'])]
    TO_DIR = path.join(CONFIG['IMAGE_DATA']['DIR'], "0")
    if path.isdir(TO_DIR):
        rmtree(TO_DIR)
    TakePic(LIST_ITEM_DIR, TO_DIR, CONFIG['IMAGE_DATA']['SIZE'], 
            CONFIG['IMAGE_DATA']['N_FRAME_TAKEN'])
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
                    CONFIG['IMAGE_DATA']['N_FRAME_TAKEN'])

            info(f'Done taking data for {item}')
        sleep(1) 

    info('Completed generating dataset')