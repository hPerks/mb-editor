import os
import platform
import shutil
from textwrap import indent

from mb_editor.interior import Interior
from mb_editor.mapping.brush import Brush
from mb_editor.simgroup import SimGroup
from mb_editor.utils import path


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
                repr(brush) for brush in self.children if isinstance(brush, Brush)
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
                        repr(brush) for brush in submap.children if isinstance(brush, Brush)
                    ), '   ') + '\n}\n'
                )

        return output

    def to_interior(self, name, keep_map=None, **fields):
        interiors_dir = path.platinum('data/interiors_pq')

        os.chdir(interiors_dir)
        if keep_map is None:
            keep_map = os.path.exists(name + '.map')

        with open(name + '.map', 'w') as f:
            f.write(repr(self))

        if platform.system() == 'Windows':
            os.system('map2dif.exe {}.map > nul'.format(name))
        else:
            os.system('./map2dif -t . -o . "{}.map" > /dev/null'.format(name))

        shutil.copy(name + '.dif', 'custom')
        os.remove(name + '.dif')
        if not keep_map:
            os.remove(name + '.map')

        return Interior.local(name + '.dif')


    @staticmethod
    def tests():
        from mb_editor.mapping.brush import Brush
        from mb_editor.mapping.texture import Texture
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

        i = m.to_interior('joj')
        assert i.interiorFile == '~/data/interiors_pq/custom/joj.dif'


if __name__ == '__main__':
    Map.tests()
