from manim import *
import itertools # este funciona pero no lo entiendo 
import math


class permutacion(Scene):
    def construct(self):

        # Crear figuras
        circulo = Circle(color=BLUE).scale(0.8)
        cuadrado = Square(color=RED).scale(0.8)
        triangulo = Triangle(color=GREEN).scale(0.8)

        # Posiciones fijas
        posiciones = [
            LEFT * 4,
            ORIGIN,
            RIGHT * 4
        ]

        # Lista base
        figuras = [circulo, cuadrado, triangulo]

        # Mostrar cantidad total = 3!
        total = math.factorial(len(figuras))

        texto = Text(
            f"Permutaciones totales = {len(figuras)}! = {total}",
            font_size=36
        ).to_edge(UP)

        self.play(Write(texto))

        # Primera disposición
        for figura, pos in zip(figuras, posiciones):
            figura.move_to(pos)

        self.play(
            LaggedStart(
                *[FadeIn(fig) for fig in figuras],
                lag_ratio=0.2
            )
        )

        self.wait(1)

        # Generar todas las permutaciones
        perms = list(itertools.permutations(figuras))

        # Animar cada permutación
        for i in range(1, total):
            self.play(
                *[
                    perms[i][j].animate.move_to(posiciones[j])
                    for j in range(len(figuras))
                ],
                run_time=1.2
            )
            self.wait(0.4)

        self.wait(2)



from manim import *
import math


class permutacion2(Scene):
    def construct(self):

        circulo = Circle(color=BLUE).scale(0.8)
        cuadrado = Square(color=RED).scale(0.8)
        triangulo = Triangle(color=GREEN).scale(0.8)

        figuras = [circulo, cuadrado, triangulo]
        indices = [0, 1, 2]

        posiciones = [
            LEFT * 4,
            ORIGIN,
            RIGHT * 4
        ]

        total = math.factorial(len(indices))

        texto = Text(
            f"Permutaciones = {len(indices)}! = {total}",
            font_size=36
        ).to_edge(UP)

        self.play(Write(texto))

        for i in indices: # primera iteracion , ubica cada elemento i en su posicion i
            figuras[i].move_to(posiciones[i])

        self.play(*[FadeIn(figuras[i]) for i in indices])

        self.wait(1)

        # Generador recursivo de permutaciones
        perms = []

        def generar(lista, inicio=0):

            if inicio == len(lista):
                perms.append(lista.copy())
                return

            for i in range(inicio, len(lista)):

                lista[inicio], lista[i] = lista[i], lista[inicio]

                generar(lista, inicio + 1)

                lista[inicio], lista[i] = lista[i], lista[inicio]

        generar(indices.copy())

        for perm in perms[1:]:

            self.play(
                *[
                    figuras[perm[j]].animate.move_to(posiciones[j])
                    for j in range(len(indices))
                ],
                run_time=1.2
            )

            self.wait(0.4)

        self.wait(2)


def busqueda_binaria(lista, objetivo, izquierda, derecha):
    if izquierda > derecha:
        return -1

    medio = (izquierda + derecha) // 2

    if lista[medio] == objetivo:
        return medio

    elif objetivo < lista[medio]:
        return busqueda_binaria(lista, objetivo, izquierda, medio - 1)

    else:
        return busqueda_binaria(lista, objetivo, medio + 1, derecha)


numeros = [2, 5, 8, 12, 16, 23, 38]

print(busqueda_binaria(numeros, 16, 0, len(numeros)-1))


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

print(permutar([1,2,3,4,5]))
print(len(permutar([1,2,3,4,5])))