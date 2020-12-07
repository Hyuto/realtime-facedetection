from sys import argv
from coloredlogs import install
from config import *

from os import environ
saved_environ = {x:environ[x] for x in ['OPENCV_VIDEOIO_PRIORITY_MSMF', 'TF_CPP_MIN_LOG_LEVEL']}
environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'
environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import dataset.generate_dataset
import models.model
import detector.detector

if __name__ == "__main__":
    install()
    args = argv[1:]
    main, args = args[0].lower(), args[1:]
    config = Config()

    if main == 'get-config':
        config.to_file()
    elif main == 'run':
        CONFIG = config.get_config()
        
        if CONFIG['RUNNING_COMMAND'].lower() == '__all__':
            dataset.generate_dataset.run(CONFIG)
            models.model.run(CONFIG)
            MODEL = models.model.load_model(path.join(CONFIG['MODEL']['DIR'], CONFIG['MODEL']['LATEST']))
            detector.detector.Live(MODEL, CONFIG)

        elif CONFIG['RUNNING_COMMAND'].lower() == 'generate-dataset':
            dataset.generate_dataset.run(CONFIG)

        elif CONFIG['RUNNING_COMMAND'].lower() == 'train-evaluate-model':
            models.model.run(CONFIG, ret = False)

        elif CONFIG['RUNNING_COMMAND'].lower() == 'live-detection':
            MODEL = models.model.load_model(path.join(CONFIG['MODEL']['DIR'], CONFIG['MODEL']['LATEST']))
            detector.detector.Live(MODEL, CONFIG)
            
        else:
            raise EnvironmentError("Invalid RUNNING-COMMAND!")
    else:
        raise EnvironmentError("Command didn't exist!")

    for x in saved_environ:
        environ[x] = saved_environ[x]