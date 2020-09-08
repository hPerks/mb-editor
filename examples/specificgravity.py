from amble import *

Mission.normal(
    name="Specific Gravity (Prototype)",
    artist="hPerks",
    desc="Low gravity has its ups and downs.",
    starthelptext="Push buttons to change your marble's gravity!",
    platinumtime=80000,
    ultimatetime=50000,
    awesometime=24000,
    generalhint="A giant PhysModTrigger on pathnodes is what makes this level work. There's all sorts of level ideas with these kind of triggers that aren't explored here. See what you can come up with!",
    ultimatehint="Usually, switching gravities saves time overall - other than that, speed is all you need.",
    awesomehint="Use that 20 second time travel to its fullest extent. You'll either need a lot of speed, precision, and strategic usage of buttons - or some better path than the one I used."
).add(
    StartPad(),
    EndPad(position='-172 -96 -204'),
    Interior.local('specificgravity'),

    PhysModTrigger('trigger_lowgravity', position='-500 -500 -1500', scale='1000 1000 1000', gravity=6),
    PathNode('appear', position='-500 -500 -500', usescale=0),
    PathNode('disappear', position='-500 -500 -1500', usescale=0),
    PathTrigger('trigger_lowgravity_appear', position='0 0 -1000', triggeronce=0, object1='trigger_lowgravity', path1='appear'),
    PathTrigger('trigger_lowgravity_disappear', position='0 0 -1000', triggeronce=0, object1='trigger_lowgravity', path1='disappear'),

    TriggerButton(position='-15 7 -2', rotation='0 0 -1 90', triggerobject='trigger_lowgravity_appear'),
    Interior.local('specificgravity_signon', position='-15 7 -1.75', rotation='0 0 -1 90'),

    [
        [
            TriggerButton(position=vec(position) - rot(rotation) * vec.i * 2, rotation=rotation, resettime=1000, triggerobject='trigger_lowgravity_disappear'),
            Interior.local('specificgravity_signoff', position=vec(position) - rot(rotation) * vec.i * 2 + '0 0 0.25', rotation=rotation),
            TriggerButton(position=vec(position) + rot(rotation) * vec.i * 2, rotation=rotation, resettime=1000, triggerobject='trigger_lowgravity_appear'),
            Interior.local('specificgravity_signon', position=vec(position) + rot(rotation) * vec.i * 2 + '0 0 0.25', rotation=rotation),
        ]
        for position, rotation in [
            ('18 22 8', '1 0 0 0'),
            ('38 -38 -40', '0 0 1 180'),
            ('-130 -40 -25', '0 0 -1 90'),
            ('-130 -76 -24', '0 0 -1 90'),
            ('-178 -114 -36', '0 0 -1 90'),
        ]
    ],

    Cannon(position=(30, -32, -39.125), force=37, yaw=270, yawboundleft=0, yawboundright=0, yawlimit=1, pitch=15, pitchboundlow=15, pitchboundhigh=45),

    Gem().copies(
        'position',
        '18 13 8', '35 13 -47', '38 -28 -40', '-104 -30 -25', '-105 -40 -25',
        '-106 -50 -25', '-120 -32 -26', '-116 -40 -26', '-110 -46 -25.5',
        '-110 -34 -25.5', '-120 -60 -25', '-108 -114 -28', '-146 -130 -32',
    ),

    Checkpoint(position='38 -32 -40', rotation='0 0 1 180'),

    TimeTravel(position='35 13 -19', timebonus=3000),
    TimeTravel(position='-172 -87 -36', timebonus=20000),

    HelpTrigger().copies(
        ('position', 'scale', 'text'),
        '-16 4 -2', '4 8 4', "Hit this button, then go back and climb up the steps!",
        '10 4 8', '12 20 8', "Use the buttons to your left to switch gravities. You might want to turn low gravity off for this drop - up to you!",
        '32 -4 -48', '12 8 4', "Climbing these steps would be easier with a lower gravity...",
        '32 -40 -40', '12 16 4', "You can use either gravity here, but make sure to adjust your cannon trajectory accordingly. Don't overshoot!",
        '-132 -68 -26', '40 44 8', "You have less traction on the ground with lower gravity.",
        '-128 -88 -24', '12 8 4', "If you have low gravity, you can jump for the gems and skip these winding pathways!",
        '-180 -120 -36', '12 12 4', "The final drop - choose your gravity and take the plunge!",
    ),

    InBoundsTrigger(position='-210 -160 -200', scale='300 200 300'),
).write('specificgravity')
