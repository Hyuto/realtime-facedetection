# Import libs
import argparse, os
from logging import error
from coloredlogs import install

# RFD
from RFD.config import Config
import RFD.dataset
import RFD.models
import RFD.detector

def run(key, CONFIG):
    if key == 'generate-dataset':
        RFD.dataset.run(CONFIG)
    elif key == 'train-evaluate-model':
        RFD.models.run(CONFIG)
    else:
        if CONFIG['MODEL']['LATEST'] != None:
            MODEL = RFD.models.load_model(os.path.join(CONFIG['MODEL']['DIR'], CONFIG['MODEL']['LATEST']))
            RFD.detector.Live(MODEL, CONFIG)
        else:
            error("Not Found Trained model. Please check 'LATEST' argument in 'MODEL' at config.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup script to run RFD")
    parser.add_argument("-r", "--run",
                        help="Running RFD",
                        action='store_true')
    parser.add_argument("-gc", "--get_config",
                        help="Generate config.json file",
                        action='store_true')
    args = parser.parse_args()
    
    install()
    config = Config()

    if args.run:
        commands = config.get_commands()
        for command in commands:
            run(command, config.config)
    elif args.get_config:
        config.to_file()