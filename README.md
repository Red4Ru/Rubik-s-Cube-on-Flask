# Rubik's Cube on Flask

This project lets you solve Rubik's cube by typing "formulas" in a form on a web page.

There are 2 pages: main page (`"/index.html"` - static) and page with cube (`"/cube/{sides}"` - dynamic).

## Pages

### Main page

Here is a form where you can choose:
- Seed for generation of cube (type 8 alphanumeric symbols or left it empty to get random seed);
- Size of a cube (from 2x2x2 to 5x5x5).
Click "Start!" to get to a cube page.

### Cube page

You can see upper, front and right side of cube directly and down, back and left side of cube as if they were in the mirrors.

Also you can see a form where you can choose:
- Sequence of commands to rotate cube sides*;
- Axis and direction to rotate cube** after formentioned sequence is applied.

Click "Apply!" to apply changes.
Click "Quit" to get to the main page.
Also there is a line with seed when you just get here from a main page. You can copy it and use afterwards to generate exactly the same cube again any time.

## Appendix
**\* - Command consists of a letter and an optional sign**

### Letters:
- U - upper side;
- F - front side;
- R - right side;
- D - down side;
- B - back side;
- L - left side.

### Signs
- No sign - rotate chosen side closkwise;
- ' - rotate chosen sign anticlockwise;
- " - rotate chosen sign 180 degrees.

**\*\* - Same: letter (axis) + optional sign but also there is Unicode arrows to remind what it means**

### Axes
- X - horizontal, from left to right;
- Y - vertical, from down to upper;
- Z - horizontal, from back to front.

### Enjoy!
