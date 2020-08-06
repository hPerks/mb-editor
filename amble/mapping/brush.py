from textwrap import indent

from amble.mapping.faces import Faces
from amble.scriptobject import ScriptObject
from amble.mapping.texture import Texture
from amble.numberlists.vector3d import Vector3D


class Brush(ScriptObject):
    classname = 'Brush'

    defaults = dict(
        model='',
        face_groups=dict(),
        manual_vertices=list(),
        manual_faces=dict(),

        center=Vector3D.zero,
        size=Vector3D.one,
    )

    def __init__(self, manual_faces=None, **fields):
        super().__init__(**fields)

        self.manual_faces = {}
        if manual_faces is not None:
            for name, face in manual_faces.items():
                new_face = Faces(self, name)
                for attr in Faces.inherited_attrs:
                    if attr in face.__dict__:
                        new_face.__dict__[attr] = face.__dict__[attr]
                self.manual_faces[name] = new_face

    def face(self, name):
        if name not in self.manual_faces:
            self.manual_faces[name] = Faces(self, name)
        return self.manual_faces[name]

    @property
    def faces(self):
        return [self.face(name) for name in self.face_groups['all']]

    @property
    def vertices(self):
        if len(self.manual_vertices) > 0:
            return self.manual_vertices

        if self.model == 'cube':
            vertices = []
            for x in [self.center.x + self.size.x / 2, self.center.x - self.size.x / 2]:
                for y in [self.center.y + self.size.y / 2, self.center.y - self.size.y / 2]:
                    for z in [self.center.z + self.size.z / 2, self.center.z - self.size.z / 2]:
                        vertices.append(Vector3D(x, y, z))
            return vertices
        return []

    def __repr__(self):
        return '{\n' + indent('\n'.join(repr(face) for face in self.faces), '   ') + '\n}'

    def move(self, offset):
        for i in range(len(self.vertices)):
            self.move_vertex(i, offset)
        return self

    def move_face(self, face, offset):
        offset = Vector3D(offset)

        for i in self.face(face).vertex_indices:
            self.move_vertex(i, offset)
        return self

    def move_vertex(self, vertex_index, offset):
        self.manual_vertices = self.vertices
        self.vertices[vertex_index] += offset
        self.model = None
        return self


    @classmethod
    def make_cube(cls, center=Vector3D.zero, size=Vector3D.one, texture=Texture.none, origin=None, skew=None, rotation=None):
        cube = cls(
            model='cube',
            center=center,
            size=size,

            face_groups={
                'x': ['right', 'left'],
                'y': ['back', 'front'],
                'z': ['top', 'bottom'],
                'side': ['right', 'left', 'back', 'front'],
                'all': ['right', 'left', 'back', 'front', 'top', 'bottom'],
            }
        )

        cube.face('right').vertex_indices = [2, 0, 1, 3]
        cube.face('left').vertex_indices = [4, 6, 7, 5]
        cube.face('back').vertex_indices = [0, 4, 5, 1]
        cube.face('front').vertex_indices = [6, 2, 3, 7]
        cube.face('top').vertex_indices = [4, 0, 2, 6]
        cube.face('bottom').vertex_indices = [1, 5, 7, 3]

        cube.face('right').normal = Vector3D.i
        cube.face('left').normal = -Vector3D.i
        cube.face('back').normal = Vector3D.j
        cube.face('front').normal = -Vector3D.j
        cube.face('top').normal = Vector3D.k
        cube.face('bottom').normal = -Vector3D.k

        if isinstance(texture, Texture):
            cube.face('all').texture = texture
        else:
            for group in texture:
                cube.face(group).texture = texture[group]

        if origin is not None:
            if isinstance(origin, dict):
                for group in origin:
                    cube.face(group).origin = origin[group]
            else:
                cube.face('all').origin = origin

        if skew is not None:
            if isinstance(skew, dict):
                for group in skew:
                    cube.face(group).skew = skew[group]
            else:
                cube.face('all').skew = skew

        cube.face('all').rotation = 0
        if rotation is not None:
            if isinstance(rotation, dict):
                for group in rotation:
                    cube.face(group).rotation = rotation[group]
            else:
                cube.face('all').rotation = rotation

        return cube


    @staticmethod
    def tests():
        c = Brush.make_cube(
            center=[0, 0, -0.25],
            size=[4, 4, 0.5],
            texture={'all': Texture.edge, 'z': Texture.hot1},
            origin={'side': '0 0 0'},
            rotation=90
        )

        assert c.face('x').texture == Texture.edge
        assert c.vertices[0] == '2 2 0'
        assert c.face('top').u == '1 0 0 128'
        assert c.face('right').skew == '0 0'
        assert c.face('side').rotation == 90

        c.move([4.5, 0, 0])
        c.face('y').origin = '4.5 0 0'
        assert c.vertices[0] == '6.5 2 0'
        assert c.face('right').shift == '0 0'
        assert c.face('back').shift == '4.5 0'
        assert c.face('top').origin == c.face('top').top_left
        assert c.face('top').u == '1 0 0 -160'

        c.move_face('back', [-1, -1, 1])
        assert c.vertices[0] == '5.5 1 1'
        assert c.face('top').skew == (1/3, 0)
        assert c.face('top').origin == c.face('top').center
        assert c.face('right').skew == (0, -1/3)

        c.move_face('back', [1, 1, -1])
        c.move_vertex(1, [0.5, 0.5, 0])
        c.move_vertex(3, [0.5, -0.5, 0])
        c.move_vertex(5, [-0.5, 0.5, 0])
        c.move_vertex(7, [-0.5, -0.5, 0])
        assert c.face('right').skew == '0 0'
        assert c.face('top').origin == c.face('top').top_left
        assert c.face('bottom').origin == c.face('bottom').center

        ccc = Brush.make_cube(texture=Texture.edge).copies(
            ('center', 'size'),
            '2 3 1', '7 1 4',
            '6 7 2', '5 3 6'
        )
        assert ccc[0].vertices[0] == '5.5 3.5 3'
        assert ccc[0].face('right').origin == '5.5 2.5 3'


if __name__ == '__main__':
    Brush.tests()
