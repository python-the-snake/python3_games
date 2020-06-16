from tkinter import *
from random import randint as ri
from copy import copy

import cell

WIDTH = 400


class App:
    def __init__(self, parent):

        self.root = parent

        # Array where all the cells are saved
        self.table = [0] * 16
        # Boolean to control user inputs to avoid too many clicks
        self._canclick = True
        # Score
        self._score = 0

        # Draws all the tkinter elements
        self.main_canvas = Canvas(self.root, width=WIDTH, height=WIDTH, bg="lightblue")
        self.main_canvas.pack()
        self.second_frame = Frame(self.root)
        self.second_frame.pack()
        self._scorevar = StringVar()
        self._scorevar.set(self._score)
        self._sframesetup()

        # Draws the horizontal and vertical lines
        self._griddraw()

        # Draws the cells
        self._cellsetup(3)

    def callback(self, direction):
        """ Handles the user input

            direction: LEFT, RIGHT, DOWN, UP = 0, 1, 2, 3"""
        if self._canclick:
            self._canclick = False  # Blocks the user input

            # Makes a copy of the table to check later if something changed or not
            backup = copy(self.table)

            d = dict(enumerate([self._left, self._right, self._down, self._up]))
            d[direction]()  # Calls the right movement function

            # Check if there is space to spawn a new cell
            if not 0 in self.table:
                self._lose()
                return

            if backup != self.table:
                # Waits until the cells stop and spawns a new one
                self.root.after(301, self._spawnnew)
            else:
                self._canclick = True

    def restart(self):
        """ Restart button callback """

        # deletes lose text
        self.main_canvas.delete("d72819d9")

        # deletes all cells
        self.table = [0] * 16

        self._cellsetup(3)
        self._scorevar.set(0)

    def _sframesetup(self):
        pointframe = Frame(self.second_frame)
        pointframe.pack(side=LEFT, pady=20, padx=20)

        Label(pointframe, text="Punteggio:").pack(side=LEFT)
        Label(pointframe, textvariable=self._scorevar).pack(side=LEFT)

        restartb = Button(self.second_frame, text="Restart", command=self.restart)
        restartb.pack(side=RIGHT, pady=20, padx=20)

    def _griddraw(self):
        """ Draws the horizontal and vertical lines """

        line_color = "blue"
        cell_width = WIDTH / 4

        for n in range(1, 4):
            # Vertical lines
            self.main_canvas.create_line(n * cell_width, 0, n * cell_width, WIDTH, fill=line_color)
            # Horizontal lines
            self.main_canvas.create_line(0, n * cell_width, WIDTH, n * cell_width, fill=line_color)

    def _cellsetup(self, nstart):
        """ Spawns 'nstart' new cells and draws them """

        for _ in range(nstart):
            self._spawnnew()

    def _lose(self):
        """ Function called when the user is not able to continue the game """

        self.main_canvas.create_text(WIDTH / 2, WIDTH / 2, text="GAME OVER", font=("Helvetica", 25), tag="d72819d9")

    def _spawnnew(self):
        """ Creates a new cell and draws it in an empty space """

        while True:
            pos = ri(0, 15)  # Pick a random idx
            if self.table[pos]:
                # If the position is already taken, restart the loop
                continue

            posconv = pos % 4, int(pos / 4)  # Converts the new idx into (x, y)

            self.table[pos] = cell.Cell(self.main_canvas, self.root, posconv, WIDTH / 4, n=2 ** ri(1, 3))
            break

        # Let the user be able to click again
        self._canclick = True

    def _right(self):
        """ Moves all the cells to the right side """

        for idx in list(range(len(self.table)))[::-1]:  # Iterates the array backwards

            if self.table[idx]:  # Checks if there's a cell

                c = self.table[idx]  # Saves the cell because 'idx' will change later
                while (idx + 1) % 4:  # Keeps going till it reaches the left side

                    # 1° CASE: Two cells add up
                    if self.table[idx + 1] and self.table[idx + 1].n == self.table[idx].n:
                        self.table[idx + 1].double()  # Doubles a cell
                        self._scorevar.set(int(self._scorevar.get()) + self.table[idx + 1].n)  # Updates the score label
                        self.table[idx] = 0  # Deletes the other
                        idx += 1
                        break

                    # 2° CASE: The cell stops
                    elif self.table[idx + 1]:
                        break

                    # 3° CASE: The cell moves to the left
                    else:
                        self.table[idx + 1] = self.table[idx]
                        self.table[idx] = 0
                        idx += 1

                # Updates the canvas object of the cell and his '.pos' attribute
                newx, newy = idx % 4, int(idx / 4)
                c.move(newx - c.pos[0], newy - c.pos[1])
                c.pos = newx, newy

    def _left(self):
        """ Moves all the cells to the left side """

        for idx in range(len(self.table)):  # # Iterates the array from the beginning

            if self.table[idx]:

                c = self.table[idx]
                while idx % 4:

                    if self.table[idx - 1] and self.table[idx].n == self.table[idx - 1].n:
                        self.table[idx - 1].double()
                        self._scorevar.set(int(self._scorevar.get()) + self.table[idx - 1].n)
                        self.table[idx] = 0
                        idx -= 1
                        break

                    elif self.table[idx - 1]:
                        break

                    else:
                        self.table[idx - 1] = self.table[idx]
                        self.table[idx] = 0
                        idx -= 1

                newx, newy = idx % 4, int(idx / 4)
                c.move(newx - c.pos[0], newy - c.pos[1])
                c.pos = newx, newy

    def _down(self):
        """ Moves all the cells to the bottom """

        for idx in list(range(len(self.table)))[::-1]:

            if self.table[idx]:

                c = self.table[idx]
                while not 12 <= idx <= 15:

                    if self.table[idx + 4] and self.table[idx + 4].n == self.table[idx].n:
                        self.table[idx + 4].double()
                        self._scorevar.set(int(self._scorevar.get()) + self.table[idx + 4].n)
                        self.table[idx] = 0
                        idx += 4
                        break

                    elif self.table[idx + 4]:
                        break

                    else:
                        self.table[idx + 4] = self.table[idx]
                        self.table[idx] = 0
                        idx += 4

                newx, newy = idx % 4, int(idx / 4)
                c.move(newx - c.pos[0], newy - c.pos[1])
                c.pos = newx, newy

    def _up(self):
        """ Moves all the cells to the top """

        for idx in range(len(self.table)):

            if self.table[idx]:

                c = self.table[idx]
                while not 0 <= idx <= 3:

                    if self.table[idx - 4] and self.table[idx - 4].n == self.table[idx].n:
                        self.table[idx - 4].double()
                        self._scorevar.set(int(self._scorevar.get()) + self.table[idx - 4].n)
                        self.table[idx] = 0
                        idx -= 4
                        break

                    elif self.table[idx - 4]:
                        break

                    else:
                        self.table[idx - 4] = self.table[idx]
                        self.table[idx] = 0
                        idx -= 4

                newx, newy = idx % 4, int(idx / 4)
                c.move(newx - c.pos[0], newy - c.pos[1])
                c.pos = newx, newy


root = Tk()

app = App(root)

root.bind("<a>", lambda event: app.callback(0))
root.bind("<d>", lambda event: app.callback(1))
root.bind("<w>", lambda event: app.callback(3))
root.bind("<s>", lambda event: app.callback(2))

root.bind("<r>", lambda event: app.restart())

root.mainloop()