from manim import *
import numpy as np

class corazon(Scene):
    def construct(self):

        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-1, 3, 1],
            x_length=6,
            y_length=5,
            axis_config={"color": WHITE, "stroke_width": 3},
            tips=True,
        )

        k = ValueTracker(0)

        def heart(x):
            if abs(x) > np.sqrt(3):
                return np.nan
            return np.cbrt(x**2) + 0.9 * np.sin(k.get_value() * x) * np.sqrt(3 - x**2)

        grafico = always_redraw(lambda: axes.plot(
            heart,
            x_range=[-1.73, 1.73, 0.01],
            color=RED_C,
            use_smoothing=True,
        ))


        ecuacion = MathTex(
            r"y = x^{\frac{2}{3}} + 0.9\sin(kx)\sqrt{3 - x^2}",
            color=RED_C,
            font_size=36
        ).to_edge(DOWN, buff=1.2).scale(2.2).shift(DOWN*3)

        k_label = always_redraw(lambda:
            MathTex(
                rf"k = {k.get_value():.2f}",#nunca aplicar cambios a grupos que contienen variables con always redraw 
                color=RED_C,
                font_size=80
            ).next_to(ecuacion, DOWN, buff=0.5)
        ).shift(DOWN*0.5)

        titulo = Text("Ecuacion de corazon", color=RED_C, font_size=40).to_edge(UP)
        grupo=VGroup(axes,grafico,titulo)
        grupo.shift(UP*2).scale(1.6)
        self.play(Write(axes), Write(grafico),Write(ecuacion), Write(k_label),Write(titulo))
        self.wait(0.5)
        
        self.play(k.animate.set_value(100), run_time=7, rate_func=smooth)
        self.wait(0.5)
