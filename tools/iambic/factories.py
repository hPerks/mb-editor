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


def trim(axis, size):
    return lambda: Brush.make_cube(
        center=(0, 0, -size if axis == 'z' else -0.25),
        size=(
            '0.5 0.5 0.5' if size == 0 else
            (
                size * 2 if axis == 'x' else 0.5,
                size * 2 if axis == 'y' else 0.5,
                size * 2 if axis == 'z' else 0.5
            )
        ),
        texture=Texture.edge
    )


def ramptrim(axis, size, slope):
    return lambda: Brush.make_cube(
        center=(0, 0, -0.25 - slope / 100 * (size if axis == 'y' else 0.25)),
        size=(
            size * 2 if axis == 'x' else 0.5,
            size * 2 if axis == 'y' else 0.5,
            0.5
        ),
        texture=Texture.edge
    ).move_face(
        'back',
        (0, 0, slope / 100 * (size * 2 if axis == 'y' else 0.5))
    )


def ramptrim_bottom(slope):
    def make():
        brushes = []
        z = -0.25 - slope / 100
        for i in range(1, 5):
            z_increment = i * slope / 100 * 0.1
            brushes.append(
                Brush.make_cube(
                    center=(0, -2.25 + 0.5 * i, z),
                    size=(0.5, 0.5, 0.5),
                    texture=Texture.edge
                ).move_face('back', (0, 0, z_increment))
            )
            z += z_increment
        return brushes

    return make


def ramptrim_top(slope):
    def make():
        brushes = []
        z = -0.25 + slope / 100
        for i in range(1, 5):
            z_increment = -i * slope / 100 * 0.1
            brushes.append(
                Brush.make_cube(
                    center=(0, 2.25 - 0.5 * i, z),
                    size=(0.5, 0.5, 0.5),
                    texture=Texture.edge
                ).move_face('front', (0, 0, z_increment))
            )
            z += z_increment
        return brushes

    return make


def ring(size):
    return lambda: Brush.make_slices(
        axis='y',
        center=(0, 0, size),
        size=(size * 2 + 1, 0.5, size * 2 + 1),
        inner_size=(size * 2, 0.5, size * 2),
        step_angle=9,
        texture=Texture.edge,
        justify=4
    )


def halfring(size):
    return lambda: Brush.make_slices(
        axis='y',
        center=(0, 0, size),
        size=(size * 2 + 1, 0.5, size * 2 + 1),
        inner_size=(size * 2, 0.5, size * 2),
        end_angle=180,
        step_angle=9,
        texture=Texture.edge,
        justify=2
    )


def quarterring(size):
    return lambda: Brush.make_slices(
        axis='x',
        center=(0, 0, size),
        size=(0.5, size * 2 + 1, size * 2 + 1),
        inner_size=(0.5, size * 2, size * 2),
        end_angle=90,
        step_angle=9,
        texture=Texture.edge,
        justify=1
    )


def platform(texture, width, length):
    return lambda: Brush.make_cube(
        center='0 0 -0.25',
        size=(width * 2, length * 2, 0.5),
        texture={
            'z': floor_textures[texture],
            'side': Texture.edge,
        }
    )


def wall(texture, width, height):
    return lambda: Brush.make_cube(
        center=(0, 0, -height),
        size=(
            width * 2,
            0.5,
            height * 2
        ),
        texture={
            'all': Texture.edge,
            'y': wall_textures[texture]
        }
    )


def ramp(texture, size, slope):
    return lambda: Brush.make_cube(
        center=(0, 0, -0.25 - slope / 100 * size),
        size=(size * 2, size * 2, 0.5),
        texture={
            'z': floor_textures[texture],
            'side': Texture.edge,
        }
    ).move_face(
        'back',
        (0, 0, slope / 100 * size * 2)
    )


def ramp_bottom(texture, size, slope):
    def make():
        brushes = []
        z = -0.25 - slope
        for i in range(1, 5):
            z_increment = i * slope / 100 * 0.1
            brushes.append(
                Brush.make_cube(
                    center=(0, -2.25 + 0.5 * i, z),
                    size=(size * 2, 0.5, 0.5),
                    texture={
                        'z': floor_textures[texture],
                        'side': Texture.edge,
                    },
                    origin={
                        'z': (-size, 0, 0)
                    }
                ).move_face('back', (0, 0, z_increment))
            )
            z += z_increment
        return brushes

    return make


