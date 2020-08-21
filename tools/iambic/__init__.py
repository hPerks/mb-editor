import typing

from amble import *
from factories import *


mission = Mission.normal(
    name='IAMBIC Tests',
    artist='hPerks',
    desc='IAMBIC: the Itemized Auxiliary Marble Blast Interiors Collection.',
).add(
    StartPad()
)
mission.next_y = 4.0


def export(factory: typing.Callable, center=0.0, size=0.5, **kwargs):
    factory_name = factory.__name__
    directory_name = factory_name.split('_')[0] if '_' in factory_name else factory_name

    filename = (
        path.join(directory_name, factory_name) +
        ('_' + kwargs['texture'] if 'texture' in kwargs else '') +
        ('_' if 'axis' in kwargs or 'x' in kwargs else '') +
        (
            ''.join(
                ([kwargs['axis']] if 'axis' in kwargs else []) +
                ([str(kwargs['length'])] if 'length' in kwargs else [])
            ) if 'axis' in kwargs else ''
        ) +
        (
            'x'.join(
                ([str(kwargs['x'])] if 'x' in kwargs else []) +
                ([str(kwargs['y'])] if 'y' in kwargs else []) +
                ([str(kwargs['z'])] if 'z' in kwargs else [])
            ) if 'x' in kwargs else ''
        ) +
        ('_slope' + str(kwargs['slope']) if 'slope' in kwargs else '') +
        ('_' + kwargs['part'] if 'part' in kwargs else '') +
        ('_' + kwargs['direction'] if 'direction' in kwargs else '')
    )

    print('export', filename)
    if 'trim' in filename or 'white' in filename:
        mission.add(Interior.local('iambic/' + filename, position=Vector3D.j * (mission.next_y + size / 2 - center)))
        mission.next_y += size + 2
    if not os.path.exists(path.platinum('data/interiors_pq/custom/iambic', filename + '.dif')):
        brushes = flatlist(factory(**kwargs)())
        return Map(
            brushes,
            Map([brush.copy() for brush in brushes])
        ).to_interior(
            os.path.basename(filename), subdir='iambic/' + os.path.dirname(filename)
        )


if __name__ == '__main__':
    export(trim_cube)
    for slope in [25, 50, 75]:
        export(trim_cube, slope=slope)
    for size in [1, 2, 3, 4, 6, 8, 12, 16]:
        for axis in 'xyz':
            export(trim, axis=axis, length=size, size=size * 2 if axis == 'y' else 0.5)
        if size <= 6:
            for slope in [25, 50, 75]:
                for axis in 'xy':
                    export(trim, axis=axis, length=size, slope=slope, size=size * 2 if axis == 'y' else 0.5)
        export(ring, x=size, y=size)
        export(halfring, x=size, y=size)
        export(quarterring, x=size, y=size, center=(size + 0.5) / 2, size=size + 0.5)
    for slope in [25, 50, 75]:
        export(trim, slope=slope, part='bottom', center=-1, size=2)
        export(trim, slope=slope, part='top', center=1, size=2)
    for texture in ['white', 'red', 'yellow', 'blue']:
        for width in [1, 2, 3, 4, 6, 8, 12, 16]:
            if width <= 6:
                for length in [1, 2, 3, 4, 6]:
                    if length % width == 0 and length >= width:
                        export(platform, texture=texture, x=width, y=length, size=length * 2)
                for length in [1, 2, 3, 4, 6]:
                    if length % width == 0 or width % length == 0:
                        export(wall, texture=texture, x=width, z=length)
                for slope in [25, 50, 75]:
                    export(ramp, texture=texture, x=width, y=width, slope=slope, size=width * 2)
                    export(ramp, texture=texture, x=width, y=width, slope=slope, part='bottom', size=2)
                    export(ramp, texture=texture, x=width, y=width, slope=slope, part='top', size=2)
                export(cube, texture=texture, x=width, y=width, z=width, size=width * 2)
            else:
                export(platform, texture=texture, x=width, y=width, size=width * 2)
            export(circle, texture=texture, x=width, y=width, size=width * 2)
            export(halfcircle, texture=texture, x=width, y=width, center=width / 2, size=width)
            export(quartercircle, texture=texture, x=width, y=width, center=width / 2, size=width)
            for length in {1, width}:
                export(pipe, texture=texture, x=width, y=width, z=length, size=length * 2)
                export(halfpipe, texture=texture, x=width, y=width, z=length, size=length * 2)
                export(quarterpipe, texture=texture, x=width, y=width, z=length, center=(length + 0.5) / 2, size=length + 0.5)
            if width <= 6:
                for direction in ['left', 'right', 'leftright']:
                    export(pipe, texture=texture, x=width, y=width, z=width, part='corner', direction=direction, center=-1 - size / 2 * (direction == 'leftright'), size=size * 2 + 2 - size * (direction == 'leftright'))
                    export(halfpipe, texture=texture, x=width, y=width, z=width, part='corner', direction=direction, center=-1 - size / 2 * (direction == 'leftright'), size=size * 2 + 2 - size * (direction == 'leftright'))
    for texture in ['bouncy', 'grass', 'ice', 'mud', 'sand', 'space', 'water']:
        for width in [1, 2, 3]:
            export(platform, texture=texture, x=width, y=width, size=width * 2)
            export(wall, texture=texture, x=width, z=width)
            for slope in [25, 50, 75]:
                export(ramp, texture=texture, x=width, y=width, slope=slope, size=width * 2)
                export(ramp, texture=texture, x=width, y=width, slope=slope, part='bottom', size=2)
                export(ramp, texture=texture, x=width, y=width, slope=slope, part='top', size=2)
            export(cube, texture=texture, x=width, y=width, z=width, size=width * 2)

    print('total interiors', len([1 for child in mission.children if type(child) == Interior]))
    mission.autobounds(horizontal_margin=100, bottom_margin=50, top_margin=1000).write('iambictests')
