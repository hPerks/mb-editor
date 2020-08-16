from amble import *


textures = {
    'white': Texture(file='pq_circles_gray_light', dimensions='4 4', scale='0.5 0.5'),
    'red': Texture(file='pq_hot_1_med', dimensions='4 4', scale='0.5 0.5'),
    'yellow': Texture(file='pq_hot_2_med', dimensions='4 4', scale='0.5 0.5'),
    'green': Texture(file='pq_neutral_5_med', dimensions='4 4', scale='0.5 0.5'),
    'blue': Texture(file='pq_neutral_6_med', dimensions='4 4', scale='0.5 0.5'),
    'purple': Texture(file='pq_rays_purple_med', dimensions='4 4', scale='0.5 0.5'),

    'bouncy': Texture(file='pq_friction_bouncy', dimensions='4 4', scale='0.5 0.5'),
    'grass': Texture(file='pq_friction_grass', dimensions='8 8', scale='0.5 0.5'),
    'ice': Texture(file='pq_friction_ice', dimensions='16 16', scale='0.5 0.5'),
    'mud': Texture(file='pq_friction_mud', dimensions='8 8', scale='0.5 0.5'),
    'sand': Texture(file='pq_friction_sand', dimensions='8 8', scale='0.5 0.5'),
    'space': Texture(file='pq_friction_space', dimensions='8 8', scale='0.5 0.5'),
    'water': Texture(file='pq_friction_water', dimensions='4 4', scale='0.5 0.5'),
}

wall_textures = {
    'white': Texture(file='pq_wall_white', dimensions='4 4', scale='0.5 0.5'),
    'red': Texture(file='pq_wall_red', dimensions='4 4', scale='0.5 0.5'),
    'yellow': Texture(file='pq_wall_yellow', dimensions='4 4', scale='0.5 0.5'),
    'green': Texture(file='pq_wall_green', dimensions='4 4', scale='0.5 0.5'),
    'blue': Texture(file='pq_wall_blue', dimensions='4 4', scale='0.5 0.5'),
    'purple': Texture(file='pq_wall_purple', dimensions='4 4', scale='0.5 0.5'),
}

mission = Mission.normal(
    name='IAMBIC Tests',
    artist='hPerks',
    desc='IAMBIC: the Itemized Auxiliary Marble Blast Interiors Collection.',
    gravity=7,
).add(
    StartPad()
)
mission.next_y = 4.0


def export(name, size, brush_maker):
    print('export', name)
    mission.add(Interior.local('iambic/' + name, position=Vector3D.j * (mission.next_y + size / 2)))
    mission.next_y += size + 2
    if not os.path.exists(path.platinum('data/interiors_pq/custom/iambic', name + '.dif')):
        brushes = flatlist(brush_maker())
        return Map(brushes, Map([brush.copy() for brush in brushes])).to_interior(name, subdir='iambic')


def platform(texture, width, length):
    return export(
        'platform_{}_{}x{}'.format(texture, width, length), length * 2,
        lambda: Brush.make_cube(
            center='0 0 -0.25',
            size=(width * 2, length * 2, 0.5),
            texture={
                'z': textures[texture],
                'side': Texture.edge,
            }
        )
    )


def ramp(texture, width, length, slope):
    return export(
        'ramp_{}_{}x{}_slope{}'.format(texture, width, length, int(slope * 100)), length * 2,
        lambda: Brush.make_cube(
            center=(0, 0, -0.25 - slope * length),
            size=(width * 2, length * 2, 0.5),
            texture={
                'z': textures[texture],
                'side': Texture.edge,
            }
        ).move_face(
            'back',
            (0, 0, slope * length * 2)
        )
    )


def trim(axis, size):
    return export(
        'trim_{}{}'.format(axis, '' if size == 0 else size), size * 2 if axis == 'y' else 0.5,
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
        )
    )


def wall(texture, width, height):
    return export(
        'wall_{}_{}x{}'.format(texture, width, height), 0.5,
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
        )
    )


def cube(texture, size):
    return export(
        'cube_{}_{}x{}x{}'.format(texture, size, size, size), size * 2,
        lambda: Brush.make_cube(
            center=(0, 0, -size),
            size=(size * 2, size * 2, size * 2),
            texture=textures[texture]
        )
    )


def circle(texture, size):
    return export(
        'circle_{}_{}x{}'.format(texture, size, size), size * 2,
        lambda: Brush.make_prism(
            sides=32,
            center=(0, 0, -0.25),
            size=(size * 2, size * 2, 0.5),
            texture={
                'z': textures[texture],
                'side': Texture.edge
            }
        )
    )


def ring(size):
    return export(
        'ring_{}x{}'.format(size, size), 0.5,
        lambda: Brush.make_slices(
            axis='y',
            center=(0, 0, -size),
            size=(size * 2, 0.5, size * 2),
            inner_size=(size * 2 - 1, 0.5, size * 2 - 1),
            step_angle=9,
            texture=Texture.edge
        )
    )


def pipe(texture, size):
    return export(
        'pipe_{}_{}x{}x{}'.format(texture, size, size, size), size * 2,
        lambda: Brush.make_slices(
            axis='y',
            center=(0, 0, -size),
            size=(size * 2, size * 2, size * 2),
            inner_size=(size * 2 - 1, size * 2, size * 2 - 1),
            step_angle=9,
            texture={
                'side': textures[texture],
                'z': Texture.edge,
            }
        )
    )


if __name__ == '__main__':
    trim('square', 0)
    for size in [1, 2, 3, 4, 6, 8, 12, 16]:
        ring(size)
        for axis in 'xyz':
            trim(axis, size)
        for texture in textures.keys():
            cube(texture, size)
            circle(texture, size)
            pipe(texture, size)
    for width in [1, 2, 3, 4, 6]:
        for texture in textures.keys():
            for slope in [0.25, 0.5, 0.75]:
                ramp(texture, width, width, slope)
            for length in [1, 2, 3, 4, 6]:
                if length % width == 0 or width % length == 0:
                    if length >= width:
                        platform(texture, width, length)
                    if texture in wall_textures.keys():
                        wall(texture, width, length)

    print('total interiors', len([1 for child in mission.children if type(child) == Interior]))
    mission.autobounds(horizontal_margin=100, bottom_margin=50, top_margin=500).write('iambictests')
