import os
import tkinter as tk
import customtkinter as ctk
import random
import math

class CyberSpaceCanvas(tk.Canvas):
    """
    Highly optimized, breathtaking premium dynamic vector floating particles.
    Provides an ultra-sleek, ahead-of-its-time gaming hub ambient background.
    Colors are styled with glowing Sapphire Blue (#00f0ff) and Electric Violet (#8a2be2) accents.
    """
    def __init__(self, master, bg_color="#07080b", **kwargs):
        super().__init__(master, bg=bg_color, highlightthickness=0, **kwargs)
        self.particles = []
        self.bind("<Configure>", self.on_resize)
        self.running = True
        self.animate()

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.particles = []
        # Local random generator to prevent process-wide random seed pollution
        rng = random.Random(1337)
        for _ in range(40):
            self.particles.append({
                "x": rng.randint(0, self.width),
                "y": rng.randint(0, self.height),
                "radius": rng.uniform(1.2, 3.8),
                "speed_y": rng.uniform(-1.2, -0.2),
                "speed_x": rng.uniform(-0.3, 0.3),
                "color": rng.choice(["#00f0ff", "#8a2be2", "#ff007f", "#00ffcc"])
            })

    def animate(self):
        if not self.running:
            return
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w > 1 and h > 1:
            for i, p in enumerate(self.particles):
                p["y"] += p["speed_y"]
                p["x"] += p["speed_x"]
                if p["y"] < 0:
                    p["y"] = h
                    p["x"] = random.randint(0, w)
                if p["x"] < 0 or p["x"] > w:
                    p["x"] = random.randint(0, w)

                # Draw glowing vector nodes
                self.create_oval(
                    p["x"] - p["radius"], p["y"] - p["radius"],
                    p["x"] + p["radius"], p["y"] + p["radius"],
                    fill=p["color"], outline=""
                )

                # Draw high-performance dynamic neural link lines between nearby particles
                for j in range(i + 1, len(self.particles)):
                    p2 = self.particles[j]
                    dist = math.sqrt((p["x"] - p2["x"])**2 + (p["y"] - p2["y"])**2)
                    if dist < 110:
                        self.create_line(p["x"], p["y"], p2["x"], p2["y"], fill="#111622", width=1)

        self.after(55, self.animate)

    def stop(self):
        self.running = False


class DigitalRainCanvas(CyberSpaceCanvas):
    """
    Alias/Fallback class for DigitalRainCanvas to prevent any import failures,
    but redirects directly to the gorgeous Modern CyberSpaceCanvas vector particle engine.
    """
    pass


class ScanningEffect(tk.Canvas):
    """
    Futuristic HUD radar scan layout with vector circles, crosshairs,
    radial sweep gradients, and neon violet/cyan targeting blips.
    Uses local Random generator to prevent process-wide random seed corruption.
    """
    def __init__(self, master, color="#00f0ff", bg_color="#090a0f", **kwargs):
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
            self.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#181c25", width=1.5)
            self.create_oval(cx - r*0.75, cy - r*0.75, cx + r*0.75, cy + r*0.75, outline="#8a2be2", width=1, dash=(5, 5))
            self.create_oval(cx - r*0.4, cy - r*0.4, cx + r*0.4, cy + r*0.4, outline="#181c25", width=1)

            # Crosshair segments
            self.create_line(cx - r, cy, cx + r, cy, fill="#181c25", width=1)
            self.create_line(cx, cy - r, cx, cy + r, fill="#181c25", width=1)

            # Dynamic Sweep Line
            rad = math.radians(self.angle)
            lx = cx + r * math.cos(rad)
            ly = cy + r * math.sin(rad)
            self.create_line(cx, cy, lx, ly, fill="#00f0ff", width=2.5)

            # Outer orbital indicators
            self.create_arc(cx - r*1.08, cy - r*1.08, cx + r*1.08, cy + r*1.08, start=self.angle, extent=75, outline="#ff007f", width=2, style="arc")
            self.create_arc(cx - r*0.9, cy - r*0.9, cx + r*0.9, cy + r*0.9, start=-self.angle, extent=45, outline="#00f0ff", width=1.5, style="arc")

            # Safe local seed generator to prevent system random corruption
            rng = random.Random(1337)
            for i in range(3):
                bx = cx + rng.randint(int(-r*0.8), int(r*0.8))
                by = cy + rng.randint(int(-r*0.8), int(r*0.8))
                dist = math.sqrt((bx-cx)**2 + (by-cy)**2)
                if dist < r:
                    self.create_oval(bx-5, by-5, bx+5, by+5, fill="#00f0ff", outline="#ffffff", width=1)

            self.angle = (self.angle + 3) % 360
        self.after(30, self.animate)

    def stop(self):
        self.running = False


class CyberButton(ctk.CTkButton):
    """
    Sleek, futuristic tactile buttons with transparent dark bodies,
    glowing Neon Sapphire Blue interactive border-edges, and high-tech typography.
    """
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="#0c0d12",
            hover_color="#151724",
            border_color="#00f0ff",
            border_width=1.5,
            text_color="#00f0ff",
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
            fg_color="#0e1017",
            border_color="#181e2b",
            border_width=1.5,
            corner_radius=12,
            **kwargs
        )
