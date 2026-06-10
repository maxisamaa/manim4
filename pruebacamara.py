from manim import *
from pathlib import Path
import math
import numpy as np

class Prueba(MovingCameraScene):
    def construct(self):
        triangulo = Triangle()
        triangulo.set_stroke(width=4, color=WHITE)
        self.play(Write(triangulo))
        
        circulo = Circle(radius=4)
        circulo.set_stroke(width=1, color=WHITE)
        elementos = VGroup(triangulo, circulo)
        
        # 1. Creamos los dos estados físicos (objetos reales) a los que queremos llegar
        triangulo_grande = triangulo.copy().scale(2)
        triangulo_chico = triangulo.copy() # Estado original (escala 1)

        # 2. Generamos la lista de animaciones usando la estructura de Transform.
        # Al transformar el triángulo original hacia copias explícitas, 
        # Manim está obligado a renderizar el cambio de tamaño fotograma a fotograma.
        lista_latidos = []
        for i in range(10):
            if i % 2 == 0:
                lista_latidos.append(Transform(triangulo, triangulo_grande.copy()))
            else:
                lista_latidos.append(Transform(triangulo, triangulo_chico.copy()))
        
        # Agrupamos los latidos en una secuencia temporal limpia
        latido_completo = Succession(*lista_latidos)
        
        # 3. ¡AHORA SÍ! Ejecución en paralelo real
        # La cámara sube fluidamente durante 5 segundos y el triángulo late 10 veces de fondo
        self.play(
            latido_completo,
            self.camera.frame.animate.shift(UP * 3),
            run_time=5,rate_func=linear
        )
        self.wait(1)
        
#self.camera.frame.animate.move_to(cartas.get_center() + UP * 2) 
# shift mueve una cantidad relativa a la posicion original
#move.to sigue una posicion absoluta , crea una grilla de posiciones . 
#next_to sirve para usar posiciones relativas a objetos ya creados




class ArbolRecursivo(Scene):
    def construct(self):
        # Punto de inicio (suelo) y vector inicial (hacia arriba)
        punto_inicio = DOWN * 3
        vector_inicial = UP * 2
        
        # Objeto que contendrá todo el árbol
        arbol = VGroup()
        self.add(arbol)
        
        # Definimos la función recursiva DENTRO de construct para usar 'self.play'
        def dibujar_rama(punto, vector, n_recursiones, mobject_arbol):
            if n_recursiones == 0:
                return

            # 1. Crear la rama actual
            fin_rama = punto + vector
            rama = Line(punto, fin_rama, color=GREEN_C, stroke_width=n_recursiones*1.5)
            
            # 2. ANIMACIÓN: Efectuamos el play EN CADA BUCLE
            # Usamos Create para que se vea cómo crece
            self.play(Create(rama), run_time=0.1)
            mobject_arbol.add(rama)

            # 3. Preparar los siguientes vectores (rotados y más cortos)
            angulo = 40 * DEGREES
            reduccion = 0.6
            
            # Matriz de rotación 2D simple
            def mat_rot(a):
                return np.array([[np.cos(a), -np.sin(a), 0],
                                 [np.sin(a),  np.cos(a), 0],
                                 [0,          0,          1]])

            vec_izq = np.dot(mat_rot(angulo), vector) * reduccion
            vec_der = np.dot(mat_rot(-angulo), vector) * reduccion

            # 4. LLAMADAS RECURSIVAS
            # Primero la rama izquierda, luego la derecha
            dibujar_rama(fin_rama, vec_izq, n_recursiones - 1, mobject_arbol)
            dibujar_rama(fin_rama, vec_der, n_recursiones - 1, mobject_arbol)

            # Nota: Este orden "primera rama entera -> segunda rama entera" 
            # se llama "Depth-First Search" (Búsqueda en profundidad).

        # --- Iniciar la recursión ---
        # 6 niveles de profundidad es un buen equilibrio para la animación
        dibujar_rama(punto_inicio, vector_inicial, 7, arbol)
        
        self.wait(2)


class VisualizacionFibonacci(Scene):
    def construct(self):
        titulo = Text("Recursión de Fibonacci visual", color=BLUE).to_edge(UP)
        self.play(Write(titulo))
        self.wait(1)
        
        # Grupo para organizar los nodos visualmente
        nodos_visuales = VGroup()
        self.add(nodos_visuales)
        
        # Posiciones iniciales para el árbol visual
        ancho_inicial = 5
        alto_paso = 1.2
        pos_inicial = UP * 1.5
        
        # Definimos la función recursiva
        # 'pos' y 'width' son para la parte visual, no para el cálculo
        def fib(n, pos, width):
            # 1. Parte visual: Crear nodo actual
            color_nodo = YELLOW if n <= 1 else WHITE
            label = Text(str(n), color=color_nodo).scale(0.7)
            circulo = Circle(color=WHITE, radius=0.35).move_to(pos)
            nodo_completo = VGroup(circulo, label)
            
            # 2. ANIMACIÓN: Efectuamos el play EN CADA BUCLE
            self.play(FadeIn(nodo_completo), run_time=0.4)
            nodos_visuales.add(nodo_completo)
            
            # Casos base
            if n == 0:
                return 0
            elif n == 1:
                return 1
            
            # Calcular posiciones para las siguientes llamadas
            pos_izq = pos + DOWN * alto_paso + LEFT * (width / 2)
            pos_der = pos + DOWN * alto_paso + RIGHT * (width / 2)
            
            # Dibujar líneas de conexión
            linea_izq = Line(circulo.get_bottom(), pos_izq, color=GRAY)
            linea_der = Line(circulo.get_bottom(), pos_der, color=GRAY)
            
            # Animamos la aparición de las ramas ANTES de las llamadas recursivas
            self.play(Create(linea_izq), Create(linea_der), run_time=0.2)
            nodos_visuales.add(linea_izq, linea_der)
            
            # 3. LLAMADAS RECURSIVAS
            # Se calculará primero TODO el árbol izquierdo antes de empezar el derecho
            resultado_izq = fib(n - 1, pos_izq, width / 2)
            resultado_der = fib(n - 2, pos_der, width / 2)
            
            return resultado_izq + resultado_der

        # --- Iniciar la recursión ---
        # fib(5) crea un árbol visualmente manejable.
        # ¡Ojo! n > 7 empezará a solapar nodos y tardará mucho en animar.
        valor_n = 5
        label_principal = MathTex(f"Calculando\\, Fib({valor_n})", color=YELLOW).next_to(titulo, DOWN)
        self.play(Write(label_principal))
        
        fib(valor_n, pos_inicial, ancho_inicial)
        
        self.wait(2)


