from amble import *
from factories import *
import exporting

mission = Mission.normal(
    name='IAMBIC Showcase',
    artist='hPerks',
    desc='IAMBIC: the Itemized Auxiliary Marble Blast Interiors Collection.',
).add(StartPad())


def add(factory, position, rotation=Rotation3D.identity, **kwargs):
    return mission.add(Interior.local('iambic/' + exporting.name(factory, **kwargs), position=Vector3D(position), rotation=Rotation3D(rotation)))


for x in [-48, -16, 16, 48]:
    for y in [-48, -16, 16, 48, 80, 112]:
        add(platform, texture='white', x=16, y=16, position=(x, y, 0))

gap = 1
max_diameter = 12
max_exterior_diameter = 13

add(trim_cube, position=(0, 2 + gap + 0.25, 0.5))

sum_lengths, sum_heights = 32 + gap * 5, 0
for slope in [25, 50]:
    add(trim, slope=slope, part='bottom', position=(0, 2 + gap + 0.5 + gap + sum_lengths + 2, 0.5 + sum_heights + 1 * slope / 100))
    sum_lengths += 2 + gap
    sum_heights += (1 + gap) * slope / 100

    add(trim_cube, slope=slope, position=(0, 2 + gap + 0.5 + gap + sum_lengths + 0.25, 0.5 + sum_heights + 0.25 * slope / 100))
    sum_lengths += 0.5 + gap
    sum_heights += (0.5 + gap) * slope / 100

    add(trim, axis='y', length=1, slope=slope, position=(0, 2 + gap + 0.5 + gap + sum_lengths + 1, 0.5 + sum_heights + 1 * slope / 100))
    sum_lengths += 1 * 2 + gap
    sum_heights += (1 * 2 + gap) * slope / 100

    add(trim, slope=slope, part='top', position=(0, 2 + gap + 0.5 + gap + sum_lengths, 0.5 + sum_heights))
    sum_lengths += 2 + gap
    sum_heights += 1 * slope / 100

add(trim, slope=75, part='top', position=(0, 2 + gap + 0.5 + gap + sum_lengths + 2, 0.5 + sum_heights - 1 * 75 / 100), rotation='0 0 1 180')
sum_lengths += 2 + gap
sum_heights -= (1 + gap) * 75 / 100

add(trim_cube, slope=75, position=(0, 2 + gap + 0.5 + gap + sum_lengths + 0.25, 0.5 + sum_heights - 0.25 * 75 / 100), rotation='0 0 1 180')
sum_lengths += 0.5 + gap
sum_heights -= (0.5 + gap) * 75 / 100

add(trim, axis='y', length=1, slope=75, position=(0, 2 + gap + 0.5 + gap + sum_lengths + 1, 0.5 + sum_heights - 1 * 75 / 100), rotation='0 0 1 180')
sum_lengths += 1 * 2 + gap
sum_heights -= (1 * 2 + gap) * 75 / 100

add(trim, slope=75, part='bottom', position=(0, 2 + gap + 0.5 + gap + sum_lengths, 0.5 + sum_heights), rotation='0 0 1 180')

