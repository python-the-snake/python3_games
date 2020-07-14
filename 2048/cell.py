from uuid import uuid4
from collections import defaultdict

import numba


WAIT = 1  # ms between frames

COLOR_TABLE = defaultdict(lambda: "#ffffff",
                          **{"2": "#f4e242", "4": "#f4b841", "8": "#f49d41", "16": "#f48241",
                             "32": "#f46741", "64": "#f45541", "128": "#f44141", "256": "#f4416d"})


def sign(n):
    """ Return the sign of a number """

    if n > 0:
        return 1
    elif n < 0:
        return -1
    return 0


class Cell:
    def __init__(self, canvas, root, pos, l, n=2):
        self.canvas = canvas
        self.root = root
        self.n = n  # Number to display
        self.pos = tuple(pos)  # Position on the table as (x, y)
        self.l = l  # Side leght
        self.font = ("Helvetica", int(self.l / 3))
        self.id = str(uuid4())  # Personal id of every cell

        self._draw()

    def move(self, x, y):
        """ Function called by the user to move the cell of (x, y) position (the grid is 4 positions wide """

        if x != 0 and y != 0:
            return  # It can't move diagonally

        self._moveloop(x * self.l, y * self.l)

    def double(self):
        self.n *= 2
        self.canvas.itemconfig(self.id + "text", text=self.n)
        self.canvas.itemconfig(self.id + "cell", fill=COLOR_TABLE[str(self.n)])

    def _draw(self):
        """ Draws the cell and his number on the canvas"""

        x, y = self.pos

        self.canvas.create_rectangle(x * self.l, y * self.l, (x + 1) * self.l, (y + 1) * self.l, fill=COLOR_TABLE[str(self.n)],
                                     tag=(self.id, self.id + "cell"))
        self.canvas.create_text(x * self.l + (self.l / 2), y * self.l + (self.l / 2), text=self.n, font=self.font, tag=(self.id, self.id + "text"))

    def _moveloop(self, tomovex, tomovey):
        """ Recursive function that moves the cell 1px each call """

        if not tomovex and not tomovey:
            return  # Break the loop

        self.canvas.move(self.id, sign(tomovex), sign(tomovey))
        newx = (abs(tomovex) - 1) * sign(tomovex)
        newy = (abs(tomovey) - 1) * sign(tomovey)

        self.root.after(WAIT, lambda: self._moveloop(newx, newy))

    def __del__(self):
        """ When the cell is overwritten his canvas elements must be deleted """

        self.canvas.tag_lower(self.id)
        self.root.after(int(self.l * 4), lambda: self.canvas.delete(self.id))

    def __repr__(self):
        """ Debug purpose """

        return "C(%s)" % self.n