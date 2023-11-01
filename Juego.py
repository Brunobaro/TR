import pygame, sys
import random
import keyboard


pygame.init()
ancho, alto = 1920, 1080
joc = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Joc")

# Colors
blanco = (255, 255, 255)
azul = (0, 0, 255)
rojo = (255, 0, 0)
negro = (0, 0, 0)
amarillo = (255, 255, 0)
verde = (0, 255, 0)

colors = [blanco, azul, rojo, amarillo] 

#Text per iniciar el joc
font = pygame.font.Font(None, 100)
text = font.render("PRESIONA ENTER PER COMENÇAR", True, blanco)
posicion_text = (360, 200)

joc.fill(negro)
joc.blit(text, posicion_text)
pygame.display.flip()

tiempo_negro_1 = random.randint(500,1000)
tiempo_negro_2 = random.randint(500,1000)
tiempo_negro_3 = random.randint(500,1000)
tiempo_negro_4 = random.randint(500,1000)
tiempos_negros = [tiempo_negro_1, tiempo_negro_2, tiempo_negro_3, tiempo_negro_4]

#Moments en que la pantalla cambiarà de color, aleatori (en milisegons)
moment_event1 = random.randint(1000, 3000)
moment_event2 = random.randint(1000, 3000) + moment_event1 + tiempo_negro_1
moment_event3 = random.randint(1000, 3000) + moment_event2 + tiempo_negro_1 + tiempo_negro_2
moment_event4 = random.randint(1000, 3000) + moment_event3 + tiempo_negro_1 + tiempo_negro_2 + tiempo_negro_3

# Llista dels moments 
momentos_cambio_color = [moment_event1, moment_event2, moment_event3, moment_event4]

# Asociem una tecla a cada color
teclas_cambio = {blanco: pygame.K_q, azul: pygame.K_w, rojo: pygame.K_o, amarillo: pygame.K_p}

#Paràmetres que utilitzarem més tard
tiempos_reaccion = []
tecla_presionada = False
juego_comenzado = False
color_actual = None
indice_cambio_color = 0
tiempo_desde_cambio = None
cambios_totales = 0
# Fem el bucle que activi el joc
ejecutando = True
while ejecutando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False
        #Comencem el joc en presionar la tecla "enter"
        if event.type == pygame.KEYDOWN and not juego_comenzado:
            if event.key == pygame.K_RETURN:
                tiempo_inicial = pygame.time.get_ticks()
                juego_comenzado = True

    if juego_comenzado:
        tiempo = pygame.time.get_ticks()
        tiempo_actual = tiempo - tiempo_inicial

        #Llògica per canviar el color
        if indice_cambio_color < len(momentos_cambio_color):
            momento_cambio_actual = momentos_cambio_color[indice_cambio_color]
            momento_cambio_real = momento_cambio_actual + tiempos_negros[indice_cambio_color]

            if tiempo_actual >= momento_cambio_actual:
                joc.fill(negro)
                
            
            
            if tiempo_actual >= momento_cambio_real:
                color_actual = random.choice(colors)
                indice_cambio_color += 1
                joc.fill(color_actual)
                tecla_presionada = False
                cambios_totales +=1
            
        if color_actual:
             for color, tecla in teclas_cambio.items():
                if color == color_actual:
                        #Llògica per enregistrar el temps de reacció (si s'encerta)
                        if pygame.key.get_pressed()[tecla] and not tecla_presionada:
                            tecla_presionada = True
                            tiempo_desde_cambio = tiempo_actual - momentos_cambio_color[indice_cambio_color - 1] - tiempos_negros[indice_cambio_color - 1]
                            tiempos_reaccion.append(f"{tiempo_desde_cambio} ms")
                            
                            with open("DatosIA.txt", "a") as archivo:
                                archivo.write(f"{tiempo_desde_cambio}ms {color_actual}\n")

                            

                        elif any (pygame.key.get_pressed()) and not pygame.key.get_pressed()[tecla] and not tecla_presionada:
                            tecla_presionada = True
                            tiempos_reaccion.append("Error")
                            with open("DatosIA.txt", "a") as archivo:
                                archivo.write(f"error {color_actual}\n")

                            

                        
                            
    #Creació del text amb els resultats
    y = 200  
    for duracion in tiempos_reaccion:
        text2 = font.render(f"Temps de reacció: {duracion}", True, verde)
        joc.blit(text2, (360, y))
        y += 100  

    #Instruccions per tornar a intentar (pressionar r)
    font2 = pygame.font.Font(None, 125)
    if len(tiempos_reaccion) == len(momentos_cambio_color):
        text3 = font2.render(f"Presiona 'r' per tornar a probar", True, negro)
        joc.blit(text3, (330, 600))
    
    pygame.display.flip()
    
    #Llògica per reiniciar el joc
    if juego_comenzado and pygame.key.get_pressed()[pygame.K_r]:
                         
        tiempos_reaccion = []
        tecla_presionada = False
        color_actual = None
        indice_cambio_color = 0
        juego_comenzado = False
        tiempo_desde_cambio = None
        joc.fill(negro)
        keyboard.press_and_release('Enter')
        if cambios_totales >= 50:
            pygame.quit()
            sys.exit()    

# Tanquem pygame un cop acaba tot
pygame.quit()
sys.exit()