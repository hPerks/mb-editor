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

if __name__ == '__main__':
    i = Interior.local("foundationRepair.dif")
    print(i)