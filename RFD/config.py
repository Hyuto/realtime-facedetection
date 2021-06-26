from os import path, mkdir
from logging import info, warning
from json import dumps, load

class Config(object):
    """
    Setup & Validate configuration for `config.json`
    """
    def __init__(self):
        self.config = {
            "RUNNING_COMMAND": "__all__",
            "N_PERSON": "AUTO",
            "PERSONS": [],
            "OUTPUT_DIR": "output",
            "IMAGE_DATA": {
                "SIZE": 224,
                "N_FRAME_TAKEN": 200,
                "DIR": "output/Image Data",
                "RANDOM_FACE_SRC_DATA_DIR": "RFD/dataset/random_data_src"
            },
            "MODEL": {
                "EPOCHS": 5,
                "BATCH_SIZE": 32,
                "VALID_SIZE": 0.2,
                "DIR": "output/Models",
                "LATEST": None
            }
        }

    def to_file(self):
        """
        Render new `config.json` file
        """
        with open('config.json', 'w') as f:
            f.write(dumps(self.config, indent=2))

    @staticmethod
    def validating(act_obj, obj:dict):
        """
        Validating `config.json`

        Args:
            act_obj      : Object from `config.json`
            obj ([dict]) : True Object

        Raises:
            KeyError: If there's any object on `config.json` that not registered on system actual config
        """
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
            DIR (str)  : Directory
            name (str) : Name
        """
        if not path.isdir(DIR):
            warning(f'{name} directory not found')
            info(f'Making new directory for {path.basename(DIR)}')
            mkdir(DIR)

    def get_config(self) -> dict:
        """
        Get configuration setup from `config.json`
        """
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

        else:
            raise EnvironmentError("file config.json didn't exist, please run with args get-config to get it.")

    def get_commands(self) -> dict:
        """
        Prepare runable command

        Raises:
            KeyError: Invalid RUNNING_COMMAND!

        Returns:
            dict: runable command
        """
        # Get good to go configurations
        self.get_config()

        validate = lambda x : x in ['generate-dataset', 'train-evaluate-model', 'live-detection']
        if type(self.config['RUNNING_COMMAND']) == str:
            if self.config['RUNNING_COMMAND'].lower() == '__all__':
                return ['generate-dataset', 'train-evaluate-model', 'live-detection']
            elif validate(self.config['RUNNING_COMMAND'].lower()):
                return [self.config['RUNNING_COMMAND'].lower()]
        elif type(self.config['RUNNING_COMMAND']) == list:
            self.config['RUNNING_COMMAND'] = [x.lower() for x in self.config['RUNNING_COMMAND']]
            if len(self.config['RUNNING_COMMAND']) == 1:
                self.config['RUNNING_COMMAND'] = self.config['RUNNING_COMMAND'][0]
                return get_commands(self.config)
            elif '__all__' not in self.config['RUNNING_COMMAND'] and all([validate(x) for x in self.config['RUNNING_COMMAND']]):
                return self.config['RUNNING_COMMAND']
        raise KeyError("Invalid RUNNING_COMMAND!")