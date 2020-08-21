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


def export(factory, name, center, size):
    print('export', name)
    if 'trim' in name or 'white' in name:
        mission.add(Interior.local('iambic/' + name, position=Vector3D.j * (mission.next_y + size / 2 - center)))
        mission.next_y += size + 2
    if not os.path.exists(path.platinum('data/interiors_pq/custom/iambic', name + '.dif')):
        brushes = flatlist(factory())
        return Map(
            brushes,
            Map([brush.copy() for brush in brushes])
        ).to_interior(
            os.path.basename(name), subdir='iambic/' + os.path.dirname(name)
        )


if __name__ == '__main__':
    export(trim('cube', 0), 'trim/trim_cube', center=0, size=0.5)
    for slope in [25, 50, 75]:
        export(ramptrim('cube', 0, slope), 'trim/trim_cube_slope{}'.format(slope), center=0, size=0.5)
    for size in [1, 2, 3, 4, 6, 8, 12, 16]:
        for axis in 'xyz':
            export(trim(axis, size), 'trim/trim_{}{}'.format(axis, size), center=0, size=size * 2 if axis == 'y' else 0.5)
        if size <= 6:
            for slope in [25, 50, 75]:
                for axis in 'xy':
                    export(ramptrim(axis, size, slope), 'trim/trim_{}{}_slope{}'.format(axis, size, slope), center=0, size=size * 2 if axis == 'y' else 0.5)
        export(ring(size), 'ring/ring_{}x{}'.format(size, size), center=0, size=0.5)
        export(halfring(size), 'halfring/halfring_{}x{}'.format(size, size), center=0, size=0.5)
        export(quarterring(size), 'quarterring/quarterring_{}x{}'.format(size, size), center=(size + 0.5) / 2, size=size + 0.5)
    for slope in [25, 50, 75]:
        export(ramptrim_bottom(slope), 'trim/trim_slope{}_bottom'.format(slope), center=-1, size=2)
        export(ramptrim_top(slope), 'trim/trim_slope{}_top'.format(slope), center=1, size=2)
    for texture in ['white', 'red', 'yellow', 'blue']:
        for width in [1, 2, 3, 4, 6, 8, 12, 16]:
            if width <= 6:
                for length in [1, 2, 3, 4, 6]:
                    if length % width == 0 and length >= width:
                        export(platform(texture, width, length), 'platform/platform_{}_{}x{}'.format(texture, width, length), center=0, size=length * 2)
                for length in [1, 2, 3, 4, 6]:
                    if length % width == 0 or width % length == 0:
                        export(wall(texture, width, length), 'wall/wall_{}_{}x{}'.format(texture, width, length), center=0, size=0.5)
                for slope in [25, 50, 75]:
                    export(ramp(texture, width, slope), 'ramp/ramp_{}_{}x{}_slope{}'.format(texture, width, width, slope), center=0, size=width * 2)
                    export(ramp_bottom(texture, width, slope), 'ramp/ramp_{}_{}x{}_slope{}_bottom'.format(texture, width, width, slope), center=-1, size=2)
                    export(ramp_top(texture, width, slope), 'ramp/ramp_{}_{}x{}_slope{}_top'.format(texture, width, width, slope), center=1, size=2)
                export(cube(texture, width), 'cube/cube_{}_{}x{}x{}'.format(texture, width, width, width), center=0, size=width * 2)
            else:
                export(platform(texture, width, width), 'platform/platform_{}_{}x{}'.format(texture, width, width), center=0, size=width * 2)
            export(circle(texture, width), 'circle/circle_{}_{}x{}'.format(texture, width, width), center=0, size=width * 2)
            export(halfcircle(texture, width), 'halfcircle/halfcircle_{}_{}x{}'.format(texture, width, width), center=width / 2, size=width)
            export(quartercircle(texture, width), 'quartercircle/quartercircle_{}_{}x{}'.format(texture, width, width), center=width / 2, size=width)
            for length in {1, width}:
                export(pipe(texture, width, length), 'pipe/pipe_{}_{}x{}x{}'.format(texture, width, width, length), center=0, size=length * 2)
                export(halfpipe(texture, width, length), 'halfpipe/halfpipe_{}_{}x{}x{}'.format(texture, width, width, length), center=0, size=length * 2)
                export(quarterpipe(texture, width, length), 'quarterpipe/quarterpipe_{}_{}x{}x{}'.format(texture, width, width, length), center=(length + 0.5) / 2, size=length + 0.5)
            if width <= 6:
                for direction in ['left', 'right', 'leftright']:
                    export(pipe_corner(texture, width, direction), 'pipe/pipe_{}_{}x{}x{}_corner_{}'.format(texture, width, width, width, direction), center=-1 - size / 2 * (direction == 'leftright'), size=size * 2 + 2 - size * (direction == 'leftright'))
                    export(halfpipe_corner(texture, width, direction), 'halfpipe/halfpipe_{}_{}x{}x{}_corner_{}'.format(texture, width, width, width, direction), center=-1 - size / 2 * (direction == 'leftright'), size=size * 2 + 2 - size * (direction == 'leftright'))
    for texture in ['bouncy', 'grass', 'ice', 'mud', 'sand', 'space', 'water']:
        for width in [1, 2, 3]:
            export(platform(texture, width, width), 'platform/platform_{}_{}x{}'.format(texture, width, width), center=0, size=width * 2)
            export(wall(texture, width, width), 'wall/wall_{}_{}x{}'.format(texture, width, width), center=0, size=0.5)
            for slope in [25, 50, 75]:
                export(ramp(texture, width, slope), 'ramp/ramp_{}_{}x{}_slope{}'.format(texture, width, width, slope), center=0, size=width * 2)
                export(ramp_bottom(texture, width, slope), 'ramp/ramp_{}_{}x{}_slope{}_bottom'.format(texture, width, width, slope), center=-1, size=2)
                export(ramp_top(texture, width, slope), 'ramp/ramp_{}_{}x{}_slope{}_top'.format(texture, width, width, slope), center=1, size=2)
            export(cube(texture, width), 'cube/cube_{}_{}x{}x{}'.format(texture, width, width, width), center=0, size=width * 2)

    print('total interiors', len([1 for child in mission.children if type(child) == Interior]))
    mission.autobounds(horizontal_margin=100, bottom_margin=50, top_margin=1000).write('iambictests')
