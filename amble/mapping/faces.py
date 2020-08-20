from amble.numberlists.vector2d import Vector2D
from amble.numberlists.vector3d import Vector3D
from amble.numberlists.rotation3d import Rotation3D
from amble.utils.numbers import repr_float, approx_div
from amble.utils.cached import Cached
from amble.utils.lists import flatlist


class Faces(Cached):
    inherited_attrs = ['vertex_indices', 'normal', 'texture', 'origin', 'skew', 'rotation', 'scale']
    cached_attrs = [
        'vertices', 'center_bisector', 'middle_bisector', 'tangent',
        'cotangent', 'alignment_vertices', 'tangent_bisector',
        'cotangent_bisector', 'origin', 'skew', 'rotation', 'scale', 'u', 'v',
        'shift'
    ]

    def __init__(self, brush, name):
        super().__init__()
        self.brush, self.name = brush, name

    def __getattr__(self, item):
        group_members = []
        for group_name, face_names in self.brush.face_groups.items():
            if self.name == group_name:
                group_members = face_names
            elif (
                self.name in face_names or (
                    len(group_members) > 0 and
                    all(group_member in face_names for group_member in group_members)
                )
            ):
                group = self.brush.face(group_name)
                try:
                    attr = getattr(group, item)
                    return attr
                except AttributeError:
                    pass
        raise AttributeError

    def __repr__(self):
        with self.cached:
            return (
                ' '.join(
                    '( ' + repr(vertex * 32) + ' )' for vertex in self.vertices[:3]
                ) + ' ' + repr(self.texture) +
                ' [ ' + repr(self.u) + ' ' + repr_float(self.shift.x * 32 / self.texture.scale.x) +
                ' ] [ ' + repr(self.v) + ' ' + repr_float(self.shift.y * 32 / self.texture.scale.y) +
                ' ] 0 ' + repr(self.scale * self.texture.scale)
            )

    @property
    def vertices(self):
        return [self.brush.vertices[i] for i in self.vertex_indices]

    @property
    def center(self):
        return sum(self.vertices) / len(self.vertices)

    @property
    def tangent(self):
        try:
            return self._tangent
        except AttributeError:
            return Rotation3D(*self.normal, self.rotation) * self.normal.tangent()

    @tangent.setter
    def tangent(self, value):
        self._tangent = Vector3D(value)
        self._cotangent = self._tangent.cross(self.normal)

    @property
    def cotangent(self):
        try:
            return self._cotangent
        except AttributeError:
            return Rotation3D(*self.normal, self.rotation) * self.normal.cotangent()

    @cotangent.setter
    def cotangent(self, value):
        self._cotangent = Vector3D(value)
        self._tangent = self.normal.cross(self._cotangent)

    @property
    def center_bisector(self):
        n = len(self.vertices)
        return sum(self.vertices[i + n // 2] - self.vertices[i] for i in range(n // 2)) / (n // 2)

    @property
    def middle_bisector(self):
        n = len(self.vertices)
        return sum(self.vertices[i + n // 4] - self.vertices[i - n // 4] for i in range(n // 2)) / (n // 2)

    @property
    def alignment_vertices(self):
        return [
            self.vertices[index]
            for index in (
                [0, 1, 2, 3] if (
                    self.middle_bisector.is_facing(self.tangent) or
                    self.center_bisector.is_facing(self.cotangent)
                ) else [1, 2, 3, 0] if (
                    self.center_bisector.is_facing(self.tangent) or
                    self.middle_bisector.is_facing(-self.cotangent)
                ) else [2, 3, 0, 1] if (
                    self.middle_bisector.is_facing(-self.tangent) or
                    self.center_bisector.is_facing(-self.cotangent)
                ) else [3, 0, 1, 2] if (
                    self.center_bisector.is_facing(-self.tangent) or
                    self.middle_bisector.is_facing(self.cotangent)
                ) else []
            )
        ]

    @property
    def tangent_bisector(self):
        vertices = self.alignment_vertices
        if len(vertices):
            return (vertices[1] + vertices[2] - vertices[0] - vertices[3]) / 2

    @property
    def cotangent_bisector(self):
        vertices = self.alignment_vertices
        if len(self.alignment_vertices):
            return (vertices[2] + vertices[3] - vertices[0] - vertices[1]) / 2

    def alignment_point(self, string=None, horizontal=0, vertical=0):
        if string is not None:
            if string == 'world':
                return Vector3D(0, 0, 0)
            horizontal = -1 if 'left' in string else 1 if 'right' in string else 0
            vertical = -1 if 'top' in string else 1 if 'bottom' in string else 0

        vertices = self.alignment_vertices
        if horizontal == -1:
            return vertices[0] + (vertices[3] - vertices[0]) * (vertical + 1) / 2
        elif horizontal == 1:
            return vertices[1] + (vertices[2] - vertices[1]) * (vertical + 1) / 2
        elif vertical == -1:
            return (vertices[0] + vertices[1]) / 2
        elif vertical == 1:
            return (vertices[3] + vertices[2]) / 2
        else:
            return self.center

    @property
    def origin(self):
        try:
            return self._origin
        except AttributeError:
            if len(self.alignment_vertices):
                return self.alignment_point(
                    horizontal=-1 if approx_div(self.tangent_bisector.dot(self.tangent), self.texture.size.x) else 0,
                    vertical=-1 if approx_div(self.cotangent_bisector.dot(self.cotangent), self.texture.size.y) else 0,
                )
            return self.center

    @origin.setter
    def origin(self, value):
        self._origin = Vector3D(value)

    def align(self, string=None, horizontal=0, vertical=0):
        self.origin = self.alignment_point(string, horizontal, vertical)
        return self

    def reset_rotation(self):
        self.origin = self.origin
        del self._tangent, self._cotangent
        return self

    @property
    def skew(self):
        try:
            return self._skew
        except AttributeError:
            if len(self.alignment_vertices):
                return Vector2D(
                    self.tangent_bisector.dot(self.cotangent) / self.tangent_bisector.dot(self.tangent),
                    self.cotangent_bisector.dot(self.tangent) / self.cotangent_bisector.dot(self.cotangent)
                )
            return Vector2D(0, 0)

    @skew.setter
    def skew(self, value):
        self._skew = Vector2D(value)

    @property
    def u(self):
        return self.tangent - self.cotangent * self.skew.y

    @property
    def v(self):
        return self.cotangent - self.tangent * self.skew.x

    @property
    def w(self):
        return self.normal

    @property
    def shift(self):
        return Vector2D(
            -self.origin.dot(self.u) / self.scale.x,
            -self.origin.dot(self.v) / self.scale.y
        )

    def from_uvw(self, uvw):
        return self.origin + uvw.x * self.u + uvw.y * self.v + uvw.z * self.w

    def to_uvw(self, point):
        return (point - self.origin).to_basis(self.u, self.v, self.w)

    def shared_vertices(self, face):
        return [vertex for vertex in self.vertices if vertex in face.vertices]

    def unify_with(self, *faces, justify=False):
        faces = flatlist([self] + list(faces))
        if justify:
            tangent_perimeter, cotangent_perimeter = 0, 0
            for face in faces:
                with face.cached:
                    tangent_perimeter += abs(face.tangent_bisector)
                    cotangent_perimeter += abs(face.cotangent_bisector)

            tangent_tiles = tangent_perimeter / (self.texture.size.x * self.scale.x * justify)
            cotangent_tiles = cotangent_perimeter / (self.texture.size.y * self.scale.y * justify)

            scale_x = tangent_tiles if round(tangent_tiles) == 0 else tangent_tiles / round(tangent_tiles)
            scale_y = cotangent_tiles if round(cotangent_tiles) == 0 else cotangent_tiles / round(cotangent_tiles)

            for face in faces:
                face.scale *= (scale_x, scale_y)

        for i in range(len(faces) - 1):
            with faces[i].cached, faces[i + 1].cached:
                vertices = faces[i].shared_vertices(faces[i + 1])
                pivot_point = sum(vertices) / len(vertices)
                uvw = faces[i].to_uvw(pivot_point)
                new_origin = faces[i + 1].from_uvw(-uvw) - faces[i + 1].origin + pivot_point
            faces[i + 1].origin = new_origin

        return self

    @classmethod
    def unify(cls, *faces, justify=False):
        faces = flatlist(*faces)
        return faces[0].unify_with(faces[1:], justify=justify)
