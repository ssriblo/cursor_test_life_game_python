import random
import tkinter as tk
from tkinter import ttk

# Simulation settings
ROWS = 50
COLS = 70
CELL_SIZE = 10  # pixels
DEFAULT_DELAY_MS = 100  # smaller = faster


class GameOfLife:
    def __init__(self, root):
        self.root = root
        self.root.title("Conway's Game of Life")

        self.rows = ROWS
        self.cols = COLS
        self.cell_size = CELL_SIZE
        self.delay_ms = DEFAULT_DELAY_MS
        self.running = False

        self.grid = self.create_grid()
        self._build_ui()
        self.draw_grid()

    # ---- Model ----
    def create_grid(self):
        return [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def clear_grid(self):
        self.grid = self.create_grid()
        self.draw_grid()

    def randomize_grid(self, density=0.2):
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c] = random.random() < density
        self.draw_grid()

    def count_neighbors(self, r, c):
        count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.grid[nr][nc]:
                        count += 1
        return count

    def step(self):
        new_grid = self.create_grid()
        for r in range(self.rows):
            for c in range(self.cols):
                alive = self.grid[r][c]
                neighbors = self.count_neighbors(r, c)

                if alive and neighbors in (2, 3):
                    new_grid[r][c] = True
                elif not alive and neighbors == 3:
                    new_grid[r][c] = True
                else:
                    new_grid[r][c] = False
        self.grid = new_grid

    # ---- UI ----
    def _build_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for grid
        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size

        self.canvas = tk.Canvas(
            main_frame,
            width=canvas_width,
            height=canvas_height,
            bg="white",
            highlightthickness=0,
        )
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        # Controls
        controls = ttk.Frame(main_frame)
        controls.pack(side=tk.TOP, fill=tk.X, pady=4)

        self.start_button = ttk.Button(controls, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=2)

        self.stop_button = ttk.Button(controls, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=2)

        self.step_button = ttk.Button(controls, text="Step", command=self.step_once)
        self.step_button.pack(side=tk.LEFT, padx=2)

        self.clear_button = ttk.Button(controls, text="Clear", command=self.clear_grid)
        self.clear_button.pack(side=tk.LEFT, padx=2)

        self.random_button = ttk.Button(
            controls, text="Random", command=lambda: self.randomize_grid(0.25)
        )
        self.random_button.pack(side=tk.LEFT, padx=2)

        # Preset patterns
        self.glider_button = ttk.Button(controls, text="Glider", command=self.add_glider)
        self.glider_button.pack(side=tk.LEFT, padx=2)

        self.pulsar_button = ttk.Button(controls, text="Pulsar", command=self.add_pulsar)
        self.pulsar_button.pack(side=tk.LEFT, padx=2)

        # Speed control
        speed_frame = ttk.Frame(controls)
        speed_frame.pack(side=tk.LEFT, padx=10)

        ttk.Label(speed_frame, text="Speed").pack(side=tk.TOP)

        # Scale: higher value = faster (smaller delay)
        self.speed_scale = ttk.Scale(
            speed_frame,
            from_=500,      # very slow (left)
            to=10,          # very fast (right)
            orient=tk.HORIZONTAL,
            command=self.on_speed_change,
        )
        self.speed_scale.set(self.delay_ms)
        self.speed_scale.pack(side=tk.TOP, fill=tk.X)

        # Bind mouse events for editing
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)

    # ---- Rendering ----
    def draw_grid(self):
        self.canvas.delete("all")

        # Draw live cells
        for r in range(self.rows):
            y0 = r * self.cell_size
            y1 = y0 + self.cell_size
            for c in range(self.cols):
                if self.grid[r][c]:
                    x0 = c * self.cell_size
                    x1 = x0 + self.cell_size
                    self.canvas.create_rectangle(
                        x0,
                        y0,
                        x1,
                        y1,
                        fill="black",
                        outline="white",
                    )

        # Optional: draw grid lines
        for r in range(self.rows + 1):
            y = r * self.cell_size
            self.canvas.create_line(0, y, self.cols * self.cell_size, y, fill="#e0e0e0")
        for c in range(self.cols + 1):
            x = c * self.cell_size
            self.canvas.create_line(x, 0, x, self.rows * self.cell_size, fill="#e0e0e0")

    # ---- Interaction ----
    def canvas_coords_to_cell(self, x, y):
        col = x // self.cell_size
        row = y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return int(row), int(col)
        return None, None

    def toggle_cell(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = not self.grid[row][col]
            self.draw_grid()

    def on_canvas_click(self, event):
        row, col = self.canvas_coords_to_cell(event.x, event.y)
        if row is not None:
            self.toggle_cell(row, col)

    def on_canvas_drag(self, event):
        row, col = self.canvas_coords_to_cell(event.x, event.y)
        if row is not None and not self.grid[row][col]:
            self.grid[row][col] = True
            self.draw_grid()

    # ---- Simulation control ----
    def on_speed_change(self, value):
        try:
            self.delay_ms = int(float(value))
        except ValueError:
            self.delay_ms = DEFAULT_DELAY_MS

    # ---- Patterns ----
    def apply_pattern(self, pattern_cells, offset_row, offset_col):
        for dr, dc in pattern_cells:
            r = offset_row + dr
            c = offset_col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                self.grid[r][c] = True
        self.draw_grid()

    def add_glider(self):
        # Classic glider pattern (relative coordinates)
        glider = [
            (0, 1),
            (1, 2),
            (2, 0), (2, 1), (2, 2),
        ]
        center_row = self.rows // 2
        center_col = self.cols // 2
        origin_row = center_row - 1
        origin_col = center_col - 1
        self.apply_pattern(glider, origin_row, origin_col)

    def add_pulsar(self):
        # Classic pulsar oscillator (period 3), radius 6 (13x13 bounding box)
        base_offsets = [
            (0, 2), (0, 3), (0, 4),
            (0, 8), (0, 9), (0, 10),
            (2, 0), (3, 0), (4, 0),
            (2, 5), (3, 5), (4, 5),
            (2, 7), (3, 7), (4, 7),
            (2, 12), (3, 12), (4, 12),
            (5, 2), (5, 3), (5, 4),
            (5, 8), (5, 9), (5, 10),
            (7, 2), (7, 3), (7, 4),
            (7, 8), (7, 9), (7, 10),
            (8, 0), (9, 0), (10, 0),
            (8, 5), (9, 5), (10, 5),
            (8, 7), (9, 7), (10, 7),
            (8, 12), (9, 12), (10, 12),
            (12, 2), (12, 3), (12, 4),
            (12, 8), (12, 9), (12, 10),
        ]
        # Normalize pattern so minimum row/col is 0
        min_r = min(r for r, _ in base_offsets)
        min_c = min(c for _, c in base_offsets)
        pattern = [(r - min_r, c - min_c) for r, c in base_offsets]

        center_row = self.rows // 2
        center_col = self.cols // 2
        # Pulsar is 13x13, origin is center - 6
        origin_row = center_row - 6
        origin_col = center_col - 6
        self.apply_pattern(pattern, origin_row, origin_col)

    def start(self):
        if not self.running:
            self.running = True
            self.run_loop()

    def stop(self):
        self.running = False

    def step_once(self):
        if not self.running:
            self.step()
            self.draw_grid()

    def run_loop(self):
        if not self.running:
            return
        self.step()
        self.draw_grid()
        self.root.after(self.delay_ms, self.run_loop)


def main():
    root = tk.Tk()
    app = GameOfLife(root)
    root.mainloop()


if __name__ == "__main__":
    main()