sum_widths, sum_exterior_widths = 0, 0
for width in [1, 2, 3, 4, 6]:
    add(trim, axis='x', length=width, position=(0.25 + gap + sum_widths + width, 2 + gap + 0.25, 0.5))
    add(trim, axis='y', length=width, position=(0, 2 + gap + 0.5 + gap + sum_widths + width, 0.5))
    add(trim, axis='z', length=width, position=(0, 2 + gap + 0.25, 0.5 + gap + sum_widths + width * 2))

    sum_lengths = 0
    for length in [1, 2, 3, 4, 6]:
        add(platform, texture='blue', x=width, y=length, position=(0.25 + gap + sum_widths + width, 2 + gap + 0.5 + gap + sum_lengths + length, 0.5))
        add(wall, texture='blue', x=width, z=length, position=(0.25 + gap + sum_widths + width, 2 + gap + 0.25, 0.5 + gap + sum_lengths + length * 2))
        sum_lengths += length * 2 + gap

    sum_heights = 0
    for slope in [25, 50]:
        add(ramp, texture='blue', x=width, y=width, slope=slope, part='bottom', position=(0.25 + gap + sum_widths + width, 2 + gap + 0.5 + gap + sum_lengths + 2, 0.5 + sum_heights + 1 * slope / 100))
        sum_lengths += 2 + gap
        sum_heights += (1 + gap) * slope / 100

        add(trim, axis='x', length=width, slope=slope, position=(0.25 + gap + sum_widths + width, 2 + gap + 0.5 + gap + sum_lengths + 0.25, 0.5 + sum_heights + 0.25 * slope / 100))
        sum_lengths += 0.5 + gap
        sum_heights += (0.5 + gap) * slope / 100

        add(ramp, texture='blue', x=width, y=width, slope=slope, position=(0.25 + gap + sum_widths + width, 2 + gap + 0.5 + gap + sum_lengths + width, 0.5 + sum_heights + width * slope / 100))
        sum_lengths += width * 2 + gap
        sum_heights += (width * 2 + gap) * slope / 100

        add(ramp, texture='blue', x=width, y=width, slope=slope, part='top', position=(0.25 + gap + sum_widths + width, 2 + gap + 0.5 + gap + sum_lengths, 0.5 + sum_heights))
        sum_lengths += 2 + gap
        sum_heights += 1 * slope / 100

    add(ramp, texture='blue', x=width, y=width, slope=75, part='top', position=(0.25 + gap + sum_widths + width, 2 + gap + 0.5 + gap + sum_lengths + 2, 0.5 + sum_heights - 1 * 75 / 100), rotation='0 0 1 180')
    sum_lengths += 2 + gap
    sum_heights -= (1 + gap) * 75 / 100

    add(trim, axis='x', length=width, slope=75, position=(0.25 + gap + sum_widths + width, 2 + gap + 0.5 + gap + sum_lengths + 0.25, 0.5 + sum_heights - 0.25 * 75 / 100), rotation='0 0 1 180')
    sum_lengths += 0.5 + gap
    sum_heights -= (0.5 + gap) * 75 / 100

    add(ramp, texture='blue', x=width, y=width, slope=75, position=(0.25 + gap + sum_widths + width, 2 + gap + 0.5 + gap + sum_lengths + width, 0.5 + sum_heights - width * 75 / 100), rotation='0 0 1 180')
    sum_lengths += width * 2 + gap
    sum_heights -= (width * 2 + gap) * 75 / 100

    add(ramp, texture='blue', x=width, y=width, slope=75, part='bottom', position=(0.25 + gap + sum_widths + width, 2 + gap + 0.5 + gap + sum_lengths, 0.5 + sum_heights), rotation='0 0 1 180')

    add(ring, x=width, y=width, position=(-0.25 - gap - max_exterior_diameter / 2, 2 + gap + max_exterior_diameter / 2 + width, 0.25), rotation='-1 0 0 90')
    add(halfring, x=width, y=width, position=(-0.25 - gap - max_exterior_diameter / 2, 2 + gap + max_exterior_diameter + gap + width, 0.25), rotation=Rotation3D('1 0 0 90') + '0 0 1 180')
    add(quarterring, x=width, y=width, position=(-0.25 - gap - max_exterior_diameter - gap / 2, 2 + gap + max_exterior_diameter + gap + 3, 0.25) + Rotation3D('0 0 -1 135') * Vector3D(width, 0, 0), rotation=Rotation3D('0 -1 0 90') + '0 0 1 45')

    add(circle, texture='blue', x=width, y=width, position=(-0.25 - gap - max_exterior_diameter - gap - max_diameter / 2, 2 + gap + max_exterior_diameter / 2, max(3 - 0.5 * width, 0.5)))
    add(halfcircle, texture='blue', x=width, y=width, position=(-0.25 - gap - max_exterior_diameter - gap - max_diameter / 2, 2 + gap + max_exterior_diameter + gap, max(3 - 0.5 * width, 0.5)))
    add(quartercircle, texture='blue', x=width, y=width, position=(-0.25 - gap - max_exterior_diameter - gap - max_diameter / 2, 2 + gap + max_exterior_diameter + gap + max_exterior_diameter / 2 + gap, max(3 - 0.5 * width, 0.5)), rotation='0 0 -1 45')

    add(pipe, texture='blue', x=width, y=width, z=1, position=(-0.25 - gap - max_exterior_diameter - gap - max_diameter - gap - max_exterior_diameter / 2, 2 + gap + max_exterior_diameter / 2 + width, 1), rotation='-1 0 0 90')
    add(halfpipe, texture='blue', x=width, y=width, z=1, position=(-0.25 - gap - max_exterior_diameter - gap - max_diameter - gap - max_exterior_diameter / 2, 2 + gap + max_exterior_diameter + gap + width, 1), rotation=Rotation3D('1 0 0 90') + '0 0 1 180')
    add(quarterpipe, texture='blue', x=width, y=width, z=1, position=(-0.25 - gap - max_exterior_diameter - gap - max_diameter - gap / 2, 2 + gap + max_exterior_diameter + gap + 3, 1) + Rotation3D('0 0 -1 135') * Vector3D(width, 0, 0), rotation=Rotation3D('0 -1 0 90') + '0 0 1 45')

    add(pipe, texture='blue', x=width, y=width, z=width, part='corner', direction='left', position=(-gap / 2, -2 - gap - sum_exterior_widths - width - 0.5, 0.5), rotation='0 0 1 90')
    add(pipe, texture='blue', x=width, y=width, z=width, part='corner', direction='leftright', position=(-gap / 2 - width - 2 - gap - 2 - width, -2 - gap - sum_exterior_widths - width - 0.5, 0.5), rotation='0 0 -1 90')
    add(pipe, texture='blue', x=width, y=width, z=width, part='corner', direction='right', position=(-gap / 2 - width - 2 - gap - 2 - width - gap, -2 - gap - sum_exterior_widths - width - 0.5, 0.5), rotation='0 0 1 90')
    add(pipe, texture='blue', x=width, y=width, z=width, position=(-gap / 2 - width - 2 - gap - 2 - width - gap - width - 2 - gap - width, -2 - gap - sum_exterior_widths - width - 0.5, 0.5), rotation='0 0 1 90')

    add(halfpipe, texture='blue', x=width, y=width, z=width, part='corner', direction='left', position=(gap / 2, -2 - gap - sum_exterior_widths - width - 0.5, 0.5), rotation='0 0 -1 90')
    add(halfpipe, texture='blue', x=width, y=width, z=width, part='corner', direction='leftright', position=(gap / 2 + width + 2 + gap + 2 + width, -2 - gap - sum_exterior_widths - width - 0.5, 0.5), rotation='0 0 1 90')
    add(halfpipe, texture='blue', x=width, y=width, z=width, part='corner', direction='right', position=(gap / 2 + width + 2 + gap + 2 + width + gap, -2 - gap - sum_exterior_widths - width - 0.5, 0.5), rotation='0 0 -1 90')
    add(halfpipe, texture='blue', x=width, y=width, z=width, position=(gap / 2 + width + 2 + gap + 2 + width + gap + width + 2 + gap + width, -2 - gap - sum_exterior_widths - width - 0.5, 0.5), rotation='0 0 -1 90')

    sum_widths += 2 * width + gap
    sum_exterior_widths += 2 * width + 1 + gap

mission.autobounds(horizontal_margin=100).write('iambicshowcase')
