from amble.sceneobject import SceneObject
from amble.utils import path


class Interior(SceneObject):
    classname = 'InteriorInstance'

    defaults = dict(
        interiorFile=''
    )

    @classmethod
    def local(cls, interiorFile, subdir='', **fields):
        if not interiorFile.endswith('.dif'):
            interiorFile += '.dif'
        return cls(interiorFile=path.join('~/data/interiors_pq/custom', subdir, interiorFile), **fields)

    @staticmethod
    def tests():
        i = Interior.local('foundationRepair')
        assert i.interiorFile == '~/data/interiors_pq/custom/foundationRepair.dif'


if __name__ == '__main__':
    Interior.tests()
