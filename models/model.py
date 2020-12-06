from os import environ
environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

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
        model.add(Conv2D(100,(3,3), input_shape=(IMG_SIZE, IMG_SIZE, 1)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Conv2D(100,(3,3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Flatten())
        model.add(Dropout(0.5))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(self.n_class, activation='softmax'))

        model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
        return model

    def train_and_evaluate(self, CONFIG):
        info("Get and spliting image data..")
        datagen = ImageDataGenerator(rescale = 1./255, rotation_range = 15, validation_split = CONFIG["MODEL"]["VALID-SIZE"])

        train = datagen.flow_from_directory(CONFIG["DATASET-DIR"], target_size=(CONFIG['IMG_SIZE'], CONFIG['IMG_SIZE']),
                                            batch_size = CONFIG["MODEL"]["BATCH-SIZE"], class_mode = "categorical", 
                                            color_mode = "grayscale", subset='training')
        valid = datagen.flow_from_directory(CONFIG["DATASET-DIR"], target_size=(CONFIG['IMG_SIZE'], CONFIG['IMG_SIZE']),
                                            color_mode = "grayscale", batch_size = CONFIG["MODEL"]["BATCH-SIZE"], class_mode = "categorical", subset='validation')

        info("Creating Model..")
        model = self.generate_model(CONFIG['IMG_SIZE'])

        checkpoint = ModelCheckpoint('models/best-model.h5', monitor='val_loss', verbose=0, 
                                    save_best_only=True, mode='auto')

        info("Fitting Model..")
        history = model.fit(train, steps_per_epoch = train.n//CONFIG["MODEL"]["BATCH-SIZE"], 
                            epochs = CONFIG["MODEL"]["EPOCHS"], validation_data=valid, callbacks=[checkpoint])

        info('Fitting Model Completed..')
        info(f'Getting model with {model.evaluate(valid, verbose = 0, return_dict = True)["accuracy"] * 100}% accuracy')

        self.model = load_model('models/best-model.h5')
        info('Modelling Process Completed')

def run(CONFIG, ret=True):
    n_class = len(CONFIG['PERSONS']) + 1
    
    info("Start Modelling Process..")
    model = Model(n_class)
    model.train_and_evaluate(CONFIG)
    
    if ret:
        return model