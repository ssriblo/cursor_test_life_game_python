# LIFE game development in Python
_Exported on 19/02/2026 at 17:17:19 GMT+4 from Cursor (2.5.17)_

---

**User**

need write "LIFE" game on python. Let suggest simple UI lib and write plan firstly

---

**Cursor**

### Suggested simple UI library

For a small, self‑contained Game of Life in Python, **`tkinter`** is a great choice:

- **Built-in**: ships with standard CPython, no extra install.
- **Simple drawing**: you can draw the grid as rectangles on a `Canvas`.
- **Basic controls**: buttons, sliders (for speed), etc., are easy to add.

(If you later want smoother animation or larger grids, `pygame` is another good option, but it’s an extra dependency.)

---

### High-level plan

#### 1. Define core game model (logic without UI)
- **Grid representation**: use a 2D list or `set` of live cell coordinates.
- **Initialization**: create an empty grid and some helper functions:
  - `create_grid(rows, cols)`
  - `randomize_grid(grid, density)`
  - `clear_grid(grid)`
- **Rules function**:
  - Implement `step(grid)` that returns a new grid after applying Conway’s rules:
    - Any live cell with 2 or 3 neighbors survives.
    - Any dead cell with exactly 3 neighbors becomes alive.
    - Otherwise, the cell is dead.

#### 2. Map model to UI coordinates
- **Cell size**: choose a fixed pixel size, e.g. `CELL_SIZE = 10`.
- **Canvas size**: `width = cols * CELL_SIZE`, `height = rows * CELL_SIZE`.
- **Conversion helpers**:
  - From grid to pixels: `(row, col) → (x0, y0, x1, y1)`.
  - From mouse click to cell: `(x, y) → (row, col)`.

#### 3. Build the `tkinter` UI skeleton
- **Main window**: create `Tk()` root.
- **Canvas**: create a `Canvas` with size from step 2.
- **Controls**:
  - Buttons: `Start`, `Stop`, `Step`, `Clear`, `Random`.
  - Optional: `Scale` widget to control simulation speed (delay in ms).
- **Layout**: use `pack()` or `grid()` to place canvas on top and controls below.

#### 4. Rendering the grid
- Implement `draw_grid(grid)`:
  - Clear the canvas (or reuse rectangles if you want to optimize later).
  - For every live cell, draw a filled rectangle.
  - Optionally draw faint grid lines for readability.

#### 5. Interaction (editing the board)
- Bind mouse events on `Canvas`:
  - On left-click (or drag), toggle the cell under the cursor alive/dead.
  - Update the grid data structure, then call `draw_grid()`.

#### 6. Simulation loop
- Maintain a `running` flag.
- Implement:
  - `start()`:
    - Set `running = True`.
    - Call a `run_step_loop()` that:
      - Calls `step(grid)` to compute the next generation.
      - Calls `draw_grid(grid)`.
      - Uses `root.after(delay_ms, run_step_loop)` to schedule the next step if `running` is still `True`.
  - `stop()`:
    - Set `running = False` to halt the loop.
  - `step_once()`:
    - Apply one `step(grid)` and redraw (without starting the continuous loop).

#### 7. Wiring everything together
- Initialize grid and UI in `main()`:
  - Create the grid.
  - Create `Tk`, canvas, and controls.
  - Bind button commands to the model/UI functions.
  - Start the event loop with `root.mainloop()`.

#### 8. Optional enhancements
- **Patterns**: save/load patterns (e.g., gliders) from simple text files.
- **Zoom / grid size selection**: allow user to set rows/cols at startup.
- **Performance tweaks**: use a `set` of live cells instead of full 2D list for sparse grids.

---

If you’re happy with this plan and `tkinter` as the UI, next I can write a complete, runnable `life.py` implementing it.

---

**User**

let write complete code

---

**Cursor**

Here’s a complete, self‑contained implementation using `tkinter`. Save as `life.py` and run with `python life.py`.

```python
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

        # Speed control
        speed_frame = ttk.Frame(controls)
        speed_frame.pack(side=tk.LEFT, padx=10)

        ttk.Label(speed_frame, text="Speed").pack(side=tk.TOP)

        # Scale: lower delay (faster) to higher delay (slower)
        self.speed_scale = ttk.Scale(
            speed_frame,
            from_=10,      # very fast
            to=500,        # very slow
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
```

You can tweak `ROWS`, `COLS`, `CELL_SIZE`, or the random density in `Random` to get different board sizes and behaviors. If you want a `pygame` version or extra features (saving patterns, etc.), tell me what to add next.

---

**User**

store this code at current project folder, file named lifeGame.py

---

**Cursor**

### File created

**Done.** I’ve saved the full Game of Life implementation as `lifeGame.py` in your current project folder.

You can run it from that directory with:

```bash
python lifeGame.py
```

If you’d like, we can next add presets (glider, pulsar, etc.) or tweak grid size and colors.

