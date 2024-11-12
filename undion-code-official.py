import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES

class UndionInterpreter:
    def __init__(self, size=20):
        self.size = size
        self.window = TkinterDnD.Tk()
        self.window.title("Undion Code")
        self.canvas = tk.Canvas(self.window, width=self.size*20, height=self.size*20)
        self.canvas.pack()
        
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.pixels = [[self.canvas.create_rectangle(
            x*20, y*20, (x+1)*20, (y+1)*20, fill="white"
        ) for x in range(self.size)] for y in range(self.size)]
        
        self.window.drop_target_register(DND_FILES)
        self.window.dnd_bind('<<Drop>>', self.load_file)

    def load_file(self, event):
        filepath = event.data.strip("{}")
        if not filepath.endswith('.udn'):
            print("The file format is incorrect. Is required .udn")
            return

        with open(filepath, 'r') as file:
            content = file.read().splitlines()

        if not content[0].startswith("\\undion on"):
            print("start in \\undion on")
            return
        
        for command in content[1:]:
            self.run_command(command)

    def run_command(self, command):
        if command.startswith("pick"):
            x, y = self._parse_coordinates(command)
            self._activate_pixel(x, y)
        elif command.startswith("depick"):
            x, y = self._parse_coordinates(command)
            self._deactivate_pixel(x, y)
        elif command == "clear":
            self._clear_grid()

    def _parse_coordinates(self, command):
        start = command.index("{") + 1
        end = command.index("}")
        coords = command[start:end]
        x, y = map(int, coords.split(":"))
        return x, y

    def _activate_pixel(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[y][x] = 1
            self.canvas.itemconfig(self.pixels[y][x], fill="black")

    def _deactivate_pixel(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[y][x] = 0
            self.canvas.itemconfig(self.pixels[y][x], fill="white")

    def _clear_grid(self):
        for y in range(self.size):
            for x in range(self.size):
                self.grid[y][x] = 0
                self.canvas.itemconfig(self.pixels[y][x], fill="white")

    def run(self):
        self.window.mainloop()

interpreter = UndionInterpreter()
interpreter.run()
