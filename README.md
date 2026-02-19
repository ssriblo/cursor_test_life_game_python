# Conway's Game of Life (Python + Tkinter)

This project is a simple implementation of **Conway's Game of Life** with a graphical interface built using Python's standard `tkinter` library. You can edit the grid with your mouse, then run the simulation to see how the pattern evolves over time.

---

## How to run

1. Make sure you have Python 3 installed.
2. From the project folder, run:

   ```bash
   python lifeGame.py
   ```

The window will open with an empty grid.

---

## File structure

- **`lifeGame.py`**: main and only source file.
  - Defines the `GameOfLife` class, which holds both the **simulation state (model)** and the **UI (view + controls)**.
  - Starts the application by creating a `tk.Tk()` root window and an instance of `GameOfLife`.

There are no external dependencies other than the Python standard library (`tkinter`, `random`).

---

## Code overview

### Global configuration

At the top of `lifeGame.py` there are a few constants:

- **`ROWS` / `COLS`**: number of rows and columns in the grid.
- **`CELL_SIZE`**: pixel size of each cell on the canvas.
- **`DEFAULT_DELAY_MS`**: delay (in milliseconds) between generations when the simulation is running.

These control the size and speed of the simulation.

### `GameOfLife` class

The `GameOfLife` class encapsulates:

- **State (model)**:
  - `self.grid`: a 2D list (`rows x cols`) of booleans. `True` means the cell is alive, `False` means dead.
  - `self.running`: whether the simulation loop is currently active.
  - `self.delay_ms`: current delay between simulation steps (controlled by the speed slider).
- **UI elements**:
  - `self.canvas`: `tk.Canvas` where the grid is drawn.
  - Control buttons (`Start`, `Stop`, `Step`, `Clear`, `Random`) and a `ttk.Scale` to control speed.

The constructor:

- Initializes the state.
- Calls `_build_ui()` to build the interface.
- Calls `draw_grid()` to render the initial (empty) grid.

---

## Model (simulation logic)

Key methods that implement the Game of Life rules:

- **`create_grid()`**: creates an empty grid filled with `False` values.
- **`clear_grid()`**: resets the grid to all-dead cells, then redraws.
- **`randomize_grid(density=0.2)`**: fills the grid with random live cells with the given probability (`density`).
- **`count_neighbors(r, c)`**: counts the number of live neighbors around cell `(r, c)` (8 neighbors max).
- **`step()`**:
  - Creates a new grid.
  - For each cell, counts live neighbors and applies Conway's rules:
    - A live cell survives if it has 2 or 3 neighbors.
    - A dead cell becomes alive if it has exactly 3 neighbors.
    - Otherwise, the cell is dead.
  - Replaces the current grid with the new grid.

---

## UI and rendering

### Layout

`_build_ui()` sets up:

- A main `ttk.Frame` as container.
- A `tk.Canvas` at the top that shows the grid.
- A controls `ttk.Frame` below with:
  - `Start`, `Stop`, `Step`, `Clear`, `Random` buttons.
  - A `Speed` slider to adjust the simulation speed.

### Drawing the grid

- **`draw_grid()`**:
  - Clears the canvas.
  - For each live cell in `self.grid`, draws a filled rectangle.
  - Optionally draws light grid lines so you can see the cell boundaries.

The mapping between grid indices and pixels is:

- `x = col * CELL_SIZE`, `y = row * CELL_SIZE`.

---

## Interaction and controls

### Mouse interaction

- **Click (`on_canvas_click`)**:
  - Converts the mouse `(x, y)` position to a `(row, col)` cell index.
  - Toggles that cell between alive and dead.
- **Drag (`on_canvas_drag`)**:
  - While the left mouse button is held down, moving over cells sets them to alive.

Coordinate conversion is handled by:

- **`canvas_coords_to_cell(x, y)`**: turns canvas pixel coordinates into grid indices.

### Simulation control

- **`start()`**:
  - Sets `self.running = True`.
  - Starts the main loop via `run_loop()`.
- **`stop()`**:
  - Sets `self.running = False` to pause the simulation.
- **`step_once()`**:
  - If not currently running, applies one `step()` and redraws.
- **`run_loop()`**:
  - If `self.running` is `True`:
    - Calls `step()` to compute the next generation.
    - Calls `draw_grid()` to update the display.
    - Uses `root.after(self.delay_ms, self.run_loop)` to schedule the next update.

### Speed slider

- **`on_speed_change(value)`** updates `self.delay_ms` whenever the user moves the slider.
- Lower values = faster simulation (shorter delay between frames).

---

## Entry point

At the bottom of `lifeGame.py`:

- **`main()`**:
  - Creates the main `tk.Tk()` window.
  - Instantiates `GameOfLife`.
  - Starts the Tk event loop with `root.mainloop()`.
- The `if __name__ == "__main__": main()` block makes the script runnable directly.

---

## Possible extensions

Some ideas for further improvements:

- Allow saving/loading patterns to/from a simple text format.
- Add preset buttons for common patterns (glider, pulsar, etc.).
- Let the user change grid size and cell size from the UI.
- Use colors or gradients for older cells or different states.
