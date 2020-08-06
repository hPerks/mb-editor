import os, platform


def join(*args):
    return os.path.join(*args).replace('\\', '/')


def platinum(*subpaths):
    if len(subpaths) > 0 and len(subpaths[0]) > 1 and subpaths[0][0] == '~':
        return platinum(*(subpaths[0][2:], *subpaths[1:]))
    return (
        join(os.getenv('APPDATA'), 'PlatinumQuest/platinum', *subpaths)
        if platform.system() == 'Windows' else
        join(os.getenv('HOME'), 'Applications/PlatinumQuest.app/platinum', *subpaths)
    )


def relative(*paths):
    return '~/' + join(*paths).split('platinum/', 1)[1]


def tests():
    assert platinum('data/missions').endswith('platinum/data/missions')
    assert platinum('~/data/missions', 'custom').endswith('platinum/data/missions/custom')
    assert relative(platinum('data/missions'), 'custom') == '~/data/missions/custom'


if __name__ == '__main__':
    tests()