def ramp_top(texture, size, slope):
    def make():
        brushes = []
        z = -0.25 + slope
        for i in range(1, 5):
            z_increment = -i * slope / 100 * 0.1
            brushes.append(
                Brush.make_cube(
                    center=(0, 2.25 - 0.5 * i, z),
                    size=(size * 2, 0.5, 0.5),
                    texture={
                        'z': floor_textures[texture],
                        'side': Texture.edge,
                    },
                    origin={
                        'z': (-size, 0, 0)
                    },
                ).move_face('front', (0, 0, z_increment))
            )
            z += z_increment
            brushes.append(brush)
        return brushes

    return make


def cube(texture, size):
    return lambda: Brush.make_cube(
        center=(0, 0, -size),
        size=(size * 2, size * 2, size * 2),
        texture=floor_textures[texture]
    )


def circle(texture, size):
    return lambda: Brush.make_prism(
        sides=40,
        center=(0, 0, -0.25),
        size=(size * 2, size * 2, 0.5),
        texture={
            'z': floor_textures[texture],
            'side': Texture.edge
        },
        origin={
            'z': (-size, size, 0)
        },
        justify=4
    )


def halfcircle(texture, size):
    return lambda: Brush.make_prism(
        sides=40,
        center=(0, 0, -0.25),
        size=(size * 2, size * 2, 0.5),
        start_angle=180,
        end_angle=360,
        texture={
            'z': floor_textures[texture],
            'side': Texture.edge
        },
        origin={
            'z': (-size, size, 0)
        },
        justify=2
    )


def quartercircle(texture, size):
    return lambda: Brush.make_prism(
        sides=40,
        center=(0, 0, -0.25),
        size=(size * 2, size * 2, 0.5),
        start_angle=270,
        end_angle=360,
        texture={
            'z': floor_textures[texture],
            'side': Texture.edge
        },
        origin={
            'z': (-size, size, 0)
        },
        justify=1
    )


def pipe(texture, size, length):
    return lambda: Brush.make_slices(
        axis='y',
        center=(0, 0, size),
        size=(size * 2 + 1, length * 2, size * 2 + 1),
        inner_size=(size * 2, length * 2, size * 2),
        step_angle=9,
        texture={
            'side': floor_textures[texture],
            'z': Texture.edge,
        },
        justify=4
    )


def halfpipe(texture, size, length):
    return lambda: Brush.make_slices(
        axis='y',
        center=(0, 0, size),
        size=(size * 2 + 1, length * 2, size * 2 + 1),
        inner_size=(size * 2, length * 2, size * 2),
        end_angle=180,
        step_angle=9,
        texture={
            'r': floor_textures[texture],
            'theta': Texture.edge,
            'z': Texture.edge,
        },
        justify=2
    )


def quarterpipe(texture, size, length):
    return lambda: Brush.make_slices(
        axis='x',
        center=(0, 0, size),
        size=(length * 2, size * 2 + 1, size * 2 + 1),
        inner_size=(length * 2, size * 2, size * 2),
        end_angle=90,
        step_angle=9,
        texture={
            'r': floor_textures[texture],
            'theta': Texture.edge,
            'z': Texture.edge,
        },
        justify=1
    )


def pipe_corner(texture, size, direction):
    def make():
        brushes = Brush.make_slices(
            axis='y',
            center=(0, -1, size),
            size=(size * 2 + 1, size * 2 + 2, size * 2 + 1),
            inner_size=(size * 2, size * 2 + 2, size * 2),
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
                ) - size
                brush.move_vertex(vertex_index, (0, y_offset, 0))
            for face in brush.face('r'):
                face.skew = '0 0'
        return brushes

    return make


def halfpipe_corner(texture, size, direction):
    def make():
        brushes = Brush.make_slices(
            axis='y',
            center=(0, -1, size),
            size=(size * 2 + 1, size * 2 + 2, size * 2 + 1),
            inner_size=(size * 2, size * 2 + 2, size * 2),
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
                ) - size
                brush.move_vertex(vertex_index, (0, y_offset, 0))
            for face_name in ['inside', 'outside', 'start', 'end']:
                brush.face(face_name).skew = '0 0'
        return brushes

    return make
