from amble import *
from factories import *
import exporting

mission = Mission.normal(
    name='IAMBIC Showcase',
    artist='hPerks',
    desc='IAMBIC: the Itemized Auxiliary Marble Blast Interiors Collection.',
).add(StartPad())
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


for x in [-48, -16, 16, 48]:
    for y in [-48, -16, 16, 48, 80, 112]:
        add(platform, texture='white', x=16, y=16, position=(x, y, 0))

gap = 1
max_diameter = 12
max_exterior_diameter = 13

save_cursor('start')

advance_cursor(y=2 + gap, z=0.5)
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
advance_cursor(x=0.25 + gap)

for width in [1, 2, 3, 4, 6]:
    advance_cursor(x=width)
    save_cursor()

    add(trim, axis='x', length=width, offset_y=0.25, advance_y=0.5 + gap)
    for length in [1, 2, 3, 4, 6]:
        add(platform, texture='blue', x=width, y=length, offset_y=length, advance_y=length * 2 + gap)
    for slope in [25, 50]:
        add(ramp, texture='blue', x=width, y=width, slope=slope, part='bottom', offset_y=2, offset_z=slope / 100, advance_y=2 + gap, advance_z=(1 + gap) * slope / 100)
        add(trim, axis='x', length=width, slope=slope, offset_y=0.25, offset_z=0.25 * slope / 100, advance_y=0.5 + gap, advance_z=(0.5 + gap) * slope / 100)
        add(ramp, texture='blue', x=width, y=width, slope=slope, offset_y=width, offset_z=width * slope / 100, advance_y=2 * width + gap, advance_z=(2 * width + gap) * slope / 100)
        add(ramp, texture='blue', x=width, y=width, slope=slope, part='top', offset_y=0, offset_z=0, advance_y=2 + gap, advance_z=slope / 100)
    add(ramp, texture='blue', x=width, y=width, slope=75, part='top', offset_y=2, offset_z=-75 / 100, advance_y=2 + gap, advance_z=-(1 + gap) * 75 / 100, rotation='0 0 1 180')
    add(trim, axis='x', length=width, slope=75, offset_y=0.25, offset_z=-0.25 * 75 / 100, advance_y=0.5 + gap, advance_z=-(0.5 + gap) * 75 / 100, rotation='0 0 1 180')
    add(ramp, texture='blue', x=width, y=width, slope=75, offset_y=width, offset_z=-width * 75 / 100, advance_y=2 * width + gap, advance_z=-(2 * width + gap) * 75 / 100, rotation='0 0 1 180')
    add(ramp, texture='blue', x=width, y=width, slope=75, part='bottom', offset_y=0, offset_z=0, rotation='0 0 1 180')

    load_cursor()
    advance_cursor(x=width + gap)

load_cursor('platforms')
advance_cursor(y=0.25, z=gap)

for height in [1, 2, 3, 4, 6]:
    advance_cursor(z=height * 2)
    save_cursor()

    add(trim, axis='z', length=height, advance_x=0.25 + gap)
    for width in [1, 2, 3, 4, 6]:
        add(wall, texture='blue', x=width, z=height, offset_x=width, advance_x=width * 2 + gap)

    load_cursor()
    advance_cursor(z=gap)

load_cursor('start')
advance_cursor(x=-0.25 - gap - max_exterior_diameter / 2, y=2 + gap + max_exterior_diameter / 2, z=0.25)
save_cursor('rings')
for width in [1, 2, 3, 4, 6]:
    add(ring, x=width, y=width, offset_y=width, rotation='-1 0 0 90')

advance_cursor(y=max_exterior_diameter / 2 + gap)
for width in [1, 2, 3, 4, 6]:
    add(halfring, x=width, y=width, offset_y=width, rotation=Rotation3D('1 0 0 90') + '0 0 1 180')

