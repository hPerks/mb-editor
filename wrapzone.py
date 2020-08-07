import math
import random

from amble import *
from amble.utils.lists import drange

mission = Mission.hunt(
    name='Wrap Zone',
    artist='hPerks',
    desc='Use the warps to navigate this wrap-around room, 3D Pacman style!',
    startHelpText='The gems might be closer than they appear...',
    gemGroups=1,
    parScore=40,
    platinumScore=60,
    ultimateScore=90,
    awesomeScore=125,
    time=180000,
    generalHint='Use the warps a lot - they were designed to be useful. The gem spawns will often be in two distant sections that are very close if you use the warps. (I\'ll leave you to guess how I implemented that.)',
    ultimateHint='You\'ll want to get a good feel for the warps, and be able to collect gems by going back and forth through warps as if they weren\'t there. You\'re given super speeds in the upper sections specifically for a reason - warping around is often the fastest way to get past the wall in the middle of the map.',
    awesomeHint='You don\'t need too much luck here if you just know how to quickly navigate the map. The trickest parts are the upper sections near the wall in the middle - fast if you do them right, easy to mess up on.'
).add(
    SpawnTrigger(position='3 15 1'),
    Interior.local('wrapzone.dif'),

    StaticShape(datablock='Tree01', scale='0.5 0.5 0.5').copies(
        ('position', 'skin'),
        '-34 18 0', 'summer',
        '-12 113 0', 'winter',
        '54 113 0', 'winter',
    ),

    StaticShape(datablock='LargeGrass').copies(
        ('position', 'scale'),
        '-34 15 0', '3.2 4 1',
        '-34 24 0', '3.2 3.2 1',
    ),

    StaticShape(datablock='Rock01').copies(
        ('position', 'scale', 'rotation'),
        '-32 16 0', '0.5 0.5 0.5', '0 0 1 0',
        '-33 15 0', '0.3 0.3 0.3', '0 0 1 90',
        '-35 23 0', '0.5 0.5 0.5', '0 0 1 0',
        '-33.5 23.5 0', '0.6 0.6 0.6', '0 0 1 120',
        '-34.05 21.8 0', '0.4 0.4 0.4', '0 0 -1 120',
        '-36.25 17.25 0', '0.4 0.4 0.4', '0 0 -1 135',
        '-37 19 0', '0.6 0.6 0.6', '0 0 1 120',
        '-36 18.25 0', '0.3 0.3 0.3', '0 0 1 0',
    ),

    StaticShape(datablock='Plant01', position='-33 19.75 0', scale='1.25 1.25 1.5'),
    StaticShape(datablock='Flowers', skin='yellow').copies(
        ('position', 'rotation'),
        '-31.5 19 0', '0 0 1 0',
        '-32 21 0', '0 0 1 42'
    ),

    StaticShape(datablock='IceShard1').copies(
        'position',
        '16 112.5 1.5',
        '21 115.5 1.5',
        '26 112.5 1.5',
        '-6.5 107 -1',
        '48.5 107 -1',
    ),

    StaticShape(datablock='Fence_5TilesLength', scale='0.75 0.75 0.6').copies(
        ('position', 'rotation'),

        '3 42 0', '0 0 1 90',
        '3 36 0', '0 0 1 90',

        '-29.75 16.25 0', '0 0 1 90',
        '-29.75 22.25 0', '0 0 1 90',
        '-29.75 28.25 0', '0 0 1 90',
        '-35.75 28.25 0', '0 0 1 0',

        '-18 42 10', '0 0 1 0',
        '-18 42 10', '0 0 1 90',
        '-18 36 10', '0 0 1 90',
        '-18 30 10', '0 0 1 0',
        '-12 32 10', '0 0 1 0',
        '-6 32 10', '0 0 1 0',
        '0 32 10', '0 0 1 0',
        '6 32 10', '0 0 1 0',
        '12 32 10', '0 0 1 0',
        '-18 65 9', '0 0 1 90',
        '30 65 9', '0 0 1 90',

        '-12.5 58 14', '0 0 1 0',
        '-8 58 14', '0 0 1 0',
        '-2 58 14', '0 0 1 90',
        '-2 52 14', '0 0 1 90',

        '8 58 10', '0 0 1 90',
        '8 52 10', '0 0 1 90',
        '8 46 10', '0 0 1 90',
        '8 58 10', '0 0 1 0',
        '9.5 58 10', '0 0 1 0',

        '-33.75 63 -2', '0 0 1 0',
        '-29.25 63 -2', '0 0 1 0',
        '-24.75 63 -2', '0 0 1 0',
        '30.75 63 -2', '0 0 1 0',
        '35.25 63 -2', '0 0 1 0',

        '16 74.5 14', '0 0 1 90',
        '16 77.5 14', '0 0 1 90',
        '16 84.25 15', '0 0 1 90',
        '16 85.75 15', '0 0 1 90',
        '16 92.5 14', '0 0 1 90',
        '16 94 14', '0 0 1 90',
        '16 94 14', '0 0 1 0',
        '22 94 14', '0 0 1 0',
        '25 94 14', '0 0 1 0',

        '10 100 10', '0 0 1 90',
        '10 94 10', '0 0 1 0',
        '13 94 10', '0 0 1 0',
    ),

    StaticShape(datablock='Tulip', scale='0.3 0.3 0.3').copies(
        'position',
        [
            rot.k(110) * (position + ' 0') * 0.06 + '-37.5 17.6 0'
            for position in [
                '1 0', '2 0', '3 0', '4 0', '2.5 -1', '2.5 -2', '2.5 -3', '2 -4', '1 -4', '0.5 -3',
                '7 -0.25', '8 0', '9 -0.25', '9.75 -1', '10 -2', '9.75 -3', '9 -3.75', '8 -4', '7 -3.75', '6.25 -3', '6 -2', '6.25 -1',
                '12.5 0', '13.5 0', '14.5 0', '15.5 0', '14 -1', '14 -2', '14 -3', '13.5 -4', '12.5 -4', '12 -3'
            ]
        ]
    ),

    SuperSpeed(position='-15 36 10'),
    SuperJump(position='-6 54 15'),
    SuperJump(position='12 54 7'),
    SuperSpeed(position='27 62 9'),
    SuperSpeed(position='12 72 6'),
    SuperSpeed(position='20 72 14'),
)

