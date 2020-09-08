from amble.numberlists import Vector2D


class Texture:
    def __init__(self, file='', dimensions=Vector2D.one, scale=Vector2D.one):
        if isinstance(file, Texture):
            self.file = file.file
            self.dimensions = file.dimensions
            self.scale = file.scale
        else:
            self.file = file
            self.dimensions = Vector2D(dimensions)
            self.scale = Vector2D(scale)

    @property
    def size(self):
        return self.dimensions * self.scale

    def __str__(self):
        return self.file

    def __len__(self):
        return 0 if self.file == 'black' else 1


    @staticmethod
    def tests():
        t = Texture('bricks', [2, 3], '0.5 0.5')
        assert t.size == (1, 1.5)
        assert t and not Texture('black')


    none, edge, hot1 = tuple(range(3))


Texture.none = Texture('black', [0.5, 0.5])
Texture.edge = Texture('pq_edge_white_2', [0.5, 0.5])
Texture.hot1 = Texture('pq_hot_1_med', [4, 4], [0.5, 0.5])


if __name__ == '__main__':
    Texture.tests()
