from amble.numberlists.vector2d import Vector2D
from amble.numberlists.vector3d import Vector3D
from amble.numberlists.rotation3d import Rotation3D
from amble.utils.numbers import repr_float, approx_div


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
            ' [ ' + repr(self.u) + ' ' + repr_float(self.shift.x * 32 / self.texture.scale.x) +
            ' ] [ ' + repr(self.v) + ' ' + repr_float(self.shift.y * 32 / self.texture.scale.y) +
            ' ] 0 ' + repr(self.texture.scale)
        )

    @property
    def vertices(self):
        return [self.brush.vertices[i] for i in self.vertex_indices]

    @property
    def top_left(self):
        return self.vertices[0]

    @property
    def center(self):
        return sum(self.vertices) / len(self.vertices)

    @property
    def left_edge(self):
        return self.vertices[-1] - self.vertices[0]

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
        return self.vertices[-2] - self.vertices[-1]

    @property
    def middle_bisector(self):
        return (self.top_edge + self.bottom_edge) / 2

    @property
    def tangent(self):
        return Rotation3D(*self.normal, self.rotation) * self.normal.tangent()

    @property
    def cotangent(self):
        return Rotation3D(*self.normal, self.rotation) * self.normal.cotangent()

    @property
    def alignment_orientation(self):
        if (
            self.center_bisector.is_perpendicular(self.tangent) or
            self.middle_bisector.is_perpendicular(self.cotangent)
        ):
            return 'normal'
        elif (
            self.middle_bisector.is_perpendicular(self.tangent) or
            self.center_bisector.is_perpendicular(self.cotangent)
        ):
            return 'rotated'
        else:
            return 'none'

    @property
    def tangent_bisector(self):
        return {
            'normal': self.middle_bisector,
            'rotated': self.center_bisector,
            'none': None
        }[self.alignment_orientation]

    @property
    def cotangent_bisector(self):
        return {
            'normal': self.center_bisector,
            'rotated': self.middle_bisector,
            'none': None
        }[self.alignment_orientation]

    @property
    def origin(self):
        try:
            return self._origin
        except AttributeError:
            if self.alignment_orientation != 'none':
                if (
                    approx_div(self.tangent_bisector.dot(self.tangent), self.texture.size.x) and
                    approx_div(self.cotangent_bisector.dot(self.cotangent), self.texture.size.y)
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
            if self.alignment_orientation == 'none':
                return Vector2D(0, 0)
            else:
                return Vector2D(
                    self.cotangent_bisector.dot(self.tangent) / self.cotangent_bisector.dot(self.cotangent),
                    self.tangent_bisector.dot(self.cotangent) / self.tangent_bisector.dot(self.tangent)
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
        return self.tangent - self.cotangent * self.skew.y

    @property
    def v(self):
        return self.cotangent - self.tangent * self.skew.x
