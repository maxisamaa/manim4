from manim import *
import math

class EscalaDinamica(Scene):
    # ---------------- ESCALA REAL ----------------
    ESCALA_REAL = 50_000_000_000
    # ---------------- FUNCION FORMATO ----------------
    def formatear_numero(n):
        return f"{int(n):,}".replace(",", ".")
    
    def construct(self):
        #titulos y parrafos
        # titulo = Text( 
        #     "Diferencia numerica entre\n"
        #     "dos contribuciones sociales\n"
        #     "medidos en escala lineal",
        #     font_size=50,
        #     color=WHITE
        # )
        titulo = Paragraph(
            "Diferencia numerica entre",
            "dos contribuciones sociales",
            "medidos en escala lineal",
            alignment="center",   # "left", "center", "right"
            font_size=50,
            color=WHITE,
        )

        titulo2 = Paragraph(
            "50 mil millones",
            "versus",
            "22 billones",
            "(22 millones de millones)",
            alignment="center",
            font_size=40)
        
        titulo.move_to(UP * 10) 
        titulo2.move_to(UP * 7) 

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
                y_length=13,
                axis_config={
                    "include_tip": False,
                    "decimal_number_config": {
                        "num_decimal_places": 0,
                        "group_with_commas": True}},
                x_axis_config={
                    "include_ticks": False,
                    "include_numbers": False},
                y_axis_config={"include_numbers": True}
                    ).shift(DOWN*3)) #.add_coordinates()
        # ---------------- BARRA PEQUEÑA ----------------
        barra1 = always_redraw(
            lambda: Rectangle(
                width=1,# altura proporcional al eje actual
                height=(valor_pequeno / max_y()) * 13, #1 es la altura del grafico en Y
                fill_color=BLUE,
                fill_opacity=1,
                stroke_width=0
            ).move_to(axes.c2p(0.8, 0),aligned_edge=DOWN))

        # ---------------- BARRA GRANDE ----------------

        barra2 = always_redraw(
            lambda: Rectangle(
                width=1,

                # altura proporcional
                height=(tracker.get_value() / max_y()) * 13,

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

class EscalaDinamica2(Scene):
    # en escala real
    def construct(self):
        ESCALA_REAL = 50      # 50 mil millones
        VALOR_EVASION = 22_000  # 22 billones

        titulo = Paragraph(
            "Diferencia numerica entre",
            "dos contribuciones sociales",
            "medidos en escala lineal",
            alignment="center",
            font_size=50,
            color=WHITE,
        )
        titulo2 = Paragraph(
            "50 mil millones",
            "versus",
            "22 billones",
            "(22 millones de millones)",
            alignment="center",
            font_size=40)
        
        titulo.move_to(UP * 10) 
        titulo2.move_to(UP * 7) 

        tracker = ValueTracker(ESCALA_REAL)  # empieza en 50 mil millones
        valor_pequeno = ESCALA_REAL          # barra fija

        def max_y():
            return max(ESCALA_REAL, tracker.get_value() * 1.2)

        def obtener_paso(valor):
            if valor < 10:
                return 1
            magnitud = 10 ** math.floor(math.log10(valor))
            return magnitud // 2

        def formatear(n):
            if n >= 1_000:
                return f"{n/1_000:.1f} bill."
            elif n >= 1:
                return f"{n/1:.0f} mil mill."
            return f"{int(n):,}"

        axes = always_redraw(
            lambda: Axes(
                x_range=[0, 2, 1],
                y_range=[0, max_y(), obtener_paso(tracker.get_value())],
                x_length=8,
                y_length=13,
                axis_config={
                    "include_tip": False,
                    "decimal_number_config": {
                        "num_decimal_places": 0,
                    }
                },
                x_axis_config={
                    "include_ticks": False,
                    "include_numbers": False
                },
                y_axis_config={"include_numbers": True}  # lo hacemos manual
            ).shift(DOWN * 3)
        )

        barra1 = always_redraw(
            lambda: Rectangle(
                width=1,
                height=(valor_pequeno / max_y()) * 13,
                fill_color=BLUE,
                fill_opacity=1,
                stroke_width=0
            ).move_to(axes.c2p(0.8, 0), aligned_edge=DOWN)
        )

        barra2 = always_redraw(
            lambda: Rectangle(
                width=1,
                height=(tracker.get_value() / max_y()) * 13,
                fill_color=RED,
                fill_opacity=1,
                stroke_width=0
            ).move_to(axes.c2p(1.6, 0), aligned_edge=DOWN)
        )

        # labels con formato legible
        valor = always_redraw(
            lambda: Text(
                formatear(tracker.get_value()),
                font_size=36,
                color=RED
            ).next_to(barra2, UP, buff=0.1)
        )
        valor2 = always_redraw(
            lambda: Text(
                formatear(valor_pequeno),
                font_size=36,
                color=BLUE
            ).next_to(barra1, UP, buff=0.1)
        )

        label1 = Text("Teletón", font_size=30).next_to(axes.c2p(0.8, 0), DOWN)
        label2 = Paragraph(
            "7% del PIB",
            "evadido",
            "por empresas",
            alignment="center",
            font_size=30
        ).next_to(axes.c2p(1.6, 0), DOWN)

        label_left = Text("En miles de millones de pesos ", font_size=35,color=BLUE_C)
        label_left.rotate(PI/2)
        label_left.next_to(axes.y_axis, LEFT, buff=1.2)
        #label_left.align_to(axes.y_axis, UP)


        self.play(Write(axes), Write(barra1), Write(barra2), Write(valor), Write(valor2))
        self.play(Write(titulo), Write(titulo2), Write(label1), Write(label2),Write(label_left))
        self.play(
            tracker.animate.set_value(VALOR_EVASION),
            run_time=10,
            rate_func=smooth
        )
        self.wait()


      




  




        