for axis, (direction, positions) in {
    'x': (
        vec.i * 2,
        [
            ('42 32 0', '-36 32 0', '1.6 8 20', 0),
            ('42 50 -2', '-36 50 -2', '1.6 8 24', 0),
            ('62 68 -2', '-34 68 -2', '1.6 8 24', 0),
            ('60 86 -2', '-18 86 -2', '1.6 8 24', 0),
        ]
    ),
    'y': (
        vec.j * 2,
        [
            ('-28 80 0', '-28 10 0', '8 1.6 20', 0),
            ('-10 118 0', '-10 6 0', '8 1.6 20', 0),
            ('8 120 0', '8 6 0', '8 1.6 20', 0),
            ('26 120 0', '26 8 0', '8 1.6 20', 0),
            ('44 116 0', '44 64 0', '8 1.6 20', 0),
        ]
    ),
    'z': (
        vec.k,
        [
            ('-10 32 20', '-10 32 0', '8 8 0.6', 0),
            ('-28 50 22', '-28 50 -2', '8 8 0.6', 0),
            ('-10 50 22', '-10 50 -2', '8 8 0.6', 0),
            ('8 50 22', '8 50 -2', '8 8 0.6', 0),
            ('26 50 22', '26 50 -2', '8 8 0.6', 0),
            ('8 68 22', '8 68 -2', '8 8 0.6', 0),
            ('0 86 22', '0 86 -2', '42 10 0.6', 0),
            ('0.5 96 22', '0.5 96 -2', '41 6 0.6', -1/3),
            ('0 102 20', '0 102 0', '42 6 0.6', 0),
        ]
    )
}.items():
    for index, (positive, negative, scale, slope) in enumerate(positions):
        positive, negative, scale = vec(positive), vec(negative), vec(scale)
        back_z_offset = slope * scale.y

        segments_proportion = 1 if back_z_offset == 0 else 0.125
        for segment in drange(0, 1, segments_proportion):
            positive_segment_offset = (vec.j * scale + vec.k * back_z_offset) * segment
            negative_segment_offset = (vec.j * scale - vec.k * back_z_offset) * segment

            mission.add(
                RelativeTPTrigger(
                    position=positive + positive_segment_offset + direction.normalized() * 0.2,
                    scale=scale * (1, segments_proportion, 1)
                ).with_destination(
                    id='dest_{}_positive_{}_{}'.format(axis, index, int(segment * segments_proportion)),
                    position=negative + negative_segment_offset + direction.normalized() * 0.2,
                    scale=scale * (1, segments_proportion, 1)
                ),

                RelativeTPTrigger(
                    position=negative + negative_segment_offset - direction + direction.normalized() * 0.2,
                    scale=scale * (1, segments_proportion, 1)
                ).with_destination(
                    id='dest_{}_negative_{}_{}'.format(axis, index, int(segment * segments_proportion)),
                    position=positive + positive_segment_offset - direction + direction.normalized() * 0.2,
                    scale=scale * (1, segments_proportion, 1)
                )
            )

        if axis == 'z':
            spectrum_offset = scale * '0.5 0.5 0'
            mission.add(
                StaticShape(
                    datablock='Spectrum',
                    scale=vec(scale.x * 0.5, 1, abs(vec(0, scale.y, back_z_offset)) * 0.25)
                ).copies(
                    ('position', 'rotation'),
                    positive + spectrum_offset + direction * 0.99 + vec.k * back_z_offset * 0.5, rot.i(90 - math.atan(slope) * 180/math.pi),
                    positive + spectrum_offset + direction * 0.01 + vec.k * back_z_offset * 0.5, rot.i(90 - math.atan(slope) * 180/math.pi),
                    negative + spectrum_offset - direction * 0.01 - vec.k * back_z_offset * 0.5, rot.i(90 + math.atan(slope) * 180/math.pi),
                    negative + spectrum_offset - direction * 0.99 - vec.k * back_z_offset * 0.5, rot.i(90 + math.atan(slope) * 180/math.pi),
                )
            )
        else:
            spectrum_offset = direction * -2 + (4, 4, scale.z * 0.5)
            mission.add(
                StaticShape(
                    datablock='Spectrum',
                    rotation='0 0 1 90' if axis == 'x' else '0 0 1 0',
                    scale=(4, 1, scale.z * 0.25)
                ).copies(
                    'position',
                    positive + spectrum_offset + direction,
                    positive + spectrum_offset,
                    negative + spectrum_offset,
                    negative + spectrum_offset - direction,
                )
            )


