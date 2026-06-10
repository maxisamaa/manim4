from manim import *

class Cronometro(Scene):
    def construct(self):

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
        texto.next_to(circulo, DOWN, buff=0.5)

        cronometro = VGroup(
            circulo,
            boton,
            manecilla,
            marcas,
            texto)
        
        cronometro.scale(1.5)
        self.play(Create(circulo),Create(boton),Create(manecilla),Write(marcas))
        self.play(Write(texto),Rotate(
                manecilla,
                angle=-PI/8,
                about_point=ORIGIN
            ),
            run_time=1.5,)

        self.wait()

