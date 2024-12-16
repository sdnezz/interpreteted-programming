import math


class Triangle:
    def __init__(self, id, vertices):
        """
        :param id: строковый идентификатор объекта
        :param vertices: список координат вершин треугольника [(x1, y1), (x2, y2), (x3, y3)]
        """
        self.id = id
        self.vertices = vertices

    def move(self, dx, dy):
        """Перемещает треугольник на dx, dy"""
        self.vertices = [(x + dx, y + dy) for x, y in self.vertices]

    def __repr__(self):
        return f"Triangle(ID={self.id}, Vertices={self.vertices})"


class Tetragon:
    def __init__(self, id, vertices):
        """
        :param id: строковый идентификатор объекта
        :param vertices: список координат вершин четырёхугольника [(x1, y1), ..., (x4, y4)]
        """
        self.id = id
        self.vertices = vertices

    def move(self, dx, dy):
        """Перемещает четырёхугольник на dx, dy"""
        self.vertices = [(x + dx, y + dy) for x, y in self.vertices]

    def __repr__(self):
        return f"Tetragon(ID={self.id}, Vertices={self.vertices})"


def is_include(triangle, tetragon):
    """
    Проверяет, включён ли четырёхугольник (tetragon) в треугольник (triangle) по каждой из 4 вершин.
    Примерная реализация через площадь.
    """
    def area_of_triangle(a, b, c):
        """Вычисление площади треугольника по трём вершинам детермиантом - половина модуля этого детерминанта"""
        return abs(a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1])) / 2

    def is_point_in_triangle(p, a, b, c):
        """Проверяет, принадлежит ли точка треугольнику лежат ли все вершины четырёхугольника внутри треугольника"""
        area_total = area_of_triangle(a, b, c)
        area1 = area_of_triangle(p, b, c)
        area2 = area_of_triangle(a, p, c)
        area3 = area_of_triangle(a, b, p)
        return math.isclose(area_total, area1 + area2 + area3, rel_tol=1e-9)

    # Проверяем все вершины четырёхугольника на принадлежность треугольнику
    for vertex in tetragon.vertices:
        if not is_point_in_triangle(vertex, *triangle.vertices):
            return False
    return True


# Пример использования
try:
    t1 = Triangle("T1", [(0, 0), (10, 0), (5, 10)])
    t2 = Tetragon("T2", [(2, 2), (3, 3), (4, 2), (3, 1)])

    print("До перемещения:", t1, t2)
    t2.move(1, 1)
    print("После перемещения:", t1, t2)

    if is_include(t1, t2):
        print("Четырёхугольник включён в треугольник")
    else:
        print("Четырёхугольник не включён в треугольник")
except Exception as e:
    print(f"Произошла ошибка: {e}")
