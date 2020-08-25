from factories import *
from exporting import export


if __name__ == '__main__':
    export(trim_cube)
    for slope in [25, 50, 75]:
        export(trim_cube, slope=slope)
    for size in [1, 2, 3, 4, 6, 8, 12, 16]:
        for axis in 'xyz':
            export(trim, axis=axis, length=size)
        if size <= 6:
            for slope in [25, 50, 75]:
                for axis in 'xy':
                    export(trim, axis=axis, length=size, slope=slope)
        for factory in (ring, halfring, quarterring):
            export(factory, x=size - 0.5, y=size - 0.5)
            export(factory, x=size, y=size)
    for slope in [25, 50, 75]:
        export(trim, slope=slope, part='bottom')
        export(trim, slope=slope, part='top')
    for texture in ['white', 'red', 'yellow', 'blue']:
        for width in [1, 2, 3, 4, 6, 8, 12, 16]:
            if width <= 6:
                for length in [1, 2, 3, 4, 6]:
                    export(platform, texture=texture, x=width, y=length)
                    export(wall, texture=texture, x=width, z=length)
                for slope in [25, 50, 75]:
                    export(ramp, texture=texture, x=width, y=width, slope=slope)
                    export(ramp, texture=texture, x=width, y=width, slope=slope, part='bottom')
                    export(ramp, texture=texture, x=width, y=width, slope=slope, part='top')
                export(cube, texture=texture, x=width, y=width, z=width)
            else:
                export(platform, texture=texture, x=width, y=width)
            for factory in [circle, halfcircle, quartercircle]:
                export(factory, texture=texture, x=width, y=width)
                for inner_width in [1, 2, 3, 4, 6]:
                    if width - 12 <= inner_width * 2 <= width - 1 and width - inner_width * 2 != 10:
                        export(factory, texture=texture, x=width, y=width, hole_x=width - inner_width * 2, hole_y=width - inner_width * 2)
            for factory in [pipe, halfpipe, quarterpipe]:
                for length in {1, width}:
                    export(factory, texture=texture, x=width, y=width, z=length)
                if factory != quarterpipe and width <= 6:
                    for direction in ['left', 'right', 'leftright']:
                        export(factory, texture=texture, x=width, y=width, z=width, part='corner', direction=direction)
    for texture in ['bouncy', 'grass', 'ice', 'mud', 'sand', 'space', 'water']:
        for width in [1, 2, 3]:
            export(platform, texture=texture, x=width, y=width)
            export(wall, texture=texture, x=width, z=width)
            for slope in [25, 50, 75]:
                export(ramp, texture=texture, x=width, y=width, slope=slope)
                export(ramp, texture=texture, x=width, y=width, slope=slope, part='bottom')
                export(ramp, texture=texture, x=width, y=width, slope=slope, part='top')
            export(cube, texture=texture, x=width, y=width, z=width)
