from manim import *
from pathlib import Path
import math

#codigo que genera cartas desde la fila original 

class cartas(Scene):
    def construct(self):
        # FUNCION RECURSIVA
        def permutar(lista):
            if len(lista) == 0:
                return [[]] # aqui se genera la lista de listas que luego se va rellenando hacia arriba.# 0! es 1 
            resultado = []
            for i in range(len(lista)): 
                actual = lista[i]
                permutaciones_restantes = permutar(lista[:i] + lista[i+1:]) # en algun momento esto queda pelao asi [] 
                for p in permutaciones_restantes: #como el primer elemento que vale p es []debido a que itera sobre [[]]
                    resultado.append([actual] + p)
            return resultado
        
        # LEER Y RENOMBRAR SVG AUTOMATICAMENTE
        carpeta = Path("assets")
        archivos = carpeta.glob("*.svg")
        
        for i, archivo in enumerate(archivos):
            # Usamos concatenación (+) y convertimos i a string con str()
            numero_con_cero = str(i).zfill(2) # para evitar que sorted ordene mal , el 11 despues del 1 
            nuevo_nombre = carpeta / ("pokercard" + numero_con_cero + ".svg")

            archivo.rename(nuevo_nombre)

        # volver a leerlos ya renombrados
        archivos = sorted(
            carpeta.glob("pokercard*.svg")
        )

        # -------------------------------------------------
        # CREAR CARTAS BASE
        # -------------------------------------------------

        cartas = VGroup()

        for archivo in archivos:

            carta = SVGMobject(archivo)

            carta.set_stroke(
                WHITE,
                width=0.2
            )

            carta.set_fill(
                WHITE,
                opacity=1
            )

            cartas.add(carta)

        cartas.arrange(
            RIGHT,
            buff=0.7
        )

        cartas.scale(1.5)

        # -------------------------------------------------
        # MOSTRAR CARTAS ORIGINALES
        # -------------------------------------------------

        self.play(*[Write(carta)for carta in cartas],run_time=1) # el * desempaqueta la lista a elementos separados por una coma
        #[Write(carta)for carta in cartas]  ES IGUAL A  
        #animaciones = []
        #for carta in cartas:
         #   animacion = Write(carta)
          #  animaciones.append(animacion)
           #     self.wait()

        # SUBIR GRUPO ORIGINAL

        self.play(
            cartas.animate.shift(UP * 9),
            run_time=1.2
        )

        # GENERAR PERMUTACIONES

        lista = list(range(len(cartas))) # list(range (4)) es  [0,1,2,3]

        permutaciones = permutar(lista)

        permutaciones = permutaciones[1:] # elimino la primera permutacion 

        # -------------------------------------------------
        # PRIMERA FILA
        # -------------------------------------------------

        posiciones_originales = [
            carta.get_center()
            for carta in cartas
        ]
        self.wait()

        # -------------------------------------------------
        # CREAR TODAS LAS PERMUTACIONES
        # -------------------------------------------------

        for i, combinacion in enumerate(permutaciones,start=1):# start=1 solo cambia el orden de las posiciones 

            nuevo_grupo = cartas.copy()

            self.add(nuevo_grupo)

            self.play(
                nuevo_grupo.animate.shift(
                    DOWN * (3.5*i)
                ),
                run_time=0.4
            )

            animaciones = []

            for j in range(len(nuevo_grupo)):

                carta = nuevo_grupo[j]

                indice_destino = combinacion[j]

                posicion_destino = posiciones_originales[indice_destino]

                posicion_destino = posicion_destino + DOWN * 3.5 * i

                animaciones.append(
                    carta.animate.move_to(posicion_destino)
                )

            self.play(*animaciones, run_time=0.6)

        self.wait(2)