gems = Gem().copies(
    ('position', 'points'),

    '12 9 1', 1,
    '12 15 0', 1,
    '3 21 1', 2,
    '-6 21 1', 1,
    '-6 12 0', 1,
    '-12 21 0', 2,
    '-18 21 1', 1,
    '-24 18 1', 1,
    '-24 24 1', 1,
    '-24 33 1', 1,
    '-30 36 1', 2,
    '36 36 1', 2,
    '30 36 1', 1,
    '24 36 0', 2,
    '18 36 1', 1,
    '12 30 1', 1,
    '12 21 1', 1,
    '33 24 1', 1,
    '30 15 1', 2,
    '-6 28 0', 1,
    '30 30 0', 1,

    '12 9 9.5', 2,
    '30 9 11.5', 2,
    '12 16 11', 1,
    '30 16 11', 1,
    '21 17 11', 1,
    '21 22 10.5', 2,
    '21 28 10', 1,
    '21 36 10', 1,
    '12 36 10', 1,
    '12 43 8', 2,
    '12 49 6', 1,
    '22.5 54 7', 1,
    '30 54 8', 1,
    '38 54 10', 2,
    '-32 54 14', 2,
    '-24 54 16', 1,
    '-16.5 54 15', 1,
    '-6 49 14', 1,
    '-6 43 12', 2,
    '-6 36 10', 1,
    '-15 39 10', 1,
    '-15 33 10', 1,

    '3 36 10', 1,
    '3 45 10', 1,
    '3 54 10', 2,
    '20 62 9', 2,
    '9 64 11', 1,
    '3 64 11', 2,
    '-3 64 11', 1,
    '-14 62 9', 2,

    '-24 45 -1', 2,
    '-6 45 -1', 2,
    '12 45 -1', 2,
    '30 45 -1', 2,

    '-33 54 -1', 2,
    '-15 54 -1', 2,
    '21 54 -1', 2,
    '39 54 -1', 2,
    '-24 72 -2', 2,
    '-12 72 -1', 1,
    '-6 72 -1', 1,
    '-6 81 -1', 1,
    '0 81 -1', 1,
    '-6 90 -1', 1,
    '-12 90 -1', 2,
    '57 90 -1', 2,
    '48 90 -1', 1,
    '56 72 -2', 2,
    '48 76.5 -1', 1,
    '36 78 -1', 1,
    '36 72 -1', 1,
    '24 72 -1', 1,
    '3 72 -2', 1,
    '48 70 -2', 2,
    '-1 59 -1', 2,
    '7 59 -2', 2,

    '-22 72 7', 1,
    '-12 72 6', 1,
    '-2 72 6', 1,
    '12 82 6', 1,
    '17 82 7', 2,
    '16 90 6', 1,
    '4 91 6', 1,
    '4 97 8', 2,
    '4 103 10', 1,
    '14 98 10', 1,
    '21 98 10', 2,
    '28 98 10', 1,
    '38 103 10', 1,
    '38 97 12', 2,
    '38 91 14', 1,
    '20 90 14', 1,
    '19 82 15', 2,
    '24 82 14', 1,
    '32 72 14', 1,
    '50 72 10.5', 1,
    '42 72 12.5', 1,

    '12 115 9', 2,
    '30 115 11', 2,
    '21 110 10', 1,
    '21 105 4', 5,

    '48 111 -1', 1,
    '52 107 -1', 1,
    '30 114 1', 1,
    '21 114 1', 1,
    '12 114 1', 2,
    '-6 111 -1', 1,
    '-10 107 -1', 1,
)


