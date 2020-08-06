from mb_editor.numberlists.vector2d import Vector2D
from mb_editor.numberlists.vector3d import Vector3D
from mb_editor.numberlists.numberlist import NumberList


class Faces:
    inherited_attrs = ['vertex_indices', 'normal', 'texture', 'origin', 'skew', 'rotation']

    def __init__(self, brush, name):
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
        return (
            ' '.join(
                '( ' + repr(vertex * 32) + ' )' for vertex in self.vertices[:3]
            ) + ' ' + repr(self.texture) +
            ' [ ' + repr(self.u) + ' ] [ ' + repr(self.v) + ' ] ' +
            repr(self.rotation) + ' ' + repr(self.texture.scale)
        )

    @property
    def vertices(self):
        return [self.brush.vertices[i] for i in self.vertex_indices]

    @property
    def top_left(self):
        return self.vertices[0]

    @property
    def center(self):
        return (self.vertices[0] + self.vertices[1] + self.vertices[2] + self.vertices[3]) / 4

    @property
    def left_edge(self):
        return self.vertices[3] - self.vertices[0]

    @property
    def right_edge(self):
        return self.vertices[2] - self.vertices[1]

    @property
    def center_bisector(self):
        return (self.left_edge + self.right_edge) / 2

    @property
    def top_edge(self):
        return self.vertices[1] - self.vertices[0]

    @property
    def bottom_edge(self):
        return self.vertices[2] - self.vertices[3]

    @property
    def middle_bisector(self):
        return (self.top_edge + self.bottom_edge) / 2

    @property
    def tangent(self):
        return self.normal.tangent()

    @property
    def cotangent(self):
        return self.normal.cotangent()

    @property
    def origin(self):
        try:
            return self._origin
        except AttributeError:
            if (
                self.middle_bisector.dot(self.tangent) % self.texture.size.x == 0 and
                self.center_bisector.dot(self.cotangent) % self.texture.size.y == 0
            ):
                return self.top_left
            return self.center

    @origin.setter
    def origin(self, value):
        self._origin = Vector3D(value)

    @property
    def skew(self):
        try:
            return self._skew
        except AttributeError:
            return Vector2D(
                self.center_bisector.dot(self.tangent) / self.center_bisector.dot(self.cotangent),
                self.middle_bisector.dot(self.cotangent) / self.middle_bisector.dot(self.tangent)
            )

    @skew.setter
    def skew(self, value):
        self._skew = Vector2D(value)

    @property
    def shift(self):
        return Vector2D(
            -self.origin.dot(self.tangent) + self.origin.dot(self.cotangent) * self.skew.x,
            -self.origin.dot(self.cotangent) + self.origin.dot(self.tangent) * self.skew.y
        )

    @property
    def u(self):
        return NumberList(*(self.tangent - self.cotangent * self.skew.x), self.shift.x * 32 / self.texture.scale.x)

    @property
    def v(self):
        return NumberList(*(self.cotangent - self.tangent * self.skew.y), self.shift.y * 32 / self.texture.scale.y)
