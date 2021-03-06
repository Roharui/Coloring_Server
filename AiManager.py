
import tensorflow.python.util.deprecation as deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False

from tensorflow.keras.models import load_model
import numpy as np
from colorManager import ColorManager
import json

def convert(o):
    if isinstance(o, np.int32): return int(o)  
    raise TypeError

class AiManager:
    def do(self, data):
        result = ""
        model = load_model('CRM.h5')
        data = list(map(int, data[0].split(',')))
        data = (np.array([data]) / 255).astype('float32')
        colors = model.predict(data)[0]
        colors = ((np.array(colors) + 0.3) * 255).astype(int)
        for co in colors:
            for c in co:
                if c > 255.0:
                    c = 255
                result += str(c) + ","
        return result[:-1]


if __name__ == '__main__':
    a = AiManager()
    print(a.do((0, 255, 255)))
