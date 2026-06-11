from manim import *
from pathlib import Path
import math
import numpy as np

class cartas(MovingCameraScene):
    def construct(self):
        
        # LEER Y RENOMBRAR SVG AUTOMATICAMENTE
        carpeta = Path("assets3")
        archivos = carpeta.glob("*.svg")
        
        for i, archivo in enumerate(archivos):
            # Usamos concatenación (+) y convertimos i a string con str()
            numero_con_cero = str(i).zfill(2) # para evitar que sorted ordene mal , el 11 despues del 1 
            nuevo_nombre = carpeta / ("pokercard" + numero_con_cero + ".svg")

            archivo.rename(nuevo_nombre)

        # volver a leerlos ya renombrados
        archivos = sorted(carpeta.glob("pokercard*.svg"))

        # -------------------------------------------------
        # CREAR CARTAS BASE
        # -------------------------------------------------

        cartas = VGroup()

        for indice_archivo,archivo in enumerate(archivos):

            carta = SVGMobject(archivo)

            carta.id_carta = indice_archivo

            carta.set_stroke(
                WHITE,
                width=0.2
            )

            carta.set_fill(
                WHITE,
                opacity=1
            )

            cartas.add(carta)

        # cartas.arrange(
        #     RIGHT,
        #     buff=-0.3
        # )
        fondos=VGroup()
        for i, carta in enumerate(cartas):
            carta.shift(UP*8+DOWN*0.35*i+LEFT*3)
            carta.set_z_index(i)
            fondo = RoundedRectangle(
            corner_radius=0.15,
            width=carta.width,
            height=carta.height,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0
        )
            fondo.move_to(carta)
            #fondos.add(fondo)
            fondos.add(fondo) # el que quiero dibujar
            fondo.set_z_index(i*0.9999)
            self.add(fondo)
            

        cartas.scale(1.2) # 1.5 para 3 objetos
        fondos.scale(1.2)
        cartas.stretch(1.5, dim=0)
        fondos.stretch(1.5, dim=0)

        # -------------------------------------------------
        # MOSTRAR CARTAS ORIGINALES
        # -------------------------------------------------

        self.play(*[Write(carta)for carta in cartas],*[Write(fondo)for fondo in fondos],run_time=1) # el * desempaqueta la lista a elementos separados por una coma
        #[Write(carta)for carta in cartas]  ES IGUAL A  
        #animaciones = []
        #for carta in cartas:
         #   animacion = Write(carta)
          #  animaciones.append(animacion)
        self.wait(2)