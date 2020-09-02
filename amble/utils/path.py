import os, platform


def join(*args):
    return os.path.join(args[0], *[
        arg[2:] if arg.startswith('~/') else arg
        for arg in args[1:]
    ]).replace('\\', '/')


def platinum(*subpaths):
    return (
        join(os.getenv('APPDATA'), 'PlatinumQuest/platinum', *subpaths)
        if platform.system() == 'Windows' else
        join(os.getenv('HOME'), 'Applications/PlatinumQuest.app/platinum', *subpaths)
    )


def relative(*paths):
    return '~/' + str(join(*paths).split('platinum/', 1)[1])


def tests():
    assert platinum('data/missions').endswith('platinum/data/missions')
    assert platinum('~/data/missions', 'custom').endswith('platinum/data/missions/custom')
    assert relative(platinum('data/missions'), 'custom') == '~/data/missions/custom'


if __name__ == '__main__':
    tests()
