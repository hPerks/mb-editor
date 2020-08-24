from amble.mapping import *


floor_textures = {
    'white': Texture(file='pq_circles_gray_light', dimensions='4 4', scale='0.5 0.5'),
    'red': Texture(file='pq_hot_1_med', dimensions='4 4', scale='0.5 0.5'),
    'yellow': Texture(file='pq_neutral_4_med', dimensions='4 4', scale='0.5 0.5'),
    'blue': Texture(file='pq_rays_blue_med', dimensions='4 4', scale='0.5 0.5'),
    'bouncy': Texture(file='pq_friction_bouncy', dimensions='4 4', scale='0.5 0.5'),
    'grass': Texture(file='pq_friction_grass', dimensions='8 8', scale='0.5 0.5'),
    'ice': Texture(file='pq_friction_ice', dimensions='16 16', scale='0.25 0.25'),
    'mud': Texture(file='pq_friction_mud', dimensions='8 8', scale='0.5 0.5'),
    'sand': Texture(file='pq_friction_sand', dimensions='8 8', scale='0.5 0.5'),
    'space': Texture(file='pq_friction_space', dimensions='8 8', scale='0.5 0.5'),
    'water': Texture(file='pq_friction_water', dimensions='4 4', scale='0.5 0.5'),
}

wall_textures = {
    'white': Texture(file='pq_wall_white', dimensions='4 4', scale='0.5 0.5'),
    'red': Texture(file='pq_wall_red', dimensions='4 4', scale='0.5 0.5'),
    'yellow': Texture(file='pq_wall_yellow', dimensions='4 4', scale='0.5 0.5'),
    'blue': Texture(file='pq_wall_blue', dimensions='4 4', scale='0.5 0.5'),
    'bouncy': Texture(file='pq_friction_bouncy', dimensions='4 4', scale='0.5 0.5'),
    'grass': Texture(file='pq_friction_grass', dimensions='8 8', scale='0.5 0.5'),
    'ice': Texture(file='pq_friction_ice', dimensions='16 16', scale='0.25 0.25'),
    'mud': Texture(file='pq_friction_mud', dimensions='8 8', scale='0.5 0.5'),
    'sand': Texture(file='pq_friction_sand', dimensions='8 8', scale='0.5 0.5'),
    'space': Texture(file='pq_friction_space', dimensions='8 8', scale='0.5 0.5'),
    'water': Texture(file='pq_friction_water', dimensions='4 4', scale='0.5 0.5'),
}


def trim_cube(slope=None, **kwargs):
    slope = slope or 0
    return lambda: Brush.make_cube(
        center=(0, 0, -0.25 - slope / 100 * 0.25),
        size='0.5 0.5 0.5',
        texture=Texture.edge
    ).move_face(
        'back',
        (0, 0, slope / 100 * 0.5)
    )


def trim(axis=None, length=None, slope=None, part=None, **kwargs):
    slope = slope or 0
    if part is None:
        return lambda: Brush.make_cube(
            center=(0, 0, -length if axis == 'z' else (-0.25 - slope / 100 * (length if axis == 'y' else 0.25))),
            size=(
                length * 2 if axis == 'x' else 0.5,
                length * 2 if axis == 'y' else 0.5,
                length * 2 if axis == 'z' else 0.5
            ),
            texture=Texture.edge
        ).move_face(
            'back',
            (0, 0, slope / 100 * (length * 2 if axis == 'y' else 0.5))
        )
    else:
        sign = -1 if part == 'bottom' else 1

        def make():
            brushes = []
            z = -0.25 + sign * slope / 100
            for i in range(1, 5):
                z_increment = -sign * i * slope / 100 * 0.1
                brushes.append(
                    Brush.make_cube(
                        center=(0, sign * (2.25 - 0.5 * i), z),
                        size=(0.5, 0.5, 0.5),
                        texture=Texture.edge
                    ).move_face('back' if part == 'bottom' else 'front', (0, 0, z_increment))
                )
                z += z_increment
            return brushes

        return make


def ring(x, y, **kwargs):
    return lambda: Brush.make_slices(
        axis='y',
        center=(0, 0, y),
        size=(x * 2 + 1, 0.5, y * 2 + 1),
        inner_size=(x * 2, 0.5, y * 2),
        step_angle=9,
        texture=Texture.edge,
        justify=4
    )


