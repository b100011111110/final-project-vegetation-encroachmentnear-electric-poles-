from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Dense, Dropout
import pickle

def LoadDllModel():
    model = load_model('./MyModel.h5')
    print("model loaded successfully")
    print(model.summary())
    return model

def loadMLmodels(modelfile):
    loaded_obj = None
    with open(modelfile, 'rb') as file:
        loaded_obj = pickle.load(file)
    return loaded_obj