advance_cursor(x=-max_exterior_diameter / 2 - gap / 2, y=3)
for width in [1, 2, 3, 4, 6]:
    add(quarterring, x=width, y=width, offset=Rotation3D('0 0 -1 135') * (width, 0, 0), rotation=Rotation3D('0 -1 0 90') + '0 0 1 45')

load_cursor('rings')
advance_cursor(x=-max_exterior_diameter / 2 - gap - max_diameter / 2, z=2.25)
save_cursor('circles')
for width in [1, 2, 3, 4, 6]:
    add(circle, texture='blue', x=width, y=width, advance_z=-0.5)

load_cursor('circles')
advance_cursor(y=max_exterior_diameter / 2 + gap)
save_cursor('halfcircles')
for width in [1, 2, 3, 4, 6]:
    add(halfcircle, texture='blue', x=width, y=width, advance_z=-0.5)

load_cursor('halfcircles')
advance_cursor(y=max_exterior_diameter / 2 + gap)
save_cursor('quartercircles')
for width in [1, 2, 3, 4, 6]:
    add(quartercircle, texture='blue', x=width, y=width, advance_z=-0.5, rotation='0 0 -1 45')

load_cursor('circles')
advance_cursor(x=-max_diameter / 2 - gap - max_exterior_diameter / 2, z=-1.5)
save_cursor('sideways-pipes')
for width in [1, 2, 3, 4, 6]:
    add(pipe, texture='blue', x=width, y=width, z=1, offset_y=width, rotation='-1 0 0 90')

advance_cursor(y=max_exterior_diameter / 2 + gap)
for width in [1, 2, 3, 4, 6]:
    add(halfpipe, texture='blue', x=width, y=width, z=1, offset_y=width, rotation=Rotation3D('1 0 0 90') + '0 0 1 180')

advance_cursor(x=max_exterior_diameter / 2 + gap / 2, y=3)
for width in [1, 2, 3, 4, 6]:
    add(quarterpipe, texture='blue', x=width, y=width, z=1, offset=Rotation3D('0 0 -1 135') * (width, 0, 0), rotation=Rotation3D('0 -1 0 90') + '0 0 1 45')

load_cursor('start')
advance_cursor(y=-2 - gap, z=0.5)
save_cursor('pipes')

for width in [1, 2, 3, 4, 6]:
    advance_cursor(y=-0.5 - width)
    save_cursor()

    advance_cursor(x=-gap)
    add(pipe, texture='blue', x=width, y=width, z=width, part='corner', direction='left', offset_x=0, advance_x=-width - 2 - gap, rotation='0 0 1 90')
    add(pipe, texture='blue', x=width, y=width, z=width, part='corner', direction='leftright', offset_x=-2 - width, advance_x=-2 - width - gap, rotation='0 0 -1 90')
    add(pipe, texture='blue', x=width, y=width, z=width, part='corner', direction='right', offset_x=0, advance_x=-width - 2 - gap, rotation='0 0 1 90')
    add(pipe, texture='blue', x=width, y=width, z=width, offset_x=-width, rotation='0 0 1 90')

    load_cursor()

    advance_cursor(x=gap)
    add(halfpipe, texture='blue', x=width, y=width, z=width, part='corner', direction='left', offset_x=0, advance_x=width + 2 + gap, rotation='0 0 -1 90')
    add(halfpipe, texture='blue', x=width, y=width, z=width, part='corner', direction='leftright', offset_x=2 + width, advance_x=2 + width + gap, rotation='0 0 1 90')
    add(halfpipe, texture='blue', x=width, y=width, z=width, part='corner', direction='right', offset_x=0, advance_x=width + 2 + gap, rotation='0 0 -1 90')
    add(halfpipe, texture='blue', x=width, y=width, z=width, offset_x=width, rotation='0 0 -1 90')

    load_cursor()
    advance_cursor(y=-width - 0.5 - gap)

mission.autobounds(horizontal_margin=100).write('iambicshowcase')
