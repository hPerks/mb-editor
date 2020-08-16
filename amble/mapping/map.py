import os
import platform
import shutil
from textwrap import indent

from amble.interior import Interior
from amble.mapping.brush import Brush
from amble.simgroup import SimGroup
from amble.utils import path


class Map(SimGroup):
    classname = 'Map'

    def __repr__(self):
        output = (
            '{\n'
            '   "classname" "worldspawn"\n'
            '   "detail_number" "0"\n'
            '   "min_pixels" "250"\n'
            '   "geometry_scale" "32"\n'
            '   "light_geometry_scale" "32"\n'
            '   "ambient_color" "0 0 0"\n'
            '   "emergency_ambient_color" "0 0 0"\n'
            '   "mapversion" "220"\n'
            '\n' + indent('\n'.join(
                repr(brush) for brush in self.children if not isinstance(brush, Map)
            ), '   ') + '\n}\n'
        )

        for submap in self.children:
            if isinstance(submap, Map):
                output += (
                    '{\n'
                    '   "classname" "Door_Elevator"\n'
                    '   "initialTargetPosition" "-1"\n'
                    '   "datablock" "PathedDefault"\n'
                    '\n' + indent('\n'.join(
                        repr(brush) for brush in submap.children if not isinstance(brush, Map)
                    ), '   ') + '\n}\n'
                )

        return output

    def write(self, filename):
        if not filename.endswith('.map'):
            filename += '.map'
        with open(path.platinum('data/interiors_pq', filename), 'w') as f:
            f.write(repr(self))

    def to_interior(self, name, subdir='', keep_map=None, verbose=False, **fields):
        if name.endswith('.dif'):
            name = name[:-4]

        os.chdir(path.platinum('data/interiors_pq'))
        if keep_map is None:
            keep_map = os.path.exists(name + '.map')

        with open(name + '.map', 'w') as f:
            f.write(repr(self))

        if platform.system() == 'Windows':
            os.system('map2dif.exe {}.map'.format(name) + ('' if verbose else ' > nul'))
        else:
            os.system('./map2dif -t . -o . "{}.map"'.format(name) + ('' if verbose else ' > /dev/null'))

        os.makedirs(path.join('custom', subdir), 0o777, True)
        shutil.copy(name + '.dif', path.join('custom', subdir))
        os.remove(name + '.dif')
        if not keep_map:
            os.remove(name + '.map')

        return Interior.local(path.join(subdir, name + '.dif'))


    @staticmethod
    def tests():
        from amble.mapping.brush import Brush
        from amble.mapping.texture import Texture
        m = Map()
        m.add(
            Brush.make_cube(
                center=[0, 0, -0.25],
                size=[4, 4, 0.5],
                texture={'all': Texture.hot1, 'side': Texture.edge}
            ),
            Map(
                Brush.make_cube(
                    texture={'all': Texture.hot1, 'side': Texture.edge}
                ).copies(
                    ('center', 'size'),
                    '-4 6 -0.25', '4 4 0.5',
                    '0 6 -0.25', '4 4 0.5',
                    '4 6 -0.25', '4 4 0.5'
                )
            )
        )

        i = m.to_interior('joj.dif', subdir='hohsis', keep_map=False)
        assert i.interiorFile == '~/data/interiors_pq/custom/hohsis/joj.dif'

        import timeit
        assert timeit.timeit(
            'repr(Map(Brush.make_cube(texture=Texture.edge)))',
            setup=(
                'from amble.mapping.map import Map\n'
                'from amble.mapping.brush import Brush\n'
                'from amble.mapping.texture import Texture\n'
            ),
            number=100
        ) < 2

        assert timeit.timeit(
            'repr(Map(Brush.make_prism(sides=16, texture=Texture.edge)))',
            setup=(
                'from amble.mapping.map import Map\n'
                'from amble.mapping.brush import Brush\n'
                'from amble.mapping.texture import Texture\n'
            ),
            number=10
        ) < 20


if __name__ == '__main__':
    Map.tests()
