"""
Home Page - Module Selection
All modules available, simple 2x2 centered layout
"""

import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.COLORS = controller.COLORS
        self.modules = [
            {
                "icon": "🖼️",
                "title": "IMAGE STEGANOGRAPHY",
                "description": "Hide data inside image files (PNG)",
                "status": "Available",
                "page": "ImagePage",
                "color": self.COLORS['primary']
            },
            {
                "icon": "📄",
                "title": "TEXT FILE STEGANOGRAPHY",
                "description": "Conceal information within text documents",
                "status": "Available",
                "page": "TextFilePage",
                "color": self.COLORS['secondary']
            },
            {
                "icon": "🎵",
                "title": "AUDIO STEGANOGRAPHY",
                "description": "Embed data in audio files (WAV)",
                "status": "Available",
                "page": "AudioPage",
                "color": "#ff9d00"
            },
            {
                "icon": "🎬",
                "title": "VIDEO STEGANOGRAPHY",
                "description": "Hide information in video streams",
                "status": "Available",
                "page": "VideoPage",
                "color": "#ff2a6d"
            }
        ]
        self.setup_page()

    def setup_page(self):
        self.configure(bg=self.COLORS['bg'])

        # Back to Start Button
        back_btn = tk.Button(
            self,
            text="← Back to Start",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['bg'],
            bg=self.COLORS['accent'],
            activeforeground=self.COLORS['bg'],
            activebackground=self.COLORS['primary'],
            borderwidth=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=lambda: self.controller.show_page("StartPage")
        )
        back_btn.pack(pady=(20,10))
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg=self.COLORS['primary']))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg=self.COLORS['accent']))

        # Page Title
        tk.Label(
            self,
            text="SELECT STEGANOGRAPHY MODE",
            font=("Courier New", 24, "bold"),
            fg=self.COLORS['primary'],
            bg=self.COLORS['bg']
        ).pack(pady=(10,5))

        tk.Label(
            self,
            text="Choose a method for hiding your secret data",
            font=("Segoe UI", 12),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['bg']
        ).pack(pady=(0,20))

        # Frame to center cards
        self.cards_frame = tk.Frame(self, bg=self.COLORS['bg'])
        self.cards_frame.pack(pady=10, anchor="n")

        # Create 2x2 grid cards
        self.cards = [self.create_module_card(m) for m in self.modules]
        for i, card in enumerate(self.cards):
            row = i // 2
            col = i % 2
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

        # Make columns equal width for centering
        for c in range(2):
            self.cards_frame.grid_columnconfigure(c, weight=1)

        # Separator
        tk.Frame(self, height=2, width=600, bg=self.COLORS['primary']).pack(pady=20)

        # Security Info
        sec_frame = tk.Frame(self, bg=self.COLORS['card_bg'], padx=15, pady=15)
        sec_frame.pack(fill="x", pady=(0,10))

        tk.Label(
            sec_frame, text="🔒", font=("Segoe UI", 20), fg=self.COLORS['primary'], bg=self.COLORS['card_bg']
        ).pack(side="left", padx=(0,10))

        tk.Label(
            sec_frame,
            text="All methods use AES-256 encryption for maximum security",
            font=("Segoe UI", 10),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg'],
            wraplength=400,
            justify="left"
        ).pack(side="left", anchor="w")

    def create_module_card(self, module):
        """Create a single module card"""
        card = tk.Frame(
            self.cards_frame,
            bg=self.COLORS['card_bg'],
            width=250,
            height=150,
            highlightbackground=module['color'],
            highlightthickness=2,
            relief="flat"
        )

        # Icon
        tk.Label(card, text=module['icon'], font=("Segoe UI", 28),
                 fg=module['color'], bg=self.COLORS['card_bg']).pack(anchor="w", padx=15, pady=(15,8))
        # Title
        tk.Label(card, text=module['title'], font=("Segoe UI", 12, "bold"),
                 fg=self.COLORS['text'], bg=self.COLORS['card_bg'], anchor="w").pack(fill="x", padx=15, pady=(0,4))
        # Description
        tk.Label(card, text=module['description'], font=("Segoe UI", 9),
                 fg=self.COLORS['secondary'], bg=self.COLORS['card_bg'],
                 wraplength=220, justify="left", anchor="w").pack(fill="x", padx=15, pady=(0,8))

        # Status Frame
        status_frame = tk.Frame(card, bg=self.COLORS['card_bg'])
        status_frame.pack(fill="x", padx=15, pady=(0,10))

        tk.Label(status_frame, text=f"Status: {module['status']}", font=("Segoe UI", 8, "italic"),
                 fg=module['color'], bg=self.COLORS['card_bg']).pack(side="left")

        btn = tk.Button(
            status_frame,
            text="SELECT →",
            font=("Segoe UI", 9, "bold"),
            fg=self.COLORS['bg'],
            bg=module['color'],
            activeforeground=self.COLORS['bg'],
            activebackground=self.COLORS['secondary'],
            borderwidth=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=lambda p=module['page']: self.controller.show_page(p)
        )
        btn.pack(side="right")
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.COLORS['secondary']))
        btn.bind("<Leave>", lambda e, b=btn, c=module['color']: b.config(bg=c))

        # Make entire card clickable
        card.bind("<Button-1>", lambda e, p=module['page']: self.controller.show_page(p))
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda e, p=module['page']: self.controller.show_page(p))

        return card
