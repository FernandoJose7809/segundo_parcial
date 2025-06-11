import os
import pickle

class Prediccion:
    def __init__(self):
        self.modelo = self.cargar_modelo()

    def cargar_modelo(self):
        MODEL_PATH = os.path.join(os.path.dirname(__file__), 'modelo_segundo_parcial.pkl')
        with open(MODEL_PATH, 'rb') as f:
            modelo = pickle.load(f)
        return modelo

    def nota_final(self, year, participation, homework, attendance, exam):
        datos = [[year, participation, homework, attendance, exam]]
        prediccion = self.modelo.predict(datos)
        return prediccion[0]
