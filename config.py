from os import path
from json import dumps, load

class Config(object):
    def __init__(self):
        self.config = {
            "RUNNING-COMMAND":"__all__",
            "IMG_SIZE":224,
            "n_person":"AUTO",
            "persons":[],
            "n_frame":200
            }

    def to_file(self):
        with open('config.json', 'w') as f:
            f.write(dumps(self.config, indent=2))

    def get_config(self):
        if path.isfile('config.json'):
            with open('config.json') as f:
                config = load(f)

            for x in config:
                try:
                    self.config[x] = config[x]
                except:
                    raise KeyError(f'Invalid arg {x} in config.json')

            if self.config['n_person'].lower() == "auto" and self.config['persons'] == []:
                raise NotImplementedError("Dataset not generated. Please fill either 'n_person' or 'persons' in config.json")
            elif type(self.config['n_person']) == int and self.config['persons'] == []:
                self.config['persons'] = [i for i in range(1, self.config['n_person'] + 1)]

            return self.config

        else:
            raise EnvironmentError("file config.json didn't exist, please run with args get-config to get it.")