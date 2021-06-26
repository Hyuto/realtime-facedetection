from json import dumps
from os import path, listdir
from logging import info, warning

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Activation, Flatten, Dropout, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator

class Model:
    def __init__(self, n_class):
        self.n_class = n_class

    def generate_model(self, IMG_SIZE):
        model=Sequential()
        model.add(Conv2D(100, (3,3), input_shape=(IMG_SIZE, IMG_SIZE, 1)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size = (2,2)))
        model.add(Conv2D(100, (3,3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size = (2,2)))
        model.add(Flatten())
        model.add(Dropout(0.5))
        model.add(Dense(50, activation = 'relu'))
        model.add(Dense(self.n_class, activation = 'softmax'))

        model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
        return model

    def get_name(self, PATH):
        name_generator = lambda x : f'Model {x}.h5'
        list_model, i = listdir(PATH), 1
        while True:
            name = name_generator(i)
            if name not in list_model:
                self.name = path.join(PATH, name)
                break
            i += 1

    def train_and_evaluate(self, CONFIG):
        info("Get and spliting image data..")
        datagen = ImageDataGenerator(rescale = 1./255, rotation_range = 5, validation_split = CONFIG["MODEL"]["VALID_SIZE"])

        train = datagen.flow_from_directory(CONFIG["IMAGE_DATA"]["DIR"], target_size = (CONFIG['IMAGE_DATA']['SIZE'], CONFIG['IMAGE_DATA']['SIZE']),
                                            batch_size = CONFIG["MODEL"]["BATCH_SIZE"], class_mode = "categorical", 
                                            color_mode = "grayscale", subset='training')
        valid = datagen.flow_from_directory(CONFIG["IMAGE_DATA"]["DIR"], target_size = (CONFIG['IMAGE_DATA']['SIZE'], CONFIG['IMAGE_DATA']['SIZE']),
                                            batch_size = CONFIG["MODEL"]["BATCH_SIZE"], class_mode = "categorical", 
                                            color_mode = "grayscale", subset='validation')

        info("Creating Model..")
        model = self.generate_model(CONFIG['IMAGE_DATA']['SIZE'])

        self.get_name(CONFIG['MODEL']['DIR'])
        checkpoint = ModelCheckpoint(self.name, monitor='val_loss', verbose = 0, 
                                    save_best_only=True, mode='auto')

        info("Fitting Model..")
        history = model.fit(train, steps_per_epoch = train.n//CONFIG["MODEL"]["BATCH_SIZE"], epochs = CONFIG["MODEL"]["EPOCHS"], 
                            validation_data = valid, callbacks = [checkpoint])

        info('Fitting Model Completed..')
        info(f'Getting model with {model.evaluate(valid, verbose = 0, return_dict = True)["accuracy"] * 100}% accuracy')

        self.model = load_model(self.name)

        CONFIG['MODEL']['LATEST'] = path.basename(self.name)
        with open('config.json', 'w') as f:
            f.write(dumps(CONFIG, indent=2))

        info('Modelling Process Completed')