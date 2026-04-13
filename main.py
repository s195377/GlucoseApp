"""main.py

Application entry point and controller.
"""

import tkinter as tk
import experiment_environment
import test_environment


def launch_picker() -> None:
    """Show a launcher window to choose what to open."""
    root = tk.Tk()
    root.title("Experiment Launcher")
    root.geometry("400x320")
    root.resizable(False, False)

    tk.Label(
        root, text="What would you like to launch?",
        font=("Arial", 13, "bold")
    ).pack(pady=(24, 16))

    # ── HTML script picker ────────────────────────────────────────────────
    scripts = list(experiment_environment.HTML_SCRIPTS.keys())
    var = tk.StringVar(value=scripts[0])

    frame = tk.LabelFrame(root, text="Visualisation", font=("Arial", 10, "bold"),
                          padx=16, pady=8)
    frame.pack(fill="x", padx=24)

    for key in scripts:
        tk.Radiobutton(
            frame, text=key, variable=var, value=key,
            font=("Arial", 10), anchor="w"
        ).pack(fill="x", pady=2)

    # ── Buttons ───────────────────────────────────────────────────────────
    bottom = tk.Frame(root, pady=20)
    bottom.pack(fill="x", side="bottom", padx=24)

    def on_visualisation():
        root.destroy()
        experiment_environment.run(var.get())

    def on_test_session():
        root.destroy()
        test_environment.run()

    tk.Button(bottom, text="Open Visualisation",
              command=on_visualisation, width=18, height=2).pack(side="right", padx=(6, 0))
    tk.Button(bottom, text="Run Test Session",
              command=on_test_session, width=16, height=2).pack(side="right", padx=6)

    root.mainloop()


def main() -> None:
    launch_picker()


if __name__ == "__main__":
    main()