============
note-trainer
============

I'm learning to improvise.

It's useful to have, in muscle memory, the locations of the
first/third/fifth/seventh for chords in common progressions,
as well as how to move between them.

This program, given a key signature / scale and a chord progression,
generates an infinite stream of notes for me to play along with.

How-to
------

.. code:: bash

    pip install .
    python -m notetrainer.app C major ii v i vi

The output looks something like this::

    Am     |Dm     |G      |C      |Am     |Dm     |C      |Am     |
    1 3 5 5|3 1 7 3|5 5 3 5|3 5 1 5|5 7 7 5|5 7 1 5|1 1 1 1|7 3 1 7|

Notes:
- You can use roman or arabic numerals to specify the degrees of your chords
- If you use roman numerals, the case is ignored.
  We always use the diatonic chords of the given scale.
  Hence for C major, ii, II and 2 all mean Dm, not D.