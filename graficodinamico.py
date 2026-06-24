from manim import *
import math

class EscalaDinamica(Scene):
    def construct(self):
        #titulos y parrafos
        titulo = Text( 
            "Diferencia de tamaños entre\n"
            "dos contribuciones sociales\n"
            "medidos en escala lineal",
            font_size=40,
            color=WHITE,
        )

        titulo2 = Paragraph(
            "50 mil millones",
            "versus",
            "22 billones",
            "(22 millones de millones)",

            alignment="center",

            font_size=40
        )
        titulo.shift(UP*9)
        titulo2.shift(UP*6)

        tracker = ValueTracker(1)

        # valor fijo barra pequeña
        valor_pequeno = 1

        # calcula el maximo del eje
        def max_y():
            return max(5, tracker.get_value() * 1.2)

        # calcula particiones dinamicas
        def obtener_paso(valor):

            if valor < 10:
                return 1

            magnitud = 10 ** math.floor(math.log10(valor))

            return magnitud // 2

        # eje dinamico

        axes = always_redraw(
            lambda: Axes(x_range=[0, 2, 1],y_range=[0,max_y(),obtener_paso(tracker.get_value())],
                x_length=8, # tamanio en pantalla 
                y_length=12,
                axis_config={
                    "include_tip": False,
                    "decimal_number_config": {
                        "num_decimal_places": 0,
                        "group_with_commas": True}},
                x_axis_config={
                    "include_ticks": False,
                    "include_numbers": False},y_axis_config={"include_numbers": True}
                    ).shift(DOWN*4)) #.add_coordinates()
        # ---------------- BARRA PEQUEÑA ----------------
        barra1 = always_redraw(
            lambda: Rectangle(
                width=1,# altura proporcional al eje actual
                height=(valor_pequeno / max_y()) * 12, #1 es la altura del grafico en Y
                fill_color=BLUE,
                fill_opacity=1,
                stroke_width=0
            ).move_to(axes.c2p(0.8, 0),aligned_edge=DOWN))

        # ---------------- BARRA GRANDE ----------------

        barra2 = always_redraw(
            lambda: Rectangle(
                width=1,

                # altura proporcional
                height=(tracker.get_value() / max_y()) * 12,

                fill_color=RED,
                fill_opacity=1,
                stroke_width=0).move_to(axes.c2p(1.6, 0),
                aligned_edge=DOWN))

        # numero arriba
        valor = always_redraw(
            lambda: DecimalNumber(
                tracker.get_value(),
                num_decimal_places=0,
                font_size=40
            ).next_to(barra2, UP)
        )
        valor2 = always_redraw(
            lambda: DecimalNumber(
                valor_pequeno,
                num_decimal_places=0,
                font_size=40
            ).next_to(barra1, UP)
        )
        label1 = Text(
            "Teletón",
            font_size=30).next_to(axes.c2p(0.8, 0),DOWN)

        label2 = Paragraph(
            "7% del PIB",
            "evadido",
            "por empresas",
            alignment="center",
            font_size=30).next_to(
            axes.c2p(1.6, 0),DOWN)

        self.play(Write(axes), Write(barra1),Write(barra2),Write(valor),Write(valor2))
        self.play(Write(titulo),Write(titulo2),Write(label1),Write(label2))
        self.play(tracker.animate.set_value(440),run_time=10,rate_func=smooth)
        self.wait()



class EscalaDinamica2(Scene): # este tiene bien la parte de los titulosd el eje x , pero se buggea la animacion del eje y
    def construct(self):

        # ---------------- ESCALA REAL ----------------

        ESCALA_REAL = 50_000_000_000

        # ---------------- FUNCION FORMATO ----------------

        def formatear_numero(n):
            return f"{int(n):,}".replace(",", ".")

        # ---------------- TRACKER ----------------

        tracker = ValueTracker(1)

        # valor fijo barra pequeña
        valor_pequeno = 1

        # ---------------- ESCALA DINAMICA ----------------

        def max_y():
            return max(5, tracker.get_value() * 1.2)

        def obtener_paso(valor):

            if valor < 10:
                return 1

            magnitud = 10 ** math.floor(math.log10(valor))

            return magnitud / 2

        # ---------------- EJE ----------------

        axes = always_redraw(
            lambda: Axes(
                x_range=[0, 2, 1],y_range=[0,max_y(),obtener_paso(tracker.get_value())],
                x_length=8,
                y_length=12,
                axis_config={
                    "include_tip": False,
                },
                x_axis_config={
                    "include_ticks": False,
                    "include_numbers": False
                }).shift(DOWN * 4))

        # ---------------- ETIQUETAS Y ----------------

        y_labels = always_redraw(
            lambda: VGroup(*[
                Text(
                    formatear_numero(y * ESCALA_REAL),
                    font_size=24
                ).next_to(
                    axes.c2p(0, y),
                    LEFT,
                    buff=0.2
                )

                for y in np.arange(
                    0,
                    max_y(),
                    obtener_paso(tracker.get_value())
                )

            ])
        )

        # ---------------- BARRA PEQUEÑA ----------------

        barra1 = always_redraw(
            lambda: Rectangle(
                width=1,

                height=
                (valor_pequeno / max_y()) * 12,

                fill_color=BLUE,
                fill_opacity=1,
                stroke_width=0

            ).move_to(
                axes.c2p(0.7, 0),
                aligned_edge=DOWN
            )
        )

        # ---------------- BARRA GRANDE ----------------

        barra2 = always_redraw(
            lambda: Rectangle(
                width=1,

                height=
                (tracker.get_value() / max_y()) * 12,

                fill_color=RED,
                fill_opacity=1,
                stroke_width=0

            ).move_to(
                axes.c2p(2, 0),
                aligned_edge=DOWN
            )
        )

        # ---------------- NUMERO ARRIBA ----------------

        valor = always_redraw(
            lambda: Text(
                formatear_numero(
                    tracker.get_value() * ESCALA_REAL
                ),
                font_size=32
            ).next_to(barra2, UP)
        )

        # ---------------- ETIQUETAS BARRAS ----------------

        label1 = Text(
            "Teletón",
            font_size=28
        ).next_to(
            axes.c2p(0.7, 0),
            DOWN
        )

        label2 = Paragraph(
            "7% del PIB",
            "evadido",
            "por empresas",

            alignment="center",

            font_size=24

        ).next_to(
            axes.c2p(2, 0),
            DOWN
        )

        # ---------------- ANIMACIONES ----------------

        self.play(
            Write(axes),
            Write(y_labels),
            Write(barra1),
            Write(barra2),
            Write(valor)
        )

        self.play(
            Write(titulo),
            Write(titulo2),
            Write(label1),
            Write(label2)
        )

        # ---------------- CRECIMIENTO ----------------

        self.play(
            tracker.animate.set_value(440),
            run_time=10,
            rate_func=smooth
        )

        self.wait()