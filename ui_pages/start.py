"""
Start Page - Welcome Screen
Clean and modern design with cyber security theme
"""

import tkinter as tk

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.COLORS = controller.COLORS
        self.setup_page()
    
    def setup_page(self):
        """Setup all page elements"""
        self.configure(bg=self.COLORS['bg'])
        
        # Main container for centering
        main_container = tk.Frame(self, bg=self.COLORS['bg'])
        main_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # ===== CYBER SYMBOL =====
        cyber_symbol = tk.Label(
            main_container,
            text="⚡",
            font=("Segoe UI", 72),
            fg=self.COLORS['primary'],
            bg=self.COLORS['bg']
        )
        cyber_symbol.pack(pady=(0, 20))
        
        # ===== MAIN TITLE =====
        title_label = tk.Label(
            main_container,
            text="CYBER STEGANOGRAPHY",
            font=("Courier New", 32, "bold"),
            fg=self.COLORS['primary'],
            bg=self.COLORS['bg']
        )
        title_label.pack(pady=(0, 10))
        
        # ===== SUBTITLE =====
        subtitle_label = tk.Label(
            main_container,
            text="Secure Data Hiding Suite",
            font=("Segoe UI", 16),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['bg']
        )
        subtitle_label.pack(pady=(0, 40))
        
        # ===== SEPARATOR =====
        separator = tk.Frame(
            main_container,
            height=2,
            width=400,
            bg=self.COLORS['primary']
        )
        separator.pack(pady=(0, 50))
        
        # ===== START BUTTON =====
        start_button = tk.Button(
            main_container,
            text="START HIDING →",
            font=("Segoe UI", 14, "bold"),
            fg=self.COLORS['bg'],
            bg=self.COLORS['accent'],
            activeforeground=self.COLORS['bg'],
            activebackground=self.COLORS['primary'],
            borderwidth=0,
            padx=40,
            pady=15,
            cursor="hand2",
            command=lambda: self.controller.show_page("HomePage")
        )
        start_button.pack()
        
        # Add hover effect
        start_button.bind("<Enter>", lambda e: start_button.config(bg=self.COLORS['primary']))
        start_button.bind("<Leave>", lambda e: start_button.config(bg=self.COLORS['accent']))
        
        # ===== VERSION INFO =====
        version_label = tk.Label(
            self,
            text="Version 1.0.0 | © 2026 Cyber Security Team",
            font=("Segoe UI", 9),
            fg="#666666",
            bg=self.COLORS['bg']
        )
        version_label.pack(side="bottom", pady=20)
