from .vector3d import Vector3D


class Rotation3D(Vector3D):

    @property
    def angle(self):
        return self[3]

    @angle.setter
    def angle(self, value):
        self[3] = value

Rotation3D.identity = Rotation3D(1, 0, 0, 0)
