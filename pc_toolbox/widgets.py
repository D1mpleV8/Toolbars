import os
import tkinter as tk
import customtkinter as ctk
import random
import math

class DigitalRainCanvas(tk.Canvas):
    """
    Highly optimized, breathtaking premium Matrix Digital Rain canvas.
    Displays falling neon-green kana/binary characters with varying opacities and speeds,
    providing the ultimate cyberpunk sensory atmosphere.
    Uses a safe local Random generator to prevent process-wide random seed pollution.
    """
    def __init__(self, master, bg_color="#000000", **kwargs):
        super().__init__(master, bg=bg_color, highlightthickness=0, **kwargs)
        self.rng = random.Random(99)
        self.columns = []
        self.bind("<Configure>", self.on_resize)
        self.running = True
        self.animate()

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        char_size = 14
        num_columns = max(1, int(self.width / char_size))
        self.columns = []
        for _ in range(num_columns):
            self.columns.append({
                "y": self.rng.randint(-100, 0),
                "speed": self.rng.uniform(2, 6),
                "chars": [chr(self.rng.randint(33, 126)) for _ in range(15)],
                "head_y": self.rng.randint(-50, 0)
            })

    def animate(self):
        if not self.running:
            return
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w > 1 and h > 1:
            char_size = 14
            for i, col in enumerate(self.columns):
                col["y"] += col["speed"]
                if col["y"] > h:
                    col["y"] = self.rng.randint(-100, 0)
                    col["speed"] = self.rng.uniform(2, 6)

                # Draw the trail of characters
                cx = i * char_size
                for j, char in enumerate(col["chars"]):
                    cy = col["y"] - (j * char_size)
                    if 0 < cy < h:
                        # Gradient from bright neon green head to dark green tail
                        if j == 0:
                            color = "#ffffff"  # Glowing white head
                        elif j < 3:
                            color = "#00ff00"  # Neon green
                        elif j < 8:
                            color = "#00bb00"  # Medium green
                        else:
                            color = "#004400"  # Dark green

                        self.create_text(
                            cx, cy,
                            text=char,
                            fill=color,
                            font=("Courier", 10, "bold"),
                            anchor="nw"
                        )

                # Randomly change characters for dynamic feel
                if self.rng.random() < 0.1:
                    col["chars"] = [chr(self.rng.randint(33, 126)) for _ in range(15)]

        self.after(40, self.animate)

    def stop(self):
        self.running = False


class ScanningEffect(tk.Canvas):
    """
    Futuristic HUD radar scan layout with vector circles, crosshairs,
    radial sweep gradients, and neon green targeting blips.
    Uses local Random generator to prevent process-wide random seed corruption.
    """
    def __init__(self, master, color="#00ff00", bg_color="#000700", **kwargs):
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
            r = min(w, h) / 2.3

            # Draw radar HUD grid rings
            self.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#001a00", width=1.5)
            self.create_oval(cx - r*0.75, cy - r*0.75, cx + r*0.75, cy + r*0.75, outline="#00ff00", width=1, dash=(5, 5))
            self.create_oval(cx - r*0.4, cy - r*0.4, cx + r*0.4, cy + r*0.4, outline="#001a00", width=1)

            # Crosshair segments
            self.create_line(cx - r, cy, cx + r, cy, fill="#001a00", width=1)
            self.create_line(cx, cy - r, cx, cy + r, fill="#001a00", width=1)

            # Dynamic Sweep Line
            rad = math.radians(self.angle)
            lx = cx + r * math.cos(rad)
            ly = cy + r * math.sin(rad)
            self.create_line(cx, cy, lx, ly, fill="#00ffcc", width=2.5)

            # Outer orbital indicators
            self.create_arc(cx - r*1.08, cy - r*1.08, cx + r*1.08, cy + r*1.08, start=self.angle, extent=75, outline="#00ff00", width=2, style="arc")
            self.create_arc(cx - r*0.9, cy - r*0.9, cx + r*0.9, cy + r*0.9, start=-self.angle, extent=45, outline="#00ffcc", width=1.5, style="arc")

            # Safe local seed generator to prevent system random corruption
            rng = random.Random(1337)
            for i in range(3):
                bx = cx + rng.randint(int(-r*0.8), int(r*0.8))
                by = cy + rng.randint(int(-r*0.8), int(r*0.8))
                dist = math.sqrt((bx-cx)**2 + (by-cy)**2)
                if dist < r:
                    self.create_oval(bx-5, by-5, bx+5, by+5, fill="#00ffcc", outline="#ffffff", width=1)

            self.angle = (self.angle + 3) % 360
        self.after(30, self.animate)

    def stop(self):
        self.running = False


class CyberButton(ctk.CTkButton):
    """
    Sleek, futuristic tactile buttons with transparent dark bodies,
    glowing Neon Matrix Green interactive border-edges, and high-tech typography.
    """
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="#000a00",
            hover_color="#001f00",
            border_color="#00ff00",
            border_width=1.5,
            text_color="#00ff00",
            font=("Consolas" if os.name == "nt" else "Courier", 12, "bold"),
            corner_radius=8,
            **kwargs
        )


class CyberCard(ctk.CTkFrame):
    """
    Futuristic semi-transparent "glassmorphic" panel with thin glowing highlights,
    providing exceptional information hierarchy and ahead-of-its-time design depth.
    """
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="#000700",
            border_color="#001f00",
            border_width=1.5,
            corner_radius=12,
            **kwargs
        )
