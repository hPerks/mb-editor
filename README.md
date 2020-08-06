# The Basics

## Setup

Create a python file in the parent directory of `amble`.
Add this line to the start of the file:

    from amble import *

## Creating a mission

    mission = Mission.normal(name = 'Random Icerope Magnet Party')

## Creating an object

    gem = Gem(
        position = '4 2 0',
        scale = '3 1 4',
    )

## Modifying an object

    gem.position = '2 2 7'
    gem.scale.x = 7  # sets scale to '7 1 4'

    gem.set(
        rotation = rot.down,
        datablock = 'GemItemGreen',
    )

## Adding objects to a mission

    mission.add(
        gem,
        TimeTravel(
            position = '6 7 2',
            timeBonus = 1337,
        ),
    )

## Adding a bounds trigger

You must do this before saving a mission, or the program throws an error. Luckily, if you've already placed all your items, you can call the following function, which will automatically add a bounds trigger based on the positions of these items.

    mission.autobounds()

Of course, you can also add it manually, like all triggers:

    mission.add(
        InBoundsTrigger(
            position = '-100 -100 -100',
            scale = '200 200 200',
        ),
    )

## Saving a mission

    mission.write('mylevel.mis')

# Features

## Vectors

Many objects in Marble Blast have a position and a scale, which are stored as triples of numbers (3D vectors). The three numbers correspond to the x, y, and z coordinates of the vector, respectively.

In the library, these vectors are `Vector3D` objects, or `vec` for shorthand. `vec` objects can be constructed in the following ways:

- from a list of arguments: `vec(4, 2, 0)`
- from a string: `vec('4 2 0')`
- from a list: `vec([4, 2, 0])`
- from a tuple: `vec((4, 2, 0))`

`vec` objects have properties `x`, `y` and `z`. These are accessible and mutable:

    v = vec(6, 7, 2)
    v.x = 2
    v.z /= v.x
    v  # '2 7 1'

When assigning to a field that takes a vector (e.g. position), the library automatically calls the `vec` constructor if you give it a string, list or tuple. So you can go:

    object.position = vec(4, 2, 0)
    object.position = '4 2 0'

etc.

The vectors are assigned by value, not by reference:

    s = vec(3, 1, 4)
    object.scale = s
    s.x = 7
    object.scale  # '3 1 4'

### Special vectors

The following vector constants are available for shorthand:

    vec.i = vec(1, 0, 0)
    vec.j = vec(0, 1, 0)
    vec.k = vec(0, 0, 1)
    vec.zero = vec(0, 0, 0)
    vec.one = vec(1, 1, 1)

### Vector operations

Vectors support addition, subtraction, and scaling.

    vec(2, 3, 1) + vec(3, 5, 5)  # '5 8 6'
    vec(2, 1, 0) * 2  # '4 2 0'

A vector can be added or subtracted with a tuple, list, or string in the format above, provided the left side of the operator is a `vec` object.

    vec.i + '2 1 4'  # '3 1 4'
    '2 1 4' + vec.i  # throws an error!

In addition, piecewise operations can be performed using the `map()` function:

    mul = lambda x, y: x * y
    vec(2, 2, 7).map(mul, '2 1 0')  # '4 2 0'

## Rotations

Rotations in Marble Blast are stored as lists of four numbers, in 'axis-angle' format. The first three numbers are the axis of rotation as a 3D vector, and the last number is the angle to rotate.

In the library, these rotations are `Rotation3D` objects, or `rot` for shorthand. `rot` objects can be constructed in the following ways:

- from a list of arguments, string, list or tuple, analogous to `vec`: `rot(1, 0, 0, 90)`, etc.
- from an axis and an angle, by *unwrapping* the axis: `rot(*vec.i, 90)`
- from an axis and an angle, with a constructor method for a particular axis: `rot.i(90)`

### Special rotations

The following common rotations are available for shorthand and ease of use. The naming conventions are based on the position of the top face of a cube after applying the rotation.

    rot.identity = rot(1, 0, 0, 0)
    rot.up = rot(1, 0, 0, 0)
    rot.down = rot(1, 0, 0, 180)
    rot.right = rot(0, -1, 0, 90)
    rot.left = rot(0, 1, 0, 90)
    rot.towards = rot(-1, 0, 0, 90)
    rot.away = rot(1, 0, 0, 90)

### Rotation operations

Rotations can be combined using addition and subtraction:

    rot(1, 0, 0, 90) + rot(0, 1, 0, 90)  # '0.577 0.577 0.577 120'

Rotations also support scaling, in the intuitive way - simply scaling the angle without changing the axis:

    rot(1, 0, 0, 180) * 0.5  # rot(1, 0, 0, 90)

## Polyhedrons

Triggers in Marble Blast, and other objects with volume, have a 'polyhedron' property that determines its shape (more accurately called a parallelepiped). This is stored as a list of four 3D vectors, as twelve numbers. The first vector specifies a vertex of the parallelepiped, and the next three are the endpoints of the three edges of the parallelepiped that touch that vertex.

In the library, these polyhedrons are `Polyhedron3D` objects, or `polyhedron` for shorthand. `polyhedron` objects can be constructed in the following ways:

- analogous to `rot` and `vec`: `polyhedron(0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1)`
- from four vectors, with the constructor method: `polyhedron.make(o=vec.zero, i=vec.i, j=vec.j, k=vec.k)`