from sys import argv
from coloredlogs import install
from config import *
import dataset.generate_dataset

if __name__ == "__main__":
    install()
    args = argv[1:]
    main, args = args[0], args[1:]
    config = Config()

    if main == 'get-config':
        config.to_file()
    elif main == 'run':
        CONFIG = config.get_config()
        
        if CONFIG['RUNNING-COMMAND'] == '__all__':
            dataset.generate_dataset.run(CONFIG, path.dirname(dataset.__file__))
        elif CONFIG['RUNNING-COMMAND'] == 'generate-dataset':
            dataset.generate_dataset.run(CONFIG, path.dirname(dataset.__file__))
        else:
            raise EnvironmentError("Invalid RUNNING-COMMAND!")
    else:
        raise EnvironmentError("Command didn't exist!")