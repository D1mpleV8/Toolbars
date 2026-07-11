import os
import tkinter as tk
import customtkinter as ctk
import random
import math

class DigitalRainCanvas(tk.Canvas):
    """
    Subtle, elegant high-tech Matrix digital code stream with thin, glowing
    semi-transparent trails that float dynamically in the background.
    Optimized to be resource-friendly, using an ahead-of-its-time holographic palette.
    """
    def __init__(self, master, color="#00ffcc", bg_color="#080c10", **kwargs):
        super().__init__(master, bg=bg_color, highlightthickness=0, **kwargs)
        self.color = color
        self.bg_color = bg_color
        self.columns = []
        self.font_size = 13
        # Futuristic glyphs/symbols
        self.chars = "ΞΟΦΨΩαβγδεζηθικλμνξοπρστυφχψω0123456789ΔΛ"
        self.bind("<Configure>", self.on_resize)
        self.running = True
        self.animate()

    def on_resize(self, event):
        width = event.width
        height = event.height
        num_columns = max(1, width // (self.font_size + 4))
        self.columns = []
        for _ in range(num_columns):
            self.columns.append({
                "y": random.randint(-height, 0),
                "speed": random.randint(4, 10),
                "chars": [random.choice(self.chars) for _ in range(max(10, height // self.font_size))]
            })

    def animate(self):
        if not self.running:
            return
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        if width > 1 and height > 1:
            for i, col in enumerate(self.columns):
                x = i * (self.font_size + 4)
                col["y"] += col["speed"]
                if col["y"] > height:
                    col["y"] = random.randint(-200, 0)
                    col["speed"] = random.randint(4, 10)

                # Draw subtle holographic trails with glowing white heads
                num_tail = 15
                for j in range(num_tail):
                    char_y = col["y"] - (j * self.font_size)
                    if 0 <= char_y < height:
                        char = random.choice(self.chars) if random.random() < 0.05 else col["chars"][int(char_y // self.font_size) % len(col["chars"])]

                        # High-tech gradient: bright white head, neon mint/cyan trail, fading into deep obsidian
                        if j == 0:
                            col_val = "#ffffff"  # Glowing core
                        elif j < 3:
                            col_val = "#00ffcc"  # Neon Mint
                        elif j < 7:
                            col_val = "#00b3e6"  # Electric Cyan
                        elif j < 11:
                            col_val = "#005580"  # Deep Tech Blue
                        else:
                            col_val = "#0c151c"  # Dark Ambient Cyber

                        self.create_text(
                            x, char_y,
                            text=char,
                            fill=col_val,
                            font=("Segoe UI Semibold" if os.name == "nt" else "Courier", self.font_size)
                        )
        self.after(45, self.animate)

    def stop(self):
        self.running = False


class ScanningEffect(tk.Canvas):
    """
    Holographic Circular Sci-Fi Scanner with clean circular orbits, orbital arcs,
    grid alignment ticks, and glowing data blips in Neon Mint.
    """
    def __init__(self, master, color="#00ffcc", bg_color="#080c10", **kwargs):
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

            # Sophisticated futuristic design elements (Holographic guidelines)
            # Outer rings
            self.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#0d2535", width=1)
            self.create_oval(cx - r*0.8, cy - r*0.8, cx + r*0.8, cy + r*0.8, outline="#143c54", width=1.5)
            self.create_oval(cx - r*0.5, cy - r*0.5, cx + r*0.5, cy + r*0.5, outline="#0d2535", width=1)

            # Grid Crosshairs
            self.create_line(cx - r, cy, cx + r, cy, fill="#0d2535", width=1, dash=(4, 4))
            self.create_line(cx, cy - r, cx, cy + r, fill="#0d2535", width=1, dash=(4, 4))

            # Clean sweep line (glowing Mint gradient)
            rad = math.radians(self.angle)
            lx = cx + r * math.cos(rad)
            ly = cy + r * math.sin(rad)
            self.create_line(cx, cy, lx, ly, fill="#00ffcc", width=2.5)

            # Orbital arc elements (flickering details)
            self.create_arc(cx - r*1.05, cy - r*1.05, cx + r*1.05, cy + r*1.05, start=self.angle, extent=60, outline="#00e5ff", width=2, style="arc")
            self.create_arc(cx - r*0.9, cy - r*0.9, cx + r*0.9, cy + r*0.9, start=self.angle + 180, extent=45, outline="#00ffcc", width=1, style="arc")

            # Soft glowing targets (blips)
            random.seed(99)  # Uniform mock positions
            for i in range(4):
                bx = cx + random.randint(int(-r*0.85), int(r*0.85))
                by = cy + random.randint(int(-r*0.85), int(r*0.85))
                dist = math.sqrt((bx-cx)**2 + (by-cy)**2)
                if dist < r * 0.9:
                    alpha_factor = abs(math.sin(math.radians(self.angle - i*30)))
                    glow_color = "#00ffcc" if alpha_factor > 0.5 else "#005550"
                    self.create_oval(bx-5, by-5, bx+5, by+5, fill=glow_color, outline="#ffffff", width=1)

            self.angle = (self.angle + 2) % 360
        self.after(25, self.animate)

    def stop(self):
        self.running = False


class CyberButton(ctk.CTkButton):
    """
    Sleek, futuristic tactile buttons with transparent dark bodies,
    glowing Neon Mint interactive border-edges, and high-tech typography.
    """
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="#0d1b2a",
            hover_color="#1b4965",
            border_color="#00ffcc",
            border_width=1.5,
            text_color="#00ffcc",
            font=("Segoe UI Semibold", 12, "bold"),
            corner_radius=6,
            **kwargs
        )


class CyberCard(ctk.CTkFrame):
    """
    Futuristic semi-transparent "glassmorphic" panel with thin neon borders,
    providing exceptional information hierarchy and ahead-of-its-time design depth.
    """
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="#081017",
            border_color="#102a43",
            border_width=1.5,
            corner_radius=10,
            **kwargs
        )
