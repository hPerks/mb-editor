from amble import *


def tests():
    class JoJite(ScriptObject):
        classname = 'JoJite'
        defaults = dict(home='Planet JoJ')

    class Infomercial(ScriptObject):
        defaults = dict(datablock='Infomercial', creator='cs188', index=Implicit(0))

    group = ScriptObject.from_string('''
        new SimGroup(HohSisGroup) {
            new JoJite(WesleySeeton) {
                catchphrase = "do it all over again";
            };
            new JoJite(RichardSwiney) {
                catchphrase = "100% unsatisfied";
            };

            new SimGroup(Infomercials) {
                new ScriptObject() {
                    datablock = "Infomercial";
                    index = "0";
                    title = "No one needs foundation repair";
                };

                new ScriptObject() {
                    datablock = "Infomercial";
                    index = "1";
                    title = "He's Got The House Completely Covered";
                };

                new ScriptObject() {
                    datablock = "Infomercial";
                    index = "2";
                    title = "Escape from HoH SiS";
                };
            };
        };
    ''')

    assert type(group) == SimGroup
    assert len(group.children) == 3

    wesley = group.children[0]
    assert (type(wesley), wesley.home, wesley.catchphrase) == (JoJite, 'Planet JoJ', 'do it all over again')

    vid = group.children[2].children[0]
    assert (type(vid), vid.creator, vid.index, vid.title) == (Infomercial, 'cs188', 0, 'No one needs foundation repair')


if __name__ == '__main__':
    tests()
