import tkinter as tk
from main import task_combo, current_phase, root

animation_speed = 20 




def update_animation():
    task = task_combo.get()
    x0, y0, x1, y1 = canvas.coords(mouse)
    if current_phase == "thinking":
        if task == "Move Mouse Up":
            if y0 > 0:
                canvas.move(mouse, 0, -animation_speed)
            else:
                canvas.coords(mouse, 190, 390, 210, 410)
        elif task == "Move Mouse Down":
            if y1 < 400:
                canvas.move(mouse, 0, animation_speed)
            else:
                canvas.coords(mouse, 190, -10, 210, 10)
        elif task == "Move Mouse Left":
            if x0 > 0:
                canvas.move(mouse, -animation_speed, 0)
            else:
                canvas.coords(mouse, 390, 190, 410, 210)
        elif task == "Move Mouse Right":
            if x1 < 400:
                canvas.move(mouse, animation_speed, 0)
            else:
                canvas.coords(mouse, -10, 190, 10, 210)
        elif task == "Click":
            canvas.itemconfig(mouse, fill="red")
            root.after(100, lambda: canvas.itemconfig(mouse, fill="black"))