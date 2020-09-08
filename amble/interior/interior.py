import amble
from amble.utils import path


class Interior(amble.SceneObject):
    classname = 'InteriorInstance'

    defaults = dict(interiorfile='')

    @classmethod
    def local(cls, interiorfile, subdir='', **fields):
        if not interiorfile.endswith('.dif'):
            interiorfile += '.dif'
        return cls(interiorfile=path.join('~/data/interiors_pq/custom', subdir, interiorfile), **fields)

    @staticmethod
    def tests():
        i = Interior.local('foundationRepair')
        assert i.interiorFile == '~/data/interiors_pq/custom/foundationRepair.dif'


if __name__ == '__main__':
    Interior.tests()

__all__ = ['Interior']
