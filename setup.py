import os
from sys import argv
from coloredlogs import install
from json import dumps, load
import dataset.generate_dataset

class Config(object):
    def __init__(self):
        self.config = {
            "IMG_SIZE":224,
            "n_person":"AUTO",
            "persons":[]
            }

    def to_file(self):
        with open('config.json', 'w') as f:
            f.write(dumps(self.config, indent=2))

    def get_config(self):
        if os.path.isfile('config.json'):
            with open('config.json') as f:
                config = load(f)

            for x in config:
                try:
                    self.config[x] = config[x]
                except:
                    raise KeyError(f'Invalid arg {x} in config.json')
            return self.config

        else:
            raise EnvironmentError("file config.json didn't exist, please run with args get-config to get it.")

if __name__ == "__main__":
    install()
    args = argv[1:]
    main, args = args[0], args[1:]
    config = Config()

    if main == 'get-config':
        config.to_file()
    elif main == 'run':
        CONFIG = config.get_config()
        
        dataset.generate_dataset.run(
            CONFIG['persons'],
            os.path.dirname(dataset.__file__),
            CONFIG['IMG_SIZE']
        )
    else:
        raise EnvironmentError("Command didn't exist!")