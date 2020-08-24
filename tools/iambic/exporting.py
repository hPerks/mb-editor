from amble import *


def name(factory, **kwargs):
    factory_name = factory.__name__
    directory_name = factory_name.split('_')[0] if '_' in factory_name else factory_name

    return (
        directory_name + '/' + factory_name +
        ('_' + kwargs['texture'] if 'texture' in kwargs else '') +
        ('_' if 'axis' in kwargs or 'x' in kwargs else '') +
        (
            ''.join(
                ([kwargs['axis']] if 'axis' in kwargs else []) +
                ([str(kwargs['length'])] if 'length' in kwargs else [])
            ) if 'axis' in kwargs else ''
        ) +
        (
            'x'.join(
                ([str(kwargs['x'])] if 'x' in kwargs else []) +
                ([str(kwargs['y'])] if 'y' in kwargs else []) +
                ([str(kwargs['z'])] if 'z' in kwargs else [])
            ) if 'x' in kwargs else ''
        ) +
        ('_slope' + str(kwargs['slope']) if 'slope' in kwargs else '') +
        ('_' + kwargs['part'] if 'part' in kwargs else '') +
        ('_' + kwargs['direction'] if 'direction' in kwargs else '') +
        ('_hole' + str(kwargs['hole_x']) + 'x' + str(kwargs['hole_y']) if 'hole_x' in kwargs else '')
    )


def export(factory, **kwargs):
    filename = name(factory, **kwargs)
    print('export', filename)
    if not os.path.exists(path.platinum('data/interiors_pq/custom/iambic', filename + '.dif')):
        brushes = flatlist(factory(**kwargs)())
        return Map(
            brushes,
            Map([brush.copy() for brush in brushes])
        ).to_interior(
            os.path.basename(filename), subdir='iambic/' + os.path.dirname(filename)
        )
