import tkinter as tk
import random
from PIL import ImageTk, Image

tk.sys.setrecursionlimit(10000)


class mainMenu:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        tk.Label(
            self.frame,
            bg="white",
            text="Game Of Life",
            font=("Verdona", 20),
            fg="black",
        ).grid(row=0, columnspan=2, sticky="ew")
        tk.Label(
            self.frame,
            text="Enter Game Options",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="black",
            pady=10,
        ).grid(row=1, columnspan=2, pady=10)
        tk.Label(
            self.frame,
            text="Number of Columns:",
            font=("Verdona", 10, "bold"),
            fg="black",
            pady=10,
        ).grid(row=2, column=0, sticky="w")
        tk.Label(
            self.frame,
            text="Number of Rows:",
            font=("Verdona", 10, "bold"),
            fg="black",
            pady=10,
        ).grid(row=3, column=0, sticky="w")
        tk.Label(
            self.frame,
            text="Number of Cells Alive:",
            font=("Verdona", 10, "bold"),
            fg="black",
            pady=10,
        ).grid(row=4, column=0, sticky="w")

        columns = tk.IntVar()
        columns.set(10)
        rows = tk.IntVar()
        rows.set(10)
        liveCells = tk.IntVar()
        liveCells.set(20)

        e1 = tk.Entry(
                self.frame,
                textvariable=columns,
                width=17,
                justify="center",
            )
        e2 = tk.Entry(
                self.frame,
                textvariable=rows,
                width=17,
                justify="center",
            )
        e3 = tk.Entry(
                self.frame,
                textvariable=liveCells,
                width=17,
                justify="center",
            )

        e1.grid(row=2, column=1)
        e2.grid(row=3, column=1)
        e3.grid(row=4, column=1)

        tk.Button(
            self.frame,
            text="Quit",
            command=self.master.quit,
        ).grid(row=5, column=1, sticky="W", pady=4)
        tk.Button(
            self.frame,
            text="Start",
            command=lambda: self.loadGame(
                columns=int(e1.get()), rows=int(e2.get()), liveCells=int(e3.get())
            ),
        ).grid(row=5, column=1, sticky="E")

    def loadGame(self, columns, rows, liveCells):
        self.gameWindow = tk.Toplevel(self.master)
        self.game = gameFrame(self.gameWindow, rows, columns, liveCells)


class gameFrame:
    def __init__(self, master, rows=0, columns=0, liveCells=0):
        self.master = master
        self.master.resizable(False, False)
        self.frame = tk.Frame(
                        self.master,
                        height=10 * rows + 4,
                        width=columns * 10 + 4
                    )
        self.frame.pack()
        self.liveCells = 0
        self.rows = rows
        self.columns = columns
        self.grid = [[0 for j in range(columns)] for i in range(rows)]
        self.gameCanvasBoard = tk.Canvas(
            self.frame, width=columns * 10 + 1, height=rows * 10 + 1
        )
        self.gameCanvasBoard.pack()
        while self.liveCells != liveCells:
            x = random.randrange(0, rows)
            y = random.randrange(0, columns)
            if self.grid[x][y] != 1:
                self.grid[x][y] = 1
                self.liveCells += 1
        self.createTable()

    def updateTable(self):
        self.newGrid = [[0 for i in range(self.columns)] for j in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                liveCells = 0
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        if (
                            i + a > -1 and i + a < self.rows and
                            j + b > -1 and j + b < self.columns
                        ):
                            if self.grid[i + a][j + b] == 1:
                                liveCells += 1
                self.determineFate(liveCells, i, j)
        self.grid = self.newGrid.copy()

    def determineFate(self, liveCells, x, y):
        if self.grid[x][y] == 1 and liveCells < 2:
            self.newGrid[x][y] = 0
        elif self.grid[x][y] == 1 and (liveCells == 2 or liveCells == 3):
            self.newGrid[x][y] = 1
        elif self.grid[x][y] == 1 and liveCells > 3:
            self.newGrid[x][y] = 0
        elif self.grid[x][y] == 0 and liveCells == 3:
            self.newGrid[x][y] = 1
        else:
            self.newGrid[x][y] = self.grid[x][y]

    def createTable(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j] == 0:
                    self.gameCanvasBoard.create_rectangle(
                        j * 10,
                        i * 10,
                        j * 10 + 10,
                        i * 10 + 10,
                        fill='black',
                    )
                elif self.grid[i][j] == 1:
                    self.gameCanvasBoard.create_rectangle(
                        j * 10,
                        i * 10,
                        j * 10 + 10,
                        i * 10 + 10,
                        fill='white'
                    )
        self.updateTable()
        self.master.after(500, self.createTable)


def main():
    root = tk.Tk(className="Game of Life")
    root.title("Game of Life")
    root.call("wm", "iconphoto", root._w, tk.PhotoImage(file="i.png"))
    root.resizable(False, False)
    app = mainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()