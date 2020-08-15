from textwrap import indent

from amble.mapping.faces import Faces
from amble.scriptobject import ScriptObject
from amble.mapping.texture import Texture
from amble.numberlists.vector3d import Vector3D
from amble.numberlists.vector2d import Vector2D
from amble.numberlists.rotation3d import Rotation3D
from amble.utils.lists import drange


class Brush(ScriptObject):
    classname = 'Brush'

    defaults = dict(
        model='',
        face_groups=dict(),
        manual_vertices=list(),
        manual_faces=dict(),

        sides=0,
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
            return [
                Vector3D(x, y, z)
                for x in [self.center.x + self.size.x / 2, self.center.x - self.size.x / 2]
                for y in [self.center.y + self.size.y / 2, self.center.y - self.size.y / 2]
                for z in [self.center.z + self.size.z / 2, self.center.z - self.size.z / 2]
            ]
        elif self.model == 'prism':
            return [
                Vector3D(
                    self.center.x + self.size.x / 2 * (Rotation3D.k(angle) * Vector3D.i).x,
                    self.center.y + self.size.y / 2 * (Rotation3D.k(angle) * Vector3D.i).y,
                    z
                )
                for angle in drange(0, 360, 360 / self.sides)
                for z in [self.center.z + self.size.z / 2, self.center.z - self.size.z / 2]
            ]
        return []

    def __repr__(self):
        return '{\n' + indent('\n'.join(repr(face) for face in self.faces), '   ') + '\n}'

    def _set_face_attributes(self, **face_attributes):
        self.face('all').texture = Texture.none
        self.face('all').rotation = 0
        self.face('all').scale = Vector2D.one

        for face_attribute, value in face_attributes.items():
            if isinstance(value, dict):
                for group in value:
                    setattr(self.face(group), face_attribute, value[group])
            else:
                setattr(self.face('all'), face_attribute, value)

    def move(self, offset):
        if len(self.manual_vertices) == 0:
            self.center += offset
        else:
            for i in range(len(self.vertices)):
                self.move_vertex(i, offset)
            return self

    def move_face(self, face, offset):
        for i in self.face(face).vertex_indices:
            self.move_vertex(i, offset)
        return self

    def move_vertex(self, vertex_index, offset):
        self.manual_vertices = self.vertices
        self.vertices[vertex_index] += offset
        self.model = None
        return self

    def rotate(self, rotation, center=None):
        rotation = Rotation3D(rotation)
        if center is None:
            center = sum(self.vertices) / len(self.vertices)

        self.manual_vertices = self.vertices
        for i, vertex in enumerate(self.vertices):
            self.vertices[i] = rotation * (vertex - center) + center
        for face in self.faces:
            face.normal = rotation * face.normal
            face.rotation += rotation.angle * face.normal.dot(rotation.axis)
        return self


    @classmethod
    def make_cube(cls, center=Vector3D.zero, size=Vector3D.one, **face_attributes):
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

        cube._set_face_attributes(**face_attributes)

        return cube

    @classmethod
    def make_prism(cls, sides=3, center=Vector3D.zero, size=Vector3D.one, **face_attributes):
        center, size = Vector3D(center), Vector3D(size)
        prism = cls(
            model='prism',
            sides=sides,
            center=center,
            size=size,

            face_groups={
                'z': ['top', 'bottom'],
                'side': ['side{}'.format(side) for side in range(sides)],
                'all': ['side{}'.format(side) for side in range(sides)] + ['top', 'bottom'],
            }
        )

        for side in range(sides):
            prism.face('side{}'.format(side)).vertex_indices = [
                2 * side,
                (2 * side + 2) % (2 * sides),
                (2 * side + 3) % (2 * sides),
                2 * side + 1
            ]
            prism.face('side{}'.format(side)).normal = (
                (Rotation3D.k((side + 0.5) * 360 / sides) * Vector3D.i) *
                (size.y, size.x, 0)
            ).normalized()

        prism.face('top').vertex_indices = [2 * side for side in range(sides - 1, -1, -1)]
        prism.face('bottom').vertex_indices = [2 * side + 1 for side in range(sides)]
        prism.face('top').normal = Vector3D.k
        prism.face('bottom').normal = -Vector3D.k
        prism.face('z').skew = Vector2D(0, 0)

        prism._set_face_attributes(**face_attributes)

        perimeter = sum(abs(prism.face('side{}'.format(side)).middle_bisector) for side in range(sides))
        scale_x = perimeter / round(perimeter / prism.face('side').scale.x)
        prism.face('side').scale *= Vector2D(scale_x, 1)

        prism.face('side0').origin = prism.face('side0').top_left
        for side in range(1, sides):
            prism.face('side{}'.format(side)).unify_with(prism.face('side{}'.format(side - 1)))

        return prism


    @staticmethod
    def tests():
        c = Brush.make_cube(
            center=[0, 0, -0.25],
            size=[4, 4, 0.5],
            texture={'all': Texture.edge, 'z': Texture.hot1},
            origin={'y': '0 0 0'},
            rotation=90
        )

        assert c.face('x').texture == Texture.edge
        assert c.vertices[0] == '2 2 0'
        assert c.face('bottom').origin == c.face('bottom').top_left
        assert c.face('top').shift == '-2 2'
        assert c.face('right').skew == '0 0'
        assert c.face('side').rotation == 90

        c.move([4.5, 0, 0])
        c.face('y').origin = '4.5 0 0'
        assert c.vertices[0] == '6.5 2 0'
        assert c.face('right').shift == '0 2'
        assert c.face('back').shift == '0 4.5'
        assert c.face('top').origin == c.face('top').top_left
        assert c.face('top').u == '0 1 0'

        c.move_face('back', [-1, -1, 1])
        assert c.vertices[0] == '5.5 1 1'
        assert c.face('top').skew == (-1/3, 0)
        assert c.face('top').origin == c.face('top').center
        assert c.face('right').skew == (0, 1/3)

        c.move_face('back', [1, 1, -1])
        c.move_vertex(1, [0.5, 0.5, 0])
        c.move_vertex(3, [0.5, -0.5, 0])
        c.move_vertex(5, [-0.5, 0.5, 0])
        c.move_vertex(7, [-0.5, -0.5, 0])
        assert c.face('right').skew == '0 0'
        assert c.face('top').origin == c.face('top').top_left
        assert c.face('bottom').origin == c.face('bottom').center

        c.rotate('1 0 0 30')
        c.face('back').origin = c.face('back').top_left
        c.face('front').origin = c.face('front').top_left
        assert c.face('top').u == (0, pow(0.75, 0.5), 0.5)
        assert c.face('right').u == (0, -0.5, pow(0.75, 0.5))
        assert c.face('right').shift == '-0.033493649053890594 2.125'

        ccc = Brush.make_cube(texture=Texture.edge).copies(
            ('center', 'size'),
            '2 3 1', '7 1 4',
            '6 7 2', '5 3 6'
        )
        assert ccc[0].vertices[0] == '5.5 3.5 3'
        assert ccc[0].face('right').origin == '5.5 2.5 3'

        p = Brush.make_prism(16, '0 0 -0.5', '4 2 1', texture=Texture('PQ/pq_edge_white_2', '0.5 0.5', '2 2'))
        assert len(p.face_groups['all']) == 18
        assert p.face('top').skew == '0 0'
        assert p.face('side0').scale == '0.9626350356771984 1'
        assert p.face('side1').shift == '1.7264992203753446 0'


if __name__ == '__main__':
    Brush.tests()
