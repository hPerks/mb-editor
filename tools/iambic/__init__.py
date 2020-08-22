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
        export(ring, x=size, y=size)
        export(halfring, x=size, y=size)
        export(quarterring, x=size, y=size)
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
            export(circle, texture=texture, x=width, y=width)
            export(halfcircle, texture=texture, x=width, y=width)
            export(quartercircle, texture=texture, x=width, y=width)
            for length in {1, width}:
                export(pipe, texture=texture, x=width, y=width, z=length)
                export(halfpipe, texture=texture, x=width, y=width, z=length)
                export(quarterpipe, texture=texture, x=width, y=width, z=length)
            if width <= 6:
                for direction in ['left', 'right', 'leftright']:
                    export(pipe, texture=texture, x=width, y=width, z=width, part='corner', direction=direction)
                    export(halfpipe, texture=texture, x=width, y=width, z=width, part='corner', direction=direction)
    for texture in ['bouncy', 'grass', 'ice', 'mud', 'sand', 'space', 'water']:
        for width in [1, 2, 3]:
            export(platform, texture=texture, x=width, y=width)
            export(wall, texture=texture, x=width, z=width)
            for slope in [25, 50, 75]:
                export(ramp, texture=texture, x=width, y=width, slope=slope)
                export(ramp, texture=texture, x=width, y=width, slope=slope, part='bottom')
                export(ramp, texture=texture, x=width, y=width, slope=slope, part='top')
            export(cube, texture=texture, x=width, y=width, z=width)
