from manim import *
import numpy as np

class GraficoDiscretoDoble(Scene):
    def construct(self):
        config.frame_width = 9 # esto cambia el bastidor a uno de dimensiones invertidas al 16:9 , es 9:16 por lo que tengo otro espacio y proporciones 
        config.frame_height = 16    
        axes = Axes(
            x_range=[2012, 2022, 1],
            y_range=[4.8, 7.8, 0.3],
            x_length=8,
            y_length=8,
            axis_config={"include_tip": False},

        )
        axes.add_coordinates( # ajustes finos de add cordinates
            font_size=35
        )

        for label in axes.x_axis.numbers:
            valor = int(label.get_value())
            label.become(Text(str(valor)).scale(0.4).move_to(label))

        y_axis_right = NumberLine(
        x_range=[50, 86, 4],
         length=5,
        )

        y_axis_right.add_numbers(font_size=24)

        # rotarlo para que sea vertical
        y_axis_right.rotate(PI/2)

        # alinearlo con el eje izquierdo (misma altura)
        y_axis_right.match_height(axes.y_axis) # igualo tamanio de ejes.ejey

        # moverlo al extremo derecho del eje X
        y_axis_right.next_to(axes.x_axis, RIGHT, buff=-0.25) # lo pongo justo al ladito del eje x 

        # subirlo para que coincida con el origen
        y_axis_right.align_to(axes.y_axis, DOWN) # alineo el eje y derecho con la parte inferior del eje y izquierdo 
        y_axis_right.shift(DOWN * 0.025)

        # años
        years = [2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]

        # línea punteada (degrees - negro en la imagen)
        values_deg = [4.8,4.9,5.0,5.3,6.1,7.4,7.3,6.2,6.2,6.3]

        # línea continua (hydropower - rojo en la imagen)
        # (reescalada aprox para que calce en el mismo eje)
        values_hydro = [4.9,4.8,5.4,5.2,5.8,7.4,7.2,5.9,6.3,6.4]

        # convertir a coordenadas
        points_deg = [axes.c2p(x, y) for x, y in zip(years, values_deg)] # agrega puntos a un sistema cordenado en referencia a axes
        points_hydro = [axes.c2p(x, y) for x, y in zip(years, values_hydro)]

        graph_deg = VMobject()
        graph_deg.set_points_as_corners(points_deg)
        graph_deg.set_color(BLUE_C)
        graph_deg.set_stroke(width=3)  # efecto punteado

        # curva continua (naranjo)
        graph_hydro = VMobject()
        graph_hydro.set_points_as_corners(points_hydro)
        graph_hydro.set_color(ORANGE)
        graph_hydro.set_stroke(width=4)

        # puntos
        dots_deg = VGroup(*[Dot(p, color=BLUE_C, radius=0.05) for p in points_deg]) # a cada punto c2p le da un grosor
        dots_hydro = VGroup(*[Dot(p, color=ORANGE, radius=0.05) for p in points_hydro])

        # animación
        title1 = Text(
            "Títulos de maestría otorgados\nen tecnologías de ingeniería",
            font_size=60,
            color=BLUE_C
        )

        subtitle = Text("correlacionan con", font_size=60)

        title2 = Text(
            "Energía hidroeléctrica \n generada en Vietnam",
            font_size=60,
            color=ORANGE
        )

        # agrupar en vertical
        title_group = VGroup(title1, subtitle, title2).arrange(DOWN, buff=0.4)

        # mover arriba de la escena
        title_group.to_edge(UP,buff=0.1) # lo muevo al borde superior
        title_group.shift(UP * 3)

        grafico = VGroup(
            axes,
            y_axis_right,
            graph_deg,
            graph_hydro,
            dots_deg,
            dots_hydro
        )
        grafico.scale(1.2, about_point=axes.get_center())
        grafico.shift(DOWN * 1.5)

        label_left = Text("Titulos de Maestria (miles)", font_size=35,color=BLUE_C)
        label_right = Text("Billones de kWh", font_size=35,color=ORANGE)
        label_left.rotate(PI/2)
        label_right.rotate(-PI/2)

        label_left.next_to(axes.y_axis, LEFT, buff=0.5)
        label_right.next_to(y_axis_right, RIGHT, buff=0.5)

        label_left.align_to(axes.y_axis, UP)
        label_right.align_to(y_axis_right, UP)

        ref1 = Text(
            "Títulos de maestría en ingeniería · Fuente: NCES",
            font_size=20,
            color=GRAY
        )

        ref2 = Text(
            "Energía hidroeléctrica en Vietnam · Fuente: EIA",
            font_size=20,
            color=GRAY
        )

        corr = Text(
            "2012–2021 · r = 0.969 · r² = 0.939 · p < 0.01",
            font_size=20,
            color=GRAY
        )

        # líneas tipo leyenda
        line_blue = Line(LEFT, RIGHT).scale(0.3).set_color(BLUE_C)
        line_orange = Line(LEFT, RIGHT).scale(0.3).set_color(ORANGE)

        legend1 = VGroup(line_blue, ref1).arrange(RIGHT, buff=0.2)
        legend2 = VGroup(line_orange, ref2).arrange(RIGHT, buff=0.2)

        # agrupar todo
        refs = VGroup(legend1, legend2, corr).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.2
        ).scale(1.8)

        # posicionar abajo
        refs.to_edge(DOWN, buff=0.4)
        refs.shift(DOWN*2)

        
        #self.play(DrawBorderThenFill(axes),DrawBorderThenFill(y_axis_right))
        #self.play(LaggedStart(*[FadeIn(dot) for dot in dots_deg], lag_ratio=0.1),FadeIn(label_left), FadeIn(label_right)) # aparecen los puntos uno a uno con undesface , el lagged start

        self.play(AnimationGroup(DrawBorderThenFill(axes),DrawBorderThenFill(y_axis_right),LaggedStart(*[FadeIn(dot) for dot in dots_deg], lag_ratio=0.1),lag_ratio=0.2))

        #self.play(Create(graph_deg), run_time=1.2, rate_func=linear)
        #self.play(FadeIn(dots_hydro)) # aparecen todos los puntos al mismo tiempo
        self.play(AnimationGroup(Create(graph_deg,run_time=1.5, rate_func=linear),FadeIn(dots_hydro,run_time=1.5),Create(graph_hydro,run_time=2),lag_ratio=0.4)) # laggedstrt funciona para animaciones finas de varios elementos chicos de una animacion y lag ratio 
        #funciona con animationgroup para solapar dos animaciones distintas 
        #self.play(Create(graph_hydro),run_time=1.5)

        self.play(Write(title_group),FadeIn(label_left), FadeIn(label_right), run_time=1) # animacion titulos

        self.play(LaggedStart(*[FadeIn(r) for r in refs], lag_ratio=0.2))

        self.wait()

#grafico doble , en funcion de variable comun e