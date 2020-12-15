# Import libs
from sys import argv
from logging import error
from coloredlogs import install

# RFD
from RFD.config import *
import RFD.dataset
import RFD.models
import RFD.detector

def get_commands(CONFIG):
    validate = lambda x : x in ['generate-dataset', 'train-evaluate-model', 'live-detection']
    if type(CONFIG['RUNNING_COMMAND']) == str:
        if CONFIG['RUNNING_COMMAND'].lower() == '__all__':
            return ['generate-dataset', 'train-evaluate-model', 'live-detection']
        elif validate(CONFIG['RUNNING_COMMAND'].lower()):
            return [CONFIG['RUNNING_COMMAND'].lower()]
    elif type(CONFIG['RUNNING_COMMAND']) == list:
        CONFIG['RUNNING_COMMAND'] = [x.lower() for x in CONFIG['RUNNING_COMMAND']]
        if len(CONFIG['RUNNING_COMMAND']) == 1:
            CONFIG['RUNNING_COMMAND'] = CONFIG['RUNNING_COMMAND'][0]
            return get_commands(CONFIG)
        elif '__all__' not in CONFIG['RUNNING_COMMAND'] and all([validate(x) for x in CONFIG['RUNNING_COMMAND']]):
            return CONFIG['RUNNING_COMMAND']
    raise KeyError("Invalid RUNNING_COMMAND!")

def run(key, CONFIG):
    if key == 'generate-dataset':
        RFD.dataset.run(CONFIG)
    elif key == 'train-evaluate-model':
        RFD.models.run(CONFIG)
    else:
        if CONFIG['MODEL']['LATEST'] != None:
            MODEL = RFD.models.load_model(path.join(CONFIG['MODEL']['DIR'], CONFIG['MODEL']['LATEST']))
            RFD.detector.Live(MODEL, CONFIG)
        else:
            error("Not Found Trained model. Please check 'LATEST' argument in 'MODEL' at config.json")

if __name__ == "__main__":
    args = argv[1:]
    if args != []:
        install()
        main, args = args[0].lower(), args[1:]
        config = Config()

        if main == 'get-config':
            config.to_file()
        elif main == 'run':
            CONFIG = config.get_config()
            commands = get_commands(CONFIG)
            for command in commands:
                run(command, CONFIG)
        else:
            raise KeyError("Command didn't exist!")
    else:
        print(
            """
Realtime Face Detection 
setup.py is designed for running RFD code with these commands:
'get-config' : to generate config.json file
'run'        : to run RFD code with configurations based on config.json file
            """
        )