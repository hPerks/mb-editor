import os

from amble import *


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

mission = Mission.normal(
    name='IAMBIC Tests',
    artist='hPerks',
    desc='IAMBIC: the Itemized Auxiliary Marble Blast Interiors Collection.',
).add(
    StartPad()
)
mission.next_y = 4.0


def export(brush_maker, name, center, size):
    print('export', name)
    if 'trim' in name or 'white' in name:
        mission.add(Interior.local('iambic/' + name, position=Vector3D.j * (mission.next_y + size / 2 - center)))
        mission.next_y += size + 2
    if not os.path.exists(path.platinum('data/interiors_pq/custom/iambic', name + '.dif')):
        brushes = flatlist(brush_maker())
        return Map(
            brushes,
            Map([brush.copy() for brush in brushes])
        ).to_interior(
            os.path.basename(name), subdir='iambic/' + os.path.dirname(name)
        )


def trim(axis, size):
    return export(
        lambda: Brush.make_cube(
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
        ),
        name='trim/trim_{}{}'.format(axis, '' if size == 0 else size),
        center=0,
        size=size * 2 if axis == 'y' else 0.5
    )


def ramptrim(axis, size, slope):
    return export(
        lambda: Brush.make_cube(
            center=(0, 0, -0.25 - slope * (size if axis == 'y' else 0.25)),
            size=(
                size * 2 if axis == 'x' else 0.5,
                size * 2 if axis == 'y' else 0.5,
                0.5
            ),
            texture=Texture.edge
        ).move_face(
            'back',
            (0, 0, slope * (size * 2 if axis == 'y' else 0.5))
        ),
        name='trim/trim_{}{}_slope{}'.format(axis, '' if size == 0 else size, int(slope * 100)),
        center=0,
        size=size * 2 if axis == 'y' else 0.5
    )


def ramptrim_bottom(slope):
    def make():
        brushes = []
        z = -0.25 - slope
        for i in range(1, 5):
            brush = Brush.make_cube(
                center=(0, -2.25 + 0.5 * i, z),
                size=(0.5, 0.5, 0.5),
                texture=Texture.edge
            ).move_face('back', (0, 0, i * slope * 0.1))
            z += i * slope * 0.1
            brushes.append(brush)
        return brushes

    return export(
        make,
        'trim/trim_slope{}_bottom'.format(int(slope * 100)),
        center=-1,
        size=2
    )


def ramptrim_top(slope):
    def make():
        brushes = []
        z = -0.25 + slope
        for i in range(1, 5):
            brush = Brush.make_cube(
                center=(0, 2.25 - 0.5 * i, z),
                size=(0.5, 0.5, 0.5),
                texture=Texture.edge
            ).move_face('front', (0, 0, -i * slope * 0.1))
            z -= i * slope * 0.1
            brushes.append(brush)
        return brushes

    return export(
        make,
        'trim/trim_slope{}_top'.format(int(slope * 100)),
        center=1,
        size=2
    )


def ring(size):
    return export(
        lambda: Brush.make_slices(
            axis='y',
            center=(0, 0, size),
            size=(size * 2 + 1, 0.5, size * 2 + 1),
            inner_size=(size * 2, 0.5, size * 2),
            step_angle=9,
            texture=Texture.edge,
            justify=4
        ),
        name='ring/ring_{}x{}'.format(size, size),
        center=0,
        size=0.5
    )


def halfring(size):
    return export(
        lambda: Brush.make_slices(
            axis='y',
            center=(0, 0, size),
            size=(size * 2 + 1, 0.5, size * 2 + 1),
            inner_size=(size * 2, 0.5, size * 2),
            end_angle=180,
            step_angle=9,
            texture=Texture.edge,
            justify=2
        ),
        name='halfring/halfring_{}x{}'.format(size, size),
        center=0,
        size=0.5
    )


def quarterring(size):
    return export(
        lambda: Brush.make_slices(
            axis='x',
            center=(0, 0, size),
            size=(0.5, size * 2 + 1, size * 2 + 1),
            inner_size=(0.5, size * 2, size * 2),
            end_angle=90,
            step_angle=9,
            texture=Texture.edge,
            justify=1
        ),
        name='quarterring/quarterring_{}x{}'.format(size, size),
        center=size / 2 + 0.25,
        size=size + 0.5
    )


def platform(texture, width, length):
    return export(
        lambda: Brush.make_cube(
            center='0 0 -0.25',
            size=(width * 2, length * 2, 0.5),
            texture={
                'z': floor_textures[texture],
                'side': Texture.edge,
            }
        ),
        name='platform/platform_{}_{}x{}'.format(texture, width, length),
        center=0,
        size=length * 2
    )


def wall(texture, width, height):
    return export(
        lambda: Brush.make_cube(
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
        ),
        name='wall/wall_{}_{}x{}'.format(texture, width, height),
        center=0,
        size=0.5
    )


def ramp(texture, size, slope):
    return export(
        lambda: Brush.make_cube(
            center=(0, 0, -0.25 - slope * size),
            size=(size * 2, size * 2, 0.5),
            texture={
                'z': floor_textures[texture],
                'side': Texture.edge,
            }
        ).move_face(
            'back',
            (0, 0, slope * size * 2)
        ),
        name='ramp/ramp_{}_{}x{}_slope{}'.format(texture, size, size, int(slope * 100)),
        center=0,
        size=size * 2
    )


