import joblib
import os
import pickle

# Ruta relativa dentro de la app

class Predicion:
    def notaFinal(self, Year, Participation, Homework, Attendance, Exam):
        modelo = self.cargar_modelo()
        datos = [[Year, Participation, Homework, Attendance, Exam]]
        prediccion = modelo.predict(datos)
        return prediccion[0]  # Devolver solo el número

    def cargar_modelo(self):
        MODEL_PATH = os.path.join(os.path.dirname(__file__), 'modelo_segundo_parcial.pkl')
        with open(MODEL_PATH, 'rb') as f:
            modelo = pickle.load(f)
        return modelo