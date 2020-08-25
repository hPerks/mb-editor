from amble import *
from factories import *
import exporting

mission = Mission.normal(
    name='IAMBIC Showcase',
    artist='hPerks',
    desc='A comprehensive look at the interiors available for use in IAMBIC: the Itemized Auxiliary Marble Blast Interiors Collection.',
    startHelpText='',
).add(StartPad(position='-4 0 0', rotation='0 0 1 90'))
mission.cursor = Vector3D(0, 0, 0)
mission._saved_cursors = {}


def advance_cursor(v=Vector3D.zero, x=0.0, y=0.0, z=0.0):
    mission.cursor += Vector3D(v) + (x, y, z)


def set_cursor(*args):
    mission.cursor = Vector3D(*args)


def save_cursor(name=''):
    mission._saved_cursors[name] = Vector3D(mission.cursor)


def load_cursor(name=''):
    mission.cursor = Vector3D(mission._saved_cursors[name])


def add(factory, position=None, offset=Vector3D.zero, offset_x=0.0, offset_y=0.0, offset_z=0.0, advance=Vector3D.zero, advance_x=0.0, advance_y=0.0, advance_z=0.0, rotation=Rotation3D.identity, **kwargs):
    offset = Vector3D(offset) + (offset_x, offset_y, offset_z)
    mission.add(Interior.local('iambic/' + exporting.name(factory, **kwargs), position=mission.cursor + offset if position is None else position, rotation=rotation))
    advance_cursor(v=advance, x=advance_x, y=advance_y, z=advance_z)


gap = 1.5
max_diameter = 12
max_exterior_diameter = 13

advance_cursor(x=0, y=-0.25, z=0.5)
save_cursor('platforms')

add(trim_cube, offset_y=0.25, advance_y=0.5 + gap)
for length in [1, 2, 3, 4, 6]:
    add(trim, axis='y', length=length, offset_y=length, advance_y=length * 2 + gap)
for slope in [25, 50]:
    add(trim, slope=slope, part='bottom', offset_y=2, offset_z=slope / 100, advance_y=2 + gap, advance_z=(1 + gap) * slope / 100)
    add(trim_cube, slope=slope, offset_y=0.25, offset_z=0.25 * slope / 100, advance_y=0.5 + gap, advance_z=(0.5 + gap) * slope / 100)
    add(trim, axis='y', length=1, slope=slope, offset_y=1, offset_z=slope / 100, advance_y=2 + gap, advance_z=(2 + gap) * slope / 100)
    add(trim, slope=slope, part='top', offset_y=0, offset_z=0, advance_y=2 + gap, advance_z=slope / 100)
add(trim, slope=75, part='top', offset_y=2, offset_z=-75 / 100, advance_y=2 + gap, advance_z=-(1 + gap) * 75 / 100, rotation='0 0 1 180')
add(trim_cube, slope=75, offset_y=0.25, offset_z=-0.25 * 75 / 100, advance_y=0.5 + gap, advance_z=-(0.5 + gap) * 75 / 100, rotation='0 0 1 180')
add(trim, axis='y', length=1, slope=75, offset_y=1, offset_z=-75 / 100, advance_y=2 + gap, advance_z=-(2 + gap) * 75 / 100, rotation='0 0 1 180')
add(trim, slope=75, part='bottom', offset_y=0, offset_z=0, rotation='0 0 1 180')

load_cursor('platforms')
advance_cursor(y=-0.25 - gap)

for height in [1, 2, 3, 4, 6]:
    save_cursor()

    add(trim, axis='z', length=height, offset_z=2 * height - 0.5, advance_x=0.25 + gap)
    for width in [1, 2, 3, 4, 6]:
        for texture in ['red', 'yellow', 'blue']:
            add(wall, texture=texture, x=width, z=height, offset_x=width, offset_z=2 * height - 0.5, advance_x=width * 2 + gap)

    load_cursor()
    if height < 6:
        advance_cursor(y=-0.5 - gap)

