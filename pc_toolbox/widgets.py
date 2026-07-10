import tkinter as tk
import customtkinter as ctk
import random
import math

class DigitalRainCanvas(tk.Canvas):
    """
    Highly optimized and resource-friendly Digital Rain canvas widget.
    Implements hardware-friendly animation with smooth neon-green dripping effects
    resembling the classic Matrix rain.
    """
    def __init__(self, master, color="#00FF00", bg_color="#000000", **kwargs):
        super().__init__(master, bg=bg_color, highlightthickness=0, **kwargs)
        self.color = color
        self.bg_color = bg_color
        self.columns = []
        self.font_size = 14
        self.chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=[]{}|;':\",./<>?"
        self.bind("<Configure>", self.on_resize)
        self.running = True
        self.animate()

    def on_resize(self, event):
        width = event.width
        height = event.height
        num_columns = max(1, width // self.font_size)
        self.columns = []
        for _ in range(num_columns):
            self.columns.append({
                "y": random.randint(-height, 0),
                "speed": random.randint(5, 15),
                "chars": [random.choice(self.chars) for _ in range(max(5, height // self.font_size))]
            })

    def animate(self):
        if not self.running:
            return
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        if width > 1 and height > 1:
            for i, col in enumerate(self.columns):
                x = i * self.font_size
                col["y"] += col["speed"]
                if col["y"] > height:
                    col["y"] = random.randint(-150, 0)
                    col["speed"] = random.randint(5, 15)

                # Draw trailing characters with fading shades of green
                # Modern Matrix rain uses a bright white head, followed by neon and then darker green
                num_tail = 12
                for j in range(num_tail):
                    char_y = col["y"] - (j * self.font_size)
                    if 0 <= char_y < height:
                        char = random.choice(self.chars) if random.random() < 0.1 else col["chars"][int(char_y // self.font_size) % len(col["chars"])]
                        # Head of the stream is white, following characters are neon green, tail is dark green
                        if j == 0:
                            col_val = "#FFFFFF"
                        elif j < 4:
                            col_val = "#00FF00"
                        elif j < 8:
                            col_val = "#008800"
                        else:
                            col_val = "#003300"
                        self.create_text(x, char_y, text=char, fill=col_val, font=("Courier", self.font_size, "bold"))
        self.after(50, self.animate)

    def stop(self):
        self.running = False


class ScanningEffect(tk.Canvas):
    """
    A glowing, futuristic scanner/radar scanning animation effect.
    Visual feedback that mimics high-tech Cyber Ops tools scanning systems.
    """
    def __init__(self, master, color="#00FF00", bg_color="#000000", **kwargs):
        super().__init__(master, bg=bg_color, highlightthickness=0, **kwargs)
        self.color = color
        self.angle = 0
        self.bind("<Configure>", self.on_resize)
        self.running = True
        self.animate()

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height

    def animate(self):
        if not self.running:
            return
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w > 1 and h > 1:
            cx, cy = w / 2, h / 2
            r = min(w, h) / 2.2

            # Outer futuristic scanning circle
            self.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#004400", width=2)
            self.create_oval(cx - r*0.7, cy - r*0.7, cx + r*0.7, cy + r*0.7, outline="#003300", width=1, dash=(5, 5))
            self.create_oval(cx - r*0.4, cy - r*0.4, cx + r*0.4, cy + r*0.4, outline="#003300", width=1)

            # Draw radar line
            rad = math.radians(self.angle)
            lx = cx + r * math.cos(rad)
            ly = cy + r * math.sin(rad)
            self.create_line(cx, cy, lx, ly, fill="#00FF00", width=3)

            # Add scanning fading trails
            for i in range(1, 10):
                trail_angle = self.angle - i * 4
                tr_rad = math.radians(trail_angle)
                tx = cx + r * math.cos(tr_rad)
                ty = cy + r * math.sin(tr_rad)
                alpha_color = "#008800" if i < 5 else "#003300"
                self.create_line(cx, cy, tx, ty, fill=alpha_color, width=1.5)

            # Target dots (blips)
            random.seed(42)  # Consistent mock targets
            for _ in range(3):
                bx = cx + random.randint(int(-r*0.8), int(r*0.8))
                by = cy + random.randint(int(-r*0.8), int(r*0.8))
                dist = math.sqrt((bx-cx)**2 + (by-cy)**2)
                if dist < r:
                    self.create_oval(bx-4, by-4, bx+4, by+4, fill="#00FF00", outline="#FFFFFF")

            self.angle = (self.angle + 3) % 360
        self.after(30, self.animate)

    def stop(self):
        self.running = False


class CyberButton(ctk.CTkButton):
    """
    Sleek, next-generation CustomTkinter button styled for the Matrix theme.
    """
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="#001a00",
            hover_color="#003300",
            border_color="#00FF00",
            border_width=1,
            text_color="#00FF00",
            font=("Courier", 13, "bold"),
            corner_radius=4,
            **kwargs
        )
