import tkinter as tk

class Canvas:
    def __init__(self, width, height):
        self.tk = tk.Tk()
        self.tk.title("Breakout")
        self.canvas = tk.Canvas(self.tk, width=width, height=height, bg="white")
        self.canvas.pack()
        self.tk.update()
        self.objects = {}

    def create_rectangle(self, x1, y1, x2, y2, fill_color, outline_color=None):
        outline = outline_color if outline_color else fill_color
        obj_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=outline)
        self.objects[obj_id] = obj_id
        self.tk.update()
        return obj_id

    def create_oval(self, x1, y1, x2, y2, fill_color):
        obj_id = self.canvas.create_oval(x1, y1, x2, y2, fill=fill_color, outline=fill_color)
        self.objects[obj_id] = obj_id
        self.tk.update()
        return obj_id

    def move(self, obj_id, dx, dy):
        self.canvas.move(obj_id, dx, dy)
        self.tk.update()

    def moveto(self, obj_id, new_x, new_y):
        coords = self.canvas.coords(obj_id)
        if coords:
            current_x = coords[0]
            current_y = coords[1]
            dx = new_x - current_x
            dy = new_y - current_y
            self.move(obj_id, dx, dy)

    def get_left_x(self, obj_id):
        return self.canvas.coords(obj_id)[0]

    def get_top_y(self, obj_id):
        return self.canvas.coords(obj_id)[1]

    def find_overlapping(self, x1, y1, x2, y2):
        return self.canvas.find_overlapping(x1, y1, x2, y2)

    def delete(self, obj_id):
        self.canvas.delete(obj_id)
        self.tk.update()

    def get_mouse_x(self):
        self.tk.update()
        try:
            return self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        except:
            return None