class Espiral(MovingCameraScene):
    def construct(self):
        espiral_group = VGroup()
        self.add(espiral_group)

        FACTOR_GROSOR = 1.25
        DIRECCIONES = [RIGHT, UP, LEFT, DOWN]

        def agregar_cuadrado_recursivo(n, paso, punto_anclaje):
            if n > 6:  # Cambiado a 6 para controlar el número de iteraciones de forma óptima
                # 1. Primer cuadrado de lado 1 en el origen
                c1 = Square(side_length=1, stroke_width=4, color=YELLOW).move_to(ORIGIN)
                t1 = Text("1").scale(0.5).move_to(c1.get_center())
                cuadrado1 = VGroup(c1, t1)
                
                # 2. Segundo cuadrado de lado 1 a la DERECHA del primero
                c2 = Square(side_length=1, stroke_width=4, color=YELLOW).next_to(c1, RIGHT, buff=0)
                t2 = Text("1").scale(0.5).move_to(c2.get_center())
                cuadrado2 = VGroup(c2, t2)
                
                # Los animamos y agregamos al grupo general
                self.play(Create(cuadrado1), Create(cuadrado2), run_time=0.5)
                espiral_group.add(cuadrado1, cuadrado2)
                
                # El truco para conectar con el de lado 2:
                # El cuadrado de lado 2 necesita posicionarse arriba. El anclaje correcto
                # para que la esquina coincida es la esquina superior derecha del segundo cuadrado.
                punto_retorno_anclaje = c2.get_corner(UP + RIGHT)
                
                return 1, 1, punto_retorno_anclaje

            direccion_actual = DIRECCIONES[paso % 4]
            
            f_ant1, f_ant2, siguiente_anclaje = agregar_cuadrado_recursivo(n + 1, paso + 1, punto_anclaje)
            
            lado_actual = f_ant1 + f_ant2

            cuadrado = Square(side_length=lado_actual, stroke_width=5, color=YELLOW)
            
            if np.array_equal(direccion_actual, RIGHT):
                cuadrado.next_to(siguiente_anclaje, RIGHT, buff=0).align_to(siguiente_anclaje, DOWN)
                nuevo_punto_anclaje = cuadrado.get_corner(UP + RIGHT)
            elif np.array_equal(direccion_actual, UP):
                cuadrado.next_to(siguiente_anclaje, UP, buff=0).align_to(siguiente_anclaje, RIGHT)
                nuevo_punto_anclaje = cuadrado.get_corner(UP + LEFT)
            elif np.array_equal(direccion_actual, LEFT):
                cuadrado.next_to(siguiente_anclaje, LEFT, buff=0).align_to(siguiente_anclaje, UP)
                nuevo_punto_anclaje = cuadrado.get_corner(DOWN + LEFT)
            else: # DOWN
                cuadrado.next_to(siguiente_anclaje, DOWN, buff=0).align_to(siguiente_anclaje, LEFT)
                nuevo_punto_anclaje = cuadrado.get_corner(DOWN + RIGHT)

            texto_numero = Text(str(lado_actual)).scale(0.5 if lado_actual < 3 else 0.8).move_to(cuadrado.get_center())
            cuadrado_completo = VGroup(cuadrado, texto_numero)

            # =========================================================================
            # ¡AQUÍ ESTÁ EL TRUCO DE LA CÁMARA!
            # =========================================================================
            # 1. Obtenemos el centro exacto del cuadrado que se va a construir AHORA
            centro_futuro = cuadrado_completo.get_center()

            # 2. Si el cuadrado es grande, movemos y alejamos la cámara ANTES de crearlo.
            # Apuntamos directamente a 'centro_futuro' en lugar de al grupo entero.
            if lado_actual >= 4:
                self.play(
                    self.camera.frame.animate.move_to(centro_futuro).set_width(lado_actual * 4.5), 
                    run_time=0.5
                )
            elif lado_actual == 2:
                # Ajuste inicial para cuando empieza a crecer
                self.play(self.camera.frame.animate.move_to(centro_futuro), run_time=0.4)

            # 3. Ahora que la cámara está perfectamente centrada en el objetivo, lo dibujamos
            self.play(Create(cuadrado_completo), run_time=0.5)
            espiral_group.add(cuadrado_completo)
            # =========================================================================

            return lado_actual, f_ant1, nuevo_punto_anclaje

        punto_inicial = ORIGIN
        agregar_cuadrado_recursivo(1, 0, punto_inicial)
        self.wait(2)