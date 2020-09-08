from amble import *

trim = Texture('pq_edge_white_2', [0.5, 0.5])
floor = Texture('pq_neutral_7_med', [4, 4], [0.5, 0.5])
wall = Texture('pq_wall_blue', [4, 4], [0.5, 0.5])
ceiling = Texture('pq_ray_wall_combo', [4, 4], [0.5, 0.5])
mp_floor = Texture('pq_neutral_5_med', [4, 4], [0.5, 0.5])
caution = Texture('stripe_caution', [4, 4], [0.5, 0.5])

Mission.normal(
    name="Example Mission",
    artist="hPerks",
    desc="Showcasing some of the features in my text-based MB level maker. This entire level - including the interior - was constructed in under 200 lines of Python code.",
    starthelptext="",
    platinumtime=25000,
    ultimatetime=18000,
    awesometime=15500,
    music='Good To Jump To.ogg',

    sky=Sky.blender1,
    sun=Sun(ambient=(0.3, 0.3, 0.4, 1))
).add(
    StartPad('StartPoint', position=vec.zero),
    Map(
        [
            Brush.make_cube(
                center=center, size=size,
                texture={'top': floor, 'side': wall, 'bottom': ceiling},
                origin='0 0 0'
            ) for center, size in [
                ('0 0 -0.25', '8 8 0.5'),
                ('0 4.25 2.5', '8 0.5 6'),
                ('0 10 5.75', '8 12 0.5'),
                ('8 12 5.75', '8 8 0.5'),
                ('12.25 12 11.5', '0.5 8 12'),
                ('16 12 17.75', '8 8 0.5'),
                ('24 0 17.75', '8 32 0.5'),
                ('11.75 -12 23.5', '0.5 8 12'),
                ('8 -12 29.75', '8 8 0.5'),

                ('24 10 35.75', '8 12 0.5'),
                ('24 3.75 41.5', '8 0.5 12'),
                ('24 0 47.75', '8 8 0.5'),
                ('24 -3.75 43.5', '8 0.5 8'),
                ('24 -10 39.75', '8 12 0.5'),
            ]
        ],

        Brush.make_cube(
            center='0 -12 29.75', size='8 8 0.5',
            texture={'top': floor, 'side': caution, 'bottom': ceiling},
            origin='0 0 0'
        ),

        Brush.make_cube(
            center='0 12 29.75', size='8 8 0.5',
            texture={'top': floor, 'side': caution, 'bottom': ceiling},
            origin='0 0 0'
        ),

        Brush.make_cube(
            texture={'top': floor, 'side': wall, 'bottom': ceiling},
            center='12 12 29.75', size='16 8 0.5', origin='0 0 0'
        ).move_face('right', '0 0 6'),

        Brush.make_cube(
            texture={'all': ceiling, 'top': floor},
            center='12 0 23.75', size='16 16 48.5', origin='0 0 0'
        ),

        [
            Brush.make_cube(center=center, size=size, texture=trim) for center, size in [
                ('0 -4.25 -0.25', '8 0.5 0.5'),
                ('-4.25 0 -0.25', '0.5 9 0.5'),
                ('-4.25 4.25 2.75', '0.5 0.5 5.5'),
                ('-4.25 10 5.75', '0.5 12 0.5'),
                ('4 16.25 5.75', '17 0.5 0.5'),
                ('12.25 16.25 11.75', '0.5 0.5 11.5'),
                ('20 16.25 17.75', '16 0.5 0.5'),
                ('28.25 0 17.75', '0.5 33 0.5'),
                ('24 -16.25 17.75', '8 0.5 0.5'),
                ('11.75 -16.25 23.5', '0.5 0.5 12'),
                ('4 -16.25 29.75', '16 0.5 0.5'),
                ('-4.25 0 29.75', '0.5 33 0.5'),
                ('0 16.25 29.75', '8 0.5 0.5'),
                ('24 16.25 35.75', '8 0.5 0.5'),
                ('28.25 10 35.75', '0.5 13 0.5'),
                ('28.25 3.75 41.75', '0.5 0.5 11.5'),
                ('28.25 0 47.75', '0.5 8 0.5'),
                ('28.25 -3.75 43.75', '0.5 0.5 7.5'),
                ('28.25 -10 39.75', '0.5 13 0.5'),
                ('24 -16.25 39.75', '8 0.5 0.5'),
                ('19.75 -12.25 39.75', '0.5 8.5 0.5'),
            ]
        ],

        Brush.make_cube(texture=trim, center='12 16.25 29.75', size='16 0.5 0.5').move_face('right', '0 0 6'),

        Map(
            Brush.make_cube(
                texture={'top': mp_floor, 'side': caution, 'bottom': ceiling},
                center='16 -12 17.75', size='8 8 0.5', origin='0 0 0'
            ),
            Brush.make_cube(texture=trim, center='16 -16.25 17.75', size='8 0.5 0.5')
        )
    ).to_interior('examplemission'),

    SuperJump(position='0 3 0'),
    HelpTrigger(
        position='-4.5 -4.5 0', scale='8.5 8.5 4',
        text="Items are placed with a single tiny line of code, and customized however much you want."
    ),

    TimeTravel(position='-4 16 6.5', timebonus=2000),

    GravityModifier(position='11 12 7', rotation=rot.right),
    GravityModifier(position='13 12 19', rotation=rot.right + rot.right),
    HelpTrigger(
        position='10 8 6', scale='2 8.5 4',
        text="There are many tools for handling lists of numbers like positions and rotations. You can even "
             "(finally) combine rotations with a simple + sign!"
    ),

    Bumper(scale='1.5 1.5 1.5').copies(
        'position',
        '21 -3 18', '25 -3 18',
        '23 -1 18', '27 -1 18',
        '21 1 18', '25 1 18',
        '23 3 18', '27 3 18',
    ),
    HelpTrigger(
        position='20 -8 18', scale='8.5 16 4',
        text="Placing multiple similar items is made super easy with functions like copies(), as well as the "
             "builtlin loops and list comprehensions in Python."
    ),

    MovingInterior.make(
        PathedInterior.local('examplemission', 0),
        Path.make_accelerate('0 0 0', 3500, '0 0 12', 1500, '0 0 0')
    ),
    HelpTrigger(
        position='12 -16.5 18', scale='8 8.5 12',
        text='There are quite a few convenient ways to build moving platforms. This one uses the '
             'MovingInterior.make() and Path.make_accelerate() builders.'
    ),

    TrapDoor().copies('position', [(x, y, 30) for x in range(-3, 5, 2) for y in range(-7, 9, 2)]),
    HelpTrigger(
        position='-4.5 -8 30', scale='8.5 16 4',
        text="These trapdoors would take ages to make and tweak using either the LE or a normal text editor. "
             "Here it's done in one simple line of code, using copies() and Python\'s range()."
    ),

    HelpTrigger(
        polyhedron=polyhedron.make(o='4 8 30', i='16 0 6', j='0 8 0', k='0 0 4'),
        text="This help trigger is skewed so as to align with the ramp. You can't activate it from below!",
    ),

    TeleportTrigger(position='22.5 4.5 36', scale='3 3 2')
    .with_destination('destination', '24 0 48')
    .with_pad(offset='1.5 1.5 0', scale='.25 .25 .25'),

    HelpTrigger(
        position='20 4 36', scale='8.5 12.5 4',
        text="Friends and the ObjectName type facilitate linking objects, like teleports and destinations. "
             "Additional methods such as TeleportTrigger.with_destination() make this even simpler."
    ),

    NestEgg(position='24 -6 40'),
    TeleportTrigger(position='22.5 -13.5 40', scale='3 3 2', destination='destination')
    .with_pad(offset='1.5 1.5 0', scale='.25 .25 .25'),

    EndPad(position='12 0 48', rotation='0 0 -1 90').with_sign(),

    HelpTrigger(
        position='4 -8 48', scale='24 16 4',
        text="Finally, the autobounds() function adds a bounds trigger to your level automatically. Trying to save "
             "your level without a bounds trigger throws an error!"
    ),

).autobounds().write('examplemission')
