from sys import argv
from coloredlogs import install

from RFD.config import *
import RFD.dataset
import RFD.models
import RFD.detector

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
            RFD.dataset.run(CONFIG)
            RFD.models.run(CONFIG)
            MODEL = RFD.models.load_model(path.join(CONFIG['MODEL']['DIR'], CONFIG['MODEL']['LATEST']))
            RFD.detector.Live(MODEL, CONFIG)

        elif CONFIG['RUNNING_COMMAND'].lower() == 'generate-dataset':
            RFD.dataset.run(CONFIG)

        elif CONFIG['RUNNING_COMMAND'].lower() == 'train-evaluate-model':
            RFD.models.run(CONFIG)

        elif CONFIG['RUNNING_COMMAND'].lower() == 'live-detection':
            MODEL = RFD.models.load_model(path.join(CONFIG['MODEL']['DIR'], CONFIG['MODEL']['LATEST']))
            RFD.detector.Live(MODEL, CONFIG)
            
        else:
            raise EnvironmentError("Invalid RUNNING-COMMAND!")
    else:
        raise EnvironmentError("Command didn't exist!")