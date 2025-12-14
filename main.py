import tkinter as tk
from tkinter import messagebox

class SteganographyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cyber Steganography Suite")
        self.state('zoomed')  # Maximized window
        self.resizable(True, True)

        # ===== COLOR THEME =====
        self.COLORS = {
            'bg': "#0a0e14",
            'primary': "#00ff9d",
            'secondary': "#00b8ff",
            'accent': "#ff2a6d",
            'text': "#e6e6e6",
            'card_bg': "#1a1f29",
            'warning': "#ffaa00",
            'success': "#28a745",
            'error': "#dc3545"
        }

        # ===== APP STATE =====
        self.frames = {}

        # ===== UI SETUP =====
        self.configure(bg=self.COLORS['bg'])
        self.setup_header()
        self.setup_container()
        self.setup_footer()

        # ===== LOAD PAGES =====
        self.load_pages()
        self.show_page("StartPage")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # ===== HEADER =====
    def setup_header(self):
        self.header = tk.Frame(self, height=50, bg=self.COLORS['bg'])
        self.header.pack(fill="x", padx=20, pady=(10, 0))

        self.title_label = tk.Label(
            self.header,
            text="🔒 CYBER STEGANOGRAPHY",
            font=("Courier New", 18, "bold"),
            fg=self.COLORS['primary'],
            bg=self.COLORS['bg']
        )
        self.title_label.pack(side="left")

        self.back_btn = tk.Button(
            self.header,
            text="← Main Menu",
            font=("Segoe UI", 10),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['bg'],
            borderwidth=0,
            cursor="hand2",
            command=lambda: self.show_page("HomePage")
        )

        self.status_label = tk.Label(
            self.header,
            text="⚡ Ready",
            font=("Consolas", 10),
            fg=self.COLORS['primary'],
            bg=self.COLORS['bg']
        )
        self.status_label.pack(side="right", padx=10)

    # ===== CONTAINER =====
    def setup_container(self):
        self.container = tk.Frame(self, bg=self.COLORS['bg'])
        self.container.pack(fill="both", expand=True, padx=20, pady=10)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    # ===== FOOTER =====
    def setup_footer(self):
        self.footer = tk.Frame(self, height=30, bg=self.COLORS['bg'])
        self.footer.pack(fill="x", side="bottom", pady=(0, 10))
        tk.Label(self.footer, text="© 2024 Cyber Steganography | v1.0.0",
                 font=("Segoe UI", 8), fg="#666666", bg=self.COLORS['bg']).pack(side="left", padx=20)
        tk.Label(self.footer, text="🔐 All operations are encrypted",
                 font=("Segoe UI", 9), fg=self.COLORS['secondary'], bg=self.COLORS['bg']).pack(side="right", padx=20)

    # ===== PAGE LOADING =====
    def load_pages(self):
        pages_to_load = [
            ("StartPage", "ui_pages.start"),
            ("HomePage", "ui_pages.home"),
            ("ImagePage", "ui_pages.image_page"),
            ("TextFilePage", "ui_pages.textfile_page"),
            ("AudioPage", "ui_pages.audio_page"),
            ("VideoPage", "ui_pages.video_page")
        ]

        for page_name, module_path in pages_to_load:
            try:
                module = __import__(module_path, fromlist=[page_name])
                page_class = getattr(module, page_name)
                frame = page_class(parent=self.container, controller=self)
            except Exception:
                frame = self.create_placeholder_page(page_name)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    # ===== PLACEHOLDER PAGE =====
    def create_placeholder_page(self, page_name):
        frame = tk.Frame(self.container, bg=self.COLORS['bg'])
        tk.Label(frame, text=f"🚧 {page_name.replace('Page', ' Module')}", font=("Courier New", 24, "bold"),
                 fg=self.COLORS['warning'], bg=self.COLORS['bg']).pack(pady=100)
        tk.Label(frame, text="Coming Soon", font=("Segoe UI", 14),
                 fg=self.COLORS['secondary'], bg=self.COLORS['bg']).pack(pady=20)
        tk.Button(frame, text="← Return to Home", font=("Segoe UI", 12),
                  fg=self.COLORS['primary'], bg=self.COLORS['bg'], borderwidth=0, cursor="hand2",
                  command=lambda: self.show_page("HomePage")).pack(pady=30)
        return frame

    # ===== PAGE NAVIGATION =====
    def show_page(self, page_name):
        if page_name not in self.frames:
            messagebox.showerror("Error", f"Page '{page_name}' not found")
            return
        frame = self.frames[page_name]
        frame.tkraise()
        self.update_header(page_name)
        self.status_label.config(text=f"⚡ Viewing {page_name.replace('Page', '')}")

    def update_header(self, page_name):
        if page_name in ["StartPage", "HomePage"]:
            self.back_btn.pack_forget()
        else:
            self.back_btn.pack(side="left", padx=20)

    # ===== CLOSE HANDLER =====
    def on_closing(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.destroy()


# ===== APP ENTRY POINT =====
def main():
    app = SteganographyApp()
    app.mainloop()


if __name__ == "__main__":
    main()
