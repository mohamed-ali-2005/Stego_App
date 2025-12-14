import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import base64
import json
from cryptography.fernet import Fernet
import hashlib
import re

class TextFilePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Get colors from controller
        self.COLORS = controller.COLORS
        
        # State variables
        self.source_text_file_path = ""
        self.output_text_file_path = ""
        self.encoded_text_file_path = ""
        
        # Setup page
        self.setup_page()
    
    def setup_page(self):
        """Setup all page elements"""
        # Configure frame
        self.configure(bg=self.COLORS['bg'])
        
        # ===== PAGE HEADER =====
        self.setup_header()
        
        # ===== MAIN CONTENT (TWO COLUMNS) =====
        self.setup_main_content()
        
        # ===== PAGE FOOTER =====
        self.setup_footer()
    
    def setup_header(self):
        """Setup page header"""
        header_frame = tk.Frame(self, bg=self.COLORS['bg'], height=80)
        header_frame.pack(fill="x", pady=(10, 0))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="📄 ADVANCED TEXT FILE STEGANOGRAPHY",
            font=("Courier New", 22, "bold"),
            fg=self.COLORS['primary'],
            bg=self.COLORS['bg']
        )
        title_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Hide & Extract Messages in Text Files | Whitespace & Zero-Width Character Methods",
            font=("Segoe UI", 11),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['bg']
        )
        subtitle_label.pack()
        
        # Method info
        method_info = tk.Label(
            header_frame,
            text="📌 Whitespace: Spaces & Tabs | 📌 Zero-Width: Invisible Unicode Characters",
            font=("Segoe UI", 10, "italic"),
            fg="#ffaa00",
            bg=self.COLORS['bg']
        )
        method_info.pack(pady=(5, 0))
        
        # Separator
        separator = tk.Frame(
            header_frame,
            height=2,
            bg=self.COLORS['primary']
        )
        separator.pack(fill="x", pady=(10, 0))
    
    def setup_main_content(self):
        """Setup two-column main content"""
        main_frame = tk.Frame(self, bg=self.COLORS['bg'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configure grid for two columns
        main_frame.grid_columnconfigure(0, weight=1, uniform="col")
        main_frame.grid_columnconfigure(1, weight=1, uniform="col")
        main_frame.grid_rowconfigure(0, weight=1)
        
        # ===== LEFT COLUMN - HIDE SECTION =====
        hide_frame = tk.LabelFrame(
            main_frame,
            text=" 🔒 ENCODE MESSAGE ",
            font=("Courier New", 14, "bold"),
            fg=self.COLORS['primary'],
            bg=self.COLORS['card_bg'],
            relief="groove",
            bd=2,
            padx=15,
            pady=15
        )
        hide_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # ===== RIGHT COLUMN - EXTRACT SECTION =====
        extract_frame = tk.LabelFrame(
            main_frame,
            text=" 🔓 DECODE MESSAGE ",
            font=("Courier New", 14, "bold"),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            relief="groove",
            bd=2,
            padx=15,
            pady=15
        )
        extract_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Fill both sections
        self.setup_hide_section(hide_frame)
        self.setup_extract_section(extract_frame)
    
    def setup_hide_section(self, parent):
        """Setup left column - Hide section"""
        # ===== SOURCE TEXT FILE SELECTION =====
        tk.Label(
            parent,
            text="Source Text File:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        source_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        source_frame.pack(fill="x", pady=(0, 10))
        
        self.source_entry = tk.Entry(
            source_frame,
            font=("Segoe UI", 10),
            fg=self.COLORS['text'],
            bg="#0f151f",
            insertbackground=self.COLORS['primary'],
            width=30,
            relief="sunken"
        )
        self.source_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.source_entry.insert(0, "Select source text file...")
        self.source_entry.config(fg="#666666")
        
        # Add placeholder functionality
        self.source_entry.bind("<FocusIn>", self.on_source_focus_in)
        self.source_entry.bind("<FocusOut>", self.on_source_focus_out)
        
        tk.Button(
            source_frame,
            text="📁",
            font=("Arial", 11),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=4,
            command=self.select_source_file
        ).pack(side="right")
        
        # File preview button
        tk.Button(
            source_frame,
            text="👁",
            font=("Arial", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=3,
            command=self.preview_source_file
        ).pack(side="right", padx=(0, 5))
        
        # ===== OUTPUT TEXT FILE SELECTION =====
        tk.Label(
            parent,
            text="Output Text File:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        output_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        output_frame.pack(fill="x", pady=(0, 10))
        
        self.output_entry = tk.Entry(
            output_frame,
            font=("Segoe UI", 10),
            fg=self.COLORS['text'],
            bg="#0f151f",
            insertbackground=self.COLORS['primary'],
            width=30,
            relief="sunken"
        )
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.output_entry.insert(0, "Save encoded text file...")
        self.output_entry.config(fg="#666666")
        
        # Add placeholder functionality
        self.output_entry.bind("<FocusIn>", self.on_output_focus_in)
        self.output_entry.bind("<FocusOut>", self.on_output_focus_out)
        
        tk.Button(
            output_frame,
            text="📁",
            font=("Arial", 11),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=4,
            command=self.select_output_file
        ).pack(side="right")
        
        # ===== METHOD SELECTION =====
        method_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        method_frame.pack(fill="x", pady=(0, 10))
        
        # Method selection
        tk.Label(
            method_frame,
            text="Method:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        self.method_var = tk.StringVar(value="Whitespace")
        
        method_subframe = tk.Frame(method_frame, bg=self.COLORS['card_bg'])
        method_subframe.pack(fill="x", pady=(0, 10))
        
        methods = [
            ("Whitespace (Spaces & Tabs at end of lines)", "Whitespace"),
            ("Zero-Width Characters (Invisible Unicode)", "ZeroWidth")
        ]
        
        for text, value in methods:
            rb = tk.Radiobutton(
                method_subframe,
                text=text,
                variable=self.method_var,
                value=value,
                font=("Segoe UI", 9),
                fg=self.COLORS['text'],
                bg=self.COLORS['card_bg'],
                activebackground=self.COLORS['card_bg'],
                activeforeground=self.COLORS['primary'],
                selectcolor=self.COLORS['bg'],
                cursor="hand2",
                command=self.on_method_change
            )
            rb.pack(anchor="w", pady=2)
        
        # Method info label
        self.method_info_label = tk.Label(
            method_frame,
            text="Space = 0, Tab = 1 (End of each line)",
            font=("Segoe UI", 9, "italic"),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg']
        )
        self.method_info_label.pack(anchor="w", pady=(0, 10))
        
        # ===== PASSWORD FIELD =====
        self.password_label = tk.Label(
            parent,
            text="Encryption Key:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        )
        self.password_label.pack(anchor="w", pady=(0, 5))
        
        password_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        password_frame.pack(fill="x", pady=(0, 10))
        
        self.hide_password = tk.Entry(
            password_frame,
            font=("Consolas", 10),
            fg=self.COLORS['primary'],
            bg="#0f151f",
            insertbackground=self.COLORS['primary'],
            show="•",
            width=25,
            relief="sunken"
        )
        self.hide_password.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.hide_password_show = False
        tk.Button(
            password_frame,
            text="👁",
            font=("Arial", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=3,
            command=self.toggle_hide_password
        ).pack(side="left")
        
        # Generate random password button
        tk.Button(
            password_frame,
            text="🎲",
            font=("Arial", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=3,
            command=self.generate_random_password
        ).pack(side="left", padx=(5, 0))
        
        # ===== SECRET MESSAGE =====
        tk.Label(
            parent,
            text="Secret Message:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        # Text widget with scrollbar
        text_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        text_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.secret_text = tk.Text(
            text_frame,
            font=("Consolas", 10),
            fg=self.COLORS['text'],
            bg="#0f151f",
            insertbackground=self.COLORS['primary'],
            width=40,
            height=6,
            wrap="word",
            relief="sunken"
        )
        self.secret_text.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame, command=self.secret_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.secret_text.config(yscrollcommand=scrollbar.set)
        
        # Character counter
        self.hide_char_count = tk.Label(
            parent,
            text="Characters: 0",
            font=("Segoe UI", 9),
            fg="#666666",
            bg=self.COLORS['card_bg']
        )
        self.hide_char_count.pack(anchor="e", pady=(0, 10))
        
        # Bind key release to update counter
        self.secret_text.bind("<KeyRelease>", self.update_hide_counter)
        
        # ===== ENCODE BUTTON =====
        encode_btn = tk.Button(
            parent,
            text="🔒 ENCRYPT & ENCODE",
            font=("Segoe UI", 11, "bold"),
            fg=self.COLORS['bg'],
            bg=self.COLORS['accent'],
            activeforeground=self.COLORS['bg'],
            activebackground=self.COLORS['primary'],
            borderwidth=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.encode_message
        )
        encode_btn.pack(pady=(5, 0))
        
        # Hover effect
        encode_btn.bind("<Enter>", lambda e: encode_btn.config(bg=self.COLORS['primary']))
        encode_btn.bind("<Leave>", lambda e: encode_btn.config(bg=self.COLORS['accent']))
        
        # استدعاء on_method_change لتهيئة العرض الأولي
        self.on_method_change()
    
    def setup_extract_section(self, parent):
        """Setup right column - Extract section"""
        # ===== ENCODED TEXT FILE SELECTION =====
        tk.Label(
            parent,
            text="Encoded Text File:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        encoded_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        encoded_frame.pack(fill="x", pady=(0, 10))
        
        self.encoded_entry = tk.Entry(
            encoded_frame,
            font=("Segoe UI", 10),
            fg=self.COLORS['text'],
            bg="#0f151f",
            insertbackground=self.COLORS['primary'],
            width=30,
            relief="sunken"
        )
        self.encoded_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.encoded_entry.insert(0, "Select encoded text file...")
        self.encoded_entry.config(fg="#666666")
        
        # Add placeholder functionality
        self.encoded_entry.bind("<FocusIn>", self.on_encoded_focus_in)
        self.encoded_entry.bind("<FocusOut>", self.on_encoded_focus_out)
        
        tk.Button(
            encoded_frame,
            text="📁",
            font=("Arial", 11),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=4,
            command=self.select_encoded_file
        ).pack(side="right")
        
        # Preview encoded file button
        tk.Button(
            encoded_frame,
            text="👁",
            font=("Arial", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=3,
            command=self.preview_encoded_file
        ).pack(side="right", padx=(0, 5))
        
        # ===== DECODING METHOD SELECTION =====
        tk.Label(
            parent,
            text="Decoding Method:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        self.decode_method_var = tk.StringVar(value="Auto Detect")
        
        decode_method_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        decode_method_frame.pack(fill="x", pady=(0, 10))
        
        decode_methods = [
            ("Auto Detect (Recommended)", "Auto Detect")
        ]
        
        for text, value in decode_methods:
            rb = tk.Radiobutton(
                decode_method_frame,
                text=text,
                variable=self.decode_method_var,
                value=value,
                font=("Segoe UI", 9),
                fg=self.COLORS['text'],
                bg=self.COLORS['card_bg'],
                activebackground=self.COLORS['card_bg'],
                activeforeground=self.COLORS['primary'],
                selectcolor=self.COLORS['bg'],
                cursor="hand2"
            )
            rb.pack(anchor="w", pady=2)
        
        # ===== PASSWORD FIELD =====
        tk.Label(
            parent,
            text="Decryption Key:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        decode_password_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        decode_password_frame.pack(fill="x", pady=(0, 10))
        
        self.extract_password = tk.Entry(
            decode_password_frame,
            font=("Consolas", 10),
            fg=self.COLORS['primary'],
            bg="#0f151f",
            insertbackground=self.COLORS['primary'],
            show="•",
            width=25,
            relief="sunken"
        )
        self.extract_password.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.extract_password_show = False
        tk.Button(
            decode_password_frame,
            text="👁",
            font=("Arial", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=3,
            command=self.toggle_extract_password
        ).pack(side="left")
        
        # Copy password button
        tk.Button(
            decode_password_frame,
            text="📋",
            font=("Arial", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=3,
            command=self.copy_password_from_hide
        ).pack(side="left", padx=(5, 0))
        
        # ===== DECODE BUTTON =====
        decode_btn = tk.Button(
            parent,
            text="🔓 DECRYPT & DECODE",
            font=("Segoe UI", 11, "bold"),
            fg=self.COLORS['bg'],
            bg=self.COLORS['secondary'],
            activeforeground=self.COLORS['bg'],
            activebackground=self.COLORS['primary'],
            borderwidth=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.decode_message
        )
        decode_btn.pack(pady=(0, 10))
        
        # Hover effect
        decode_btn.bind("<Enter>", lambda e: decode_btn.config(bg=self.COLORS['primary']))
        decode_btn.bind("<Leave>", lambda e: decode_btn.config(bg=self.COLORS['secondary']))
        
        # ===== RESULT AREA =====
        result_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        result_frame.pack(fill="both", expand=True)
        
        tk.Label(
            result_frame,
            text="Extracted Message:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        # Text widget for results with scrollbar
        result_text_frame = tk.Frame(result_frame, bg=self.COLORS['card_bg'])
        result_text_frame.pack(fill="both", expand=True)
        
        self.result_text = tk.Text(
            result_text_frame,
            font=("Consolas", 10),
            fg=self.COLORS['text'],
            bg="#0f151f",
            insertbackground=self.COLORS['primary'],
            width=40,
            height=6,
            wrap="word",
            state="disabled",
            relief="sunken"
        )
        self.result_text.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        result_scrollbar = tk.Scrollbar(result_text_frame, command=self.result_text.yview)
        result_scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=result_scrollbar.set)
        
        # Result counter and method info
        self.result_info_frame = tk.Frame(result_frame, bg=self.COLORS['card_bg'])
        self.result_info_frame.pack(fill="x", pady=(5, 0))
        
        self.result_char_count = tk.Label(
            self.result_info_frame,
            text="Characters: 0",
            font=("Segoe UI", 9),
            fg="#666666",
            bg=self.COLORS['card_bg']
        )
        self.result_char_count.pack(side="left")
        
        self.result_method_label = tk.Label(
            self.result_info_frame,
            text="Method: Unknown",
            font=("Segoe UI", 9, "italic"),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg']
        )
        self.result_method_label.pack(side="right")
        
        # ===== ACTION BUTTONS =====
        action_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        action_frame.pack(fill="x", pady=(10, 0))
        
        # Copy button
        tk.Button(
            action_frame,
            text="📋 Copy",
            font=("Segoe UI", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            command=self.copy_result_to_clipboard
        ).pack(side="left", padx=(0, 5))
        
        # Save button
        tk.Button(
            action_frame,
            text="💾 Save",
            font=("Segoe UI", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            command=self.save_extracted_message
        ).pack(side="left", padx=(0, 5))
        
        # Clear button
        tk.Button(
            action_frame,
            text="🗑️ Clear",
            font=("Segoe UI", 9),
            fg=self.COLORS['accent'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            command=self.clear_extract_section
        ).pack(side="left")
    
    def setup_footer(self):
        """Setup page footer"""
        footer_frame = tk.Frame(self, bg=self.COLORS['bg'], height=50)
        footer_frame.pack(fill="x", side="bottom", pady=(0, 10))
        
        # Status bar
        self.status_label = tk.Label(
            footer_frame,
            text="Ready",
            font=("Segoe UI", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['bg']
        )
        self.status_label.pack(side="left", padx=20)
        
        # Method info
        method_info = tk.Label(
            footer_frame,
            text="🔧 Whitespace: Space=0, Tab=1 | 🔧 Zero-Width: Invisible Unicode",
            font=("Segoe UI", 9),
            fg="#666666",
            bg=self.COLORS['bg']
        )
        method_info.pack(side="left", padx=20, expand=True)
        
        # Clear all button
        clear_all_btn = tk.Button(
            footer_frame,
            text="🗑️ Clear All",
            font=("Segoe UI", 9),
            fg=self.COLORS['accent'],
            bg=self.COLORS['bg'],
            activeforeground=self.COLORS['primary'],
            activebackground=self.COLORS['bg'],
            borderwidth=0,
            cursor="hand2",
            command=self.clear_all_fields
        )
        clear_all_btn.pack(side="right", padx=20)
    
    # ===== EVENT HANDLERS =====
    
    def on_source_focus_in(self, event=None):
        """Handle source entry focus in"""
        if self.source_entry.get() == "Select source text file...":
            self.source_entry.delete(0, tk.END)
            self.source_entry.config(fg=self.COLORS['text'])
    
    def on_source_focus_out(self, event=None):
        """Handle source entry focus out"""
        if self.source_entry.get() == "":
            self.source_entry.insert(0, "Select source text file...")
            self.source_entry.config(fg="#666666")
    
    def on_output_focus_in(self, event=None):
        """Handle output entry focus in"""
        if self.output_entry.get() == "Save encoded text file...":
            self.output_entry.delete(0, tk.END)
            self.output_entry.config(fg=self.COLORS['text'])
    
    def on_output_focus_out(self, event=None):
        """Handle output entry focus out"""
        if self.output_entry.get() == "":
            self.output_entry.insert(0, "Save encoded text file...")
            self.output_entry.config(fg="#666666")
    
    def on_encoded_focus_in(self, event=None):
        """Handle encoded entry focus in"""
        if self.encoded_entry.get() == "Select encoded text file...":
            self.encoded_entry.delete(0, tk.END)
            self.encoded_entry.config(fg=self.COLORS['text'])
    
    def on_encoded_focus_out(self, event=None):
        """Handle encoded entry focus out"""
        if self.encoded_entry.get() == "":
            self.encoded_entry.insert(0, "Select encoded text file...")
            self.encoded_entry.config(fg="#666666")
    
    def on_method_change(self):
        """Update method info based on selected method"""
        method = self.method_var.get()
        if method == "Whitespace":
            self.method_info_label.config(
                text="Space = 0, Tab = 1 (End of each line)",
                fg=self.COLORS['secondary']
            )
        else:  # ZeroWidth
            self.method_info_label.config(
                text="U+200B-Zero Width Space, U+200C-ZWNJ, U+200D-ZWJ",
                fg=self.COLORS['secondary']
            )
    
    # ===== FILE SELECTION METHODS =====
    
    def select_source_file(self):
        """Select source text file"""
        file_path = filedialog.askopenfilename(
            title="Select Source Text File",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, file_path)
            self.source_entry.config(fg=self.COLORS['text'])
            self.source_text_file_path = file_path
            self.update_status(f"Source selected: {os.path.basename(file_path)}")
            
            # Calculate capacity
            capacity = self.calculate_capacity()
            self.update_status(f"Capacity: {capacity} characters", "info")
    
    def select_output_file(self):
        """Select output text file path"""
        file_path = filedialog.asksaveasfilename(
            title="Save Encoded Text File As",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            # Ensure .txt extension
            if not file_path.lower().endswith('.txt'):
                file_path += '.txt'
            
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)
            self.output_entry.config(fg=self.COLORS['text'])
            self.output_text_file_path = file_path
    
    def select_encoded_file(self):
        """Select encoded text file for decoding"""
        file_path = filedialog.askopenfilename(
            title="Select Encoded Text File",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.encoded_entry.delete(0, tk.END)
            self.encoded_entry.insert(0, file_path)
            self.encoded_entry.config(fg=self.COLORS['text'])
            self.encoded_text_file_path = file_path
            self.update_status(f"Encoded file selected: {os.path.basename(file_path)}")
    
    def preview_source_file(self):
        """Preview source file content"""
        if not self.source_text_file_path:
            messagebox.showinfo("Info", "Please select a source file first.")
            return
        
        try:
            with open(self.source_text_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.show_preview_window("Source File Preview", content)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {str(e)}")
    
    def preview_encoded_file(self):
        """Preview encoded file content"""
        if not self.encoded_text_file_path:
            messagebox.showinfo("Info", "Please select an encoded file first.")
            return
        
        try:
            with open(self.encoded_text_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.show_preview_window("Encoded File Preview", content)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {str(e)}")
    
    def show_preview_window(self, title, content):
        """Show preview window with text content"""
        preview_window = tk.Toplevel(self)
        preview_window.title(title)
        preview_window.geometry("600x400")
        preview_window.configure(bg=self.COLORS['bg'])
        
        # Title
        tk.Label(
            preview_window,
            text=title,
            font=("Courier New", 14, "bold"),
            fg=self.COLORS['primary'],
            bg=self.COLORS['bg']
        ).pack(pady=(10, 5))
        
        # Text widget with scrollbars
        text_frame = tk.Frame(preview_window, bg=self.COLORS['bg'])
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        text_widget = tk.Text(
            text_frame,
            font=("Consolas", 10),
            fg=self.COLORS['text'],
            bg="#0f151f",
            wrap="word"
        )
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")
        
        # Add scrollbars
        y_scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
        y_scrollbar.pack(side="right", fill="y")
        text_widget.config(yscrollcommand=y_scrollbar.set)
        
        x_scrollbar = tk.Scrollbar(text_frame, orient="horizontal", command=text_widget.xview)
        x_scrollbar.pack(side="bottom", fill="x")
        text_widget.config(xscrollcommand=x_scrollbar.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        
        # Character count
        char_count = len(content)
        line_count = len(content.splitlines())
        tk.Label(
            preview_window,
            text=f"Characters: {char_count} | Lines: {line_count}",
            font=("Segoe UI", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['bg']
        ).pack(pady=(5, 10))
        
        # Close button
        tk.Button(
            preview_window,
            text="Close",
            font=("Segoe UI", 10),
            fg=self.COLORS['bg'],
            bg=self.COLORS['accent'],
            command=preview_window.destroy
        ).pack(pady=(0, 10))
    
    # ===== PASSWORD METHODS =====
    
    def toggle_hide_password(self):
        """Toggle hide password visibility"""
        self.hide_password_show = not self.hide_password_show
        self.hide_password.config(show="" if self.hide_password_show else "•")
    
    def toggle_extract_password(self):
        """Toggle extract password visibility"""
        self.extract_password_show = not self.extract_password_show
        self.extract_password.config(show="" if self.extract_password_show else "•")
    
    def copy_password_from_hide(self):
        """Copy password from hide section to extract section"""
        password = self.hide_password.get()
        if password:
            self.extract_password.delete(0, tk.END)
            self.extract_password.insert(0, password)
            self.update_status("Password copied to extract field", "info")
    
    def generate_random_password(self):
        """Generate a random password"""
        import random
        import string
        
        # Generate 16-character random password
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(16))
        
        self.hide_password.delete(0, tk.END)
        self.hide_password.insert(0, password)
        self.update_status("Random password generated", "info")
    
    # ===== COUNTER METHODS =====
    
    def update_hide_counter(self, event=None):
        """Update hide section character counter"""
        text = self.secret_text.get("1.0", "end-1c").strip()
        count = len(text)
        self.hide_char_count.config(text=f"Characters: {count}")
        
        # Change color based on capacity
        capacity = self.calculate_capacity()
        if capacity > 0:
            if count > capacity:
                self.hide_char_count.config(fg=self.COLORS['accent'])
                self.hide_char_count.config(text=f"Characters: {count} (Exceeds capacity: {capacity})")
            elif count > capacity * 0.8:
                self.hide_char_count.config(fg="#ffaa00")
                self.hide_char_count.config(text=f"Characters: {count} ({capacity} available)")
            else:
                self.hide_char_count.config(fg="#666666")
    
    def calculate_capacity(self):
        """Calculate capacity based on method and source file"""
        if not self.source_text_file_path:
            return 0
        
        try:
            with open(self.source_text_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            method = self.method_var.get()
            
            if method == "Whitespace":
                # Each line can hold 1 bit
                lines = content.splitlines()
                capacity = len(lines) // 8  # 8 bits per character
                return capacity
            else:  # ZeroWidth
                # Can insert after every character
                char_count = len(content)
                capacity = char_count // 8
                return capacity
                
        except Exception as e:
            print(f"Error calculating capacity: {e}")
            return 0
    
    def update_result_counter(self, method="Unknown"):
        """Update result section character counter"""
        self.result_text.config(state="normal")
        text = self.result_text.get("1.0", "end-1c").strip()
        self.result_text.config(state="disabled")
        
        count = len(text)
        if text.startswith("Error:"):
            self.result_char_count.config(text="Error in extraction", fg=self.COLORS['accent'])
            self.result_method_label.config(text="Method: Failed")
        else:
            self.result_char_count.config(text=f"Characters: {count}", fg="#666666")
            self.result_method_label.config(text=f"Method: {method}")
    
    # ===== CRYPTOGRAPHY METHODS =====
    
    def generate_key(self, password: str) -> bytes:
        """Generate a Fernet key from a password"""
        # Use SHA256 to create consistent 32-byte key
        password_bytes = password.encode('utf-8')
        # Hash the password to get 32 bytes
        hashed = hashlib.sha256(password_bytes).digest()
        # Convert to base64 url-safe
        key = base64.urlsafe_b64encode(hashed)
        return key
    
    def encrypt_message(self, message: str, password: str) -> str:
        """Encrypt message using Fernet"""
        try:
            key = self.generate_key(password)
            f = Fernet(key)
            token = f.encrypt(message.encode('utf-8'))
            return token.decode('utf-8')
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")
    
    def decrypt_message(self, token: str, password: str) -> str:
        """Decrypt message using Fernet"""
        try:
            key = self.generate_key(password)
            f = Fernet(key)
            message = f.decrypt(token.encode('utf-8'))
            return message.decode('utf-8')
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")
    
    # ===== STEGANOGRAPHY METHODS =====
    
    def whitespace_encode(self, text, secret_message):
        """
        Hide secret message using spaces and tabs at the end of each line.
        Space = 0, Tab = 1
        """
        # Convert message → binary
        binary = ''.join(format(ord(c), '08b') for c in secret_message)

        # Add end marker
        binary += "1111111111111110"  # FE marker

        # Split text into lines
        lines = text.split("\n")

        # Need enough lines to hide bits
        if len(binary) > len(lines):
            raise ValueError("Text file is too small to hide this message!")

        encoded_lines = []

        for i, line in enumerate(lines):
            if i < len(binary):
                bit = binary[i]
                if bit == "0":
                    line += " "   # space
                else:
                    line += "\t"  # tab
            encoded_lines.append(line)

        return "\n".join(encoded_lines)
    
    def whitespace_decode(self, text):
        """
        Extract secret message from whitespace at end of each line.
        Space = 0, Tab = 1
        """
        lines = text.split("\n")
        binary = ""

        for line in lines:
            if line.endswith("\t"):
                binary += "1"
            elif line.endswith(" "):
                binary += "0"
            # else: no hidden bit in this line

        # Convert binary → text
        message = ""
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) != 8:
                break

            char = chr(int(byte, 2))
            message += char

            # Check for FE marker
            if message.endswith("\xfe"):
                return message[:-2]

        return message
    
    def zero_width_encode(self, text, secret_message):
        """
        Hide secret message using zero-width Unicode characters.
        U+200B = 0, U+200C = 1
        """
        # Convert message → binary
        binary = ''.join(format(ord(c), '08b') for c in secret_message)
        
        # Add end marker
        binary += "1111111111111110"  # FE marker
        
        # Need enough characters to hide bits
        if len(binary) > len(text):
            raise ValueError("Text file is too small to hide this message!")
        
        result = []
        char_index = 0
        
        for char in text:
            result.append(char)
            
            # Insert zero-width character after this character
            if char_index < len(binary):
                bit = binary[char_index]
                if bit == "0":
                    result.append("\u200b")  # Zero Width Space
                else:
                    result.append("\u200c")  # Zero Width Non-Joiner
                char_index += 1
        
        return ''.join(result)
    
    def zero_width_decode(self, text):
        """
        Extract secret message from zero-width characters.
        U+200B = 0, U+200C = 1
        """
        binary = ""
        
        # Find all zero-width characters
        for char in text:
            if char == "\u200b":  # Zero Width Space
                binary += "0"
            elif char == "\u200c":  # Zero Width Non-Joiner
                binary += "1"
            elif char in ["\u200d", "\ufeff", "\u180e"]:  # Other zero-width chars
                continue
        
        # Convert binary → text
        message = ""
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) != 8:
                break

            char = chr(int(byte, 2))
            message += char

            # Check for FE marker
            if message.endswith("\xfe"):
                return message[:-2]

        return message
    
    # ===== MAIN FUNCTIONS =====
    
    def encode_message(self):
        """Encode (hide) message in text file"""
        try:
            # Get inputs
            source_file = self.source_entry.get()
            output_file = self.output_entry.get()
            secret_text = self.secret_text.get("1.0", "end-1c").strip()
            password = self.hide_password.get()
            method = self.method_var.get()
            
            # Validate inputs
            validation_errors = []
            
            if not source_file or "Select source text file" in source_file:
                validation_errors.append("Please select a source text file.")
            
            if not output_file or "Save encoded text file" in output_file:
                validation_errors.append("Please specify output text file path.")
            
            if not secret_text:
                validation_errors.append("Please enter a secret message.")
            
            if not password:
                validation_errors.append("Encryption key is required.")
            
            if validation_errors:
                messagebox.showwarning("Input Error", "\n".join(validation_errors))
                return
            
            # Check capacity
            capacity = self.calculate_capacity()
            if len(secret_text) > capacity:
                messagebox.showwarning(
                    "Capacity Warning",
                    f"Text file too small for message.\n\n"
                    f"File capacity: {capacity} characters\n"
                    f"Message length: {len(secret_text)} characters\n\n"
                    f"Suggestions:\n"
                    f"• Use a larger text file\n"
                    f"• Shorten your message\n"
                    f"• Try the Zero-Width method for higher capacity"
                )
                return
            
            # Read source file
            with open(source_file, 'r', encoding='utf-8') as f:
                source_text = f.read()
            
            # Encrypt message
            encrypted_message = self.encrypt_message(secret_text, password)
            
            # Encode based on method
            if method == "Whitespace":
                encoded_text = self.whitespace_encode(source_text, encrypted_message)
            else:  # ZeroWidth
                encoded_text = self.zero_width_encode(source_text, encrypted_message)
            
            # Write output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(encoded_text)
            
            # Show success
            file_size = os.path.getsize(output_file) / 1024  # KB
            messagebox.showinfo(
                "Success",
                f"✅ Message encoded successfully!\n\n"
                f"• Method: {method}\n"
                f"• Output: {os.path.basename(output_file)}\n"
                f"• Size: {file_size:.1f} KB\n"
                f"• Message length: {len(secret_text)} characters\n\n"
                f"⚠️ Remember your encryption key for extraction!"
            )
            
            # Auto-fill encoded file field
            self.encoded_entry.delete(0, tk.END)
            self.encoded_entry.insert(0, output_file)
            self.encoded_entry.config(fg=self.COLORS['text'])
            
            # Auto-fill extract password
            self.extract_password.delete(0, tk.END)
            self.extract_password.insert(0, password)
            
            self.update_status(f"Message encoded with {method} method", "success")
            
        except ValueError as e:
            messagebox.showerror("Capacity Error", str(e))
            self.update_status("Encoding failed - capacity exceeded", "error")
        except Exception as e:
            messagebox.showerror("Encoding Error", f"An error occurred:\n\n{str(e)}")
            self.update_status("Encoding failed", "error")
    
    def decode_message(self):
        """Decode (extract) message from text file"""
        try:
            # Get inputs
            encoded_file = self.encoded_entry.get()
            password = self.extract_password.get()
            decode_method = self.decode_method_var.get()
            
            # Validate inputs
            if not encoded_file or "Select encoded text file" in encoded_file:
                messagebox.showwarning("Input Error", "Please select an encoded text file.")
                return
            
            if not password:
                messagebox.showwarning("Security Error", "Decryption key is required.")
                return
            
            # Read encoded file
            with open(encoded_file, 'r', encoding='utf-8') as f:
                encoded_text = f.read()
            
            extracted_encrypted = ""
            method_used = "Unknown"
            
            # Determine decoding method
            if decode_method == "Auto Detect":
                # Try to detect which method was used
                # Check for zero-width characters
                if "\u200b" in encoded_text or "\u200c" in encoded_text:
                    try:
                        extracted_encrypted = self.zero_width_decode(encoded_text)
                        method_used = "ZeroWidth"
                    except:
                        pass
                
                # If zero-width failed or not found, try whitespace
                if not extracted_encrypted:
                    try:
                        extracted_encrypted = self.whitespace_decode(encoded_text)
                        method_used = "Whitespace"
                    except:
                        pass
            elif decode_method == "Whitespace":
                extracted_encrypted = self.whitespace_decode(encoded_text)
                method_used = "Whitespace"
            else:  # ZeroWidth
                extracted_encrypted = self.zero_width_decode(encoded_text)
                method_used = "ZeroWidth"
            
            if not extracted_encrypted:
                raise Exception("Could not extract encrypted message. File may not contain hidden data.")
            
            # Decrypt the message
            decrypted_text = self.decrypt_message(extracted_encrypted, password)
            
            # Display result
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", decrypted_text)
            self.result_text.config(state="disabled")
            
            # Update counter and method info
            self.update_result_counter(method_used)
            
            # Update status
            self.update_status(f"Message extracted ({len(decrypted_text)} chars) using {method_used}", "success")
            
        except Exception as e:
            error_msg = str(e)
            
            # Display error in result area
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", f"Error: {error_msg}")
            self.result_text.config(state="disabled")
            
            # Update counter
            self.update_result_counter("Failed")
            
            # Show appropriate error message
            if "password" in error_msg.lower() or "decrypt" in error_msg.lower():
                messagebox.showerror("Decryption Error", "Incorrect decryption key!")
            elif "capacity" in error_msg.lower():
                messagebox.showerror("Capacity Error", error_msg)
            else:
                messagebox.showerror("Decoding Error", f"Failed to decode message:\n\n{error_msg}")
            
            self.update_status("Decoding failed", "error")
    
    # ===== UTILITY FUNCTIONS =====
    
    def copy_result_to_clipboard(self):
        """Copy extracted message to clipboard"""
        self.result_text.config(state="normal")
        text = self.result_text.get("1.0", "end-1c").strip()
        self.result_text.config(state="disabled")
        
        if text and not text.startswith("Error:"):
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update_status("Copied to clipboard", "success")
        elif text.startswith("Error:"):
            messagebox.showwarning("Cannot Copy", "Cannot copy error message.")
    
    def save_extracted_message(self):
        """Save extracted message to file"""
        self.result_text.config(state="normal")
        text = self.result_text.get("1.0", "end-1c").strip()
        self.result_text.config(state="disabled")
        
        if text and not text.startswith("Error:"):
            file_path = filedialog.asksaveasfilename(
                title="Save Extracted Message",
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(text)
                    self.update_status(f"Message saved to {os.path.basename(file_path)}", "success")
                except Exception as e:
                    messagebox.showerror("Save Error", f"Failed to save file:\n{str(e)}")
        elif text.startswith("Error:"):
            messagebox.showwarning("Cannot Save", "Cannot save error message.")
    
    def clear_extract_section(self):
        """Clear only extract section fields"""
        self.encoded_entry.delete(0, tk.END)
        self.encoded_entry.insert(0, "Select encoded text file...")
        self.encoded_entry.config(fg="#666666")
        
        self.extract_password.delete(0, tk.END)
        
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")
        
        self.result_char_count.config(text="Characters: 0", fg="#666666")
        self.result_method_label.config(text="Method: Unknown")
        
        self.encoded_text_file_path = ""
        
        self.update_status("Extract section cleared", "info")
    
    def clear_all_fields(self):
        """Clear all fields in both sections"""
        # Clear hide section
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, "Select source text file...")
        self.source_entry.config(fg="#666666")
        
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, "Save encoded text file...")
        self.output_entry.config(fg="#666666")
        
        self.hide_password.delete(0, tk.END)
        
        self.secret_text.delete("1.0", tk.END)
        self.hide_char_count.config(text="Characters: 0", fg="#666666")
        
        # Clear extract section
        self.clear_extract_section()
        
        # Reset state variables
        self.source_text_file_path = ""
        self.output_text_file_path = ""
        
        # Reset method selections
        self.method_var.set("Whitespace")
        self.decode_method_var.set("Auto Detect")
        
        # Update method info
        self.on_method_change()
        
        self.update_status("All fields cleared", "info")
    
    def update_status(self, message, status_type="info"):
        """Update status label"""
        colors = {
            "info": self.COLORS['secondary'],
            "success": self.COLORS['primary'],
            "error": self.COLORS['accent'],
            "warning": "#ffaa00"
        }
        
        color = colors.get(status_type, self.COLORS['secondary'])
        self.status_label.config(text=message, fg=color)