def ramp_bottom(texture, size, slope):
    def make():
        brushes = []
        z = -0.25 - slope
        for i in range(1, 5):
            brush = Brush.make_cube(
                center=(0, -2.25 + 0.5 * i, z),
                size=(size * 2, 0.5, 0.5),
                texture={
                    'z': floor_textures[texture],
                    'side': Texture.edge,
                },
                origin={
                    'z': (-size, 0, 0)
                },
            ).move_face('back', (0, 0, i * slope * 0.1))
            z += i * slope * 0.1
            brushes.append(brush)
        return brushes

    return export(
        make,
        'ramp/ramp_{}_{}x{}_slope{}_bottom'.format(texture, size, size, int(slope * 100)),
        center=-1,
        size=2
    )


def ramp_top(texture, size, slope):
    def make():
        brushes = []
        z = -0.25 + slope
        for i in range(1, 5):
            brush = Brush.make_cube(
                center=(0, 2.25 - 0.5 * i, z),
                size=(size * 2, 0.5, 0.5),
                texture={
                    'z': floor_textures[texture],
                    'side': Texture.edge,
                },
                origin={
                    'z': (-size, 0, 0)
                },
            ).move_face('front', (0, 0, -i * slope * 0.1))
            z -= i * slope * 0.1
            brushes.append(brush)
        return brushes

    return export(
        make,
        name='ramp/ramp_{}_{}x{}_slope{}_top'.format(texture, size, size, int(slope * 100)),
        center=1,
        size=2
    )


def cube(texture, size):
    return export(
        lambda: Brush.make_cube(
            center=(0, 0, -size),
            size=(size * 2, size * 2, size * 2),
            texture=floor_textures[texture]
        ),
        name='cube/cube_{}_{}x{}x{}'.format(texture, size, size, size),
        center=0,
        size=size * 2
    )


def circle(texture, size):
    return export(
        lambda: Brush.make_prism(
            sides=40,
            center=(0, 0, -0.25),
            size=(size * 2, size * 2, 0.5),
            texture={
                'z': floor_textures[texture],
                'side': Texture.edge
            },
            justify=4
        ),
        name='circle/circle_{}_{}x{}'.format(texture, size, size),
        center=0,
        size=size * 2
    )


def pipe(texture, size, length):
    return export(
        lambda: Brush.make_slices(
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
        ),
        name='pipe/pipe_{}_{}x{}x{}'.format(texture, size, size, length),
        center=0,
        size=length * 2
    )


def halfpipe(texture, size, length):
    return export(
        lambda: Brush.make_slices(
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
        ),
        name='halfpipe/halfpipe_{}_{}x{}x{}'.format(texture, size, size, length),
        center=0,
        size=length * 2
    )


def quarterpipe(texture, size, length):
    return export(
        lambda: Brush.make_slices(
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
        ),
        name='quarterpipe/quarterpipe_{}_{}x{}x{}'.format(texture, size, size, length),
        center=size / 2 + 0.25,
        size=size + 0.5
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
            for face_name in ['inside', 'outside']:
                brush.face(face_name).skew = '0 0'
        return brushes

    return export(
        make,
        name='pipe/pipe_{}_{}x{}x{}_corner_{}'.format(texture, size, size, size, direction),
        center=-1 - size / 2 * (direction == 'leftright'),
        size=size * 2 + 2 - size * (direction == 'leftright')
    )


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

    return export(
        make,
        name='halfpipe/halfpipe_{}_{}x{}x{}_corner_{}'.format(texture, size, size, size, direction),
        center=-1 - size / 2 * (direction == 'leftright'),
        size=size * 2 + 2 - size * (direction == 'leftright')
    )


if __name__ == '__main__':
    trim('square', 0)
    for slope in [0.25, 0.5, 0.75]:
        ramptrim('square', 0, slope)
    for size in [1, 2, 3, 4, 6, 8, 12, 16]:
        for axis in 'xyz':
            trim(axis, size)
        if size <= 6:
            for slope in [0.25, 0.5, 0.75]:
                for axis in 'xy':
                    ramptrim(axis, size, slope)
        ring(size)
        halfring(size)
        quarterring(size)
    for slope in [0.25, 0.5, 0.75]:
        ramptrim_bottom(slope)
        ramptrim_top(slope)
    for texture in ['white', 'red', 'yellow', 'blue']:
        for width in [1, 2, 3, 4, 6, 8, 12, 16]:
            if width <= 6:
                for length in [1, 2, 3, 4, 6]:
                    if length % width == 0 and length >= width:
                        platform(texture, width, length)
                for length in [1, 2, 3, 4, 6]:
                    if length % width == 0 or width % length == 0:
                        wall(texture, width, length)
                for slope in [0.25, 0.5, 0.75]:
                    ramp(texture, width, slope)
                    ramp_bottom(texture, width, slope)
                    ramp_top(texture, width, slope)
                cube(texture, width)
            else:
                platform(texture, width, width)
            circle(texture, width)
            for length in {1, width}:
                pipe(texture, width, length)
                halfpipe(texture, width, length)
                quarterpipe(texture, width, length)
            if width <= 6:
                for direction in ['left', 'right', 'leftright']:
                    pipe_corner(texture, width, direction)
                    halfpipe_corner(texture, width, direction)
    for texture in ['bouncy', 'grass', 'ice', 'mud', 'sand', 'space', 'water']:
        for width in [1, 2, 3]:
            platform(texture, width, width)
            wall(texture, width, width)
            for slope in [0.25, 0.5, 0.75]:
                ramp(texture, width, slope)
                ramp_bottom(texture, width, slope)
                ramp_top(texture, width, slope)
            cube(texture, width)

    print('total interiors', len([1 for child in mission.children if type(child) == Interior]))
    mission.autobounds(horizontal_margin=100, bottom_margin=50, top_margin=1000).write('iambictests')
