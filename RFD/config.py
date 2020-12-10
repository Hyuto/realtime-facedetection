from . import path, mkdir
from . import info, warning
from . import dumps, load

class Config(object):
    def __init__(self):
        self.config = {
            "RUNNING_COMMAND": "__all__",
            "N_PERSON": "AUTO",
            "PERSONS": [],
            "OUTPUT_DIR": "output",
            "IMAGE_DATA": {
                "SIZE": 224,
                "N_FRAME_TAKEN": 200,
                "DIR": "output\\Image Data",
                "RANDOM_FACE_SRC_DATA_DIR": "RFD\\dataset\\random_data_src"
            },
            "MODEL": {
                "EPOCHS": 5,
                "BATCH_SIZE": 32,
                "VALID_SIZE": 0.2,
                "DIR": "output\\Models",
                "LATEST": None
            }
        }

    def to_file(self):
        with open('config.json', 'w') as f:
            f.write(dumps(self.config, indent=2))

    @staticmethod
    def validating(act_obj, obj):
        for x in obj:
            try:
                if type(act_obj[x]) == dict:
                    Config.validating(act_obj[x], obj[x])
                else:
                    act_obj[x] = obj[x]
            except:
                raise KeyError(f'Invalid arg {x} in config.json')

    @staticmethod
    def CheckDir(DIR:str, name:str):
        """
        Checking if Directory is available

        Args:
            DIR (str): Directory
            name (str): Name
        """
        if not path.isdir(DIR):
            warning(f'{name} directory not found')
            info(f'Making new directory for {path.basename(DIR)}')
            mkdir(DIR)

    def get_config(self):
        if path.isfile('config.json'):
            info('Setting Configuration..')
            with open('config.json') as f:
                config = load(f)
                
            self.validating(self.config, config)

            if self.config['N_PERSON'].lower() == "auto" and self.config['PERSONS'] == []:
                raise NotImplementedError("Dataset not generated. Please fill either 'n_person' or 'persons' in config.json")
            elif type(self.config['N_PERSON']) == int and self.config['PERSONS'] == []:
                self.config['PERSONS'] = [i for i in range(1, self.config['N_PERSON'] + 1)]

            # Check Directory
            self.CheckDir(self.config['OUTPUT_DIR'], 'Output Directory')
            self.CheckDir(self.config['IMAGE_DATA']['DIR'], 'Image dataset')
            self.CheckDir(self.config['IMAGE_DATA']['RANDOM_FACE_SRC_DATA_DIR'], 'Random face source data')
            self.CheckDir(self.config['MODEL']['DIR'], 'Model')

            return self.config

        else:
            raise EnvironmentError("file config.json didn't exist, please run with args get-config to get it.")