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

exported = []


def export(brush, name):
    print('export', name)
    exported.append('iambic/' + name)
    if not os.path.exists(path.platinum('data/interiors_pq/custom/iambic', name + '.dif')):
        return Map(brush, Map(brush.copy())).to_interior(name, subdir='iambic')


def platform(texture, width, length):
    return export(
        Brush.make_cube(
            center='0 0 -0.25',
            size=(width * 2, length * 2, 0.5),
            texture={
                'z': textures[texture],
                'side': Texture.edge,
            }
        ),
        'platform_{}_{}x{}'.format(texture, width, length)
    )


def ramp(texture, width, length, slope):
    return export(
            Brush.make_cube(
            center=(0, 0, -0.25 - slope * length),
            size=(width * 2, length * 2, 0.5),
            texture={
                'z': textures[texture],
                'side': Texture.edge,
            }
        ).move_face(
            'back',
            (0, 0, slope * length * 2)
        ),
        'ramp_{}_{}x{}_slope{}'.format(texture, width, length, int(slope * 100))
    )


def trim(axis, size):
    return export(
        Brush.make_cube(
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
        'trim_{}{}'.format(axis, '' if size == 0 else size)
    )


def wall(texture, width, height):
    return export(
        Brush.make_cube(
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
        'wall_{}_{}x{}'.format(texture, width, height)
    )


def cube(texture, size):
    return export(
        Brush.make_cube(
            center=(0, 0, -size),
            size=(size * 2, size * 2, size * 2),
            texture=textures[texture]
        ),
        'cube_{}_{}x{}x{}'.format(texture, size, size, size)
    )


def circle(texture, size):
    brush = Brush.make_prism(
        sides=3,
        center=(0, 0, -0.25),
        size=(size * 2, size * 2, 0.5),
        texture={
            'z': textures[texture],
            'side': Texture.edge
        }
    )
    return export(
        brush,
        'circle_{}_{}x{}'.format(texture, size, size)
    )


if __name__ == '__main__':
    trim('square', 0)
    for length in [1, 2, 3, 4, 6]:
        for axis in 'xyz':
            trim(axis, length)
        for texture in textures.keys():
            cube(texture, length)
            circle(texture, length)
            for slope in [0.25, 0.5, 0.75]:
                ramp(texture, length, length, slope)
            for width in [1, 2, 3, 4, 6]:
                if length % width == 0 or width % length == 0:
                    if length >= width:
                        platform(texture, width, length)
                    if texture in wall_textures.keys():
                        wall(texture, width, length)

    print('total interiors', len(exported))
    Mission.normal(
        name='IAMBIC Tests',
        artist='hPerks',
        desc='IAMBIC: the Itemized Auxiliary Marble Blast Interiors Collection.',
        gravity=7,
    ).add(
        StartPad(),
        [
            Interior.local(filename, position=Vector3D.j * 12 * (i + 1))
            for i, filename in enumerate(exported)
        ]
    ).autobounds(horizontal_margin=100).write('iambictests')
