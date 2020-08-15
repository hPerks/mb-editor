from amble import *

mission = Mission.normal(
    name='Foundations of Physics',
    artist='hPerks',
    desc='Explore this industrial playground and learn the many varieties of physics modifications.',
    startHelpText='Pick your path, pick your physics changes!',
    platinumTime=60000,
    ultimateTime=40000,
    awesomeTime=26500
).add(
    StartPad(position='0 0 0.5'),
    EndPad(position='-21 -5 0', rotation='0 0 1 90'),
    Interior.local('foundationsofphysics'),

    Gem().copies(
        'position',
        '-8 24 24.5',
        '32 24 12.5',
        '17 7 -11.5',
        '6 18 -15.5',
        '-21 7 84.5',
    ),

    PhysModTrigger(noEmitters=1, gravity=2.5, jumpImpulse=12).copies(
        ('position', 'scale'),
        '-16 4 0', '12 4 32',
        '-16 8 0', '16 10 32',
    ),

    PhysModTrigger(noEmitters=1, jumpImpulse=27).copies(
        ('position', 'scale'),
        '8 2 -12', '6 10 26',
        '20 2 -12', '12 14 26',
        '14 2 -12', '6 2 26',
        '12 10 -12', '16 10 26',
        '12 20 -12', '8 4 26',
    ),

    PhysModTrigger(noEmitters=1, bounceRestitution=1.5).copies(
        ('position', 'scale'),
        '0 12 -16', '12 3 2',
        '0 21 -16', '12 3 2',
        '0 15 -16', '3 6 2',
        '9 15 -16', '3 6 2',
    ),

    PhysModTrigger(noEmitters=1, gravity=50, position='0 24 12', scale='12 8 14'),
    PhysModTrigger(noEmitters=1, gravity=-0.1, position='-24 14 30', scale='6 6 54'),
    PhysModTrigger(noEmitters=1, gravity=100, position='-24 -8 0', scale='8 8 84'),

    HelpTrigger().copies(
        ('position', 'scale', 'text'),
        '-16 4 0', '16 14 32',
        'The blue zone is low gravity - scaling this wall is easier than it looks!',
        '-4 24 12', '16 8 14',
        'The red zone is high gravity - be very careful rolling down this slope!',
        '12 2 -12', '20 22 26',
        'The yellow zone is high jump - try it out!',
        '3 15 -16', '6 6 2',
        'The orange zone is high bounce - use it to escape this pit!',
        '-22 20 24', '2 8 2',
        'Get ready for zero gravity!',
        '-26 -10 84', '10 30 100',
        'You made it! Get the gem and fall down to the finish!'
    ),

    HelpTrigger(
        text='Once you have 4 gems, ride this speedy track to the top. Hold on tight!'
    ).copies(
        ('position', 'scale'),
        '-2 -8 0', '4 4 2',
        '36 28 12', '8 8 2',
        '-20 28 24', '8 8 2',
    ),
)

for (position, scale) in [
    ('-16 -10 0', '14 6 1'),
    ('2 -10 0', '6 4 1'),
    ('8 -10 0', '17.5 8 1'),
    ('25.5 -3.5 0', '11 1 5'),
    ('36.5 -3.5 4', '3.5 1 1'),
    ('40 -4 4', '6 6 1'),
    ('44.5 2 4', '1 4 1'),
    ('44.5 6 4', '1 19 9'),
    ('44.5 25 12', '1 3 1'),
    ('40 32 12', '6 6 1'),
    ('32 36.5 12', '4 1 1'),
    ('5 36.5 12', '27 1 13'),
    ('-12 36.5 24', '17 1 1'),
    ('-22 32 24', '6 6 1'),
    ('-22 20 24', '2 12 1'),
]:
    position, scale = vec(position), vec(scale)

    mission.add(PhysModTrigger(
        noEmitters=1,
        position=position, scale=scale,
        maxRollVelocity=40,
        angularAcceleration=100,
        bounceRestitution=0.1,
        gravity=40,
    ))
    mission.add(PhysModTrigger(
        noEmitters=1,
        position=position + vec.k * scale.z,
        scale=(scale.x, scale.y, 6),
        gravity=200,
    ))

mission.autobounds().write('foundationsofphysics')
