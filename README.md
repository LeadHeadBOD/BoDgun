# Shotgun in BoD

[![VIDEO DEMONSTRATION](https://img.youtube.com/vi/r97QfIiLoQ8/0.jpg)](https://www.youtube.com/watch?v=r97QfIiLoQ8)

This is a proof-of-concept more than anything else. There are several issues with the way it's been done in the present iteration and I have no time or motivation to elaborate on this idea, although it's definitely possible to develop it further.


### How?
The shotgun is a visual replacement for the light bow.
When the function to release an arrow is called, it applies a +/- 1.1 random orientation offset multiplier for the arrow on all axes.
Then 7 duplicated arrows are created and for each of them the random offset applied.
All arrows are then made invisible.
If a killing blow is scored with an arrow and the hit body part is the head, we decapitate the target and apply 10000 upward impulse.

And that's basically all there is to it.

### Why?
Because I was bored.

>[!CAUTION]
>Sounds are not provided in this repository since for the demonstration video, they were ripped directly from Doom 3.

The files have to be merged manually:
* `Lib/Actions.py` has 3 new functions and 2 altered ones
* `Lib/Damage.py` has a couple lines of code added for decapitation with arrows
* `ARCO.bmp` has to be manually merged inside an .mmp file
* `ACRO.bod` goes straight in the 3dobjs folder


## Known issues
There are multiple issues in the current state and I am well aware of them.

* The shotgun model is oversized
* Arrows are vsible when drawn (have to manually set arrow `alpha=0` to work like in video)
* The random spread is biased depending on shooting direction
* The secondary arrows created are set always as attacker being `Player1`