def distance_by_warp(vec1, vec2):
    vec1, vec2 = vec(vec1), vec(vec2)
    return abs(vec(
        min(
            abs(vec1.x - vec2.x),
            abs(vec1.x - vec2.x - 80),
            abs(vec1.x - vec2.x + 80)
        ),
        abs(
            (vec1.y if vec1.y < 67 else vec1.y - 126) -
            (vec2.y if vec2.y < 67 else vec2.y - 126)
        ),
        abs(vec1.z - vec2.z)
    ))


def is_close_by_warp(vec1, vec2):
    return abs(abs(vec(vec1) - vec2) - distance_by_warp(vec1, vec2)) > 1


gem_groups = SimGroup(id='GemGroups')
for gem in gems[::2]:
    nearby_gems = sorted(
        [
            nearby_gem for nearby_gem in gems if
            abs(nearby_gem.position.z - gem.position.z) < 6
        ],
        key=lambda nearby_gem: distance_by_warp(nearby_gem.position, gem.position)
    )

    gem_group = SimGroup(gem.copy())
    for nearby_gem in nearby_gems[1:9]:
        if is_close_by_warp(gem.position, nearby_gem.position) and len(gem_group.children) < 6:
            gem_group.add(nearby_gem.copy())
    for nearby_gem in nearby_gems[1:9]:
        if not is_close_by_warp(gem.position, nearby_gem.position) and len(gem_group.children) < 6:
            gem_group.add(nearby_gem.copy())

    gem_groups.add(gem_group)

