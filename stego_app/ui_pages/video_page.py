import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import struct
import json
import base64
from cryptography.fernet import Fernet
import hashlib
import cv2
import numpy as np
import time
import threading
import subprocess
from PIL import Image, ImageTk

class VideoPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Get colors from controller
        self.COLORS = controller.COLORS
        
        # State variables
        self.source_video_path = ""
        self.output_video_path = ""
        self.encoded_video_path = ""
        self.encoding_in_progress = False
        self.decoding_in_progress = False
        
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
            text="🎬 VIDEO STEGANOGRAPHY",
            font=("Courier New", 22, "bold"),
            fg=self.COLORS['primary'],
            bg=self.COLORS['bg']
        )
        title_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Hide & Extract Messages in Video Files | 3 Advanced Methods",
            font=("Segoe UI", 11),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['bg']
        )
        subtitle_label.pack()
        
        # Method info
        method_info = tk.Label(
            header_frame,
            text="🔧 LSB in Frames | 📋 Metadata | 📁 EOF Injection",
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
        # ===== SOURCE VIDEO SELECTION =====
        tk.Label(
            parent,
            text="Source Video:",
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
        self.source_entry.insert(0, "Select source video...")
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
            command=self.select_source_video
        ).pack(side="right")
        
        # Video info button
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
            command=self.show_video_info
        ).pack(side="right", padx=(0, 5))
        
        # ===== OUTPUT VIDEO SELECTION =====
        tk.Label(
            parent,
            text="Output Video:",
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
        self.output_entry.insert(0, "Save encoded video...")
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
            command=self.select_output_video
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
        
        # Create rows for radio buttons
        row1 = tk.Frame(method_subframe, bg=self.COLORS['card_bg'])
        row1.pack(fill="x", pady=(0, 5))
        row2 = tk.Frame(method_subframe, bg=self.COLORS['card_bg'])
        row2.pack(fill="x")
        
        methods = [
            ("LSB in Frames (High Capacity)", "LSB"),
            ("Metadata Hiding (Fast & Safe)", "Metadata"),
            ("EOF Injection (Stealth)", "EOF")
        ]
        
        # First two methods in row1
        rb1 = tk.Radiobutton(
            row1,
            text=methods[0][0],
            variable=self.method_var,
            value=methods[0][1],
            font=("Segoe UI", 9),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg'],
            activebackground=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            selectcolor=self.COLORS['bg'],
            cursor="hand2",
            command=self.on_method_change
        )
        rb1.pack(side="left", padx=(0, 20))
        
        rb2 = tk.Radiobutton(
            row1,
            text=methods[1][0],
            variable=self.method_var,
            value=methods[1][1],
            font=("Segoe UI", 9),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg'],
            activebackground=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            selectcolor=self.COLORS['bg'],
            cursor="hand2",
            command=self.on_method_change
        )
        rb2.pack(side="left")
        
        # Third method in row2
        rb3 = tk.Radiobutton(
            row2,
            text=methods[2][0],
            variable=self.method_var,
            value=methods[2][1],
            font=("Segoe UI", 9),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg'],
            activebackground=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            selectcolor=self.COLORS['bg'],
            cursor="hand2",
            command=self.on_method_change
        )
        rb3.pack(anchor="w")
        
        # Method info label
        self.method_info_label = tk.Label(
            method_frame,
            text="Hide message in LSB bits of video frames",
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
        # ===== ENCODED VIDEO SELECTION =====
        tk.Label(
            parent,
            text="Encoded Video:",
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
        self.encoded_entry.insert(0, "Select encoded video...")
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
            command=self.select_encoded_video
        ).pack(side="right")
        
        # Video info button
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
            command=self.show_encoded_video_info
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
        
        # Create rows for radio buttons
        decode_row1 = tk.Frame(decode_method_frame, bg=self.COLORS['card_bg'])
        decode_row1.pack(fill="x", pady=(0, 5))
        decode_row2 = tk.Frame(decode_method_frame, bg=self.COLORS['card_bg'])
        decode_row2.pack(fill="x")
        
        decode_methods = [
            ("Auto Detect (Recommended)", "Auto"),
            ("Force LSB Method", "LSB"),
            ("Force Metadata Method", "Metadata"),
            ("Force EOF Method", "EOF")
        ]
        
        # First two methods in decode_row1
        rb1 = tk.Radiobutton(
            decode_row1,
            text=decode_methods[0][0],
            variable=self.decode_method_var,
            value=decode_methods[0][1],
            font=("Segoe UI", 9),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg'],
            activebackground=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            selectcolor=self.COLORS['bg'],
            cursor="hand2"
        )
        rb1.pack(side="left", padx=(0, 20))
        
        rb2 = tk.Radiobutton(
            decode_row1,
            text=decode_methods[1][0],
            variable=self.decode_method_var,
            value=decode_methods[1][1],
            font=("Segoe UI", 9),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg'],
            activebackground=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            selectcolor=self.COLORS['bg'],
            cursor="hand2"
        )
        rb2.pack(side="left")
        
        # Next two methods in decode_row2
        rb3 = tk.Radiobutton(
            decode_row2,
            text=decode_methods[2][0],
            variable=self.decode_method_var,
            value=decode_methods[2][1],
            font=("Segoe UI", 9),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg'],
            activebackground=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            selectcolor=self.COLORS['bg'],
            cursor="hand2"
        )
        rb3.pack(side="left", padx=(0, 20))
        
        rb4 = tk.Radiobutton(
            decode_row2,
            text=decode_methods[3][0],
            variable=self.decode_method_var,
            value=decode_methods[3][1],
            font=("Segoe UI", 9),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg'],
            activebackground=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            selectcolor=self.COLORS['bg'],
            cursor="hand2"
        )
        rb4.pack(side="left")
        
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
        
        # Progress bar
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(
            footer_frame,
            variable=self.progress_var,
            maximum=100,
            length=150,
            mode='determinate'
        )
        self.progress_bar.pack(side="left", padx=10)
        
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
        if self.source_entry.get() == "Select source video...":
            self.source_entry.delete(0, tk.END)
            self.source_entry.config(fg=self.COLORS['text'])
    
    def on_source_focus_out(self, event=None):
        """Handle source entry focus out"""
        if self.source_entry.get() == "":
            self.source_entry.insert(0, "Select source video...")
            self.source_entry.config(fg="#666666")
    
    def on_output_focus_in(self, event=None):
        """Handle output entry focus in"""
        if self.output_entry.get() == "Save encoded video...":
            self.output_entry.delete(0, tk.END)
            self.output_entry.config(fg=self.COLORS['text'])
    
    def on_output_focus_out(self, event=None):
        """Handle output entry focus out"""
        if self.output_entry.get() == "":
            self.output_entry.insert(0, "Save encoded video...")
            self.output_entry.config(fg="#666666")
    
    def on_encoded_focus_in(self, event=None):
        """Handle encoded entry focus in"""
        if self.encoded_entry.get() == "Select encoded video...":
            self.encoded_entry.delete(0, tk.END)
            self.encoded_entry.config(fg=self.COLORS['text'])
    
    def on_encoded_focus_out(self, event=None):
        """Handle encoded entry focus out"""
        if self.encoded_entry.get() == "":
            self.encoded_entry.insert(0, "Select encoded video...")
            self.encoded_entry.config(fg="#666666")
    
    def on_method_change(self):
        """Show method info based on selected method"""
        method = self.method_var.get()
        if method == "LSB":
            self.method_info_label.config(text="Hide message in LSB bits of video frames")
        elif method == "Metadata":
            self.method_info_label.config(text="Hide message in video metadata")
        else:  # EOF
            self.method_info_label.config(text="Hide message at end of video file")
    
    # ===== FILE SELECTION METHODS =====
    
    def select_source_video(self):
        """Select source video file"""
        file_path = filedialog.askopenfilename(
            title="Select Source Video",
            filetypes=[
                ("Video Files", "*.mp4 *.avi *.mov *.mkv *.wmv"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, file_path)
            self.source_entry.config(fg=self.COLORS['text'])
            self.source_video_path = file_path
            self.update_status(f"Source: {os.path.basename(file_path)}")
    
    def select_output_video(self):
        """Select output video path"""
        file_path = filedialog.asksaveasfilename(
            title="Save Encoded Video As",
            defaultextension=".mp4",
            filetypes=[
                ("MP4 Video", "*.mp4"),
                ("AVI Video", "*.avi"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            if not file_path.lower().endswith('.mp4'):
                file_path += '.mp4'
            
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)
            self.output_entry.config(fg=self.COLORS['text'])
            self.output_video_path = file_path
    
    def select_encoded_video(self):
        """Select encoded video for decoding"""
        file_path = filedialog.askopenfilename(
            title="Select Encoded Video",
            filetypes=[
                ("Video Files", "*.mp4 *.avi *.mov *.mkv *.wmv"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.encoded_entry.delete(0, tk.END)
            self.encoded_entry.insert(0, file_path)
            self.encoded_entry.config(fg=self.COLORS['text'])
            self.encoded_video_path = file_path
            self.update_status(f"Encoded: {os.path.basename(file_path)}")
    
    def show_video_info(self):
        """Show video information"""
        if not self.source_video_path:
            messagebox.showwarning("No Video", "Please select a source video first.")
            return
        
        try:
            size = os.path.getsize(self.source_video_path) / (1024 * 1024)  # MB
            messagebox.showinfo("Video Information", 
                f"File: {os.path.basename(self.source_video_path)}\n"
                f"Size: {size:.2f} MB\n"
                f"Path: {self.source_video_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get video info:\n{str(e)}")
    
    def show_encoded_video_info(self):
        """Show encoded video information"""
        if not self.encoded_video_path:
            messagebox.showwarning("No Video", "Please select an encoded video first.")
            return
        
        self.show_video_info()
    
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
        password = ''.join(secrets.choice(chars) for _ in range(12))
        self.hide_password.delete(0, tk.END)
        self.hide_password.insert(0, password)
        self.update_status("Random password generated", "info")
    
    def copy_password_from_hide(self):
        """Copy password from hide section to extract section"""
        password = self.hide_password.get()
        if password:
            self.extract_password.delete(0, tk.END)
            self.extract_password.insert(0, password)
            self.update_status("Password copied", "info")
    
    # ===== COUNTER METHODS =====
    
    def update_hide_counter(self, event=None):
        """Update hide section character counter"""
        text = self.secret_text.get("1.0", "end-1c")
        count = len(text)
        self.hide_char_count.config(text=f"Characters: {count}")
        
        # Change color based on length
        method = self.method_var.get()
        if method == "LSB":
            # LSB has high capacity, warning at 5000 chars
            if count > 5000:
                self.hide_char_count.config(fg=self.COLORS['accent'])
            elif count > 2000:
                self.hide_char_count.config(fg="#ffaa00")
            else:
                self.hide_char_count.config(fg="#666666")
        else:
            # Metadata/EOF have lower capacity
            if count > 1000:
                self.hide_char_count.config(fg=self.COLORS['accent'])
            elif count > 500:
                self.hide_char_count.config(fg="#ffaa00")
            else:
                self.hide_char_count.config(fg="#666666")
    
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
    
    # ===== LSB METHOD =====
    
    def lsb_encode(self, video_path, message, output_path):
        """LSB encoding in video frames"""
        try:
            # Encrypt message
            password = self.hide_password.get()
            encrypted_message = self.encrypt_message(message, password)
            
            # Convert to binary with marker
            message_with_marker = encrypted_message + "###END###"
            binary_message = ''.join(format(ord(c), '08b') for c in message_with_marker)
            
            # Open video
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise Exception("Cannot open video file")
            
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            bit_index = 0
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if bit_index < len(binary_message):
                    # Encode bits in this frame
                    encoded_frame = self._lsb_encode_frame(frame, binary_message, bit_index)
                    frame_capacity = width * height * 3  # 3 channels
                    bit_index += frame_capacity
                else:
                    encoded_frame = frame
                
                out.write(encoded_frame)
                frame_count += 1
                
                # Update progress
                if frame_count % 10 == 0:
                    progress = min(100, (bit_index / len(binary_message)) * 100)
                    self.progress_var.set(int(progress))
                    self.update_status(f"Encoding frame {frame_count}/{total_frames} ({progress:.1f}%)", "info")
                
                if bit_index >= len(binary_message):
                    # Copy remaining frames
                    while True:
                        ret, remaining_frame = cap.read()
                        if not ret:
                            break
                        out.write(remaining_frame)
                    break
            
            cap.release()
            out.release()
            
            if bit_index < len(binary_message):
                raise ValueError(f"Video too short! Could only encode {bit_index//8} chars, needed {len(binary_message)//8}")
            
            # Preserve audio by merging with ffmpeg
            try:
                temp_audio = output_path + '_temp_audio.aac'
                final_output = output_path
                
                # Extract audio from original video
                subprocess.run([
                    'ffmpeg', '-i', video_path, '-vn', '-acodec', 'copy', temp_audio
                ], check=True, capture_output=True)
                
                # Merge video with audio
                temp_video = output_path + '_temp_video.mp4'
                os.rename(output_path, temp_video)
                
                subprocess.run([
                    'ffmpeg', '-i', temp_video, '-i', temp_audio, 
                    '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0', 
                    '-shortest', final_output
                ], check=True, capture_output=True)
                
                # Clean up temp files
                if os.path.exists(temp_video):
                    os.remove(temp_video)
                if os.path.exists(temp_audio):
                    os.remove(temp_audio)
                    
            except subprocess.CalledProcessError as e:
                # If ffmpeg fails, keep the video without audio
                self.update_status("Warning: Could not preserve audio (ffmpeg not found or failed)", "warning")
            except FileNotFoundError:
                self.update_status("Warning: ffmpeg not installed, video saved without audio", "warning")
            
            return True
            
        except Exception as e:
            raise Exception(f"LSB encoding failed: {str(e)}")
    
    def _lsb_encode_frame(self, frame, binary_message, start_index):
        """Encode bits in a single frame"""
        height, width, channels = frame.shape
        encoded_frame = frame.copy()
        
        bit_index = start_index
        
        for y in range(height):
            for x in range(width):
                for c in range(min(channels, 3)):  # RGB channels
                    if bit_index >= len(binary_message):
                        return encoded_frame
                    
                    # Get bit value
                    bit = int(binary_message[bit_index])
                    
                    # Modify LSB
                    encoded_frame[y, x, c] = (encoded_frame[y, x, c] & 0xFE) | bit
                    
                    bit_index += 1
        
        return encoded_frame
    
    def lsb_decode(self, video_path):
        """LSB decoding from video frames"""
        try:
            # Open video
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise Exception("Cannot open video file")
            
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            binary_message = ""
            frame_capacity = width * height * 3
            frame_count = 0
            max_frames = 1000  # Limit to prevent infinite processing
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Decode bits from frame
                frame_bits = self._lsb_decode_frame(frame)
                binary_message += frame_bits
                
                frame_count += 1
                
                # Safety check: limit processing to prevent hanging
                if frame_count > max_frames:
                    raise Exception(f"Processing limit reached ({max_frames} frames). Video may be too large or corrupted.")
                
                # Update progress
                if frame_count % 10 == 0:
                    progress = min(100, (len(binary_message) / (frame_capacity * 10)) * 100)
                    self.progress_var.set(int(progress))
                    self.update_status(f"Decoding frame {frame_count}/{total_frames} ({progress:.1f}%)", "info")
                
                # Check for end marker
                if "###END###" in self._binary_to_string(binary_message):
                    break
            
            cap.release()
            
            # Convert binary to string
            text = self._binary_to_string(binary_message)
            if "###END###" in text:
                encrypted_message = text.replace("###END###", "")
                return encrypted_message
            else:
                raise Exception("End marker not found")
            
        except Exception as e:
            raise Exception(f"LSB decoding failed: {str(e)}")
    
    def _lsb_decode_frame(self, frame):
        """Decode bits from a single frame using numpy for faster processing"""
        # Extract LSB from RGB channels only (first 3 channels)
        lsb_bits = frame[:, :, :3] & 1
        # Flatten and convert to string
        binary_message = ''.join(map(str, lsb_bits.flatten()))
        return binary_message
    
    def _binary_to_string(self, binary):
        """Convert binary string to text"""
        chars = []
        for i in range(0, len(binary), 8):
            if i + 8 > len(binary):
                break
            byte = binary[i:i+8]
            chars.append(chr(int(byte, 2)))
        return ''.join(chars)
    
    # ===== METADATA METHOD =====
    
    def metadata_encode(self, video_path, message, output_path):
        """Metadata encoding"""
        try:
            # Encrypt message
            password = self.hide_password.get()
            encrypted_message = self.encrypt_message(message, password)
            
            # Read original video
            with open(video_path, 'rb') as f:
                video_data = f.read()
            
            # Create metadata
            metadata = {
                'stego': 'true',
                'method': 'metadata',
                'message': encrypted_message
            }
            metadata_str = json.dumps(metadata)
            
            # Create marker and data
            marker = b'METASTEGO'
            metadata_bytes = metadata_str.encode('utf-8')
            metadata_len = struct.pack('<I', len(metadata_bytes))
            
            # Find a good place to insert (after major chunks)
            insert_pos = len(video_data) - 100  # Near end of file
            
            # Insert metadata
            encoded_data = (
                video_data[:insert_pos] +
                marker +
                metadata_len +
                metadata_bytes +
                video_data[insert_pos:]
            )
            
            # Write to output
            with open(output_path, 'wb') as f:
                f.write(encoded_data)
            
            return True
            
        except Exception as e:
            raise Exception(f"Metadata encoding failed: {str(e)}")
    
    def metadata_decode(self, video_path):
        """Metadata decoding"""
        try:
            # Read video file
            with open(video_path, 'rb') as f:
                data = f.read()
            
            # Look for metadata marker
            marker = b'METASTEGO'
            index = data.find(marker)
            
            if index == -1:
                raise Exception("No metadata marker found")
            
            # Read metadata length
            len_start = index + len(marker)
            metadata_len = struct.unpack('<I', data[len_start:len_start+4])[0]
            
            # Read metadata
            metadata_start = len_start + 4
            metadata_end = metadata_start + metadata_len
            
            if metadata_end > len(data):
                raise Exception("Invalid metadata length")
            
            metadata_bytes = data[metadata_start:metadata_end]
            metadata_str = metadata_bytes.decode('utf-8')
            metadata = json.loads(metadata_str)
            
            if metadata.get('stego') != 'true' or metadata.get('method') != 'metadata':
                raise Exception("Invalid metadata format")
            
            encrypted_message = metadata['message']
            return encrypted_message
            
        except Exception as e:
            raise Exception(f"Metadata decoding failed: {str(e)}")
    
    # ===== EOF METHOD =====
    
    def eof_encode(self, video_path, message, output_path):
        """EOF injection encoding"""
        try:
            # Encrypt message
            password = self.hide_password.get()
            encrypted_message = self.encrypt_message(message, password)
            
            # Read original video
            with open(video_path, 'rb') as f:
                video_data = f.read()
            
            # Create marker and data
            marker = b'EOFSTEGO'
            message_bytes = encrypted_message.encode('utf-8')
            message_len = struct.pack('<I', len(message_bytes))
            
            # Append to video (true EOF injection)
            encoded_data = video_data + marker + message_len + message_bytes
            
            # Write to output
            with open(output_path, 'wb') as f:
                f.write(encoded_data)
            
            return True
            
        except Exception as e:
            raise Exception(f"EOF encoding failed: {str(e)}")
    
    def eof_decode(self, video_path):
        """EOF injection decoding"""
        try:
            # Read video file
            with open(video_path, 'rb') as f:
                data = f.read()
            
            # Look for EOF marker at the end
            marker = b'EOFSTEGO'
            index = data.rfind(marker)
            
            if index == -1:
                raise Exception("No EOF marker found")
            
            # Read message length
            len_start = index + len(marker)
            message_len = struct.unpack('<I', data[len_start:len_start+4])[0]
            
            # Read message
            message_start = len_start + 4
            message_end = message_start + message_len
            
            if message_end != len(data):
                raise Exception("Invalid EOF data - not at actual end of file")
            
            encrypted_message = data[message_start:message_end].decode('utf-8')
            return encrypted_message
            
        except Exception as e:
            raise Exception(f"EOF decoding failed: {str(e)}")
    
    # ===== MAIN ENCODE/DECODE FUNCTIONS =====
    
    def encode_message(self):
        """Encode (hide) message in video"""
        if self.encoding_in_progress:
            return
            
        try:
            # Get inputs
            source_file = self.source_entry.get()
            output_file = self.output_entry.get()
            secret_text = self.secret_text.get("1.0", "end-1c").strip()
            password = self.hide_password.get()
            method = self.method_var.get()
            
            # Validate inputs
            validation_errors = []
            
            if not source_file or "Select source video" in source_file:
                validation_errors.append("Please select a source video.")
            
            if not output_file or "Save encoded video" in output_file:
                validation_errors.append("Please specify output video file path.")
            
            if not secret_text:
                validation_errors.append("Please enter a secret message.")
            
            if not password:
                validation_errors.append("Encryption key is required.")
            
            if validation_errors:
                messagebox.showwarning("Input Error", "\n".join(validation_errors))
                return
            
            # Check file existence
            if not os.path.exists(source_file):
                messagebox.showerror("Error", "Source video file does not exist.")
                return
            
            # Reset progress
            self.progress_var.set(0)
            self.encoding_in_progress = True
            self.update_status(f"Starting {method} encoding...", "info")
            
            # Start encoding in thread
            threading.Thread(target=self._encode_thread, 
                           args=(source_file, output_file, secret_text, password, method),
                           daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n\n{str(e)}")
            self.update_status("Encoding failed", "error")
            self.encoding_in_progress = False
    
    def _encode_thread(self, source_file, output_file, secret_text, password, method):
        """Encoding thread function"""
        try:
            # Encode based on method
            if method == "LSB":
                success = self.lsb_encode(source_file, secret_text, output_file)
            elif method == "Metadata":
                success = self.metadata_encode(source_file, secret_text, output_file)
            elif method == "EOF":
                success = self.eof_encode(source_file, secret_text, output_file)
            else:
                raise ValueError(f"Unknown method: {method}")
            
            if success:
                self.after(0, self._encode_success, output_file, password, method, len(secret_text))
            else:
                self.after(0, self._encode_failed)
                
        except Exception as e:
            self.after(0, self._encode_error, str(e))
    
    def _encode_success(self, output_file, password, method, msg_length):
        """Handle successful encoding"""
        self.encoding_in_progress = False
        self.progress_var.set(100)
        
        # Show success
        video_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        messagebox.showinfo(
            "Success",
            f"✅ Message encoded successfully!\n\n"
            f"• Method: {method}\n"
            f"• Output: {os.path.basename(output_file)}\n"
            f"• Size: {video_size:.1f} MB\n"
            f"• Message length: {msg_length} characters\n\n"
            f"⚠️ Remember your encryption key for extraction!"
        )
        
        # Auto-fill encoded video field
        self.encoded_entry.delete(0, tk.END)
        self.encoded_entry.insert(0, output_file)
        self.encoded_entry.config(fg=self.COLORS['text'])
        
        # Auto-fill extract password
        self.extract_password.delete(0, tk.END)
        self.extract_password.insert(0, password)
        
        self.update_status(f"Message encoded with {method} method", "success")
    
    def _encode_failed(self):
        """Handle encoding failure"""
        self.encoding_in_progress = False
        self.progress_var.set(0)
        self.update_status("Encoding failed", "error")
    
    def _encode_error(self, error_msg):
        """Handle encoding error"""
        self.encoding_in_progress = False
        self.progress_var.set(0)
        messagebox.showerror("Encoding Error", f"An error occurred:\n\n{error_msg}")
        self.update_status("Encoding failed", "error")
    
    def decode_message(self):
        """Decode (extract) message from video"""
        if self.decoding_in_progress:
            return
            
        try:
            # Get inputs
            encoded_file = self.encoded_entry.get()
            password = self.extract_password.get()
            
            # Validate inputs
            if not encoded_file or "Select encoded video" in encoded_file:
                messagebox.showwarning("Input Error", "Please select an encoded video.")
                return
            
            if not password:
                messagebox.showwarning("Security Error", "Decryption key is required.")
                return
            
            # Check file existence
            if not os.path.exists(encoded_file):
                messagebox.showerror("Error", "Encoded video file does not exist.")
                return
            
            # Reset progress
            self.progress_var.set(0)
            self.decoding_in_progress = True
            self.update_status("Starting decoding...", "info")
            
            # Start decoding in thread
            threading.Thread(target=self._decode_thread, 
                           args=(encoded_file, password),
                           daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n\n{str(e)}")
            self.update_status("Decoding failed", "error")
            self.decoding_in_progress = False
    
    def _decode_thread(self, encoded_file, password):
        """Decoding thread function"""
        try:
            extracted_encrypted = ""
            method_used = "Unknown"
            
            # Try different methods based on selection
            decode_method = self.decode_method_var.get()
            
            if decode_method == "Auto":
                # Try methods in order of reliability
                methods_to_try = [
                    ("EOF", self.eof_decode),
                    ("Metadata", self.metadata_decode),
                    ("LSB", self.lsb_decode)
                ]
                
                for method_name, decode_func in methods_to_try:
                    try:
                        self.update_status(f"Trying {method_name} method...", "info")
                        extracted_encrypted = decode_func(encoded_file)
                        if extracted_encrypted:
                            method_used = method_name
                            break
                    except Exception as e:
                        print(f"{method_name} decode failed: {e}")
                        continue
                
                if not extracted_encrypted:
                    raise Exception("Could not extract message with any method")
            
            elif decode_method == "LSB":
                extracted_encrypted = self.lsb_decode(encoded_file)
                method_used = "LSB"
            
            elif decode_method == "Metadata":
                extracted_encrypted = self.metadata_decode(encoded_file)
                method_used = "Metadata"
            
            elif decode_method == "EOF":
                extracted_encrypted = self.eof_decode(encoded_file)
                method_used = "EOF"
            
            # Decrypt the message
            decrypted_text = self.decrypt_message(extracted_encrypted, password)
            
            self.after(0, self._decode_success, decrypted_text, method_used)
            
        except Exception as e:
            self.after(0, self._decode_error, str(e))
    
    def _decode_success(self, decrypted_text, method_used):
        """Handle successful decoding"""
        self.decoding_in_progress = False
        self.progress_var.set(100)
        
        # Display result
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", decrypted_text)
        self.result_text.config(state="disabled")
        
        # Update counter and method info
        self.update_result_counter(method_used)
        
        # Update status
        self.update_status(f"Message extracted ({len(decrypted_text)} chars) using {method_used}", "success")
    
    def _decode_error(self, error_msg):
        """Handle decoding error"""
        self.decoding_in_progress = False
        self.progress_var.set(0)
        
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
        self.encoded_entry.insert(0, "Select encoded video...")
        self.encoded_entry.config(fg="#666666")
        
        self.extract_password.delete(0, tk.END)
        
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")
        
        self.result_char_count.config(text="Characters: 0", fg="#666666")
        self.result_method_label.config(text="Method: Unknown")
        
        self.encoded_video_path = ""
        self.progress_var.set(0)
        
        self.update_status("Extract section cleared", "info")
    
    def clear_all_fields(self):
        """Clear all fields in both sections"""
        # Clear hide section
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, "Select source video...")
        self.source_entry.config(fg="#666666")
        
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, "Save encoded video...")
        self.output_entry.config(fg="#666666")
        
        self.hide_password.delete(0, tk.END)
        
        self.secret_text.delete("1.0", tk.END)
        self.hide_char_count.config(text="Characters: 0", fg="#666666")
        
        # Clear extract section
        self.clear_extract_section()
        
        # Reset state variables
        self.source_video_path = ""
        self.output_video_path = ""
        
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