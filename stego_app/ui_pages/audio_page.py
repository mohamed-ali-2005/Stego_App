import tkinter as tk
from tkinter import filedialog, messagebox
import os
import struct
import wave
import numpy as np
import base64
from cryptography.fernet import Fernet
import hashlib
import random

class AudioPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Get colors from controller
        self.COLORS = controller.COLORS
        
        # State variables
        self.source_audio_path = ""
        self.output_audio_path = ""
        self.encoded_audio_path = ""
        
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
            text="🎵 ADVANCED AUDIO STEGANOGRAPHY",
            font=("Courier New", 22, "bold"),
            fg=self.COLORS['primary'],
            bg=self.COLORS['bg']
        )
        title_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Hide & Extract Messages in WAV Audio Files | LSB & Chunk Injection Methods",
            font=("Segoe UI", 11),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['bg']
        )
        subtitle_label.pack()
        
        # Method info
        method_info = tk.Label(
            header_frame,
            text="📌 LSB: Sample-based hiding | 📌 Chunk: WAV metadata injection",
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
        # ===== SOURCE AUDIO SELECTION =====
        tk.Label(
            parent,
            text="Source WAV Audio:",
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
        self.source_entry.insert(0, "Select source WAV audio...")
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
            command=self.select_source_audio
        ).pack(side="right")
        
        # Audio info button
        tk.Button(
            source_frame,
            text="ℹ️",
            font=("Arial", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=3,
            command=self.show_audio_info
        ).pack(side="right", padx=(0, 5))
        
        # ===== OUTPUT AUDIO SELECTION =====
        tk.Label(
            parent,
            text="Output WAV Audio:",
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
        self.output_entry.insert(0, "Save encoded audio as WAV...")
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
            command=self.select_output_audio
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
        
        self.method_var = tk.StringVar(value="LSB")
        
        method_subframe = tk.Frame(method_frame, bg=self.COLORS['card_bg'])
        method_subframe.pack(fill="x", pady=(0, 10))
        
        methods = [
            ("LSB (Sample-based Hiding)", "LSB"),
            ("Chunk Injection (WAV Metadata)", "Chunk")
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
            text="1 LSB bit per audio sample",
            font=("Segoe UI", 9, "italic"),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg']
        )
        self.method_info_label.pack(anchor="w", pady=(0, 10))
        
        # ===== PASSWORD FIELD =====
        tk.Label(
            parent,
            text="Encryption Key:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
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
            text="🔑",
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
        
        # Initialize method display
        self.on_method_change()
    
    def setup_extract_section(self, parent):
        """Setup right column - Extract section"""
        # ===== ENCODED AUDIO SELECTION =====
        tk.Label(
            parent,
            text="Encoded WAV Audio:",
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
        self.encoded_entry.insert(0, "Select encoded WAV audio...")
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
            command=self.select_encoded_audio
        ).pack(side="right")
        
        # Audio info button
        tk.Button(
            encoded_frame,
            text="ℹ️",
            font=("Arial", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=3,
            command=self.show_encoded_audio_info
        ).pack(side="right", padx=(0, 5))
        
        # ===== DECODING METHOD SELECTION =====
        tk.Label(
            parent,
            text="Decoding Method:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        self.decode_method_var = tk.StringVar(value="Auto")
        
        decode_method_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        decode_method_frame.pack(fill="x", pady=(0, 10))
        
        decode_methods = [
            ("Auto Detect (Recommended)", "Auto"),
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
            text="🔧 LSB: 1-bit per sample | 🔧 Chunk: WAV metadata injection",
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
        if self.source_entry.get() == "Select source WAV audio...":
            self.source_entry.delete(0, tk.END)
            self.source_entry.config(fg=self.COLORS['text'])
    
    def on_source_focus_out(self, event=None):
        """Handle source entry focus out"""
        if self.source_entry.get() == "":
            self.source_entry.insert(0, "Select source WAV audio...")
            self.source_entry.config(fg="#666666")
    
    def on_output_focus_in(self, event=None):
        """Handle output entry focus in"""
        if self.output_entry.get() == "Save encoded audio as WAV...":
            self.output_entry.delete(0, tk.END)
            self.output_entry.config(fg=self.COLORS['text'])
    
    def on_output_focus_out(self, event=None):
        """Handle output entry focus out"""
        if self.output_entry.get() == "":
            self.output_entry.insert(0, "Save encoded audio as WAV...")
            self.output_entry.config(fg="#666666")
    
    def on_encoded_focus_in(self, event=None):
        """Handle encoded entry focus in"""
        if self.encoded_entry.get() == "Select encoded WAV audio...":
            self.encoded_entry.delete(0, tk.END)
            self.encoded_entry.config(fg=self.COLORS['text'])
    
    def on_encoded_focus_out(self, event=None):
        """Handle encoded entry focus out"""
        if self.encoded_entry.get() == "":
            self.encoded_entry.insert(0, "Select encoded WAV audio...")
            self.encoded_entry.config(fg="#666666")
    
    def on_method_change(self):
        """Show/Hide LSB info based on selected method"""
        method = self.method_var.get()
        if method == "LSB":
            self.method_info_label.config(text="1 LSB bit per audio sample")
        else:  # Chunk
            self.method_info_label.config(text="Custom chunk in WAV metadata")
    
    # ===== FILE SELECTION METHODS =====
    
    def select_source_audio(self):
        """Select source audio (WAV only)"""
        file_path = filedialog.askopenfilename(
            title="Select Source WAV Audio",
            filetypes=[
                ("WAV Audio Files", "*.wav"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            # Check if file is WAV
            if not file_path.lower().endswith('.wav'):
                messagebox.showwarning("Invalid Format", "Please select a WAV audio file.")
                return
            
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, file_path)
            self.source_entry.config(fg=self.COLORS['text'])
            self.source_audio_path = file_path
            self.update_status(f"Source selected: {os.path.basename(file_path)}")
            
            # Load and display audio info
            try:
                with wave.open(file_path, 'rb') as audio:
                    info = f"Channels: {audio.getnchannels()} | Sample Rate: {audio.getframerate()} Hz | Duration: {audio.getnframes()/audio.getframerate():.1f}s"
                    self.update_status(info, "info")
                    
                    # Calculate LSB capacity
                    total_samples = audio.getnframes() * audio.getnchannels()
                    capacity = total_samples // 8  # 1 bit per sample, 8 bits per byte
                    self.update_status(f"LSB capacity: ~{capacity} characters", "info")
            except Exception as e:
                self.update_status(f"Error loading audio: {str(e)}", "error")
    
    def select_output_audio(self):
        """Select output audio path (WAV only)"""
        file_path = filedialog.asksaveasfilename(
            title="Save Encoded WAV Audio As",
            defaultextension=".wav",
            filetypes=[
                ("WAV Audio Files", "*.wav"),
            ]
        )
        if file_path:
            # Ensure .wav extension
            if not file_path.lower().endswith('.wav'):
                file_path += '.wav'
            
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)
            self.output_entry.config(fg=self.COLORS['text'])
            self.output_audio_path = file_path
    
    def select_encoded_audio(self):
        """Select encoded audio for decoding (WAV only)"""
        file_path = filedialog.askopenfilename(
            title="Select Encoded WAV Audio",
            filetypes=[
                ("WAV Audio Files", "*.wav"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            # Check if file is WAV
            if not file_path.lower().endswith('.wav'):
                messagebox.showwarning("Invalid Format", "Please select a WAV audio file.")
                return
            
            self.encoded_entry.delete(0, tk.END)
            self.encoded_entry.insert(0, file_path)
            self.encoded_entry.config(fg=self.COLORS['text'])
            self.encoded_audio_path = file_path
            self.update_status(f"Encoded audio selected: {os.path.basename(file_path)}")
    
    def show_audio_info(self):
        """Show information about source audio"""
        if not self.source_audio_path:
            messagebox.showwarning("No Audio", "Please select a source WAV audio file first.")
            return
        
        try:
            with wave.open(self.source_audio_path, 'rb') as audio:
                info = f"""
Audio Information:
• Channels: {audio.getnchannels()}
• Sample Width: {audio.getsampwidth()} bytes
• Frame Rate: {audio.getframerate()} Hz
• Frames: {audio.getnframes()}
• Duration: {audio.getnframes() / audio.getframerate():.2f} seconds
• Compression: {audio.getcompname()}
                """
                messagebox.showinfo("Audio Information", info.strip())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read audio file:\n{str(e)}")
    
    def show_encoded_audio_info(self):
        """Show information about encoded audio"""
        if not self.encoded_audio_path:
            messagebox.showwarning("No Audio", "Please select an encoded WAV audio file first.")
            return
        
        try:
            with wave.open(self.encoded_audio_path, 'rb') as audio:
                info = f"""
Audio Information:
• Channels: {audio.getnchannels()}
• Sample Width: {audio.getsampwidth()} bytes
• Frame Rate: {audio.getframerate()} Hz
• Frames: {audio.getnframes()}
• Duration: {audio.getnframes() / audio.getframerate():.2f} seconds
                """
                messagebox.showinfo("Audio Information", info.strip())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read audio file:\n{str(e)}")
    
    # ===== PASSWORD METHODS =====
    
    def toggle_hide_password(self):
        """Toggle hide password visibility"""
        self.hide_password_show = not self.hide_password_show
        self.hide_password.config(show="" if self.hide_password_show else "•")
    
    def toggle_extract_password(self):
        """Toggle extract password visibility"""
        self.extract_password_show = not self.extract_password_show
        self.extract_password.config(show="" if self.extract_password_show else "•")
    
    def generate_random_password(self):
        """Generate random password"""
        import secrets
        import string
        
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(chars) for _ in range(16))
        self.hide_password.delete(0, tk.END)
        self.hide_password.insert(0, password)
        self.update_status("Random password generated", "info")
    
    def copy_password_from_hide(self):
        """Copy password from hide section to extract section"""
        password = self.hide_password.get()
        if password:
            self.extract_password.delete(0, tk.END)
            self.extract_password.insert(0, password)
            self.update_status("Password copied to extract field", "info")
    
    # ===== COUNTER METHODS =====
    
    def update_hide_counter(self, event=None):
        """Update hide section character counter"""
        text = self.secret_text.get("1.0", "end-1c")
        count = len(text)
        self.hide_char_count.config(text=f"Characters: {count}")
        
        # Change color based on length
        method = self.method_var.get()
        if method == "LSB" and self.source_audio_path:
            max_chars = self.calculate_lsb_capacity()
            if count > max_chars:
                self.hide_char_count.config(fg=self.COLORS['accent'])
                self.hide_char_count.config(text=f"Characters: {count} (Exceeds capacity: {max_chars})")
            elif count > max_chars * 0.8:
                self.hide_char_count.config(fg="#ffaa00")
            else:
                self.hide_char_count.config(fg="#666666")
        else:  # Chunk
            if count > 5000:
                self.hide_char_count.config(fg=self.COLORS['accent'])
            elif count > 2000:
                self.hide_char_count.config(fg="#ffaa00")
            else:
                self.hide_char_count.config(fg="#666666")
    
    def calculate_lsb_capacity(self):
        """Calculate LSB capacity for current audio"""
        if not self.source_audio_path:
            return 0
        
        try:
            with wave.open(self.source_audio_path, 'rb') as audio:
                total_samples = audio.getnframes() * audio.getnchannels()
                
                # Total bits available (1 bit per sample)
                total_bits = total_samples
                # Convert to characters (8 bits per char)
                # Account for ###END### marker (8*8 = 64 bits)
                max_chars = (total_bits - 64) // 8
                
                return max_chars
        except:
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
        password_bytes = password.encode('utf-8')
        hashed = hashlib.sha256(password_bytes).digest()
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
    
    # ===== LSB STEGANOGRAPHY METHODS =====
    
    def lsb_encode(self, audio_path, message):
        """LSB encoding method for WAV audio"""
        try:
            # Read audio file
            with wave.open(audio_path, 'rb') as audio:
                params = audio.getparams()
                frames = audio.readframes(audio.getnframes())
            
            # Encrypt the message
            password = self.hide_password.get()
            encrypted_message = self.encrypt_message(message, password) + "###END###"
            
            # Convert to binary
            binary_message = ''.join(format(ord(c), '08b') for c in encrypted_message)
            
            # Convert audio frames to numpy array
            if params.sampwidth == 2:  # 16-bit
                audio_data = np.frombuffer(frames, dtype=np.int16)
            elif params.sampwidth == 1:  # 8-bit
                audio_data = np.frombuffer(frames, dtype=np.uint8)
            else:
                raise ValueError(f"Unsupported sample width: {params.sampwidth}")
            
            # Check capacity
            if len(binary_message) > len(audio_data):
                raise ValueError(f"Message too long! Capacity: {len(audio_data)//8} chars, Needed: {len(binary_message)//8} chars")
            
            # Apply LSB encoding
            encoded_audio = audio_data.copy()
            for i in range(len(binary_message)):
                encoded_audio[i] = (audio_data[i] & ~1) | int(binary_message[i])
            
            # Convert back to bytes
            if params.sampwidth == 2:
                encoded_frames = encoded_audio.astype(np.int16).tobytes()
            else:
                encoded_frames = encoded_audio.astype(np.uint8).tobytes()
            
            return encoded_frames, params
            
        except Exception as e:
            raise Exception(f"LSB encoding failed: {str(e)}")
    
    def lsb_decode(self, audio_path):
        """LSB decoding method for WAV audio"""
        try:
            # Read audio file
            with wave.open(audio_path, 'rb') as audio:
                params = audio.getparams()
                frames = audio.readframes(audio.getnframes())
            
            # Convert audio frames to numpy array
            if params.sampwidth == 2:
                audio_data = np.frombuffer(frames, dtype=np.int16)
            elif params.sampwidth == 1:
                audio_data = np.frombuffer(frames, dtype=np.uint8)
            else:
                raise ValueError(f"Unsupported sample width: {params.sampwidth}")
            
            # Extract LSB bits
            binary_message = ""
            for sample in audio_data:
                binary_message += str(sample & 1)
            
            # Convert binary to string
            chars = []
            for i in range(0, len(binary_message), 8):
                byte = binary_message[i:i+8]
                if len(byte) < 8:
                    break
                chars.append(chr(int(byte, 2)))
                if ''.join(chars[-8:]).endswith("###END###"):
                    break
            
            encrypted_message = ''.join(chars).replace("###END###", "")
            return encrypted_message
            
        except Exception as e:
            raise Exception(f"LSB decoding failed: {str(e)}")
    
    # ===== CHUNK INJECTION METHODS =====
    
    def chunk_encode(self, audio_path, message):
        """Chunk injection encoding method"""
        try:
            # Read the entire audio file
            with open(audio_path, 'rb') as f:
                audio_data = f.read()
            
            # Encrypt the message
            password = self.hide_password.get()
            encrypted_message = self.encrypt_message(message, password)
            
            # Create custom chunk
            chunk_id = b"steg"  # Custom chunk ID
            message_bytes = encrypted_message.encode('utf-8')
            chunk_size = struct.pack("<I", len(message_bytes))
            
            # Append chunk to audio data
            encoded_data = audio_data + chunk_id + chunk_size + message_bytes
            
            return encoded_data
            
        except Exception as e:
            raise Exception(f"Chunk encoding failed: {str(e)}")
    
    def chunk_decode(self, audio_path):
        """Chunk injection decoding method"""
        try:
            # Read the entire audio file
            with open(audio_path, 'rb') as f:
                data = f.read()
            
            # Look for our custom chunk
            chunk_id = b"steg"
            index = data.rfind(chunk_id)
            
            if index == -1:
                raise Exception("No steganography chunk found")
            
            # Extract chunk size
            chunk_size = struct.unpack("<I", data[index+4:index+8])[0]
            
            # Extract message
            message_start = index + 8
            message_end = message_start + chunk_size
            encrypted_message = data[message_start:message_end].decode('utf-8')
            
            return encrypted_message
            
        except Exception as e:
            raise Exception(f"Chunk decoding failed: {str(e)}")
    
    # ===== MAIN FUNCTIONS =====
    
    def encode_message(self):
        """Encode (hide) message in audio"""
        try:
            # Get inputs
            source_file = self.source_entry.get()
            output_file = self.output_entry.get()
            secret_text = self.secret_text.get("1.0", "end-1c").strip()
            password = self.hide_password.get()
            method = self.method_var.get()
            
            # Validate inputs
            validation_errors = []
            
            if not source_file or "Select source WAV audio" in source_file:
                validation_errors.append("Please select a source WAV audio.")
            
            if not output_file or "Save encoded audio as WAV" in output_file:
                validation_errors.append("Please specify output WAV file path.")
            
            if not secret_text:
                validation_errors.append("Please enter a secret message.")
            
            if not password:
                validation_errors.append("Encryption key is required.")
            
            # Check file extension
            if source_file and not source_file.lower().endswith('.wav'):
                validation_errors.append("Source file must be a WAV audio.")
            
            if output_file and not output_file.lower().endswith('.wav'):
                output_file += '.wav'
                self.output_entry.delete(0, tk.END)
                self.output_entry.insert(0, output_file)
            
            if validation_errors:
                messagebox.showwarning("Input Error", "\n".join(validation_errors))
                return
            
            # Check audio size for LSB
            if method == "LSB":
                capacity = self.calculate_lsb_capacity()
                if len(secret_text) > capacity:
                    messagebox.showwarning(
                        "Capacity Warning",
                        f"Audio too short for message with LSB.\n\n"
                        f"Audio capacity: {capacity} characters\n"
                        f"Message length: {len(secret_text)} characters\n\n"
                        f"Suggestions:\n"
                        f"• Use Chunk method instead\n"
                        f"• Use a longer audio file\n"
                        f"• Shorten your message"
                    )
                    return
            
            # Encode based on method
            if method == "LSB":
                encoded_frames, params = self.lsb_encode(source_file, secret_text)
                
                # Save encoded audio
                with wave.open(output_file, 'wb') as output_audio:
                    output_audio.setparams(params)
                    output_audio.writeframes(encoded_frames)
            else:  # Chunk
                encoded_data = self.chunk_encode(source_file, secret_text)
                
                # Save with chunk
                with open(output_file, 'wb') as f:
                    f.write(encoded_data)
            
            # Show success
            audio_size = os.path.getsize(output_file) / 1024  # KB
            messagebox.showinfo(
                "Success",
                f"✅ Message encoded successfully!\n\n"
                f"• Method: {method}\n"
                f"• Output: {os.path.basename(output_file)}\n"
                f"• Size: {audio_size:.1f} KB\n"
                f"• Message length: {len(secret_text)} characters\n\n"
                f"⚠️ Remember your encryption key for extraction!"
            )
            
            # Auto-fill encoded audio field
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
        """Decode (extract) message from audio"""
        try:
            # Get inputs
            encoded_file = self.encoded_entry.get()
            password = self.extract_password.get()
            
            # Validate inputs
            if not encoded_file or "Select encoded WAV audio" in encoded_file:
                messagebox.showwarning("Input Error", "Please select an encoded WAV audio.")
                return
            
            if not password:
                messagebox.showwarning("Security Error", "Decryption key is required.")
                return
            
            # Check file extension
            if not encoded_file.lower().endswith('.wav'):
                messagebox.showwarning("Invalid Format", "Only WAV files are supported.")
                return
            
            extracted_encrypted = ""
            method_used = "Unknown"
            decoded_successfully = False
            
            # Try Chunk method first
            try:
                extracted_encrypted = self.chunk_decode(encoded_file)
                if extracted_encrypted:
                    method_used = "Chunk"
                    decoded_successfully = True
            except Exception as e:
                print(f"Chunk decode failed: {e}")
                pass
            
            # If chunk failed, try LSB method
            if not decoded_successfully:
                try:
                    extracted_encrypted = self.lsb_decode(encoded_file)
                    if extracted_encrypted:
                        method_used = "LSB"
                        decoded_successfully = True
                except Exception as e:
                    print(f"LSB decode failed: {e}")
                    pass
            
            if not decoded_successfully or not extracted_encrypted:
                raise Exception("Could not extract message. Audio may not contain hidden data.")
            
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
            elif "WAV" in error_msg:
                messagebox.showerror("Format Error", "Please use WAV format only.")
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
        self.encoded_entry.insert(0, "Select encoded WAV audio...")
        self.encoded_entry.config(fg="#666666")
        
        self.extract_password.delete(0, tk.END)
        
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")
        
        self.result_char_count.config(text="Characters: 0", fg="#666666")
        self.result_method_label.config(text="Method: Unknown")
        
        self.encoded_audio_path = ""
        
        self.update_status("Extract section cleared", "info")
    
    def clear_all_fields(self):
        """Clear all fields in both sections"""
        # Clear hide section
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, "Select source WAV audio...")
        self.source_entry.config(fg="#666666")
        
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, "Save encoded audio as WAV...")
        self.output_entry.config(fg="#666666")
        
        self.hide_password.delete(0, tk.END)
        
        self.secret_text.delete("1.0", tk.END)
        self.hide_char_count.config(text="Characters: 0", fg="#666666")
        
        # Clear extract section
        self.clear_extract_section()
        
        # Reset state variables
        self.source_audio_path = ""
        self.output_audio_path = ""
        
        # Reset method selections
        self.method_var.set("LSB")
        self.decode_method_var.set("Auto")
        
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