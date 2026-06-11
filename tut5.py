from manim import *
from pathlib import Path
import math

# 3 cartas
class cartas(MovingCameraScene):
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

        cartas.arrange(
            RIGHT,
            buff=0.7
        )

        cartas.scale(1.5) # 1.5 para 3 objetos

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
            cartas.animate.shift(UP * 9),# era 9
            run_time=1
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
        self.wait(0.5)

        todas_las_filas = VGroup()

        todas_las_filas.add(cartas)

        # -------------------------------------------------
        # CREAR TODAS LAS PERMUTACIONES
        # -------------------------------------------------
        cartas_estatico=cartas
        
        for i, combinacion in enumerate(permutaciones,start=1):# start=1 solo cambia el orden de las posiciones 
            
            cartas = cartas.copy()

            self.add(cartas)

            self.play(
                cartas.animate.shift(
                    DOWN * (3.5) # cambiar de 1  3.5 , para 3 cartas
                ),
                run_time=0.4
            )

            animaciones = []
            if i>3:
                animaciones.append(self.camera.frame.animate.shift(3.5*DOWN))
            for j in range(len(cartas)):
                carta = cartas[j]
                for indice,elemento in enumerate(cartas_estatico):
                    if carta.id_carta==elemento.id_carta:
                        indice1=indice

                        indice_destino = combinacion[indice1]

                        posicion_destino = posiciones_originales[indice_destino]

                        posicion_destino = posicion_destino + DOWN * 3.5 * i # cambiar 1 a 3.5 , 3 cartas

                        animaciones.append(carta.animate.move_to(posicion_destino))

                        break
            
            todas_las_filas.add(cartas)
            # self.play(*animaciones,
            # self.camera.frame.animate.move_to(cartas_puntero.get_center()), run_time=0.6)
            self.play(*animaciones, run_time=0.6)
            
#centro_destino = posiciones_originales[1] + DOWN * 3.5 * i  # columna del medio
#self.play(*animaciones,
#self.camera.frame.animate.move_to(centro_destino), run_time=0.6)

        #cronometro
        # borde exterior
        radio=1.5
        circulo = Circle(radius=radio)
        circulo.set_stroke(width=8,color=RED)

        # botón superior
        boton = Rectangle(
            width=0.8,
            height=0.4
        ).next_to(circulo, UP, buff=0.2)
        boton.set_stroke(width=5)

        # manecilla
        manecilla = Line(
            ORIGIN,
            UP * 1,
            stroke_width=10
        )

        marcas=VGroup()
        for i in range(12):
            marca = Line(
                UP * (radio*0.8),
                UP * (radio*0.9)
            )

            marca.rotate(
                i * TAU / 12,
                about_point=ORIGIN
            )

            marcas.add(marca)

        texto = Text(
            "6 segundos",
            font_size=50
        )
        texto.next_to(circulo, DOWN*2, buff=0.5)
        texto2 = Text(
            "Si 1 permutacion equivale \n"
            "a 1 segundo entonces :",
            font_size=64
        )
        texto2.next_to(circulo, UP*16, buff=0.2)

        cronometro = VGroup(
            circulo,
            boton,
            manecilla,
            marcas,
            texto)
        cronometro.scale(1.5)

        anim_cartas = todas_las_filas.animate.shift(LEFT * 12)
        anim_cronometro = AnimationGroup(Create(circulo), Create(boton),Create(manecilla), Write(marcas),Write(texto2))
        self.play(AnimationGroup(anim_cartas,anim_cronometro,lag_ratio=0.5))
        self.wait(1)
        self.play(Write(texto),Rotate(
                manecilla,
                angle=-PI/8,
                about_point=ORIGIN
            ),
            run_time=1.5,)
        self.wait(1)

        grupoCompleto=VGroup(circulo,
            boton,
            manecilla,
            marcas,
            texto,texto2)
        self.play(grupoCompleto.animate.shift(LEFT*13),run_time=1)