mission.add(gem_groups)


# tulip bushes

for position, angle in [
    ('0 22 1', 0),
    ('6 22 1', 0),
    ('-25 21 1', 90),
    ('-23.25 36.75 1', -45),
    ('11.25 36.75 1', 45),
    ('29.25 24.75 1', 45),
    ('12.75 20.25 1', 45),
    ('-7 78 -1', 90),
    ('-7 84 -1', 90),
    ('36.75 71.25 -1', 45),
    ('42 79 -1', 0),
    ('-5.25 90.75 -1', -45),
    ('-5.25 71.25 -1', 45),
]:
    random.seed(position)

    position = vec(position)
    scale = vec.one * random.choice([0.8, 0.9, 1])
    rotation = rot.k(random.randint(0, 359))

    mission.add(StaticShape(
        datablock='Plant01',
        position=position,
        scale=scale,
        rotation=rotation
    ))

    for offset in ['-0.75 0 0', '0.5 0.25 0', '0.75 -0.25 0']:
        mission.add(StaticShape(
            position=position + rot.k(angle) * offset * scale.x,
            scale=scale,
            rotation=rotation,

            datablock='Tulip',
            skin='yellow' if position.y < 67 else 'purple'
        ))


# ferns

for position in [
    '-23 26 1',
    '-25 31 1',
    '-28 36 1',
    '35 35 1',
    '13 31 1',
    '11 26 1',
    '31 19 1',

    '-11 89 -1',
    '31 73 -1',
    '36 76 -1',
    '46 78 -1',
    '53 90 -1',
]:
    random.seed(position)

    scale = vec.one * random.choice([0.8, 0.9, 1])
    rotation = rot.k(random.randint(0, 359))

    mission.add(StaticShape(
        datablock='Fern01',
        position=position,
        rotation=rotation,
        scale=scale
    ))


## flowers

for position in [
    '2 14 1',
    '4 16 1',
    '-5 20 1',
    '-7 22 1',
    '-17 20 1',
    '-19 22 1',
    '-25 17 1',
    '-23 18 1',
    '-32 35 1',
    '-34 37 1',
    '40 35 1',
    '38 37 1',
    '31 37 1',
    '29 35 1',
    '19 37 1',
    '17 35 1',
    '11 10 1',
    '13 8 1',
    '34 25 1',
    '33 23 1',
    '29 16 1',
    '31 14 1',

    '39 55 -1',
    '41 53 -1',
    '-35 55 -1',
    '-33 53 -1',
    '-16 55 -1',
    '-14 53 -1',
    '20 55 -1',
    '22 53 -1',

    '-11 73 -1',
    '-13 71 -1',
    '1 82 -1',
    '-1 80 -1',
    '-14 91 -1',
    '-16 89 -1',
    '58 91 -1',
    '56 89 -1',
    '49 91 -1',
    '47 89 -1',

    '23 73 -1',
    '25 71 -1',
    '47 74 -1',
    '49 76 -1',
]:
    random.seed(position)

    position = vec(position)
    scale = vec.one * random.choice([0.8, 0.9, 1])
    rotation = rot.k(random.randint(0, 359))

    mission.add(StaticShape(
        position=position,
        rotation=rotation,
        scale=scale,
        datablock='Flowers',
        skin=(
            random.choice(['yellow', 'green'])
            if position.y < 67
            else random.choice(['purple', 'blue'])
        )
    ))

mission.autobounds().write('wrapzone.mis')
