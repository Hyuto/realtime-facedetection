from .model import load_model, Model, info

def run(CONFIG):
    n_class = len(CONFIG['PERSONS']) + 1
    
    info("Start Modelling Process..")
    model = Model(n_class)
    model.train_and_evaluate(CONFIG)