min_x = mission.cursor.x
min_y = mission.cursor.y

load_cursor('platforms')
advance_cursor(x=0.25 + gap)

for width in [1, 2, 3, 4, 6]:
    for texture in ['red', 'yellow', 'blue']:
        advance_cursor(x=width)
        save_cursor()

        add(trim, axis='x', length=width, offset_y=0.25, advance_y=0.5 + gap)
        for length in [1, 2, 3, 4, 6]:
            add(platform, texture=texture, x=width, y=length, offset_y=length, advance_y=length * 2 + gap)
        for slope in [25, 50]:
            add(ramp, texture=texture, x=width, y=width, slope=slope, part='bottom', offset_y=2, offset_z=slope / 100, advance_y=2 + gap, advance_z=(1 + gap) * slope / 100)
            add(trim, axis='x', length=width, slope=slope, offset_y=0.25, offset_z=0.25 * slope / 100, advance_y=0.5 + gap, advance_z=(0.5 + gap) * slope / 100)
            add(ramp, texture=texture, x=width, y=width, slope=slope, offset_y=width, offset_z=width * slope / 100, advance_y=2 * width + gap, advance_z=(2 * width + gap) * slope / 100)
            add(ramp, texture=texture, x=width, y=width, slope=slope, part='top', offset_y=0, offset_z=0, advance_y=2 + gap, advance_z=slope / 100)
        add(ramp, texture=texture, x=width, y=width, slope=75, part='top', offset_y=2, offset_z=-75 / 100, advance_y=2 + gap, advance_z=-(1 + gap) * 75 / 100, rotation='0 0 1 180')
        add(trim, axis='x', length=width, slope=75, offset_y=0.25, offset_z=-0.25 * 75 / 100, advance_y=0.5 + gap, advance_z=-(0.5 + gap) * 75 / 100, rotation='0 0 1 180')
        add(ramp, texture=texture, x=width, y=width, slope=75, offset_y=width, offset_z=-width * 75 / 100, advance_y=2 * width + gap, advance_z=-(2 * width + gap) * 75 / 100, rotation='0 0 1 180')
        add(ramp, texture=texture, x=width, y=width, slope=75, part='bottom', offset_y=0, offset_z=0, advance_y=2 + gap, advance_z=-75 / 100, rotation='0 0 1 180')

        for inner_width in [1, 2]:
            if inner_width * 2 < width:
                add(quartercircle, texture=texture, x=width, y=width, hole_x=width - 2 * inner_width, hole_y=width - 2 * inner_width, offset_z=width - 0.5, advance_y=0.5 + gap, rotation=Rotation3D('-1 0 0 90') + '0 -1 0 135')
        add(quartercircle, texture=texture, x=width, y=width, offset_z=width - 0.5, advance_y=0.5 + gap, rotation=Rotation3D('-1 0 0 90') + '0 -1 0 135')
        add(quarterring, x=width - 0.5, y=width - 0.5, offset=Rotation3D('0 -1 0 135') * (width - 0.5, 0, 0) + (0, 0.25, width - 0.5), advance_y=0.5 + gap, rotation=Rotation3D('0 0 1 90') + '0 -1 0 45')
        add(quarterring, x=width, y=width, offset=Rotation3D('0 -1 0 135') * (width, 0, 0) + (0, 0.25, width), advance_y=0.5 + gap, rotation=Rotation3D('0 0 1 90') + '0 -1 0 45')
        if width > 1:
            add(quarterpipe, texture=texture, x=width, y=width, z=1, offset=Rotation3D('0 -1 0 135') * (width, 0, 0) + (0, 1, width), advance_y=2 + gap, rotation=Rotation3D('0 0 1 90') + '0 -1 0 45')
        add(quarterpipe, texture=texture, x=width, y=width, z=width, offset=Rotation3D('0 -1 0 135') * (width, 0, 0) + (0, width, width), advance_y=2 * width + gap, rotation=Rotation3D('0 0 1 90') + '0 -1 0 45')

        for inner_width in [1, 2]:
            if inner_width * 2 < width:
                add(halfcircle, texture=texture, x=width, y=width, hole_x=width - 2 * inner_width, hole_y=width - 2 * inner_width, offset_z=width - 0.5, advance_y=0.5 + gap, rotation=Rotation3D('-1 0 0 90') + '0 1 0 180')
        add(halfcircle, texture=texture, x=width, y=width, offset_z=width - 0.5, advance_y=0.5 + gap, rotation=Rotation3D('-1 0 0 90') + '0 1 0 180')
        add(halfring, x=width - 0.5, y=width - 0.5, offset_y=0.25, advance_y=0.5 + gap)
        add(halfring, x=width, y=width, offset_y=0.25, advance_y=0.5 + gap)
        if width > 1:
            add(halfpipe, texture=texture, x=width, y=width, z=1, offset_y=1, advance_y=2 + gap)
        add(halfpipe, texture=texture, x=width, y=width, z=width, offset_y=width, advance_y=2 * width + gap)
        add(halfpipe, texture=texture, x=width, y=width, z=width, part='corner', direction='left', offset_y=2 + width, advance_y=2 + width + gap)
        add(halfpipe, texture=texture, x=width, y=width, z=width, part='corner', direction='leftright', offset_y=0, advance_y=width + 2 + gap, rotation='0 0 1 180')
        add(halfpipe, texture=texture, x=width, y=width, z=width, part='corner', direction='right', offset_y=2 + width, advance_y=2 + gap)

        add(pipe, texture=texture, x=width, y=width, z=width, part='corner', direction='right', offset_y=width, advance_y=2 + 2 * width + gap, rotation='0 0 1 180')
        add(pipe, texture=texture, x=width, y=width, z=width, part='corner', direction='leftright', offset_y=2 + width, advance_y=2 + gap)
        add(pipe, texture=texture, x=width, y=width, z=width, part='corner', direction='left', offset_y=width, advance_y=2 * width + 2 + gap, rotation='0 0 1 180')
        add(pipe, texture=texture, x=width, y=width, z=width, offset_y=width, advance_y=2 * width + gap, rotation='0 0 1 180')
        if width > 1:
            add(pipe, texture=texture, x=width, y=width, z=1, offset_y=1, advance_y=2 + gap, rotation='0 0 1 180')
        add(ring, x=width, y=width, offset_y=0.25, advance_y=0.5 + gap, rotation='0 0 1 180')
        add(ring, x=width - 0.5, y=width - 0.5, offset_y=0.25, advance_y=0.5 + gap, rotation='0 0 1 180')
        add(circle, texture=texture, x=width, y=width, offset_z=width - 0.5, advance_y=0.5 + gap, rotation='-1 0 0 90')
        for inner_width in [2, 1]:
            if inner_width < width:
                add(circle, texture=texture, x=width, y=width, hole_x=width - 2 * inner_width, hole_y=width - 2 * inner_width, offset_z=width - 0.5, advance_y=0.5 + gap, rotation='-1 0 0 90')

        add(cube, texture=texture, x=width, y=width, z=width, offset_y=width, offset_z=2 * width - 0.5)

        if not (texture == 'blue' and width == 6):
            load_cursor()
            advance_cursor(x=width + gap)

max_x = mission.cursor.x + 6
max_y = mission.cursor.y + 12

for x in list(range(round((min_x + 14) / 2) * 2, round((max_x - 14) / 2) * 2, 16)) + [round((max_x - 14) / 2) * 2]:
    for y in list(range(round((min_y + 14) / 2) * 2, round((max_y - 14) / 2) * 2, 16)) + [round((max_y - 14) / 2) * 2]:
        add(platform, texture='white', x=16, y=16, position=(x, y, 0))
add(platform, texture='white', x=2, y=2, position='-4 0 0')

print(len(mission.children))

mission.autobounds(horizontal_margin=100).write('iambicshowcase')