def halfring(x, y, **kwargs):
    return lambda: Brush.make_slices(
        axis='y',
        center=(0, 0, y),
        size=(x * 2 + 1, 0.5, y * 2 + 1),
        inner_size=(x * 2, 0.5, y * 2),
        end_angle=180,
        step_angle=9,
        texture=Texture.edge,
        justify=2
    )


def quarterring(x, y, **kwargs):
    return lambda: Brush.make_slices(
        axis='x',
        center=(0, 0, x),
        size=(0.5, y * 2 + 1, x * 2 + 1),
        inner_size=(0.5, y * 2, x * 2),
        end_angle=90,
        step_angle=9,
        texture=Texture.edge,
        justify=1
    )


def platform(texture, x, y, **kwargs):
    return lambda: Brush.make_cube(
        center='0 0 -0.25',
        size=(x * 2, y * 2, 0.5),
        texture={
            'z': floor_textures[texture],
            'side': Texture.edge,
        }
    )


def wall(texture, x, z, **kwargs):
    return lambda: Brush.make_cube(
        center=(0, 0, -z),
        size=(
            x * 2,
            0.5,
            z * 2
        ),
        texture={
            'all': Texture.edge,
            'y': wall_textures[texture]
        }
    )


def ramp(texture, x, y, slope, part=None, **kwargs):
    if part is None:
        return lambda: Brush.make_cube(
            center=(0, 0, -0.25 - slope / 100 * y),
            size=(x * 2, y * 2, 0.5),
            texture={
                'z': floor_textures[texture],
                'side': Texture.edge,
            }
        ).move_face(
            'back',
            (0, 0, slope / 100 * y * 2)
        )
    else:
        sign = -1 if part == 'bottom' else 1

        def make():
            brushes = []
            z = -0.25 + sign * slope / 100
            for i in range(1, 5):
                z_increment = -sign * i * slope / 100 * 0.1
                brushes.append(
                    Brush.make_cube(
                        center=(0, sign * (2.25 - 0.5 * i), z),
                        size=(x * 2, 0.5, 0.5),
                        texture={
                            'z': floor_textures[texture],
                            'side': Texture.edge,
                        },
                        origin={
                            'z': (-x, 0, 0)
                        }
                    ).move_face('back' if part == 'bottom' else 'front', (0, 0, z_increment))
                )
                z += z_increment
            return brushes

        return make


def cube(texture, x, y, z, **kwargs):
    return lambda: Brush.make_cube(
        center=(0, 0, -z),
        size=(x * 2, y * 2, z * 2),
        texture=floor_textures[texture]
    )


def circle(texture, x, y, hole_x=None, hole_y=None, **kwargs):
    if hole_x is None:
        return lambda: Brush.make_prism(
            sides=40,
            center=(0, 0, -0.25),
            size=(x * 2, y * 2, 0.5),
            texture={
                'z': floor_textures[texture],
                'side': Texture.edge
            },
            origin={
                'z': (-x, y, 0)
            },
            justify=4
        )
    else:
        return lambda: Brush.make_slices(
            axis='z',
            center=(0, 0, -0.25),
            size=(x * 2, y * 2, 0.5),
            inner_size=(hole_x * 2, hole_y * 2, 0.5),
            step_angle=9,
            texture={
                'z': floor_textures[texture],
                'side': Texture.edge
            },
            origin={
                'z': (-x, y, 0)
            },
            justify={
                'r': 4
            }
        )


def halfcircle(texture, x, y, hole_x=None, hole_y=None, **kwargs):
    if hole_x is None:
        return lambda: Brush.make_prism(
            sides=40,
            center=(0, 0, -0.25),
            size=(x * 2, y * 2, 0.5),
            start_angle=180,
            end_angle=360,
            texture={
                'z': floor_textures[texture],
                'side': Texture.edge
            },
            origin={
                'z': (-x, y, 0)
            },
            justify=2
        )
    else:
        return lambda: Brush.make_slices(
            axis='z',
            center=(0, 0, -0.25),
            size=(x * 2, y * 2, 0.5),
            inner_size=(hole_x * 2, hole_y * 2, 0.5),
            start_angle=180,
            end_angle=360,
            step_angle=9,
            texture={
                'z': floor_textures[texture],
                'side': Texture.edge
            },
            origin={
                'z': (-x, y, 0)
            },
            justify={
                'r': 2
            }
        )


