from textwrap import indent

import amble
from amble.numberlists import *
from amble.interior.mapping.faces import Faces
from amble.interior.mapping.texture import Texture
from amble.utils.lists import drange
from amble.utils.numbers import mean_of_angles


class Brush(amble.ScriptObject):
    classname = 'Brush'

    defaults = dict(
        vertices=list(),
        faces=dict(),
        face_groups=dict(),
    )

    def __init__(self, faces=None, **fields):
        super().__init__(**fields)

        self.faces = {}
        if faces is not None:
            for name, face in faces.items():
                new_face = Faces(self, name)
                for attr in Faces.copied_attrs:
                    if attr in face.__dict__:
                        setattr(new_face, attr, face.__dict__[attr])
                self.faces[name] = new_face

    def face(self, name):
        if name not in self.faces:
            self.faces[name] = Faces(self, name)
        return self.faces[name]

    def __str__(self):
        return '{\n' + indent('\n'.join(str(face) for face in self.face('all')), '   ') + '\n}'

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
        for i in range(len(self.vertices)):
            self.move_vertex(i, offset)
        return self

    def move_face(self, face, offset):
        for i in self.face(face).vertex_indices:
            self.move_vertex(i, offset)
        return self

    def move_vertex(self, vertex_index, offset):
        self.vertices[vertex_index] += offset
        return self

    def rotate(self, rotation, center=None):
        rotation = Rotation3D(rotation)
        if center is None:
            center = sum(self.vertices) / len(self.vertices)

        for face in self.face('all'):
            with face.cached:
                face._offset_uvw = -face.to_uvw(face.vertices[0])

        for i, vertex in enumerate(self.vertices):
            self.vertices[i] = rotation * (vertex - center) + center

        for face in self.face('all'):
            normal, tangent = face.normal, face.tangent
            face.normal = rotation * normal
            face.tangent = rotation * tangent
            with face.cached:
                face.origin = face.from_uvw(face._offset_uvw) - face.origin + face.vertices[0]
            del face._offset_uvw

        return self

    def rotate_to_axis(self, axis, center):
        if axis != 'z':
            self.rotate(
                Rotation3D.towards + (0, 0, -1, 90 if axis == 'x' else 0),
                center=center
            )

            for face in self.face('side'):
                face.reset_rotation()
                if axis == 'x':
                    face.tangent = '1 0 0'
                else:
                    face.cotangent = '0 -1 0'

        return self


    @classmethod
    def make_cube(cls, center=Vector3D.zero, size=Vector3D.one, **face_attributes):
        center, size = Vector3D(center), Vector3D(size)

        cube = cls(
            vertices=[
                Vector3D(x, y, z)
                for x in [center.x + size.x / 2, center.x - size.x / 2]
                for y in [center.y + size.y / 2, center.y - size.y / 2]
                for z in [center.z + size.z / 2, center.z - size.z / 2]
            ],

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
    def make_prism(cls, sides=3, axis='z', center=Vector3D.zero, size=Vector3D.one, start_angle=0, end_angle=360, **face_attributes):
        center, size = Vector3D(center), Vector3D(size).on_axis(axis)

        delta_angle = end_angle - start_angle
        effective_sides = sides * delta_angle // 360 + (delta_angle <= 180) + (delta_angle < 180)

        prism = cls(
            vertices=[
                Vector3D(
                    center.x + size.x / 2 * (Rotation3D.k(angle) * Vector3D.i).x,
                    center.y + size.y / 2 * (Rotation3D.k(angle) * Vector3D.i).y,
                    z
                )
                for angle in drange(
                    start_angle, end_angle, 360 / sides,
                    include_end=(end_angle - start_angle <= 180),
                )
                for z in [center.z + size.z / 2, center.z - size.z / 2]
            ] + (
                [
                    Vector3D(center.x, center.y, z)
                    for z in [center.z + size.z / 2, center.z - size.z / 2]
                ] if end_angle - start_angle < 180 else []
            ),

            face_groups={
                'z': ['top', 'bottom'],
                'side': [f'side{side}' for side in range(effective_sides)],
                'all': [f'side{side}' for side in range(effective_sides)] + ['top', 'bottom'],
            }
        )

        for side in range(effective_sides):
            prism.face(f'side{side}').vertex_indices = [
                (2 * side + 2) % (2 * effective_sides),
                2 * side,
                2 * side + 1,
                (2 * side + 3) % (2 * effective_sides)
            ]

            if delta_angle < 180 and side == effective_sides - 2:
                angle = start_angle + (side * 360 / sides) + 90
            elif delta_angle <= 180 and side == effective_sides - 1:
                angle = start_angle + 270
            else:
                angle = start_angle + (side + 0.5) * 360 / sides
            prism.face(f'side{side}').normal = ((Rotation3D.k(angle) * Vector3D.i) / size).normalized()

        prism.face('top').vertex_indices = [2 * side for side in range(effective_sides)]
        prism.face('bottom').vertex_indices = [2 * side + 1 for side in range(effective_sides - 1, -1, -1)]
        prism.face('top').normal = Vector3D.k
        prism.face('bottom').normal = -Vector3D.k
        prism.face('z').origin = center
        prism.face('z').skew = '0 0'

        prism.rotate_to_axis(axis, center)

        prism.face('side0').align('bottom left' if axis == 'x' else 'top left' if axis == 'y' else 'top right')
        Faces.unify(
            [prism.face(f'side{side}') for side in range(sides * delta_angle // 360)],
            justify=face_attributes['justify'] if 'justify' in face_attributes else True
        )

        return prism

    @classmethod
    def make_slice(cls, axis='z', center=Vector3D.zero, size=Vector3D.one, inner_size=Vector3D.zero, start_angle=0, end_angle=90, **face_attributes):
        center, size, inner_size = Vector3D(center), Vector3D(size).on_axis(axis), Vector3D(inner_size).on_axis(axis)

        has_inside = not (inner_size.x == 0 or inner_size.y == 0)
        inner_size.z = 0

        if has_inside:
            slice = cls(
                vertices=[
                    Vector3D(
                        center.x + size2.x / 2 * (Rotation3D.k(angle) * Vector3D.i).x,
                        center.y + size2.y / 2 * (Rotation3D.k(angle) * Vector3D.i).y,
                        z
                    )
                    for size2 in [size, inner_size]
                    for angle in [start_angle, end_angle]
                    for z in [center.z + size.z / 2, center.z - size.z / 2]
                ],

                face_groups={
                    'r': ['outside', 'inside'],
                    'theta': ['start', 'end'],
                    'z': ['top', 'bottom'],
                    'side': ['outside', 'inside', 'start', 'end'],
                    'all': ['outside', 'inside', 'start', 'end', 'top', 'bottom'],
                }
            )
        else:
            slice = cls(
                vertices=[
                    Vector3D(
                        center.x + size.x / 2 * (Rotation3D.k(angle) * Vector3D.i).x,
                        center.y + size.y / 2 * (Rotation3D.k(angle) * Vector3D.i).y,
                        z
                    )
                    for angle in [start_angle, end_angle]
                    for z in [center.z + size.z / 2, center.z - size.z / 2]
                ] + [
                    Vector3D(center.x, center.y, z)
                    for z in [center.z + size.z / 2, center.z - size.z / 2]
                ],

                face_groups={
                    'r': ['outside'],
                    'theta': ['start', 'end'],
                    'z': ['top', 'bottom'],
                    'side': ['outside', 'start', 'end'],
                    'all': ['outside', 'start', 'end', 'top', 'bottom'],
                }
            )

        slice.face('outside').vertex_indices = [2, 0, 1, 3]
        slice.face('start').vertex_indices = [0, 4, 5, 1]

        if has_inside:
            slice.face('inside').vertex_indices = [4, 6, 7, 5]
            slice.face('end').vertex_indices = [6, 2, 3, 7]
            slice.face('top').vertex_indices = [4, 0, 2, 6]
            slice.face('bottom').vertex_indices = [1, 5, 7, 3]
        else:
            slice.face('end').vertex_indices = [4, 2, 3, 5]
            slice.face('top').vertex_indices = [4, 0, 2]
            slice.face('bottom').vertex_indices = [1, 5, 3]

        slice.face('outside').normal = ((Rotation3D.k(mean_of_angles(start_angle, end_angle)) * Vector3D.i) / size).normalized()
        slice.face('start').normal = ((Rotation3D.k(start_angle) * Vector3D.j) / (size - inner_size)).normalized()
        slice.face('end').normal = ((Rotation3D.k(end_angle) * -Vector3D.j) / (size - inner_size)).normalized()
        slice.face('top').normal = Vector3D.k
        slice.face('bottom').normal = -Vector3D.k

        if has_inside:
            inner_size.z = 1
            slice.face('inside').normal = ((Rotation3D.k(mean_of_angles(start_angle, end_angle)) * -Vector3D.i) / inner_size).normalized()

        slice.face('z').skew = '0 0'
        slice._set_face_attributes(**face_attributes)

        slice.rotate_to_axis(axis, center)

        return slice

    @classmethod
    def make_slices(cls, axis='z', center=Vector3D.zero, size=Vector3D.one, inner_size=Vector3D.zero, start_angle=0, end_angle=360, step_angle=90, justify=False, **face_attributes):
        inner_size = Vector3D(inner_size)

        slices = [
            cls.make_slice(
                axis=axis,
                center=center,
                size=size,
                inner_size=inner_size,
                start_angle=angle,
                end_angle=angle + step_angle,
                **face_attributes
            )
            for angle in drange(start_angle, end_angle, step_angle)
        ]

        if justify:
            if not isinstance(justify, dict):
                justify = {'z': justify, 'r': justify}

            for group in justify:
                for face in slices[0].face(group):
                    if face.name == 'outside':
                        face.origin = face.vertices[1]
                    elif face.name == 'inside':
                        face.origin = face.vertices[0]
                    elif face.name == 'top':
                        for slice in slices:
                            slice.face('top').tangent = slice.face('top').middle_bisector.normalized()
                            slice.face('top').origin = slice.face('top').vertices[0]
                    elif face.name == 'bottom':
                        for slice in slices:
                            slice.face('bottom').tangent = slice.face('bottom').middle_bisector.normalized()
                            slice.face('bottom').origin = slice.face('bottom').vertices[1]

                    if justify[group]:
                        Faces.unify(
                            [slice.face(face.name) for slice in slices],
                            justify=justify[group]
                        )

        return slices


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
        assert c.face('bottom').origin == c.face('bottom').alignment_point('top left')
        assert c.face('top').shift == '2 2'
        assert c.face('right').skew == '0 0'
        assert c.face('side').rotation == 90

        c.move([4.5, 0, 0])
        c.face('y').origin = '4.5 0 0'
        assert c.vertices[0] == '6.5 2 0'
        assert c.face('right').shift == '0 2'
        assert c.face('back').shift == '0 -4.5'
        assert c.face('top').origin == c.face('top').alignment_point('top left')
        assert c.face('top').u == '0 -1 0'

        c.move_face('back', [-1, -1, 1])
        assert c.vertices[0] == '5.5 1 1'
        assert c.face('top').skew == (-1/3, 0)
        assert c.face('top').origin == c.face('top').alignment_point('top')
        assert c.face('right').skew == (0, 1/3)

        c.move_face('back', [1, 1, -1])
        c.move_vertex(1, [0.5, 0.5, 0])
        c.move_vertex(3, [0.5, -0.5, 0])
        c.move_vertex(5, [-0.5, 0.5, 0])
        c.move_vertex(7, [-0.5, -0.5, 0])
        assert c.face('right').skew == '0 0'
        assert c.face('top').origin == c.face('top').alignment_point('top left')
        assert c.face('bottom').origin == c.face('bottom').alignment_point('center')

        c.rotate('1 0 0 30')
        c.face('back').align('top left')
        c.face('front').align('top left')
        assert c.face('top').u == (0, -pow(0.75, 0.5), 0.5)
        assert c.face('right').u == (0, -0.5, -pow(0.75, 0.5))
        assert c.face('right').shift == '0.0334936490538904 2.125'

        scaled_edge = Texture('pq_edge_white_2', '0.5 0.5', '2 2')

        p = Brush.make_prism(sides=16, axis='z', center='0 0 -0.5', size='4 2 1', texture=scaled_edge)
        assert len(p.face_groups['all']) == 18
        assert p.face('top').skew == '0 0'
        assert p.face('side0').scale == '0.9626350356771984 1'
        assert p.face('side1').shift == '-1.7264992203753446 0'

        s = Brush.make_slice(axis='x', center='0 0 -0.5', size='1 2 4', inner_size='1 1 2', start_angle=45, end_angle=90, texture=scaled_edge)
        assert len(s.vertices) == 8
        assert s.vertices[2] == '0.5 0 -1.5'
        assert s.face('end').normal == '0 -1 0'

        s.rotate('0 0 1 90', '0 0 0')
        assert s.vertices[2] == '0 -0.5 -1.5'
        assert s.face('top').normal == '0 -1 0'
        assert s.face('outside').tangent == '0 -1 0'
        assert s.face('outside').shift == '-0.5 -0.4179080861115082'

        ss = Brush.make_slice(axis='z', center='0 0 -0.5', size='4 2 1', inner_size='0 0 0', start_angle=45, end_angle=90, texture=scaled_edge)
        assert len(ss.vertices) == 6
        assert ss.vertices[4] == '0 0 0'

        Brush.make_slices(axis='y', center='0 -0.5 0', size='4 1 2', inner_size='2 1 1', step_angle=15, texture=scaled_edge)


if __name__ == '__main__':
    Brush.tests()

__all__ = ['Brush']
