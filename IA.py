import tensorflow as tf
from tensorflow import keras
from PIL import ImageGrab
import numpy as np
import time, cv2
import pyautogui as auto
import keyboard


colors = np.array([
    [1,1,1],  # Blanco
    [0,0,1],  # Azul
    [1,0,0],  # Rojo
    [1,1,0]   # Amarillo
])





teclas = np.array([
    [1, 0, 0, 0],  # 'q'
    [0, 1, 0, 0],  # 'w'
    [0, 0, 1, 0],  # 'o'
    [0, 0, 0, 1]   # 'p'
])


colors_prueba = np.array([(1,1,1), (1,0,0), (1,1,0), (1,1,0), (0,0,1), (1,0,0), (1,1,1), (1,1,0), (1,0,0), (0,0,1), (1,0,0), (0,0,1), (1,0,0), (0,0,1), (1,1,1), (1,0,0), (1,1,1), (1,0,0)])
tecla_prueba = np.array([(1,0,0,0), (0,0,1,0) , (0,0,0,1), (0,0,0,1), (0,1,0,0), (0,0,1,0), (1,0,0,0), (0,0,0,1), (0,0,1,0), (0,1,0,0), (0,0,1,0), (0,1,0,0), (0,0,1,0), (0,1,0,0), (1,0,0,0), (0,0,1,0), (1,0,0,0), (0,0,1,0)])

# Crear un model secuencial

model = keras.Sequential()

# Agregar una capa densa amb 4 neurones de sortida
model.add(keras.layers.Dense(units = 4, input_shape = (3,) , activation='softmax'))

# Compilar el modelo
model.compile(loss='categorical_crossentropy', optimizer = tf.keras.optimizers.Adam(1))
Entrenament_completat = False
while not Entrenament_completat:
    print("Entrenant")
    Entrenament = model.fit(colors_prueba, tecla_prueba, epochs = 100, verbose = False)
    Entrenament_completat = True
print("Entrenament complert")

model.summary()



tecla_anterior = None
Descans =  0.01 #segons
encés = True

while encés:
    if keyboard.is_pressed('Esc'):
        encés = False

    Pantalla = ImageGrab.grab(bbox = (10,10,20,20))

    Imatge = Pantalla.resize((40,30))

    Imatge.save('C:/Users/bbaro/TR/Imatge.png')

    color_anterior = None

    Color = np.array(Imatge)
    Color_processat = cv2.resize(Color, (3,1))/255.0
    Tecla_ia_presionada = False
    

    if np.all(Color_processat == [1, 1, 1]) or \
   np.all(Color_processat == [1, 1, 0]) or \
   np.all(Color_processat == [1, 0, 0]) or \
   np.all(Color_processat == [0, 0, 1]):
        
        if not np.all(Color_processat == color_anterior):
            predicció = model.predict([[Color_processat]])
            predicció_real = np.round(predicció) 
            teclas_map = {0:'q', 1:'w', 2:'o', 3:'p'}
            tecla_correcta = [teclas_map[np.argmax(fila)] for fila in predicció_real]
            color_anterior = Color_processat
        
    
            if not Tecla_ia_presionada:
                print("Predicción real:", predicció_real)
                keyboard.press_and_release(tecla_correcta)
                Tecla_ia_presionada = True
    
            
    time.sleep(Descans)


