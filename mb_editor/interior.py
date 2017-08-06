from mb_editor.physicalobject import PhysicalObject


class Interior(PhysicalObject):
    classname = "InteriorInstance"

    local_dir = "~/data/interiors"

    defaults = dict(
        interiorFile=""
    )

    @classmethod
    def local(cls, interiorFile, **fields):
        return cls(interiorFile="{}/{}".format(cls.local_dir, interiorFile), **fields)


    @staticmethod
    def tests():
        i = Interior.local("foundationRepair.dif")
        return i.interiorFile == "~/data/interiors/foundationRepair.dif"

if __name__ == '__main__':
    Interior.tests()
