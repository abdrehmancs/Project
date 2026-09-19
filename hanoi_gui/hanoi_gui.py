"""A graphical Tower of Hanoi puzzle built with Tkinter."""

import tkinter as tk
from tkinter import messagebox, ttk


class TowerOfHanoiGUI:
    """Interactive Tower of Hanoi game with click-to-move controls."""

    DISK_COLORS = (
        "#e57373",  # red
        "#ba68c8",  # purple
        "#64b5f6",  # blue
        "#81c784",  # green
        "#ffd54f",  # amber
        "#4db6ac",  # teal
        "#f06292",  # pink
        "#90a4ae",  # grey
    )

    def __init__(self, root, disk_count=3):
        self.root = root
        self.root.title("Tower of Hanoi")
        self.root.resizable(False, False)

        self.disk_count = disk_count
        self.rods = [[], [], []]  # Each rod holds disk sizes, largest at index 0
        self.selected_disk = None
        self.selected_rod = None
        self.moves = 0
        self.min_moves = 2**disk_count - 1
        self.game_won = False
        self.animating = False

        self.disk_height = 34
        self.peg_width = 14
        self.rod_width = 300
        self.canvas_width = self.rod_width * 3 + 60
        self.canvas_height = self.disk_count * self.disk_height + 130

        self._init_state()
        self._build_ui()
        self._draw()

    def _init_state(self):
        """Reset the game state."""
        self.rods = [[], [], []]
        self.rods[0] = list(range(self.disk_count, 0, -1))  # Largest disk first
        self.selected_disk = None
        self.selected_rod = None
        self.moves = 0
        self.game_won = False

    def _build_ui(self):
        """Create all visual widgets."""
        # Title
        title = tk.Label(
            self.root,
            text="Tower of Hanoi",
            font=("Helvetica", 22, "bold"),
            fg="#37474f",
        )
        title.pack(pady=(15, 5))

        # Status bar
        self.status_var = tk.StringVar(value="Click a disk to select it")
        status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Helvetica", 12),
            fg="#546e7a",
        )
        status_label.pack(pady=(0, 10))

        # Canvas for the game board
        self.canvas = tk.Canvas(
            self.root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#fafafa",
            highlightthickness=2,
            highlightbackground="#b0bec5",
        )
        self.canvas.pack(padx=15, pady=(0, 15))
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        # Info row
        info_frame = tk.Frame(self.root)
        info_frame.pack(fill="x", padx=15, pady=(0, 10))

        self.moves_var = tk.StringVar(value=f"Moves: 0 / {self.min_moves}")
        moves_label = tk.Label(
            info_frame,
            textvariable=self.moves_var,
            font=("Helvetica", 12, "bold"),
            fg="#37474f",
        )
        moves_label.pack(side="left")

        # Controls
        controls = tk.Frame(self.root)
        controls.pack(fill="x", padx=15, pady=(0, 15))

        ttk.Button(
            controls,
            text="Reset",
            command=self.reset_game,
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            controls,
            text="Auto Solve",
            command=self.auto_solve,
        ).pack(side="left", padx=(0, 8))

        # Disk count selector
        ttk.Label(controls, text="Disks:").pack(side="left", padx=(12, 0))
        self.disk_var = tk.IntVar(value=self.disk_count)
        disk_selector = ttk.Combobox(
            controls,
            textvariable=self.disk_var,
            values=tuple(range(3, 9)),
            width=4,
            state="readonly",
        )
        disk_selector.pack(side="left", padx=(5, 0))
        disk_selector.bind("<<ComboboxSelected>>", self._on_disk_count_change)

        # Instructions
        instructions = tk.Label(
            self.root,
            text="Goal: move all disks from rod A to rod C. Larger disks may never sit on smaller ones.",
            font=("Helvetica", 10),
            fg="#78909c",
            wraplength=self.canvas_width,
            justify="center",
        )
        instructions.pack(padx=15, pady=(0, 15))

    def _draw(self):
        """Render rods, pegs, and disks on the canvas."""
        self.canvas.delete("all")

        ground_y = self.canvas_height - 30
        base_y = ground_y + 22

        # Draw the base
        self.canvas.create_rectangle(
            10,
            base_y,
            self.canvas_width - 10,
            base_y + 8,
            fill="#8d6e63",
            outline="#5d4037",
        )

        # Draw each rod
        for i in range(3):
            center_x = 30 + self.rod_width / 2 + i * self.rod_width
            peg_top = ground_y - self.disk_count * self.disk_height - 25

            # Peg
            self.canvas.create_rectangle(
                center_x - self.peg_width / 2,
                peg_top,
                center_x + self.peg_width / 2,
                ground_y,
                fill="#8d6e63",
                outline="#5d4037",
            )

            # Rod label
            self.canvas.create_text(
                center_x,
                base_y + 24,
                text="ABC"[i],
                font=("Helvetica", 14, "bold"),
                fill="#37474f",
            )

            # Draw disks on this rod
            rod = self.rods[i]
            for disk_index, disk in enumerate(rod):
                y_bottom = ground_y - disk_index * self.disk_height
                y_top = y_bottom - self.disk_height + 4
                width = 60 + disk * (self.rod_width - 110) / max(self.disk_count - 1, 1)

                color = self.DISK_COLORS[(disk - 1) % len(self.DISK_COLORS)]

                # Highlight selected disk
                if self.selected_disk == disk and self.selected_rod == i:
                    outline = "#ff9800"
                    outline_width = 3
                else:
                    outline = "#455a64"
                    outline_width = 1

                self.canvas.create_rectangle(
                    center_x - width / 2,
                    y_top,
                    center_x + width / 2,
                    y_bottom,
                    fill=color,
                    outline=outline,
                    width=outline_width,
                )

                # Disk number
                self.canvas.create_text(
                    center_x,
                    (y_top + y_bottom) / 2,
                    text=str(disk),
                    font=("Helvetica", 12, "bold"),
                    fill="white",
                )

    def _rod_from_x(self, x):
        """Return the rod index (0, 1, or 2) clicked based on x coordinate."""
        if 15 <= x < 15 + self.rod_width:
            return 0
        if 15 + self.rod_width <= x < 15 + self.rod_width * 2:
            return 1
        if 15 + self.rod_width * 2 <= x < self.canvas_width - 15:
            return 2
        return None

    def _on_canvas_click(self, event):
        """Handle a click on the game board."""
        if self.animating or self.game_won:
            return

        rod = self._rod_from_x(event.x)
        if rod is None:
            return

        # If a disk is selected, try to move it to the clicked rod
        if self.selected_disk is not None:
            if rod == self.selected_rod:
                self.selected_disk = None
                self.selected_rod = None
                self.status_var.set("Disk deselected. Click a disk to select it")
                self._draw()
                return

            if self._can_move(self.selected_rod, rod):
                self._move_disk(self.selected_rod, rod)
            else:
                self.status_var.set("Invalid move: a larger disk cannot go on a smaller one")
            self.selected_disk = None
            self.selected_rod = None
            self._draw()
            return

        # No disk selected — select the top disk on this rod
        if self.rods[rod]:
            self.selected_disk = self.rods[rod][-1]
            self.selected_rod = rod
            self.status_var.set(
                f"Disk {self.selected_disk} selected. Click a rod to move it"
            )
            self._draw()
        else:
            self.status_var.set("That rod is empty. Click a disk to select it")

    def _can_move(self, source_rod, target_rod):
        """Return True if moving the top disk is legal."""
        if not self.rods[source_rod]:
            return False
        if not self.rods[target_rod]:
            return True
        return self.rods[source_rod][-1] < self.rods[target_rod][-1]

    def _move_disk(self, source_rod, target_rod):
        """Move the top disk from one rod to another."""
        disk = self.rods[source_rod].pop()
        self.rods[target_rod].append(disk)
        self.moves += 1
        self.moves_var.set(f"Moves: {self.moves} / {self.min_moves}")

        if self._check_win():
            self.game_won = True
            self.status_var.set(
                f"Solved in {self.moves} moves! Click Reset to play again"
            )
            messagebox.showinfo("Congratulations!", f"Solved in {self.moves} moves!")
        else:
            self.status_var.set(f"Moved disk {disk} to rod {'ABC'[target_rod]}")

    def _check_win(self):
        """Return True if all disks are on rod C."""
        return len(self.rods[2]) == self.disk_count

    def _on_disk_count_change(self, _event=None):
        """Handle a change in the disk count selector."""
        self.disk_count = self.disk_var.get()
        self.min_moves = 2**self.disk_count - 1
        self.canvas_height = self.disk_count * self.disk_height + 130
        self.canvas.config(height=self.canvas_height)
        self.reset_game()

    def reset_game(self):
        """Reset the puzzle to its initial state."""
        self._init_state()
        self.moves_var.set(f"Moves: 0 / {self.min_moves}")
        self.status_var.set("Click a disk to select it")
        self._draw()

    def auto_solve(self):
        """Solve the puzzle automatically using the classic recursive algorithm."""
        if self.animating:
            return
        self.reset_game()
        self.animating = True
        self.status_var.set("Auto-solving...")

        moves = []
        self._generate_moves(self.disk_count, 0, 2, 1, moves)

        def step(index):
            if index >= len(moves):
                self.animating = False
                self.status_var.set("Auto-solve complete")
                return
            source, target = moves[index]
            disk = self.rods[source].pop()
            self.rods[target].append(disk)
            self.moves += 1
            self.moves_var.set(f"Moves: {self.moves} / {self.min_moves}")
            self._draw()
            self.root.after(350, step, index + 1)

        self.root.after(400, step, 0)

    def _generate_moves(self, n, source, target, auxiliary, moves):
        """Generate the sequence of moves needed to solve the puzzle."""
        if n == 0:
            return
        self._generate_moves(n - 1, source, auxiliary, target, moves)
        moves.append((source, target))
        self._generate_moves(n - 1, auxiliary, target, source, moves)


def main():
    root = tk.Tk()
    app = TowerOfHanoiGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