def quartercircle(texture, x, y, hole_x=None, hole_y=None, **kwargs):
    if hole_x is None:
        return lambda: Brush.make_prism(
            sides=40,
            center=(0, 0, -0.25),
            size=(x * 2, y * 2, 0.5),
            start_angle=270,
            end_angle=360,
            texture={
                'z': floor_textures[texture],
                'side': Texture.edge
            },
            origin={
                'z': (-x, y, 0)
            },
            justify=1
        )
    else:
        return lambda: Brush.make_slices(
            axis='z',
            center=(0, 0, -0.25),
            size=(x * 2, y * 2, 0.5),
            inner_size=(hole_x * 2, hole_y * 2, 0.5),
            start_angle=270,
            end_angle=360,
            step_angle=9,
            texture={
                'z': floor_textures[texture],
                'side': Texture.edge
            },
            origin={
                'z': (-x, y, 0)
            },
            justify={
                'r': 1
            }
        )


def pipe(texture, x, y, z, part=None, direction=None, **kwargs):
    if part is None:
        return lambda: Brush.make_slices(
            axis='y',
            center=(0, 0, y),
            size=(x * 2 + 1, z * 2, y * 2 + 1),
            inner_size=(x * 2, z * 2, y * 2),
            step_angle=9,
            texture={
                'side': floor_textures[texture],
                'z': Texture.edge,
            },
            justify=4
        )
    else:
        def make():
            brushes = Brush.make_slices(
                axis='y',
                center=(0, -1, y),
                size=(x * 2 + 1, z * 2 + 2, y * 2 + 1),
                inner_size=(x * 2, z * 2 + 2, y * 2),
                step_angle=9,
                texture={
                    'side': floor_textures[texture],
                    'z': Texture.edge,
                },
                justify=4
            )
            for brush in brushes:
                for vertex_index in brush.face('bottom').vertex_indices:
                    vertex = brush.vertices[vertex_index]
                    y_offset = (
                        -abs(vertex.x) if direction == 'leftright' else
                        vertex.x if direction == 'left' else
                        -vertex.x
                    ) - x
                    brush.move_vertex(vertex_index, (0, y_offset, 0))
                for face in brush.face('r'):
                    face.skew = '0 0'
            return brushes

        return make


def halfpipe(texture, x, y, z, part=None, direction=None, **kwargs):
    if part is None:
        return lambda: Brush.make_slices(
            axis='y',
            center=(0, 0, y),
            size=(x * 2 + 1, z * 2, y * 2 + 1),
            inner_size=(x * 2, z * 2, y * 2),
            end_angle=180,
            step_angle=9,
            texture={
                'r': floor_textures[texture],
                'theta': Texture.edge,
                'z': Texture.edge,
            },
            justify=2
        )
    else:
        def make():
            brushes = Brush.make_slices(
                axis='y',
                center=(0, -1, y),
                size=(x * 2 + 1, z * 2 + 2, y * 2 + 1),
                inner_size=(x * 2, z * 2 + 2, y * 2),
                end_angle=180,
                step_angle=9,
                texture={
                    'r': floor_textures[texture],
                    'theta': Texture.edge,
                    'z': Texture.edge,
                },
                justify=2
            )
            for brush in brushes:
                for vertex_index in brush.face('bottom').vertex_indices:
                    vertex = brush.vertices[vertex_index]
                    y_offset = (
                        -abs(vertex.x) if direction == 'leftright' else
                        vertex.x if direction == 'left' else
                        -vertex.x
                    ) - x
                    brush.move_vertex(vertex_index, (0, y_offset, 0))
                for face_name in ['inside', 'outside', 'start', 'end']:
                    brush.face(face_name).skew = '0 0'
            return brushes

        return make


def quarterpipe(texture, x, y, z, **kwargs):
    return lambda: Brush.make_slices(
        axis='x',
        center=(0, 0, x),
        size=(z * 2, y * 2 + 1, x * 2 + 1),
        inner_size=(z * 2, y * 2, x * 2),
        end_angle=90,
        step_angle=9,
        texture={
            'r': floor_textures[texture],
            'theta': Texture.edge,
            'z': Texture.edge,
        },
        justify=1
    )
